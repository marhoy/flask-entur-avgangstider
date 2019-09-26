import functools
from dataclasses import dataclass


@dataclass
class Departure:
    """A data class to hold information about a departure"""
    line_id: str
    line_name: str
    destination: str
    platform: str
    departure_time: str
    bg_color: str
    fg_color: str

    def __str__(self):
        return "{:2s} -> {:15s} @ {}".format(
            self.line_name, self.destination, self.departure_time
        )


@dataclass
@functools.total_ordering
class Situation:
    """A data class to hold situations for a line id"""
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

    # Define what it takes for one Situations to be less than another
    def __lt__(self, other):
        return (self.line_name, self.summary) < \
               (other.line_name, other.summary)

    def __str__(self):
        return "{}: {}".format(self.line_name, self.summary)
