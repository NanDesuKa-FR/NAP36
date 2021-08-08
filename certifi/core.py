# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\certifi\core.py
"""
certifi.py
~~~~~~~~~~

This module returns the installation location of cacert.pem.
"""
import os

def where():
    f = os.path.dirname(__file__)
    return os.path.join(f, 'cacert.pem')


if __name__ == '__main__':
    print(where())