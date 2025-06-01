__version__ = "0.16.0"

from .dispatcher import Simplerr

# Import Core Web
from .web import web, make_response

# Import Grammar Helpers
from .methods import GET, POST, PUT, DELETE, PATCH
from .cors import CORS
