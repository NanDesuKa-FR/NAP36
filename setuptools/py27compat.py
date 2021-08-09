# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\py27compat.py
"""
Compatibility Support for Python 2.7 and earlier
"""
import platform
from setuptools.extern import six

def get_all_headers(message, key):
    """
    Given an HTTPMessage, return all headers matching a given key.
    """
    return message.get_all(key)


if six.PY2:

    def get_all_headers(message, key):
        return message.getheaders(key)


linux_py2_ascii = platform.system() == 'Linux' and six.PY2
rmtree_safe = str if linux_py2_ascii else (lambda x: x)