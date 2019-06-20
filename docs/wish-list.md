Urgent for 0.16 Release
=======================

The 0.16 release aims to stabilise basic web routing and functionality, as well
as provide adequate documentation to get developers started in the world of
Simplerr Development.


0. Asset handling
-----------------

    @web.js('all_financials_js', source_dir='/financials/static')
    def jsbundle():
        """Bundle up the javascript files

        note: in jinja must include the following snippet

            {% assets "all_financials_js" %}
                <script type="text/javascript" src="{{ ASSET_URL }}"></script>
            {% endassets %}
        """

        yield 'app.controller.js'
        yield 'app.service.js'



0. Basic features still missing
-------------------------------

[x] Easy file upload - already supported by werkzeug
[x] Easy access to request and response objects

[ ] Config to specify filenames for security, eg

      * `web.config['WEB_FILES'] = ['*.py']` - default
      * `web.config['WEB_FILES'] = ['index.py', 'api.py']`
      * `web.config['WEB_FILES_PREFIX'] = ['__web__']`
      * See flask inplementation: https://github.com/pallets/flask/blob/16d83d6bb413bec09a656a659b98d897e7abcc81/flask/globals.py
      * Uses wekzeug Locals: http://werkzeug.pocoo.org/docs/0.14/local/

[ ] Make routes relative to folder, eg for http://example.com/foo/bar/hello

    # File /foo/bar/index.py
    #
    # @web('/hello')
    # def hello(r):
    #   return "World"
    #

Notes:

1) We can simply add two routes for each @web(), one including the folder path
2) If we detect and old route, send deprecation warning


1. Fix issues when errors occur
-------------------------------

[x] 1.1 Test when not in debug mode - currently not able to disable debug mode from manage.py
[ ] 1.2 Create cusomisable error templates

2. Bug where by responses slow down after an error, test errors with 1 thread to replicate
------------------------------------------------------------------------------------------

Could not replicate - needs more testing

3. Bug in json posts
3. Bug in json posts

Temp work around is to json.loads(request.data)

4. Ensure multiple routes to the same method are possible
---------------------------------------------------------

For example, we should be able to allow the same method to be used for multiple
routes, for example::

    python
    @web('/e/<msg>')
    @web('/echo/<msg>')
    def echo(request, msg):
      return msg


5. Ensure methods=['GET', 'POST', 'DELETE', 'PUT', 'ANY'] are respected
-----------------------------------------------------------------------


For example, we should be able to request routes as per the example below::

    python
    @web('/form/action', methods=['POST'])
    def form_action(request):
      return request.form['var']


6. Static file sending improvements
-----------------------------------

6.1 Ensure that we can specify allowed file types when proxying files, for example::

    python
    @web('/static/<path:file>', file=True, allow=['*.html', '*.js', '*.css'])
    def static(request, file):
      return file


6.2 Review efficient file handing - streaming, and web server bypass

7. Egg builds and PyPy install
------------------------------

See example package implementations below
 - http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/quickstart.html
 - http://veekaybee.github.io/2017/09/26/python-packaging/?utm_source=mybridge&utm_medium=blog&utm_campaign=read_more for a workflow.
 - https://milkr.io/kfei/5-common-patterns-to-version-your-Python-package

8. Ability to easily add filters to template eng
---------------------------------------------------

9. Review introduction of __web__.py file to register routes
------------------------------------------------------------

10. Improved routing grammar
----------------------------

Target grammar will be::

    @web('/src/abc', '/templates/somefile.html', POST, GET)
    @web('/src/abc', POST)

Implementation will follow the syntax below::

    # methods.py
    class Method(object):

        def __call__(self, method):
            self.method

    # Export these classes from method.py
    GET = Method('GET')
    POST = Method('POST')
    DELETE = Method('DELETE')
    PUT = Method('PUT')


## 11. Improved authentication gram
-----------------------------------

Imporoved pythonic authentication, pseudo code below::

    @web.auth()
    def auth_default(request):
      # Auth checks go here


    # Override
    @web('/index', auth=None)
    def public_page(request):
      # Some public method

