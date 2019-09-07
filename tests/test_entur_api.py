
def test_str_to_datetime():
    from datetime import datetime, timezone, timedelta
    from rutertider.utils import iso_str_to_datetime
    timestamp = datetime(2019, 1, 2, 3, 4, 5,
                         tzinfo=timezone(timedelta(seconds=7200)))
    assert iso_str_to_datetime('2019-01-02T03:04:05+0200') == timestamp
    assert iso_str_to_datetime('2019-01-02T03:04:05+02:00') == timestamp


def test_journey_planner_query():
    from rutertider.entur_query import create_departure_query,\
        create_situation_query, journey_planner_api
    query = create_departure_query(stop_id='NSR:StopPlace:58366')
    response = journey_planner_api(query)
    assert response.ok is True
    query = create_situation_query(line_id='RUT:Line:3')
    response = journey_planner_api(query)
    assert response.ok is True
