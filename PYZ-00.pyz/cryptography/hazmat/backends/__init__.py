# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\backends\__init__.py
from __future__ import absolute_import, division, print_function
_default_backend = None

def default_backend():
    global _default_backend
    if _default_backend is None:
        from cryptography.hazmat.backends.openssl.backend import backend
        _default_backend = backend
    return _default_backend