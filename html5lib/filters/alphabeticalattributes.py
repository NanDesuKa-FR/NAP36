# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\filters\alphabeticalattributes.py
from __future__ import absolute_import, division, unicode_literals
from . import base
from collections import OrderedDict

def _attr_key(attr):
    """Return an appropriate key for an attribute for sorting

    Attributes have a namespace that can be either ``None`` or a string. We
    can't compare the two because they're different types, so we convert
    ``None`` to an empty string first.

    """
    return (
     attr[0][0] or '', attr[0][1])


class Filter(base.Filter):
    __doc__ = 'Alphabetizes attributes for elements'

    def __iter__(self):
        for token in base.Filter.__iter__(self):
            if token['type'] in ('StartTag', 'EmptyTag'):
                attrs = OrderedDict()
                for name, value in sorted((token['data'].items()), key=_attr_key):
                    attrs[name] = value

                token['data'] = attrs
            yield token