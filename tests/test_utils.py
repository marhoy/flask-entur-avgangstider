from datetime import datetime, timedelta

import rutertider.utils
from rutertider.utils import iso_str_to_datetime


class FixedDateTime:
    def __init__(self, iso_string):
        self.timestamp = datetime.fromisoformat(iso_string)

    def now(self, tz=None):
        return self.timestamp

    @staticmethod
    def fromisoformat(string):
        return datetime.fromisoformat(string)


def test_iso_str_to_datetime():
    from datetime import datetime, timezone, timedelta
    timestamp = datetime(2019, 1, 2, 3, 4, 5,
                         tzinfo=timezone(timedelta(seconds=7200)))
    assert iso_str_to_datetime('2019-01-02T03:04:05+0200') == timestamp
    assert iso_str_to_datetime('2019-01-02T03:04:05+02:00') == timestamp


def test_util():
    mocked_now_string = '2019-01-01T12:00:00+01:00'
    mocked_now = datetime.fromisoformat(mocked_now_string)

    rutertider.utils.datetime = FixedDateTime(mocked_now_string)

    departure = mocked_now + timedelta(seconds=59)
    string = rutertider.utils.format_departure_string(
        departure.isoformat())
    assert string == 'nå'

    departure = mocked_now + timedelta(minutes=12)
    string = rutertider.utils.format_departure_string(
        departure.isoformat())
    assert string == '12 min'

    departure = mocked_now + timedelta(minutes=30)
    string = rutertider.utils.format_departure_string(
        departure.isoformat())
    assert string == '30 min'

    departure = mocked_now + timedelta(minutes=31)
    string = rutertider.utils.format_departure_string(
        departure.isoformat())
    assert string == departure.strftime('%H:%M')
