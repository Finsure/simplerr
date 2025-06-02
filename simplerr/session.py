from secure_cookie.session import FilesystemSessionStore as WerkzeugFilesystemSessionStore


class SessionSignalMixin:

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


class FileSystemSessionStore(WerkzeugFilesystemSessionStore, SessionSignalMixin):

    def __init__(self, session_class=None):
        # Number of minutes before sessions expire
        self.expire = 40

        self.COOKIE_NAME = "sessionfast"
        WerkzeugFilesystemSessionStore.__init__(self, session_class=None)

    def clean(self):
        pass
