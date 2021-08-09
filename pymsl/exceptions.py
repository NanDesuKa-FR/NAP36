# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\pymsl\exceptions.py
"""This module stores various exceptions used by the client"""

class KeyExchangeError(Exception):
    __doc__ = 'Exception for key exchange issues'


class ManifestError(Exception):
    __doc__ = 'Exception for manifest parsing issues'


class LicenseError(Exception):
    __doc__ = 'Exception for license parsing issues'


class UserAuthDataError(Exception):
    __doc__ = 'Exception for user_auth_data syntax issues'