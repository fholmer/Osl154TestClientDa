# -*- coding: utf-8 -*-
"""A setuptools based setup module.

Code style:
    python -m isort -rc osl154 tests
    python -m black osl154 tests

Build wheel:
    python setup.py bdist_wheel

Update requirements:
    python -m pip freeze -r requirements.txt > requirements.txt

Upload to pypi:
    python -m twine upload dist/*

"""

# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

from osl154 import __version__ as app_version

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="osl154",
    version=app_version,
    description="Opc Da command line test client for Osl154 specification",
    long_description=long_description,
    keywords="osl154 project template",
    url="https://github.com/fholmer/Osl154TestClientDa",
    author="Frode Holmer",
    author_email="fholmer+osl154@gmail.com",
    license="GNU General Public License (GPL)",
    project_urls={"Source Code": "https://github.com/fholmer/Osl154TestClientDa"},
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=find_packages(include=["osl154*"]),
    install_requires=[
        "OpenOPC-Python3x==1.3.1",
        "Pyro4==4.80",
        "pywin32==228; sys_platform == 'win32'",
        "Pillow==8.0.1",
    ],
    entry_points={
        'console_scripts': [
            'osl154=osl154.__main__:main',
        ],
    },
)
