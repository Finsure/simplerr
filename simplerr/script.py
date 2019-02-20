from pathlib import Path
import importlib.util

from werkzeug.exceptions import HTTPException, NotFound
"""
TODO: Review werkzeug.utils.find_modules

# werkzeug.utils.find_modules(import_path, include_packages=False, recursive=False)

Finds all the modules below a package. This can be useful to automatically
import all views / controllers so that their metaclasses / function decorators
have a chance to register themselves on the application.

Packages are not returned unless include_packages is True. This can also
recursively list modules but in that case it will import all the packages to
get the correct load path of that module.

Parameters:
    - import_path – the dotted name for the package to find child modules.
    - include_packages – set to True if packages should be returned, too.
    - recursive – set to True if recursion should happen.
Returns:
    - generator

"""

class script(object):

    # Set path to root of project
    # cwd = '/var/www/example.com'
    #
    # Route paths always maps to a physical files, as this is part of the
    # design
    #
    # route = '/'


    def __init__(self, cwd, route):
        self.cwd = Path(cwd)
        self.route = Path( "." + route)

    def get_script(self):
        # Examples
        #  /var/www/example.com/app/login
        #  /var/www/example.com/app/login/
        #  /var/www/example.com/app/login/exit
        #  /var/www/example.com/app/login/exit/1

        # Maximum search path, start the top of the
        # route and continue down. By using route
        # we ensure we don't dig deaper then the 
        # web path (cwd).

        # We also use pathlibs for a more OO view of the filesystem
        max_depth = self.route.parts.__len__()

        # First edge case, were calling site root '/', path treats this as 0 length
        # so it wont go into search loop below
        if max_depth == 0:
            root_index_py = self.cwd / 'index.py'
            if root_index_py.exists():
                return root_index_py.absolute().__str__()


        for i in range(max_depth,0,-1):
            search = self.route.parts[:i]
            search_path = self.cwd / Path(*search)

            # Is this a script file without the '.py'
            # eg, test for ..mple.com/app/login -> ..mple.com/app/login.py
            script_py_str = ''.join([search_path.__str__(), ".py" ])
            script_py = Path(script_py_str)

            if script_py.exists():
                return script_py.absolute().__str__()

            # Is this a folder with index.py
            # eg, test for ..mpl.com/app/login/index.py
            index_py = search_path / 'index.py'
            if index_py.exists():
                return index_py.absolute().__str__()


            # Parent folder "/app/" cant be a py file ("/.py") but can contain an
            # index.py file ("/index.py") so if i==1 then we have to test for
            # this final edge case. Note, application root is different to site
            # route and needs a different edge test
            if i!=1: continue

            root_index_py = search_path.parent / 'index.py'
            if root_index_py.exists():
                return root_index_py.absolute().__str__()

        raise NotFound('Could not find matching site file')



    def get_module(self):
        # https://www.blog.pythonlibrary.org/2016/05/27/python-201-an-intro-to-importlib/
        # https://docs.python.org/3/library/importlib.html


        # TODO: Change.. see https://dev.to/0xcrypto/dynamic-importing-stuff-in-python--1805
        # Can we replace this with the following
        # import importlib
        # module = importlib.import_module('abc')

        script = self.get_script()
        spec = importlib.util.spec_from_file_location("", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # You can no do this
        #   app = module.application()

        return module



