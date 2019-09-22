from unittest import mock


def test_static(client):
    response = client.get('/static/css/dinfont.css')
    assert response.status_code == 200
    assert b'font-face' in response.data


def test_app_without_stop_id(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Examples' in response.data


def test_app(client):
    response = client.get('/', query_string={
        'stop_id': 'NSR:StopPlace:58366'
    })
    assert response.status_code == 200
    assert b'DepartureTable' in response.data

    # Call again, but with a new stop_id
    response = client.get('/', query_string={
        'stop_id': 'NSR:StopPlace:59872'
    })
    assert response.status_code == 200
    assert b'DepartureTable' in response.data


def test_departure_table(client):
    response = client.get('/departure_table', query_string={
        'stop_id': 'NSR:StopPlace:58366'
    })
    assert response.status_code == 200


def test_deviations(client):
    # Try first without having got any departures
    # There should be no situations
    response = client.get('/deviations', query_string={
        'stop_id': 'NSR:StopPlace:58366'
    })
    assert response.status_code == 200
    assert response.data == b''

    # First, get some departures
    client.get('/departure_table', query_string={
        'stop_id': 'NSR:StopPlace:58366'
    })
    # Then get situations again
    response = client.get('/deviations', query_string={
        'stop_id': 'NSR:StopPlace:58366'
    })
    assert response.status_code == 200


def test_deviations_with_line(client):
    response = client.get('/deviations', query_string={
        'stop_id': 'NSR:StopPlace:58366',
        'line_id': 'RUT:Line:3'
    })
    assert response.status_code == 200


@mock.patch('avgangstider.get_situations')
def test_deviations_mocked(mocked_func, client, saved_situations_list):
    # Load some mocked situations
    mocked_func.return_value = saved_situations_list

    client.get('/departure_table', query_string={
        'stop_id': 'NSR:StopPlace:58366'
    })

    response = client.get('/deviations', query_string={
        'stop_id': 'NSR:StopPlace:58366'
    })
    assert response.status_code == 200
    assert b'11: Innstilt mellom Jernbanetorget og Majorstuen' in response.data
