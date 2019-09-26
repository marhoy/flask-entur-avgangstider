import json
import logging
import os.path
import pickle
from datetime import datetime

import avgangstider
import pytest

LOG = logging.getLogger(__name__)


@pytest.fixture
def fixed_datetime():
    class FixedDateTime:
        """A mock of datetime that provides a fixed value for now()"""

        def __init__(self, timestamp):
            if isinstance(timestamp, str):
                self.timestamp = datetime.fromisoformat(timestamp)
            elif isinstance(timestamp, datetime):
                self.timestamp = timestamp

        def now(self, tz=None):
            if tz is None:
                tz = self.timestamp.tzinfo
            return self.timestamp.replace(tzinfo=tz)

        @staticmethod
        def fromisoformat(string):
            return datetime.fromisoformat(string)

    return FixedDateTime


@pytest.fixture
def saved_situations_json():
    with open(os.path.join(os.path.dirname(__file__), "data",
                           "situations.json")) as file:
        json_data = json.load(file)
    return json_data


@pytest.fixture
def saved_situations_list():
    with open(os.path.join(os.path.dirname(__file__), "data",
                           "situations.pkl"), "rb") as file:
        return pickle.load(file)


@pytest.fixture
def app():
    app = avgangstider.create_app()
    return app
