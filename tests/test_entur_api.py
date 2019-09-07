
def test_str_to_datetime():
    from datetime import datetime, timezone, timedelta
    from rutertider.entur_api import str_to_datetime
    timestamp = datetime(2019, 1, 2, 3, 4, 5,
                         tzinfo=timezone(timedelta(seconds=7200)))
    assert str_to_datetime('2019-01-02T03:04:05+0200') == timestamp
    assert str_to_datetime('2019-01-02T03:04:05+02:00') == timestamp
