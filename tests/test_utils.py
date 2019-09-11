from datetime import datetime, timedelta
import rutertider.utils
from rutertider.utils import iso_str_to_datetime, format_departure_string


class FixedDateTime:

    def __init__(self, iso_string):
        self.timestamp = datetime.fromisoformat(iso_string)

    def now(self, tz=None):
        return self.timestamp

    @staticmethod
    def fromisoformat(string):
        return datetime.fromisoformat(string)


def test_util():
    rutertider.utils.datetime = FixedDateTime('2019-01-01T12:00:00+01:00')

    string = rutertider.utils.format_departure_string('2019-01-01T12:00:60+01:00')
    assert string == 'sdf'


def test_format_departure_string():
    now = datetime.now()

    timestamp = now + timedelta(seconds=29)
    string = format_departure_string(timestamp.isoformat())
    assert string == 'nå'

    timestamp = now + timedelta(minutes=1)
    string = format_departure_string(timestamp.isoformat())
    assert string == '1 min'

    timestamp = now + timedelta(minutes=30)
    string = format_departure_string(timestamp.isoformat())
    assert string == '30 min'

    timestamp = now + timedelta(minutes=31)
    string = format_departure_string(timestamp.isoformat())
    assert string == timestamp.strftime('%H:%M')


# @mock.patch('rutertider.utils.datetime.now', side_effect=lambda *args, **kw: datetime(*args, **kw))
# def test_returns_only_from_current_month_by_default(mock_date):
#     mocked_now = datetime.datetime(2017, 2, 15)
#     mock_date.now.return_value = mocked_now
#
#     def _round(number):
#         return round(number)
#     mock_date.now.__round__ = _round
#
#     format_departure_string('2019-01-02T03:04:05+0200')


# @mock.patch('rutertider.utils.datetime')
# def test_noe(mocker):
#     target = real_datetime_class(2009, 1, 1)
#     mocker.now = mock_datetime_now(target, datetime)
#     format_departure_string('2019-01-02T03:04:05+0200')
#     assert False

