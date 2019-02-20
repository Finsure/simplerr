from unittest import TestCase
from simplerr.web import web, GET, POST, DELETE, PUT, PATCH
from werkzeug.test import EnvironBuilder
import os
from pprint import pprint

"""
This test suite makes extensive use the the werkzeug test framework, it can be
found here: http://werkzeug.pocoo.org/docs/0.14/test/


"""

@web('/simple')
def simple_fn(r):
    return

@web('/response/string')
def string_response_fn(r):
    return ""

@web('/response/dict')
def dict_response_fn(r):
    return {}

@web('/response/file', file=True)
def file_response_fn(r):
    return 'assets/html/01_pure_html.html'

@web.filter('echo')
def echo_fn(msg):
    return msg


@web.filter('upper')
def upper_fn(text):
    return upper(text)

def create_env(path, method='GET'):
    from werkzeug.test import EnvironBuilder
    builder = EnvironBuilder(method=method, path=path)
    env = builder.get_environ()

    return env

# Basic Template  {{{1
class BasicWebTests(TestCase):

    def setUp(self):
       self.cwd = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def test_check_routes(self):
        self.assertEqual( web.destinations[0].endpoint, 'simple_fn' )
        self.assertEqual( web.destinations[0].route, '/simple' )

        self.assertEqual( web.destinations[1].endpoint, 'string_response_fn' )
        self.assertEqual( web.destinations[1].route, '/response/string' )

        self.assertEqual( web.destinations[2].endpoint, 'dict_response_fn' )
        self.assertEqual( web.destinations[2].route, '/response/dict' )


    def test_match_simple_route(self):
        rv = web.match(create_env('/simple'))
        self.assertEquals( rv.endpoint, 'simple_fn')


    def test_process_request(self):
        from werkzeug.wrappers import Request, Response
        env = create_env('/simple')
        req = Request(env)

        resp = web.process(req, env, self.cwd)
        self.assertIsInstance(resp, Response)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data, b'null')


    def test_response_util(self):
        from werkzeug.wrappers import Request, Response
        resp = web.response(None)
        self.assertIsInstance(resp, Response)

    def test_filter_decorator(self):
        self.assertIn('echo', web.filters)

    def test_template_util(self):
        rv = web.template(self.cwd, '/assets/html/01_pure_html.html', {})
        self.assertEquals(rv, 'Hello World')

    def test_request_redirect(self):
        from werkzeug.wrappers import Request, Response
        rv = web.response('http://example.com')
        self.assertIsInstance(rv, Response)

    def test_request_abort(self):
        from werkzeug.exceptions import NotFound, Unauthorized
        self.assertRaises(NotFound, web.abort)
        self.assertRaises(Unauthorized, web.abort, code=401)

    def test_send_files(self):
        from werkzeug.wrappers import Request, Response

        env = create_env('/response/file')
        req = Request(env)

        resp = web.process(req, env, self.cwd)

        self.assertIsInstance(resp, Response)
        self.assertEquals(resp.status_code, 200)

        # Need to disable direct passthrough for testing
        resp.direct_passthrough = False
        self.assertEqual(resp.data, b'Hello World\n')


