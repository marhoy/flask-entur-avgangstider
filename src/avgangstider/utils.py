import re
from datetime import datetime


def iso_str_to_datetime(timestamp_str: str) -> datetime:
    """Convert timestamp string to datetime object

    Args:
        timestamp_str (str): A timestamp in iso format

    Returns:
        A datetime timestamp with timezone info

    Examples:
        >>> iso_str_to_datetime('2019-01-02T03:04:05+0200')
        datetime.datetime(2019, 1, 2, 3, 4, 5,
        tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)))

        >>> iso_str_to_datetime('2019-01-02T03:04:05+02:00')
        datetime.datetime(2019, 1, 2, 3, 4, 5,
        tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)))
    """
    # If the timezone info is e.g. +0200, change to +02:00
    timestamp_str = re.sub(r'(\d{2,})(\d{2,})$', r'\1:\2', timestamp_str)
    return datetime.fromisoformat(timestamp_str)
