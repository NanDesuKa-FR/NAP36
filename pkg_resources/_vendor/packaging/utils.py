# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\pkg_resources\_vendor\packaging\utils.py
from __future__ import absolute_import, division, print_function
import re
_canonicalize_regex = re.compile('[-_.]+')

def canonicalize_name(name):
    return _canonicalize_regex.sub('-', name).lower()