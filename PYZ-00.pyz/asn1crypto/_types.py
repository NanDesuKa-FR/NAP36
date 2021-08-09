# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\asn1crypto\_types.py
from __future__ import unicode_literals, division, absolute_import, print_function
import inspect, sys
if sys.version_info < (3, ):
    str_cls = unicode
    byte_cls = str
    int_types = (int, long)

    def bytes_to_list(byte_string):
        return [ord(b) for b in byte_string]


    chr_cls = chr
else:
    str_cls = str
    byte_cls = bytes
    int_types = int
    bytes_to_list = list

    def chr_cls(num):
        return bytes([num])


def type_name(value):
    """
    Returns a user-readable name for the type of an object

    :param value:
        A value to get the type name of

    :return:
        A unicode string of the object's type name
    """
    if inspect.isclass(value):
        cls = value
    else:
        cls = value.__class__
    if cls.__module__ in set(['builtins', '__builtin__']):
        return cls.__name__
    else:
        return '%s.%s' % (cls.__module__, cls.__name__)