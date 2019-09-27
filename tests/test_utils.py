from avgangstider.utils import iso_str_to_datetime


def test_iso_str_to_datetime():
    from datetime import datetime, timezone, timedelta
    timestamp = datetime(2019, 1, 2, 3, 4, 5,
                         tzinfo=timezone(timedelta(seconds=7200)))
    assert iso_str_to_datetime('2019-01-02T03:04:05+0200') == timestamp
    assert iso_str_to_datetime('2019-01-02T03:04:05+02:00') == timestamp
