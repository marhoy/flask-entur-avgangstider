import datetime
import re
import requests


DEFAULT_STOPID = "NSR:StopPlace:5968"
DEFAULT_QUAYS = ["NSR:Quay:10949"]
DEFAULT_LINE = "RUT:Line:3"

QUERY_URL = 'https://api.entur.io/journey-planner/v2/graphql'

DEPARTURE_QUERY = """{
  stopPlace(id: STOP_PLACE) {
    name
    estimatedCalls(numberOfDepartures: 10) {
      quay {
        id
        description
      }
      expectedArrivalTime
      actualArrivalTime
      expectedDepartureTime
      actualDepartureTime
      realtime
      realtimeState
      destinationDisplay {
        frontText
      }
      serviceJourney {
        line {
          publicCode
          presentation {
            colour
            textColour
          }
        }
      }
    }
  }
}
"""

SITUATION_QUERY = """
{
  line(id: LINE_ID) {
    id
    situations {
      summary {
        value
      }
      description {
        value
      }
      detail {
        value
      }
      validityPeriod {
        startTime
        endTime
      }
    }
  }
}"""


def str_to_datetime(str):
    str = re.sub(r'0(\d)00', r'0\1:00', str)
    return datetime.datetime.fromisoformat(str)


def get_departures(stopid=DEFAULT_STOPID, platforms=None, lines=None, max_rows=0):

    if platforms is None:
        platforms = []
    if lines is None:
        lines = []

    headers = {'ET-Client-Name': 'marhoy - dashboard'}
    query = DEPARTURE_QUERY.replace('STOP_PLACE', '"{}"'.format(stopid))
    response = requests.post(QUERY_URL, headers=headers, json={'query': query})
    response.raise_for_status()

    departures = []
    for journey in response.json()['data']['stopPlace']['estimatedCalls']:
        line_name = journey['serviceJourney']['line']['publicCode']
        line_color = journey['serviceJourney']['line']['presentation']['colour']
        platform = journey['quay']['id']
        destination = journey['destinationDisplay']['frontText']
        departure_time = journey['expectedDepartureTime']

        if platforms and (platform not in platforms):
            continue
        if lines and (line_name not in lines):
            continue
        if max_rows and (len(departures) >= max_rows):
            break

        departure_time = str_to_datetime(departure_time)
        now = datetime.datetime.now(tz=departure_time.tzinfo)
        minutes = (departure_time - now).total_seconds() / 60
        minutes = round(minutes)

        if minutes <= 0:
            arrival_string = 'nå'
        elif minutes <= 30:
            arrival_string = "{} min".format(minutes)
        else:
            arrival_string = "{:02}:{:02}".format(departure_time.hour, departure_time.minute)

        departures.append({'line_name': line_name,
                           'line_color': line_color,
                           'destination': destination,
                           'departure_time': arrival_string})

    return departures


def get_situations(line=DEFAULT_LINE):

    headers = {'ET-Client-Name': 'marhoy - dashboard'}
    query = SITUATION_QUERY.replace('LINE_ID', '"{}"'.format(line))
    response = requests.post(QUERY_URL, headers=headers, json={'query': query})
    response.raise_for_status()

    situations = []

    for situation in response.json()['data']['line']['situations']:
        start_time = situation['validityPeriod']['startTime']
        end_time = situation['validityPeriod']['endTime']
        start_time = str_to_datetime(start_time)
        end_time = str_to_datetime(end_time)
        now = datetime.datetime.now(tz=start_time.tzinfo)

        if start_time < now < end_time:
            situations.append(situation['summary'][0]['value'])

    return situations
