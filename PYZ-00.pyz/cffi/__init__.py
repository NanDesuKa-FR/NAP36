# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cffi\__init__.py
__all__ = [
 'FFI', 'VerificationError', 'VerificationMissing', 'CDefError',
 'FFIError']
from .api import FFI
from .error import CDefError, FFIError, VerificationError, VerificationMissing
__version__ = '1.11.5'
__version_info__ = (1, 11, 5)
__version_verifier_modules__ = '0.8.6'