import datetime
from dataclasses import dataclass

from rutertider import entur_query, utils


@dataclass
class Departure:
    """A class to hold departure-info"""
    line_name: str
    destination: str
    departure_time: str
    bg_color: str
    fg_color: str


def get_departures(stop_id, platforms=None, lines=None,
                   max_departures=None):
    """Query the API and return a list of matching departures

    Args:
        stopid:
        platforms:
        lines:
        max_departures (int):

    Returns:
        A list of departures
    """
    # Handle optional arguments
    if platforms is None:
        platforms = []
    if lines is None:
        lines = []

    # Get response from Entur API
    query = entur_query.create_departure_query(stop_id=stop_id,
                                               max_departures=max_departures)
    response = entur_query.journey_planner_api(query)

    departures = []
    for journey in response.json()['data']['stopPlace']['estimatedCalls']:

        # Extract the elements we want from the response
        line_name = journey['serviceJourney']['line']['publicCode']
        bg_color = journey['serviceJourney']['line']['presentation']['colour']
        fg_color = journey['serviceJourney']['line']['presentation']['textColour']
        platform = journey['quay']['id']
        destination = journey['destinationDisplay']['frontText']
        departure_time_string = journey['expectedDepartureTime']

        # Skip unwanted platforms / lines and break after max_rows
        if platforms and (platform not in platforms):
            continue
        if lines and (line_name not in lines):
            continue
#        if max_rows and (len(departures) >= max_rows):
#            break

        # Format departure string and add a departure to the list
        departure_string = utils.format_departure_string(departure_time_string)
        departure = Departure(line_name=line_name,
                              destination=destination,
                              departure_time=departure_string,
                              fg_color=fg_color,
                              bg_color=bg_color)
        departures.append(departure)

    return departures


def get_situations(line):
    """Query the Entur API and return a list of relevant situations

    Args:
        line:

    Returns:

    """
    query = entur_query.create_situation_query(line)
    response = entur_query.journey_planner_api(query)

    situations = []
    for situation in response.json()['data']['line']['situations']:

        # Extract the fields we need from the response
        start_time = situation['validityPeriod']['startTime']
        end_time = situation['validityPeriod']['endTime']

        # Find start, end and current timestamp
        start_time = utils.iso_str_to_datetime(start_time)
        end_time = utils.iso_str_to_datetime(end_time)
        now = datetime.datetime.now(tz=start_time.tzinfo)

        # Add relevant situations to the list
        if start_time < now < end_time:
            situations.append(situation['summary'][0]['value'])

    return sorted(situations)
