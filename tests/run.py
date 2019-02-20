#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pathlib import Path
import sys
import unittest
from colour_runner import runner
import click


# Idenify key project directories and add them to the python search path
project_path = Path(__file__).resolve().parents[1]
sys.path.append( str(project_path) )

class test_processor(object):

    def __init__(self):
        self.modules = [
            'modules.simplerr.template',
            'modules.simplerr.script',
            'modules.simplerr.web',
            ]

        self.suite = unittest.TestSuite()
        self.verbosity = 2

    def run(self):

        for t in self.modules:
            try:
                # If the module defines a suite() function, call it to get
                # the suite.
                mod = __import__(t, globals(), locals(), ['suite'])
                suitefn = getattr(mod, 'suite')
                self.suite.addTest(suitefn())
            except (ImportError, AttributeError):
                # else, just load all the test cases from the module.
                self.suite.addTest(
                    unittest.defaultTestLoader.loadTestsFromName(t)
                )

        # unittest.TextTestRunner().run(suite)
        runner.ColourTextTestRunner(verbosity=self.verbosity).run(self.suite)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        # click.echo('Running all tests.')
        tester = tests()
        tester.run()
    else:
        # click.echo('I am about to invoke %s' % ctx.invoked_subcommand)
        click.echo('Running specified test.')
        pass


@cli.command()
def all():
    tester = tests()
    tester.run()


@cli.command()
@click.option('-m', '--module', multiple=True, default=None)
def tests(module):
    tester = test_processor()
    tester.modules = module or tester.modules
    tester.run()


if __name__ == '__main__':
    cli()
