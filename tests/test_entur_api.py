from unittest import mock

import rutertider


def test_get_departures():
    # Test without specifying line_ids
    # At Godlia T, the only passing line is 3, and there is only two quays
    departures = rutertider.get_departures(stop_id="NSR:StopPlace:5968",
                                           max_departures=10)
    assert len(departures) == 10
    for departure in departures:
        assert departure.line_name == '3'
        assert departure.platform in ('NSR:Quay:10948', 'NSR:Quay:10949')

    # Test querying a specific line (from Helsfyr)
    departures = rutertider.get_departures("NSR:StopPlace:59516",
                                           max_departures=10,
                                           line_ids=['RUT:Line:21'])
    assert len(departures) == 10
    for departure in departures:
        assert departure.line_name == '21'

    # Test querying a specific platform (Godlia T, only towards Mortensrud)
    departures = rutertider.get_departures(stop_id="NSR:StopPlace:5968",
                                           platforms=['NSR:Quay:10948'])
    assert departures
    for departure in departures:
        assert departure.line_name == '3'
        assert departure.platform == 'NSR:Quay:10948'
        assert "3 -> Mortensrud" in str(departure)


def test_get_situations():
    # Test without specifying line_ids
    situations = rutertider.get_situations(line_ids=[])
    assert situations == []
    # Test with an invalid line number
    situations = rutertider.get_situations(line_ids=["RUT:Line:0"])
    assert situations == []


@mock.patch('rutertider.entur_api.entur_query')
def test_get_situations_mocked(entur_query, saved_situations_json,
                               saved_situations_list, fixed_datetime):
    # Fake datetime.now() and the situation-json
    entur_query.journey_planner_api().json.return_value = saved_situations_json
    rutertider.entur_api.datetime = fixed_datetime('2019-09-13T20:00:00+02:00')

    # Compared returned situations with the saved result
    situations = rutertider.get_situations(["RUT:Line:1", "RUT:Line:35"])
    assert situations == saved_situations_list
    assert str(situations[0]) == str(saved_situations_list[0])
