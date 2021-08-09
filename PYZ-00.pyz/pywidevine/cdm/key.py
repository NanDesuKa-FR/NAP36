# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\pywidevine\cdm\key.py
import binascii

class Key:

    def __init__(self, kid, type, key):
        self.kid = kid
        self.type = type
        self.key = key

    def __repr__(self):
        return 'key(kid={}, type={}, key={})'.format(self.kid, self.type, binascii.hexlify(self.key))