from avgangstider.entur_query import (create_departure_query,
                                      create_departure_query_whitelist,
                                      create_situation_query,
                                      journey_planner_api)


def test_create_departure_query():
    """Get departures for a stop_id"""
    query = create_departure_query(stop_id='NSR:StopPlace:58366')
    response = journey_planner_api(query)
    assert response.ok is True
    assert response.json().get('data')


def test_create_departure_query_whitelist():
    """Get departures for a stop_id and only a list of line_ids

    Check that all returned departures are from the specified line_ids
    """
    query_lines = ['RUT:Line:1', 'RUT:Line:2', 'RUT:Line:3']
    query = create_departure_query_whitelist(
        stop_id='NSR:StopPlace:58366',
        line_ids=query_lines)
    response = journey_planner_api(query)
    assert response.ok is True
    assert response.json().get('data')
    for departure in response.json()['data']['stopPlace']['estimatedCalls']:
        assert departure['serviceJourney']['line']['id'] in query_lines


def test_create_situation_query():
    """Get situations for some line_ids"""
    query = create_situation_query(line_ids=['RUT:Line:1', 'RUT:Line:3'])
    response = journey_planner_api(query)
    assert response.ok is True
    assert response.json().get('data')
