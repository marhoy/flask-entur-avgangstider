from datetime import datetime, timedelta

import avgangstider.classes


def test_util(fixed_datetime):
    # Replace datetime in classes with a mocked class
    mocked_now_string = '2019-01-01T12:00:00+01:00'
    mocked_now = datetime.fromisoformat(mocked_now_string)
    avgangstider.classes.datetime = fixed_datetime(mocked_now_string)

    departure = avgangstider.classes.Departure(
        line_id="",
        line_name="",
        destination="",
        platform="",
        departure_datetime=mocked_now,
        bg_color="",
        fg_color=""
    )

    # Check the departure string for different timedelta's
    departure.departure_datetime = mocked_now + timedelta(seconds=59)
    assert departure.departure_string == 'nå'

    departure.departure_datetime = mocked_now + timedelta(minutes=30)
    assert departure.departure_string == '30 min'

    departure.departure_datetime = mocked_now + timedelta(minutes=31)
    time_string = departure.departure_datetime.strftime('%H:%M')
    assert departure.departure_string == time_string
