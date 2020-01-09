import logging

from avgangstider.classes import Departure, Situation
from avgangstider.entur_api import get_departures, get_situations
from avgangstider.flask_app import create_app

__version__ = "0.1.1"

# Satisfy the PEP8 linter
__all__ = ["get_departures", "get_situations", "Departure", "Situation",
           "create_app"]

# Set up package-wide logging configuration
logging.basicConfig(format='[%(levelname)s] %(name)s(%(lineno)s): %(message)s',
                    level=logging.WARNING)
LOG = logging.getLogger(__name__)
# LOG.setLevel(logging.DEBUG)
