import json
import os.path
from unittest import mock


def test_app(client):
    assert client.get('/').status_code == 200


def test_departure_table(client):
    assert client.get('/departure_table').status_code == 200


@mock.patch('rutertider.entur_api.entur_query')
def test_deviations(mocked_query, client):
    # Run once without mocking
    assert client.get('/deviations').status_code == 200

    # Mock situation and run again
    with open(os.path.join(os.path.dirname(__file__), "data",
                           "situation.json")) as file:
        json_data = json.load(file)
    mocked_query.journey_planner_api().json.return_value = json_data
    assert client.get('/deviations').status_code == 200
