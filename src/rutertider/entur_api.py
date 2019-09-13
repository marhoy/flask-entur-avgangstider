import datetime
from dataclasses import dataclass

from rutertider import entur_query, utils


@dataclass
class Departure:
    """A data class to hold departure info"""
    line_name: str
    destination: str
    platform: str
    departure_time: str
    bg_color: str
    fg_color: str


def get_departures(stop_id, platforms=None, lines=None,
                   max_departures=None):
    """Query the API and return a list of matching departures

    Args:
        stop_id:
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
    if max_departures is None:
        max_departures = 5

    # Get response from Entur API
    query = entur_query.create_departure_query(stop_id=stop_id,
                                               max_departures=max_departures)
    response = entur_query.journey_planner_api(query)

    departures = []
    for journey in response.json()['data']['stopPlace']['estimatedCalls']:

        # Extract the elements we want from the response
        line_name = journey['serviceJourney']['line']['publicCode']
        bg_color = journey['serviceJourney']['line']['presentation']['colour']
        fg_color = journey['serviceJourney']['line']['presentation']['textColour']  # noqa
        platform = journey['quay']['id']
        destination = journey['destinationDisplay']['frontText']
        departure_time_string = journey['expectedDepartureTime']

        # Skip unwanted platforms / lines
        if platforms and (platform not in platforms):
            continue
        if lines and (line_name not in lines):
            continue

        # Format departure string and add a departure to the list
        departure_string = utils.format_departure_string(departure_time_string)
        departure = Departure(line_name=line_name,
                              destination=destination,
                              departure_time=departure_string,
                              platform=platform,
                              fg_color=fg_color,
                              bg_color=bg_color)
        departures.append(departure)

    return departures


def get_situations(line_id, language='no'):
    """Query the Entur API and return a list of relevant situations

    Args:
        line_id: A string with a valid line id
        language: A language string: 'en' or 'no'

    Returns:
        A list of relevant situations for that line
    """
    query = entur_query.create_situation_query(line_id)
    response = entur_query.journey_planner_api(query)

    situations = []
    if not response.json()['data']['line']:
        # There is no data for this line, maybe its not a valid ID?
        return []
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
            for summary in situation['summary']:
                if summary['language'] == language:
                    situations.append(summary['value'])

    return sorted(situations)
