# Imports {{{1
from unittest import TestCase
from simplerr.script import script
import os


# Basic Template  {{{1
class BasicScriptTests(TestCase):

    def setUp(self):
       self.cwd = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def get_script(self, route):
        sc = script(self.cwd, route)
        return sc.get_script()

    def get_module(self, route):
        sc = script(self.cwd, route)
        return sc.get_module()


    def test_path(self):
        expect = f'{self.cwd}/assets/scripts/sc_hello_world.py'
        path = self.get_script('/assets/scripts/sc_hello_world')
        self.assertEqual(expect, path)

    def test_path_index(self):
        expect = f'{self.cwd}/assets/scripts/index.py'
        path = self.get_script('/assets/scripts')
        self.assertEqual(expect, path)

    def test_module(self):
        expect = "Hello World"
        module = self.get_module('/assets/scripts/sc_hello_world')
        self.assertEqual(expect, module.__description__)


