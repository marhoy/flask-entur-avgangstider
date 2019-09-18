from unittest import mock


def test_app(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'DepartureTable' in response.data


def test_departure_table(client):
    assert client.get('/departure_table').status_code == 200


def test_deviations(client):
    response = client.get('/deviations')  # , query_string={})
    assert response.status_code == 200


def test_deviations_with_line(client):
    response = client.get('/deviations', query_string={
        'line_id': 'RUT:Line:3'
    })
    assert response.status_code == 200


@mock.patch('rutertider.get_situations')
def test_deviations_mocked(mocked_func, client, saved_situations_list):
    # Load some mocked situations
    mocked_func.return_value = saved_situations_list
    response = client.get('/deviations')
    assert response.status_code == 200
