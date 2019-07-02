from simplerr import web
from model import Person


@web('/')
def index(request): return "working..."


@web('/echo/<msg>')
def echo(request, msg):
    return "Echo from page: {}".format(msg)


@web('/echo/args')
def echo_args(request):
    return "Echo using args: {}".format(request.args['msg'])


@web('/echo/form')
def echo_form(request):
    msg = "NOTHING"

    if "msg" in request.form.keys():
        msg = request.form["msg"]

    return """
    <html>
    <body>
     <form method=post action="">
      Mesage: <input type=text name="msg" value="" placeholder="Enter msg value"/><input type="submit">
      You typed in: "{}"
     </form>
    </body>
    </html>
    """.format(msg)


@web('/echo_json/<msg>')
def echo_json(request, msg):
    return {'msg': msg}


@web('/echo/template/<msg>', 'templates/echo.html')
def echo_template(request, msg):
    return {'msg': msg}


@web('/person/api/all')
def person_api(request):
    return Person.select()


@web('/person/api/first')
def person_first(request):
    return Person.select().get()


@web('/files/<path:file>', file=True)
def files(request, file):
    return 'assets/' + file
