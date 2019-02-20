"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from os import path

import io
import re


here = path.abspath(path.dirname(__file__))

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('simplerr/__init__.py', 'rt', encoding='utf8') as f:
    info = f.read()
    version = re.search(r'__version__ = \"(.*?)\"', info).group(1)


setup(
    name='simplerr',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=str(version),

    description='A sample Python webframework',
    long_description=readme,

    # The project's main homepage.
    url='https://github.com/yevrah/simplerr',

    # Author details
    author='Javier Woodhouse',
    author_email='javier@wingaru.com.au',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Web Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='simple web development framework',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['simplerr'],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'asn1crypto==0.24.0',
        'cffi==1.11.4',
        'click==6.7',
        'colorama==0.3.9',
        'cryptography==2.1.4',
        'idna==2.6',
        'Jinja2==2.10',
        'MarkupSafe==1.0',
        'peewee==3.0.18',
        'pycparser==2.18',
        'pyOpenSSL==17.5.0',
        'redis==2.10.6',
        'six==1.11.0',
        'termcolor==1.1.0',
        'Werkzeug==0.14.1',
        # Doesntwork on windows, but needed for some examples
        # 'mod-wsgi==4.5.24',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    #package_data={
    #    'sample': ['package_data.dat'],
    #},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file.txt'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'webserv=simplerr.__main__:main',
        ],
    },

    zip_safe=False,
)
