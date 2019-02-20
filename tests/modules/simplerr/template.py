# Imports {{{1
from unittest import TestCase
from simplerr.template import T

import os

# Basic Template  {{{1
class BasicTemplateTests(TestCase):

    def setUp(self):
       cwd = os.path.dirname(__file__)
       self.renderrer = T(cwd)

    def tearDown(self):
        pass

    def test_pure_html(self):
        expect="Hello World"
        rendered = self.renderrer.render('assets/html/01_pure_html.html')
        self.assertEqual(expect, rendered)

    def test_echo_back(self):
        expect="Hello World and Echo Back"
        stash= {"msg":expect}
        rendered = self.renderrer.render('assets/html/02_echo.html', stash)
        self.assertEqual(expect, rendered)


