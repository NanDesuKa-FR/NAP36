# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\filters\base.py
from __future__ import absolute_import, division, unicode_literals

class Filter(object):

    def __init__(self, source):
        self.source = source

    def __iter__(self):
        return iter(self.source)

    def __getattr__(self, name):
        return getattr(self.source, name)