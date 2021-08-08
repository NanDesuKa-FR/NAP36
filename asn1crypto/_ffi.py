# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\asn1crypto\_ffi.py
"""
FFI helper compatibility functions. Exports the following items:

 - LibraryNotFoundError
 - FFIEngineError
 - bytes_from_buffer()
 - buffer_from_bytes()
 - null()
"""
from __future__ import unicode_literals, division, absolute_import, print_function
from ctypes import create_string_buffer

def buffer_from_bytes(initializer):
    return create_string_buffer(initializer)


def bytes_from_buffer(buffer, maxlen=None):
    return buffer.raw


def null():
    pass


class LibraryNotFoundError(Exception):
    __doc__ = '\n    An exception when trying to find a shared library\n    '


class FFIEngineError(Exception):
    __doc__ = '\n    An exception when trying to instantiate ctypes or cffi\n    '