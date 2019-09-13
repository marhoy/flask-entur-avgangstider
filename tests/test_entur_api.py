from rutertider import get_departures


def test_get_departures():
    """Test with station Godlia T-bane
    We know the only valid line is 3, and there is only two platforms"""

    departures = get_departures(stop_id="NSR:StopPlace:5968")
    assert len(departures) == 5
    departures = get_departures(stop_id="NSR:StopPlace:5968", max_departures=3)
    assert len(departures) == 3
    for departure in departures:
        assert departure.line_name == '3'
        assert departure.platform in ('NSR:Quay:10948', 'NSR:Quay:10949')
