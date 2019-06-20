from simplerr.web import web

@web('/static/<path:file>', file=True)
def file(request, file):
    return "./assets/" + file


@web('/static/test')
def withcss(request):

    return """
    <html>
    <head>
        <link rel="stylesheet" href="/static/echo.css">
    </head>
    <body>
        <p>This should be big text!</p>
    </body>
    </html>
    """







