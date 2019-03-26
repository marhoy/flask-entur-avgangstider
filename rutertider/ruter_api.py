import datetime

import requests


DEPARTURE_URL = "http://reisapi.ruter.no/StopVisit/GetDepartures/"
DEFAULT_RUTER_STOPID = '3011310'


def get_ruter_departures(stopid=DEFAULT_RUTER_STOPID, platforms=None, lines=None,
                         max_rows=0):

    if platforms is None:
        platforms = []
    if lines is None:
        lines = []

    url = DEPARTURE_URL + stopid
    response = requests.get(url)
    response.raise_for_status()

    departures = []
    for journey in response.json():
        line_name = journey['MonitoredVehicleJourney']['PublishedLineName']
        line_color = journey['Extensions']['LineColour']
        platform = journey['MonitoredVehicleJourney']['DirectionRef']
        destination = journey['MonitoredVehicleJourney']['DestinationName']
        departure_time = journey['MonitoredVehicleJourney']['MonitoredCall']['ExpectedDepartureTime']

        if platforms and (platform not in platforms):
            continue
        if lines and (line_name not in lines):
            continue
        if max_rows and (len(departures) >= max_rows):
            break

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
