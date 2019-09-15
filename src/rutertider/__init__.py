import logging

from rutertider.entur_api import get_departures, get_situations
from rutertider.flask_app import create_app

__version__ = "0.1.0"

# Satisfy the PEP8 linter
__all__ = ["get_departures", "get_situations", "create_app"]

# Set up package-wide logging configuration
logging.basicConfig(format='[%(levelname)s] %(name)s(%(lineno)s): %(message)s',
                    level=logging.WARNING)
LOG = logging.getLogger(__name__)
# LOG.setLevel(logging.DEBUG)
