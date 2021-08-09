# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\filters\whitespace.py
from __future__ import absolute_import, division, unicode_literals
import re
from . import base
from ..constants import rcdataElements, spaceCharacters
spaceCharacters = ''.join(spaceCharacters)
SPACES_REGEX = re.compile('[%s]+' % spaceCharacters)

class Filter(base.Filter):
    __doc__ = 'Collapses whitespace except in pre, textarea, and script elements'
    spacePreserveElements = frozenset(['pre', 'textarea'] + list(rcdataElements))

    def __iter__(self):
        preserve = 0
        for token in base.Filter.__iter__(self):
            type = token['type']
            if type == 'StartTag':
                if preserve or token['name'] in self.spacePreserveElements:
                    preserve += 1
            if type == 'EndTag':
                if preserve:
                    preserve -= 1
            if not preserve:
                if type == 'SpaceCharacters':
                    if token['data']:
                        token['data'] = ' '
            if not preserve:
                if type == 'Characters':
                    token['data'] = collapse_spaces(token['data'])
            yield token


def collapse_spaces(text):
    return SPACES_REGEX.sub(' ', text)