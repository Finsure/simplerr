__version__ = "0.15.8"

from .dispatcher import Simplerr

# Import Core Web
from .web import web, make_response

# Import Grammar Helpers
from .methods import GET, POST, PUT, DELETE
from .cors import CORS
