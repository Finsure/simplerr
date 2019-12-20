#!/usr/bin/env python

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request
from werkzeug.debug import DebuggedApplication

from pathlib import Path

from .web import web
from .script import script
from .session import FileSystemSessionStore

import sys
import json


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class SiteNotFoundError(Error):
    """Exception raised for errors in the site path

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, site, message):
        self.site = message
        self.message = message


class WebEvents(object):
    """Web Request object, extends Request object."""

    def __init__(self):
        self.pre_request = []
        self.post_request = []
        self.post_exception = []
        self.error_handler = {}

    def on_error(self, code, fn):
        self.error_handler[code] = fn

    # Pre-request subscription
    def on_pre_response(self, fn):
        self.pre_request.append(fn)

    def off_pre_response(self, fn):
        self.pre_request.remove(fn)

    def fire_pre_response(self, request):
        for fn in self.pre_request:
            fn(request)

    # Post-Request subscription management
    def on_post_response(self, fn):
        self.post_request.append(fn)

    def off_post_response(self, fn):
        self.post_request.remove(fn)

    def fire_post_response(self, request, response):
        for fn in self.post_request:
            fn(request, response)

    # Post-Request exception management
    def on_post_exception(self, fn):
        self.post_exception.append(fn)

    def off_post_exception(self, fn):
        self.post_exception.remove(fn)

    def fire_post_exception(self, request, e):
        for fn in self.post_exception:
            fn(request, e)


class WebRequest(Request):
    """Web Request object, extends Request object.  """

    def __init__(self, *args, auth_class=None, **kwargs):
        super(WebRequest, self).__init__(*args, **kwargs)
        self.view_events = WebEvents()

    @property
    def json(self):
        """Adds support for JSON and other niceties"""
        try:
            data = self.data
            out = json.loads(data, encoding="utf8")
        except ValueError:
            out = None

        return out


class dispatcher(object):

    def __init__(self, cwd, global_events):
        self.cwd = cwd
        self.global_events = global_events

    def __call__(self, environ, start_response):
        """This methods provides the basic call signature required by WSGI"""
        request = WebRequest(environ)

        # Fire Pre Response Events
        self.global_events.fire_pre_response(request)
        request.view_events.fire_pre_response(request)

        # RestorePresets
        web.restore_presets()

        # Get view script and view module
        sc = script(self.cwd, request.path)
        sc.get_module()

        # Process Response, and get payload
        try:
            response = web.process(request, environ, self.cwd)
        except Exception as e:
            if hasattr(e, 'code') and self.global_events.error_handler.get(e.code) is not None:
                # Is a werkzeug error and we should handle it
                response = self.global_events.error_handler[e.code]()
            else:
                # Catch all
                self.global_events.fire_post_exception(request, e)
                raise e

        # Done, fire post response events
        request.view_events.fire_post_response(request, response)
        self.global_events.fire_post_response(request, response)

        # There should be no more user code after this being run
        return response(environ, start_response)


class Simplerr(object):

    def __init__(
        self,
        site,
        hostname,
        port,
        use_reloader=True,
        use_debugger=False,
        use_evalex=False,
        threaded=True,
        processes=1,
        use_profiler=False
    ):
        self.site = site
        self.hostname = hostname
        self.port = port
        self.use_reloader = use_reloader
        self.use_debugger = use_debugger
        self.use_evalex = use_evalex
        self.threaded = threaded
        self.processes = processes

        self.session_store = FileSystemSessionStore()
        self.cwd = self.make_cwd()

        # Add Relevent Web Events
        # NOTE: Events created at this level should fire static events that
        # are fired on every request and will share application data, all other
        # events should be reset between views. Make sure to not use the global
        # object unless you want the event called at every view.
        self.global_events = WebEvents()

        # Add session events to pre and post response
        self.global_events.on_pre_response(self.session_store.pre_response)
        self.global_events.on_post_response(self.session_store.post_response)

        # Add CWD to search path, this is where project modules will be located
        sys.path.append(self.cwd.absolute().__str__())

        # The actual WSGI application. Applied here to allow for middleware
        # e.g With socketio:
        # app.wsgi = socketio.WSGIApp(sio, app.wsgi)
        self.wsgi = dispatcher(self.cwd.absolute().__str__(), self.global_events)

    def pre_response(self, m):
        self.global_events.on_pre_response(m)

        def decorator(f, request):
            f(request)
            return f

        return decorator

    def post_response(self, m):
        self.global_events.on_post_response(m)

        def decorator(f, request, response):
            f(request, response)
            return f

        return decorator

    def post_exception(self, m):
        self.global_events.on_post_exception(m)

        def decorator(f, request, error):
            f(request, error)
            return f

        return decorator

    def errorhandler(self, code):

        def decorator(fn):
            self.global_events.on_error(code, fn)
            return fn

        return decorator

    def make_cwd(self):
        path_site = Path(self.site)
        path_with_cwd = Path.cwd() / path_site

        if path_site.exists():
            return path_site

        if path_with_cwd.exists():
            return path_with_cwd

        raise SiteNotFoundError(
            self.site,
            "Could not access folder"
        )

    def serve(self):
        """Start a new development server."""
        run_simple(
            self.hostname,
            self.port,
            DebuggedApplication(self.wsgi, evalex=True),
            use_reloader=self.use_reloader,
            use_debugger=self.use_debugger,
            threaded=self.threaded,
            processes=self.processes
        )
