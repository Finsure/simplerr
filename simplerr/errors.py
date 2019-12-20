class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class TooManyArgumentsError(Error):
    """Exception raised for errors in the web() signature"""

    def __init__(self, message):
        self.message = message


class SiteNotFoundError(Error):
    """Exception raised for errors in the site path

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, site, message):
        self.site = message
        self.message = message
