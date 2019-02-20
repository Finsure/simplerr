#!/usr/bin/env python
"""
Example usage

./manage.py runserver --site ./examples/contacts
"""
import click
import os
from simplerr import dispatcher


@click.group()
def cli(): pass

@cli.command()
@click.option('-s', '--site', type=str, default='/', help='/app_path')
@click.option('-h', '--hostname', type=str, default='localhost', help="localhost")
@click.option('-p', '--port', type=int, default=9000, help="9000")
@click.option('--reloader', is_flag=True, default=True)
@click.option('--debugger', is_flag=True, default=False)
@click.option('--evalex', is_flag=True, default=False)
@click.option('--threaded', is_flag=True)
@click.option('--processes', type=int, default=1, help="1")
def runserver(site, hostname, port, reloader, debugger, evalex, threaded, processes):

    basedir = os.path.abspath( os.getcwd() ) + site

    """Start a new development server."""
    app = dispatcher.wsgi(basedir, hostname, port,
               use_reloader=reloader,
               use_debugger=debugger,
               use_evalex=evalex,
               threaded=threaded,
               processes=processes) # , ssl_context=(crt, key))

    app.serve()



if __name__ == '__main__':
    cli()

