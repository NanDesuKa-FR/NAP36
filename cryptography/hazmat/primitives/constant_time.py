# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\primitives\constant_time.py
from __future__ import absolute_import, division, print_function
import hmac, warnings
from cryptography import utils
from cryptography.hazmat.bindings._constant_time import lib
if hasattr(hmac, 'compare_digest'):

    def bytes_eq(a, b):
        if not isinstance(a, bytes) or not isinstance(b, bytes):
            raise TypeError('a and b must be bytes.')
        return hmac.compare_digest(a, b)


else:
    warnings.warn('Support for your Python version is deprecated. The next version of cryptography will remove support. Please upgrade to a 2.7.x release that supports hmac.compare_digest as soon as possible.', utils.DeprecatedIn23)

    def bytes_eq(a, b):
        if not isinstance(a, bytes) or not isinstance(b, bytes):
            raise TypeError('a and b must be bytes.')
        return lib.Cryptography_constant_time_bytes_eq(a, len(a), b, len(b)) == 1