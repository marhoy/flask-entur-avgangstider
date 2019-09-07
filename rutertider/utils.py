import re
from datetime import datetime


def iso_str_to_datetime(timestamp_str):
    """Convert timestamp string to datetime object

    Args:
        timestamp_str (str): A timestamp in iso format

    Returns:
        A datetime timestamp with timezone info

    Examples:
        >>> iso_str_to_datetime('2019-01-02T03:04:05+0200')
        datetime.datetime(2019, 1, 2, 3, 4, 5, tzinfo=datetime.timezone(
        datetime.timedelta(seconds=7200)))

        >>> iso_str_to_datetime('2019-01-02T03:04:05+02:00')
        datetime.datetime(2019, 1, 2, 3, 4, 5, tzinfo=datetime.timezone(
        datetime.timedelta(seconds=7200)))
    """
    # If the timezone info is e.g. +0200, change to +02:00
    timestamp_str = re.sub(r'0(\d)00', r'0\1:00', timestamp_str)
    return datetime.fromisoformat(timestamp_str)


def format_departure_string(departure_timestamp_string):
    """Format the departure string

    Args:
        departure_timestamp_string: An iso-formatted timestamp string

    Returns:
        A string to be used in the output
    """
    # How long is it to the departure?
    departure_time = iso_str_to_datetime(departure_timestamp_string)
    now = datetime.now(tz=departure_time.tzinfo)
    minutes = round((departure_time - now).total_seconds() / 60)

    if minutes <= 0:
        departure_string = 'nå'
    elif minutes <= 30:
        departure_string = "{} min".format(minutes)
    else:
        departure_string = "{:02}:{:02}".format(
            departure_time.hour,
            departure_time.minute)

    return departure_string
