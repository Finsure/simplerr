from simplerr import dispatcher


site = '/Users/harvey/dev/simplerr.com/examples/01.kitchen_sink/'
hostname = 'localhost'
port = 80

wsgi = dispatcher.wsgi(site, hostname, port)
application = wsgi.make_app_prod()
