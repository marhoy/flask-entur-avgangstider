from rutertider.entur_query import create_departure_query, \
    create_situation_query, journey_planner_api


def test_reate_departure_query():
    query = create_departure_query(stop_id='NSR:StopPlace:58366')
    response = journey_planner_api(query)
    assert response.ok is True


def test_create_situation_query():
    query = create_situation_query(line_id='RUT:Line:3')
    response = journey_planner_api(query)
    assert response.ok is True
