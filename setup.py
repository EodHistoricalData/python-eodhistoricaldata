#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from os import path
import io

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    print("Can't import pypandoc - using README.md without converting to RST")
    long_description = open('README.md').read()

NAME = 'eod_historical_data'
with io.open(path.join(here, NAME, 'version.py'), 'rt', encoding='UTF-8') as f:
    exec(f.read())

install_requires = []
with open("./requirements.txt") as f:
    install_requires = f.read().splitlines()
with open("./requirements-dev.txt") as f:
    tests_require = f.read().splitlines()
    
setup(
    name=NAME,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/development.html#single-sourcing-the-version
    # version='0.0.2',
    version=__version__,

    description='End Of Day historical data using Python, Requests, Pandas',
    long_description=long_description,

    # The project's main homepage.
    url=__url__,

    # Author details
    author=__author__,
    author_email=__email__,

    # Choose your license
    license=__license__,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Intended Audience :: Financial and Insurance Industry',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Office/Business :: Financial',
        'License :: OSI Approved :: MIT License',
    ],

    keywords='python trading data stock index',
    install_requires=install_requires,
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    test_suite="tests",
    tests_require=tests_require,
    zip_safe=False,
)
