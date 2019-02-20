from .methods import POST, GET, DELETE, PUT, PATCH

class CORS(object):

    """Add basic CORS header support when provided

    More information
    ----------------
    See issue at https://github.com/pallets/werkzeug/issues/131

    Example usage
    -------------

    # Using default values
    @web('/api/login', cors=CORS())
    def login(request):
        return {'success':True}

    # Using custom configuration
    cors=CORS()
    cors.origin="localhost"
    cors.methods=[POST]

    # Will append header to defaults, if you want to reset use `cors.headers=[]`
    cors.headers.append('text/plain') 

    # Using default values
    @web('/api/login', cors=cors)
    def login(request):
        return {'success':True}


    """

    def __init__(self):
        """TODO: to be defined1. """

        self.origin="*"
        self.methods=[POST, GET, DELETE, PUT, PATCH]
        self.headers=['Content-Type', 'Authorization']

    def set(self, response):
        response.headers.add('Access-Control-Allow-Origin', '*')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,PATCH')

        response.headers.add('Access-Control-Allow-Headers',

                             # Expects string in following format
                             # 'Content-Type, Authorization'
                             ",".join(self.headers)
                             )


