# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: distutils\__init__.py
"""distutils

The main package for the Python Module Distribution Utilities.  Normally
used from a setup script as

   from distutils.core import setup

   setup (...)
"""
import sys
__version__ = sys.version[:sys.version.index(' ')]