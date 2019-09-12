

def test_app(client):
    assert client.get('/').status_code == 200


def test_departure_table(client):
    assert client.get('/departure_table').status_code == 200


def test_deviations(client):
    assert client.get('/deviations').status_code == 200