## 12. Url for functionality
------------------------------


Will need to use same syntax as flask blueprints, full relative/reference to module. Eg for a file in;

- /index view method home() - link('home') is fine
- /api/users, method add() - link('api.users.add')


13. Test having routes in one location that aliases nested apps
---------------------------------------------------------------

For example, at the root folder in index.py::

    # index.py - multiple routes test
    from simplerr import web
    impor my_app

    # my_app.py

    @web('/not_xxxactually_folder/testme')
    def testme(request):
      url_for('my_app.testme')  #<-- Maps via library-method name
      return "Hello World"




Release 0.17
============

- Improved Signals/Events Support
  - See http://flask.pocoo.org/docs/0.12/api/#core-signals-list

- Review livereload for runnserver
  - https://github.com/lepture/python-livereload
  - Use to rebuild docs
  - Run the wsgi instance
  - Can we inject livereload.js into reponse when <html> is present?

- Full Text Search Engine
  - http://sqlite.org/fts3.html
  - http://charlesleifer.com/blog/meet-scout-a-search-server-powered-by-sqlite/

- Email handling
  - Sync with imap/pop accounts
  - Thread responses
  - Track open/forward rates

- SMS Handling
  - Track responses

- Sessions using Key/Value Storage
  - https://github.com/coleifer/peewee/blob/master/playhouse/kv.py

- Better API - integrate with docstring
- Prospector integration
- Unit testing integration

- Restful API's Integregation with Swagger Docs
  - Review Marshmallow for serialisation

      - https://github.com/klen/marshmallow-peewee
      - https://pypi.python.org/pypi/Marshmallow-Peewee/1.2.7

  - See example at  http://python-eve.org/
  - With Swagger https://github.com/pyeve/eve-swagger
  - Good presentation of core issues https://speakerdeck.com/nicola/developing-restful-web-apis-with-python-flask-and-mongodb
  - Worth reviewig deployd

- Arrow for all date time fields

  - See http://arrow.readthedocs.io/en/latest/
  - Main benefit is creating global times, eg arrow.utcnow().to('US/Pacific')


Release 0.18
============

- NoSQL Integration with tinydb
- Websocket integration, as a use case look at
  https://www.willmcgugan.com/blog/tech/post/stream-btc-prices-over-websockets-with-python-and-lomond/
  https://github.com/zeekay/flask-uwsgi-websocket using debugger
  https://github.com/aldanor/SocketIO-Flask-Debug ::

    @websocket('/echo')
    def echo(request):
      return msg


- Debug bar setup - with docstring support, see

  - For unit tests; http://tungwaiyip.info/software/sample_test_report.html or https://github.com/meshy/colour-runner/tree/master/colour_runner
  - Integrateion with custom stop points for werkzeug debugger
  - sqls
  - output for prospector or other linter

- Advanced Debug - Integration with parasite for inspecting the wsgi and requests

    - See how it works at: http://pyrasite.com/
    - Connecting a shell to a process: http://pyrasite.readthedocs.io/en/latest/Shell.html
    - Details process information: http://pyrasite.readthedocs.io/en/latest/GUI.html

- Tips on starting the interactive debugger on errors: https://stackoverflow.com/questions/13174412/python-start-interactive-debugger-when-exception-would-be-otherwise-thrown


- Review web based pdb python debuggers

    - https://github.com/Kozea/wdb
    - https://pypi.org/project/web-pdb/

`Full Stack Python <https://www.fullstackpython.com>`_ has a good section on `webcokets <https://www.fullstackpython.com/websockets.html>`_


Release 0.20
============

- Tasks and Daemon Processes
- SSO Integration

Release 0.22
============

Look at implementing improved http and asyn using core c-libraries such as found in `Japantro <https://github.com/squeaky-pl/japronto>`_

Nice write up at https://medium.freecodecamp.org/million-requests-per-second-with-python-95c137af319
