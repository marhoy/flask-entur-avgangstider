import functools
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Departure:
    """A data class to hold information about a departure"""
    line_id: str
    line_name: str
    destination: str
    platform: str
    departure_datetime: datetime
    bg_color: str
    fg_color: str

    @property
    def departure_string(self) -> str:
        """Format the departure string
        Returns:
            A string to be used in the output
        """
        # How long is it to the departure?
        now = datetime.now(tz=self.departure_datetime.tzinfo)
        minutes = int((self.departure_datetime - now).total_seconds() // 60)
        if minutes <= 0:
            departure_string = 'nå'
        elif minutes <= 30:
            departure_string = "{} min".format(minutes)
        else:
            departure_string = self.departure_datetime.strftime("%H:%M")

        return departure_string

    def __str__(self):
        return "{:2s} -> {:15s} @ {}".format(
            self.line_name, self.destination, self.departure_string
        )


@dataclass
@functools.total_ordering
class Situation:
    """A data class to hold information about a situation"""
    line_id: str
    line_name: str
    transport_mode: str
    bg_color: str
    fg_color: str
    summary: str

    # Define what it takes for two Situations to be equal
    def __eq__(self, other):
        return (self.line_name, self.summary) == \
               (other.line_name, other.summary)

    # Define what it takes for one Situation to be less than another
    def __lt__(self, other):
        return (self.line_name, self.summary) < \
               (other.line_name, other.summary)

    def __str__(self):
        return "{}: {}".format(self.line_name, self.summary)
