import functools
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List

from typing_extensions import Literal

from rutertider import entur_query, utils

# Module wide logger
LOG = logging.getLogger(__name__)

# Type specification for language: Either "no" or "en"
Language = Literal["no", "en"]


@dataclass
class Departure:
    """A data class to hold information about a departure"""
    line_id: str
    line_name: str
    destination: str
    platform: str
    departure_time: str
    bg_color: str
    fg_color: str

    def __str__(self):
        return "{} -> {} @ {}".format(self.line_name, self.destination,
                                      self.departure_time)


@dataclass
@functools.total_ordering
class Situation:
    """A data class to hold situations for a line id"""
    line_id: str
    line_name: str
    transport_mode: str
    bg_color: str
    fg_color: str
    summary: str

    # Define what it takes for two Situations to be equal
    def __eq__(self, other):
        return (self.line_name, self.summary) == \
               (other.line_name, other.summary)

    # Define what it takes for one Situations to be less than another
    def __lt__(self, other):
        return (self.line_name, self.summary) < \
               (other.line_name, other.summary)

    def __str__(self):
        return "{}: {}".format(self.line_name, self.summary)


def get_departures(stop_id: str,
                   line_ids: List[str] = None,
                   platforms: List[str] = None,
                   max_departures: int = 10
                   ) -> List[Departure]:
    """Query the Entur API and return a list of matching departures

    Args:
        stop_id: The stop_id you want departures for
        line_ids: An optional list with line_ids
        platforms: An optional list with platform_ids
        max_departures: The maximum number of departures to query for

    Returns:
        A list of departures
    """
    # Get response from Entur API
    if line_ids:
        query = entur_query.create_departure_query_whitelist(
            stop_id=stop_id, line_ids=line_ids, max_departures=max_departures)
    else:
        query = entur_query.create_departure_query(
            stop_id=stop_id, max_departures=max_departures)
    response = entur_query.journey_planner_api(query)

    departures = []
    for journey in response.json()['data']['stopPlace']['estimatedCalls']:

        # Extract the elements we want from the response
        line_id = journey['serviceJourney']['line']['id']
        line_name = journey['serviceJourney']['line']['publicCode']
        bg_color = journey['serviceJourney']['line']['presentation']['colour']
        fg_color = journey['serviceJourney']['line']['presentation']['textColour']  # noqa
        platform = journey['quay']['id']
        destination = journey['destinationDisplay']['frontText']
        departure_time_string = journey['expectedDepartureTime']

        # Skip unwanted platforms
        if platforms and (platform not in platforms):
            continue

        # Format departure string and add a departure to the list
        departure_string = utils.format_departure_string(departure_time_string)
        departure = Departure(line_id=line_id,
                              line_name=line_name,
                              destination=destination,
                              departure_time=departure_string,
                              platform=platform,
                              fg_color=fg_color,
                              bg_color=bg_color)
        departures.append(departure)

    return departures


def get_situations(line_ids: List[str],
                   language: Language = "no"
                   ) -> List[Situation]:
    """Query the Entur API and return a list of relevant situations

    Args:
        line_ids: A list of strings with line_ids
        language: A language string: 'en' or 'no'

    Returns:
        A list of relevant situations for that line
    """

    LOG.debug("Getting situations for lines %s", line_ids)

    query = entur_query.create_situation_query(line_ids)
    json = entur_query.journey_planner_api(query).json()

    situations: List[Situation] = []
    if not json.get('data'):
        # If there is no valid data, return an empty list
        return situations

    for line in json['data']['lines']:
        if not line:
            # Might be empty if line_id is non-existing
            continue

        # Extract some general information about the line
        line_id = line['id']
        line_name = line['publicCode']
        transport_mode = line['transportMode']
        fg_color = line['presentation']['textColour']
        bg_color = line['presentation']['colour']

        for situation in line['situations']:

            # Extract the fields we need from the response
            start_time = situation['validityPeriod']['startTime']
            end_time = situation['validityPeriod']['endTime']

            # Find start, end and current timestamp
            start_time = utils.iso_str_to_datetime(start_time)
            end_time = utils.iso_str_to_datetime(end_time)
            now = datetime.now(tz=start_time.tzinfo)

            # Add relevant situations to the list
            if start_time < now < end_time:
                for summary in situation['summary']:
                    if summary['language'] == language:
                        situations.append(Situation(
                            line_id=line_id,
                            line_name=line_name,
                            transport_mode=transport_mode,
                            fg_color=fg_color,
                            bg_color=bg_color,
                            summary=summary['value']
                        ))

    return sorted(situations)
