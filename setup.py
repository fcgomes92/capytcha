#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def _get_version():
    with open('VERSION') as fd:
        return fd.read().strip()


setup(
    name='capytcha',
    author='Fernando Gomes',
    author_email='fcgomes.92@gmail.com',
    license='Apache Version 2.0 License',
    version=_get_version(),
    packages=find_packages('./'),
    package_dir={'': './'},
    py_modules=['capytcha_server', 'capytcha'],
    include_package_data=True
)
