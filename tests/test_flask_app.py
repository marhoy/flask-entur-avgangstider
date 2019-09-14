from unittest import mock


def test_app(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('UTF-8').find('DepartureTable')


def test_departure_table(client):
    assert client.get('/departure_table').status_code == 200


@mock.patch('rutertider.entur_api.entur_query')
def test_deviations(mocked_query, client, saved_situation):
    # Run once without mocking
    assert client.get('/deviations').status_code == 200

    # Mock situation and run again
    mocked_query.journey_planner_api().json.return_value = saved_situation
    assert client.get('/deviations').status_code == 200
