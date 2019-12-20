class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class TooManyArgumentsError(Error):
    """Exception raised for errors in the web() signature"""

    def __init__(self, message):
        self.message = message
