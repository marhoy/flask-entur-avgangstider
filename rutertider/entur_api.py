import datetime
import re
import requests


DEFAULT_STOPID = "NSR:StopPlace:5968"
DEFAULT_QUAYS = ["NSR:Quay:10949"]

QUERY = """{
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


def get_departures(stopid=DEFAULT_STOPID, platforms=None, lines=None, max_rows=0):

    if platforms is None:
        platforms = []
    if lines is None:
        lines = []

    URL = 'https://api.entur.io/journey-planner/v2/graphql'
    headers = {'ET-Client-Name': 'marhoy - dashboard'}
    query = QUERY.replace('STOP_PLACE', '"{}"'.format(stopid))
    response = requests.post(URL, headers=headers, json={'query': query})
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

        departure_time = re.sub(r'0(\d)00', r'0\1:00', departure_time)
        departure_time = datetime.datetime.fromisoformat(departure_time)
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
