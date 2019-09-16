from unittest import mock
import pytest


@pytest.mark.skip
def test_app(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('UTF-8').find('DepartureTable')


@pytest.mark.skip
def test_departure_table(client):
    assert client.get('/departure_table').status_code == 200


@mock.patch('rutertider.get_situations')
def test_deviations(mocked_func, client, saved_situations_list):
    # Run once without mocking
    # assert client.get('/deviations').status_code == 200

    # Mock situation and run again
    mocked_func.return_value = saved_situations_list
    response = client.get('/deviations', query_string={
        'stop_id': 'NSR:StopPlace:58366',
        'line_id': 'RUT:Line:1'})
    print("Response:", response.data)
    assert False
    assert response.status_code == 200
    assert client.get('/deviations').status_code == 200
