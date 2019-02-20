from simplerr.web import web


@web('/')
def index(r):
    return "Hello from Appche!!!"
