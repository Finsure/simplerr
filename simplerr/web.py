#!/usr/bin/env python
import mimetypes
import functools
from pathlib import Path

from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import wrap_file
from werkzeug.exceptions import abort
from werkzeug.routing import Map, Rule
from werkzeug.utils import redirect as wz_redirect

from .script import script
from .template import Template
from .cors import CORS
from .methods import GET, POST, DELETE, PUT, PATCH, BaseMethod
from .serialise import json_serial, tojson
from .errors import ToManyArgumentsError

# TODO: Get rid of this dependancy
from peewee import *
from peewee import ModelSelect
from playhouse.shortcuts import model_to_dict, dict_to_model


#  _   _   _   _  _  _   _ _ _  ___  ___   ___  _  _ _  ___  _  _  _  __
# | \_/ | / \ | || \| | | | | || __|| o ) | o \/ \| | ||_ _|| || \| |/ _|
# | \_/ || o || || \\ | | V V || _| | o \ |   ( o ) U | | | | || \\ ( |_n
# |_| |_||_n_||_||_|\_|  \_n_/ |___||___/ |_|\\\_/|___| |_| |_||_|\_|\__/
#
class web(object):
    """Primary routing decorator and helpers

    The `web()` decorator traps all routes and add them to a list, which is
    passed to werkzeugs `werkzeug.routing.Map()` for find the current method to
    run for the matched route.

    Decorator Format
    ==================

    The `web()` decorator (routes) wraps the `werkzueg.routing.Rule()` format
    `<converter(arguments):name>`. 

    In addition to the `Route()` parameters, `web()` also add's a `template` to
    use in rendering that endpoint.

    Routes are used in the following way:

    ::

        @web('/user/<int:id>', 'user.html')
        def get_user(request, id):
            # The return value will be used
            # as the context for the template
            return {'id':id, 'name':'John Doe'}

    Route Parameters
    ----------------

    Routes in simplerr wrap the `Rule()` class in werkzeug - highlighted below

    ::

        class werkzeug.routing.Rule(
            string,
            defaults=None,          # Not yet implemented
            subdomain=None,         # Not yet implemented
            methods=None,
            build_only=False,       # Not yet implemented
            endpoint=None,          # Assigned to same value as first string param, eg '/index'
            strict_slashes=None,    # Not yet implemented
            redirect_to=None,       # Not yet implemented
            alias=False,            # Not yet implemented
            host=None               # Not yet implemented
            )


    The 'web()' decorator has the following signature.

    ::

        class simplerr.web(
            string,         # Route
            string=None,    # Template to combine `return` value as context
            methods=None
        )


    string
        Route strings are URL paths which optionally use placeholders for
        arguments using the following format <converter(arguments):name>.

    string
        Path to the template to be rendered, the return value is supplied as the
        template context. In addition, the `request` object is also available under
        `request`.

    endpoint
        The endpoint for this rule. This can be anything. A reference to a
        function, a string, a number etc. The preferred way is using a string
        because the endpoint is used for URL generation.

    methods
        A list of http methods to accept, defaults to `None` which accepts all.
        Otherwise sepcify `'GET'`, `'POST'`, `'PUT'`, `'DELETE'`. Note that
        `'HEAD'` is accepeted on `'GET'` requests.


    Footnotes
    =========

    .. [1] Werkzeug Rule() details at http://werkzeug.pocoo.org/docs/0.14/routing/#rule-format

    """

    destinations = []

    filters = {}
    template_engine = None

    @staticmethod
    def restore_presets():
        web.destinations = []

    def __init__(self, *args, route=None, template=None, methods=None, endpoint=None, file=False, cors=None, mimetype=None):

        self.endpoint = endpoint
        self.fn = None
        self.args = None # to be set when matched() is called
        self.file = file
        self.cors = cors
        self.mimetype = mimetype

        # We can specify route, template and methods using **kwargs
        self.route = route
        self.template = template
        self.methods = methods     # Methods should be left as None to accept all

        # However, we also allow a basic grammer with optional arguments, for example:
        #
        #       @web([route],[template], [method], [method]) -> *args may be 0 or 3 long!
        #
        # More concrete examples:
        #
        #       @web('/home')
        #       @web('/templates/home.html')
        #       @web('/home', '/templates/home.html')
        #       @web('/home', 'home.html', GET)
        #       @web('/home', 'home.html', GET, POST)
        #       @web('/users', GET, POST)
        #

        # Parse Try 1: First item may be a route or template, second item may
        # be a template - ignores GET/POST types
        args_strings = [item for item in args if isinstance(item, str)]

        # We have to check not string first as issubclass fails on testing str
        # items - This extracts GET/POST which are the only non-string types expected
        args_methods = [item for item in args if not(isinstance(item, str)) and issubclass(item, BaseMethod)]

        # Aappend all methods into self.methods
        if len(args_methods) > 0:
            self.methods = self.methods or []
            for method in args_methods:
                self.methods.append(method.verb)


        # Only one string, maybe a route or template - default to route if not
        # already populated.
        if len(args_strings) == 1:
            if(self.route is None):
                self.route = args_strings[0]
            elif(self.template is None):
                self.template = args_strings[0]
            else:
                raise ToManyArgumentsError("Got too many string arguments")

        # Two strings - definately should be a route and a template
        if len(args_strings) == 2:
            if(self.route is None and self.template is None):
                self.route, self.template = args_strings
            else:
                raise ToManyArgumentsError("Got too many string arguments")

        # Way to many strings to infer what needs to happen - not something
        # currently supported.
        if len(args_strings) > 2:
            raise ToManyArgumentsError("Got too many string arguments")




    def __call__(self, fn):
        # A quick cleanup first, if no endpoint was specified we need to set it
        # to the view function
        self.endpoint = self.endpoint or id(fn) # Default endpoint name if none provided.

        # Proceed to create decorator
        self.fn = fn

        # add this function into destinations
        web.destinations.append(self)

        @functools.wraps(fn)
        def decorated(request, *args, **kwargs):
            return fn(request, *args, **kwargs)

        # Return pretty much unmodified, we really only
        # wanted this to index it into destinations
        return decorated

    @staticmethod
    def match(environ):
        map = Map()
        index = {}

        for item in web.destinations:
            # Lets create an index on routes, as urls.match returns a route
            index[item.endpoint] = item

            # Create the rule and add it tot he map
            rule = Rule(item.route, endpoint=item.endpoint, methods=item.methods)
            map.add(rule)

        # Check for match
        urls = map.bind_to_environ(environ)
        endpoint, args = urls.match()

        # Get match and attach current args
        match = index[endpoint]
        match.args = args

        return match


    @staticmethod
    def process(request, environ, cwd):
        # tid(f'web.process:(r, e cwd={cwd})')

        # Weg web() object that matches this request
        match = web.match(environ)

        # Lets extract some key response information
        args = match.args
        out = match.fn(request, **args)
        # tid(f'web.process().out = {out}')

        data = out
        template = match.template
        file = match.file
        mimetype = match.mimetype
        cors = match.cors

        # TODO: Can we replace the Model, and ModelSelct with json.dumps(data,
        # json_serial) which has been udpated to handle these types?

        # TODO: All serialisable items need to have a obj.todict() method, otheriwse
        # str(obj) will be used.

        # User has decided to run their own request object, just return this
        if isinstance(data, Response):
            return data

        # Check to see if this is a peewee model and convert to
        # dict,
        if(isinstance(data, Model)):
            out = model_to_dict(out)
            data = out


        if(isinstance(data, ModelSelect)):
            array_out = []
            for item in data:
                array_out.append(model_to_dict(item))
                out = {'results': array_out}
                data = out


        # Template expected, attempt render
        if(template != None):
            # Add request to data
            data = data or {}
            data['request'] = request
            out = web.template(cwd, template, data)

            response = Response(out)
            response.headers['Content-Type'] = 'text/html;charset=utf-8'

            # TODO: make reponse plugin based, so cors needs to be added - pre-respon
            if cors: cors.set(response)

            return response


        # Reference example implementation here
        #   http://bit.ly/2ocHYNZ
        if(file == True):
            file_path = Path(cwd) / Path(out)
            file = open(file_path.absolute().__str__(), 'rb')
            data = wrap_file(environ, file)

            mtype = mimetype or mimetypes.guess_type(file_path.__str__())[0]

            # Sometimes files are named without extensions in the local storage, so
            # instead try and infer from the route
            if mtype is None:
                urifile = environ.get('PATH_INFO').split('/')[-1:][0]
                mtype = mimetypes.guess_type(urifile)[0]


            response = Response(data, direct_passthrough=True)
            response.headers['Content-Type'] = '{};charset=utf-8'.format(mtype)
            response.headers['Cache-Control'] = 'public, max-age=10800'

            if cors: cors.set(response)
            return response

        # No template, just plain old string response
        if isinstance(data, str):
            response = Response(data)
            response.headers['Content-Type'] = 'text/html;charset=utf-8'
            if cors: cors.set(response)
            return response


        # Just raw data, send as is
        # TODO: Must be flagged as json explicity
        out = tojson(data)
        response = Response(out)
        response.headers['Content-Type'] = 'application/json'
        if cors: cors.set(response)
        return response

    @staticmethod
    def response(data, *args, **kwargs):
        # TODO: This should build a web() compliant response object
        # that handles cors, additional headers, etc
        response=Response(data, *args, **kwargs)
        # if cors: cors.set(response)


        return response

    @staticmethod
    def filter(name):

        def wrap(fn):
            # Add to filters dict
            web.filters[name] = fn

            def decorated(*args, **kwargs):
                fn(*args, **kwargs)
            return decorated
        return wrap

        @functools.wraps(fn)
        def decorated(request, *args, **kwargs):
            return fn(request, *args, **kwargs)

        # Return pretty much unmodified, we really only
        # wanted this to index it into filters dict
        return decorated

    @staticmethod
    def template(cwd, template, data):
        # This maye have to be removed if CWD proves to be mutable per request
        web.template_engine = web.template_engine or Template(cwd)

        # Add any registered filters
        for filter in web.filters.keys():
            web.template_engine.env.filters[filter] = web.filters[filter]

        # Return Rendering
        return web.template_engine.render(template, data)

    @staticmethod
    def redirect(location, code=302, Response=None):
        return wz_redirect(location, code, Response)

    @staticmethod
    def abort(code=404):
        return abort(code)

    @staticmethod
    def all():
        return web.destination

