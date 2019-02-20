from simplerr import dispatcher


site = '/Users/harvey/dev/simplerr.com/examples/03.todo/'
hostname = 'localhost'
port = 80

wsgi = dispatcher.wsgi(site, hostname, port)
application = wsgi.make_app()
