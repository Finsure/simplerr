from simplerr.web import web

@web('/api')
def docs(request):
    return """
    <pre>
        This is a basic echo json response, for example, make a request to
        '/api/echo/Hello World' to have your message reflected back.
    </pre>
    """

@web('/api/echo/<msg>')
def echo_json(request, msg):
    return {'msg': msg}
