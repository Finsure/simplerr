from werkzeug.contrib.sessions import SessionStore, SessionMiddleware
from werkzeug.contrib.sessions import FilesystemSessionStore as WerkzeugFilesystemSessionStore
from datetime import datetime, timedelta


class SessionSignalMixin():


    def pre_response(self, request):
        self.clean()
        sid = request.cookies.get(self.COOKIE_NAME)

        if sid is None:
            request.session = self.new()
        else:
            request.session = self.get(sid)

    def post_response(self, request, response):
        if request.session.should_save:
            self.save(request.session)
            response.set_cookie(self.COOKIE_NAME, request.session.sid)


class MMemorySessionStore(SessionStore, SessionSignalMixin):
    """TODO: Flesh out, sourced from
    https://github.com/pallets/werkzeug/blob/master/examples/contrib/sessions.py

    Review Flask Secure Sessions
    https://github.com/pallets/flask/blob/master/flask/sessions.py

    How to Use
    ----------

    def application(environ, start_response):
        session = environ['werkzeug.session']
        session['visit_count'] = session.get('visit_count', 0) + 1

        start_response('200 OK', [('Content-Type', 'text/html')])
        return ['''
            <!doctype html>
            <title>Session Example</title>
            <h1>Session Example</h1>
            <p>You visited this page %d times.</p>
        ''' % session['visit_count']]


    def make_app():
        return SessionMiddleware(application, MemorySessionStore())
    """


    def __init__(self, session_class=None):
        self.COOKIE_NAME = 'sessionfast'
        SessionStore.__init__(self, session_class=None)
        self.sessions = {}

        # Number of minutes before sessions expire
        self.expire = 40

    def clean(self):
        cleanup_sid = []

        # Collect sessions to cleanup
        for key in self.sessions.keys():
            accessed = self.sessions[key]['meta']['accessed']
            expiration = datetime.now() - timedelta(minutes=self.expire)

            if accessed < expiration:
                cleanup_sid.append(key)

        for expired_sid in cleanup_sid:
            self.delete(self.get(expired_sid))


    def save(self, session):
        self.sessions[session.sid] = {
            'session': session,
            'meta': {'accessed': datetime.now()}
        }

    def delete(self, session):
        self.sessions.pop(session.sid, None)

    def get(self, sid):
        if not self.is_valid_key(sid) or sid not in self.sessions:
            return self.new()
        return self.session_class(self.sessions[sid]['session'], sid, False)


    """
    From: http://werkzeug.pocoo.org/docs/0.14/contrib/sessions/

    For better flexibility it’s recommended to not use the middleware but the store
    and session object directly in the application dispatching:

    ::

        session_store = FilesystemSessionStore()

        def application(environ, start_response):
            request = Request(environ)
            sid = request.cookies.get('cookie_name')
            if sid is None:
                request.session = session_store.new()
            else:
                request.session = session_store.get(sid)
            response = get_the_response_object(request)
            if request.session.should_save:
                session_store.save(request.session)
                response.set_cookie('cookie_name', request.session.sid)
            return response(environ, start_response)


    The following provides a helper method for pre request and post request
    process.

    def pre_response(self, request):
        print("    > Cleaning Up Sessions")
        self.clean()

        print("    > Active Session: {}".format( len(self.sessions.keys())))
        sid = request.cookies.get(MemorySessionStore.COOKIE_NAME)
        print("    > Pre response session fired, cookie sid is: {}".format(sid))

        if sid is None:
            request.session = self.new()
            print("    > Generated new sid: {}".format(request.session.sid))
        else:
            request.session = self.get(sid)
            print("    > Using existing sid: {}".format(request.session.sid))

    def post_response(self, request, response):
        print("    > Post response session fired, saving sid: {}", request.session.sid)

        if request.session.should_save:
            print("    > Saving Session to cookie")
            self.save(request.session)
            response.set_cookie(MemorySessionStore.COOKIE_NAME,
                                request.session.sid)

    """

class NoSQLSessionStore(SessionStore):
    """Todo: Implement TinyDB dict session store"""
    pass

class DbSessionStore(SessionStore):
    """Todo: Implement Db session store"""
    pass



class FileSystemSessionStore(WerkzeugFilesystemSessionStore, SessionSignalMixin):

    def __init__(self, session_class=None):
        # Number of minutes before sessions expire
        self.expire = 40

        self.COOKIE_NAME = 'sessionfast'
        WerkzeugFilesystemSessionStore.__init__(self, session_class=None)

    def clean(self): pass
