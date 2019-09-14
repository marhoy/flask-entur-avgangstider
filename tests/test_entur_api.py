import json
import os.path
from datetime import datetime
from unittest import mock

import rutertider


class FixedDateTime:
    """A mock of datetime that provides a fixed value for now()"""

    def __init__(self, iso_string):
        self.timestamp = datetime.fromisoformat(iso_string)

    def now(self, tz=None):
        return self.timestamp

    @staticmethod
    def fromisoformat(string):
        return datetime.fromisoformat(string)


def test_get_departures():
    """Test with station Godlia T-bane
    We know the only valid line is 3, and there is only two platforms"""

    departures = rutertider.get_departures(stop_id="NSR:StopPlace:5968")
    assert len(departures) == 5

    departures = rutertider.get_departures(stop_id="NSR:StopPlace:5968",
                                           max_departures=3)
    assert len(departures) == 3
    for departure in departures:
        assert departure.line_name == '3'
        assert departure.platform in ('NSR:Quay:10948', 'NSR:Quay:10949')

    # Test querying a specific line (from Helsfyr)
    departures = rutertider.get_departures("NSR:StopPlace:59516",
                                           max_departures=20,
                                           line_ids=['RUT:Line:21'])
    assert departures

    # Test querying a specific platform (Godlia T, only towards Mortensrud)
    departures = rutertider.get_departures(stop_id="NSR:StopPlace:5968",
                                           platforms=['NSR:Quay:10948'])
    assert departures


def test_get_situations():
    # Test with an invalid line number
    situations = rutertider.get_situations("RUT:Line:0")
    assert len(situations) == 0


@mock.patch('rutertider.entur_api.entur_query')
def test_get_situations_mocked(mocked_json):
    with open(os.path.join(os.path.dirname(__file__), "data",
                           "situation.json")) as file:
        json_data = json.load(file)
    mocked_json.journey_planner_api().json.return_value = json_data

    mocked_now_string = '2019-09-13T20:00:00+02:00'
    rutertider.entur_api.datetime = FixedDateTime(mocked_now_string)

    situations = rutertider.get_situations("RUT:Line:120")
    assert len(situations) == 1
    assert situations[0].summary == 'Buss for trikk Jernbanetorget-Grefsen ' \
                                    'etter kl. 20:00'
