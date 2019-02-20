#!/usr/bin/env python

import click
from werkzeug.serving import run_simple

import time
from os import path
from threading import Thread
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.debug import DebuggedApplication
from werkzeug.serving import make_ssl_devcert
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from jinja2 import Environment, FileSystemLoader, Template

import functools
from pathlib import Path
import importlib.util

from .web import web
from .script import script
from .session import FileSystemSessionStore

import sys
import json

class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class SiteNoteFoundError(Error):
    """Exception raised for errors in the site path

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, site, message):
        self.site = message
        self.message = message


#
#  _   _   _   _  _  _   _ _ _ __  __  _
# | \_/ | / \ | || \| | | | | / _|/ _|| |
# | \_/ || o || || \\ | | V V \_ ( |_n| |
# |_| |_||_n_||_||_|\_|  \_n_/|__/\__/|_|
#
#  ___  ___  _   _   _  ___  _ _ _  _  ___ _  _
# | __|| o \/ \ | \_/ || __|| | | |/ \| o \ |//
# | _| |   / o || \_/ || _| | V V ( o )   /  (
# |_|  |_|\\_n_||_| |_||___| \_n_/ \_/|_|\\_|\\
#
#

class WebEvents(object):
    """Web Request object, extends Request object.  """

    def __init__(self):
        self.pre_request = []
        self.post_request = []

    # Pre-request subscription
    def on_pre_response(self, fn):
        self.pre_request.append(fn)

    def off_pre_response(self, fn):
        """Remove from pre_request"""
        self.pre_request.remove(fn)

    def fire_pre_response(self, request):
        for fn in self.pre_request:
            fn(request)

    # Post-Request subscription management
    def on_post_response(self, fn):
        self.post_request.append(fn)

    def off_post_response(self, fn):
        """Remove from pre_request"""
        self.post_request.remove(fn)

    def fire_post_response(self, request, response):
        for fn in self.post_request:
            fn(request, response)



class WebRequest(Request):
    """Web Request object, extends Request object.  """

    def __init__(self, *args, auth_class=None, **kwargs):
        super(WebRequest, self).__init__(*args, **kwargs)
        self.view_events = WebEvents()

    @property
    def json(self):
        """Adds support for JSON and other niceties"""
        # TODO: need to cache this otherwise each call runs json.loads
        # TODO: Can we use werkzeug JSONRequestMixin?
        #       see https://github.com/pallets/werkzeug/blob/master/werkzeug/contrib/wrappers.py#L44
        try:
            data = self.data
            out = json.loads(data, encoding="utf8")
        except ValueError as e:
            out = None
        return out


class dispatcher(object):

    def __init__(self, cwd, global_events):
        self.cwd = cwd
        self.global_events = global_events

    def __call__(self, environ, start_response):
        """This methods provides the basic call signature required by WSGI"""
        request = WebRequest(environ)
        response = self.dispatch_request(request, environ)
        return response(environ, start_response)

    def dispatch_request(self, request, environ):

        # Fire Pre Response Events
        self.global_events.fire_pre_response(request)
        request.view_events.fire_pre_response(request)

        # RestorePresets
        web.restore_presets()

        # Get view script and view module
        sc = script(self.cwd, request.path)
        view_module = sc.get_module()

        
        # Process Response, and get payload
        response = web.process(request, environ, self.cwd)


        # Done, fire post response events
        request.view_events.fire_post_response(request, response)
        self.global_events.fire_post_response(request, response)

        # There should be no more user code after this being run
        return response  # return web.process(route).


### WSGI Server
class wsgi(object):

    def __init__(self, site, hostname, port, use_reloader=True,
                  use_debugger=False, use_evalex=False, threaded=True,
                  processes=1, use_profiler=False):

        self.site = site
        self.hostname = hostname
        self.port = port
        self.use_reloader = use_reloader
        self.use_debugger = use_debugger
        self.use_evalex = use_evalex
        self.threaded = threaded
        self.processes = processes

        self.app = None


        # TODO: Need to update interface to handle these
        self.session_store = FileSystemSessionStore()

        self.cwd = self.make_cwd()


        # Add Relevent Web Events
        # NOTE: Events created at this level should fire static events that
        # are fired on every request and will share application data, all other
        # events should be reset between views. Make sure to not use the global
        # object unless you want the event called at every view.
        self.global_events = WebEvents()

        # Add some key events
        self.global_events.on_pre_response(self.session_store.pre_response)
        self.global_events.on_post_response(self.session_store.post_response)

        # Add CWD to search path, this is where project modules will be located
        sys.path.append( self.cwd.absolute().__str__() )

    def make_cwd(self):
        path_site = Path(self.site)
        path_with_cwd = Path.cwd() / path_site

        if path_site.exists():
            return path_site

        if path_with_cwd.exists():
            return path_with_cwd

        raise SiteNoteFoundError(
            self.site,
            "Could not access folder"
        )

    def make_app(self):
        from werkzeug.contrib.profiler import ProfilerMiddleware
        # self.app = ProfilerMiddleware(dispatcher(self.cwd.absolute().__str__(), self.global_events))
        self.app = dispatcher(self.cwd.absolute().__str__(), self.global_events)

        # if self.use_profiler:
        #     self.app = ProfilerMiddleware(self.app)




        return self.app

    def make_app_debug(self):
        self.app = DebuggedApplication(
            #dispatcher(self.cwd.absolute().__str__()),
            self.make_app(),
            evalex=True
        )

        return self.app

    def serve(self):
        """Start a new development server."""

        self.make_app_debug()

        """Generate SSL Keys, not currently used, needs some improvements"""
        # (crt, key) = make_ssl_devcert('/tmp/', host='localhost')

        run_simple(self.hostname,
                   self.port,
                   self.app,
                   use_reloader=self.use_reloader,
                   use_debugger=self.use_debugger,
                   threaded=self.threaded,
                   processes=self.processes) # , ssl_context=(crt, key))

