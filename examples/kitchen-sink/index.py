from simplerr import web, GET, POST

@web('/')
def plain(request):
    return web.redirect('/TOC')

@web('/TOC', '/assets/toc.html')
def template(request):
    import simplerr
    return {"version": simplerr.__version__}

@web('/echo/<msg>')
def echo(request, msg):
    return "Echo from index: {}".format(msg)

@web('/echo/args')
def echo_args(request):
    return "Echo using args: {}".format(request.args['msg'])

@web('/echo/form', GET)
def echo_form(request):
    request.session['abc']=10

    return """
    <html>
    <body>
     <form method=post action="">
      Message: <input type="text" name="msg" placeholder="Enter msg value"/>
      <input type="submit">
     </form>
    </body>
    </html>
    """

@web('/echo/form', POST)
def echo_form_post(request):
    msg = request.form["msg"]

    return """
    <html>
    <body>
      You typed in: "{}"
    </body>
    </html>
    """.format(msg)

class storeme():
    def __init__(self, name):
        self.name = name

@web('/echo/session/set')
def session_set(request):

    request.session['Hello'] = "Session World!"

    sme = storeme('John Doe')
    request.session['testobj'] = sme

    return "Added session Hello: {}".format( request.session['Hello'] )

@web('/echo/session/get')
def session_get(request):
    smeget = request.session['testobj']
    return "Getting session Hello: {}, {}".format( request.session['Hello'], smeget.name )

@web.filter('myupper')
def myupper(input):
    return input.upper()

@web('/echo/filter/<msg>', template="/assets/filter.html")
def echo_filter(request, msg):
    return {'msg': msg}

@web('/redirect')
def redirect(request):
    return web.redirect('http://google.com')

@web('/abort')
def redirect(request):
    return web.abort()

@web('/favicon.ico')
def favicon(request):
    return ""
