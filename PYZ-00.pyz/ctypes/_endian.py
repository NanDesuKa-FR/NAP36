# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: ctypes\_endian.py
import sys
from ctypes import *
_array_type = type(Array)

def _other_endian(typ):
    """Return the type with the 'other' byte order.  Simple types like
    c_int and so on already have __ctype_be__ and __ctype_le__
    attributes which contain the types, for more complicated types
    arrays and structures are supported.
    """
    if hasattr(typ, _OTHER_ENDIAN):
        return getattr(typ, _OTHER_ENDIAN)
    else:
        if isinstance(typ, _array_type):
            return _other_endian(typ._type_) * typ._length_
        if issubclass(typ, Structure):
            return typ
    raise TypeError('This type does not support other endian: %s' % typ)


class _swapped_meta(type(Structure)):

    def __setattr__(self, attrname, value):
        if attrname == '_fields_':
            fields = []
            for desc in value:
                name = desc[0]
                typ = desc[1]
                rest = desc[2:]
                fields.append((name, _other_endian(typ)) + rest)

            value = fields
        super().__setattr__(attrname, value)


if sys.byteorder == 'little':
    _OTHER_ENDIAN = '__ctype_be__'
    LittleEndianStructure = Structure

    class BigEndianStructure(Structure, metaclass=_swapped_meta):
        __doc__ = 'Structure with big endian byte order'
        __slots__ = ()
        _swappedbytes_ = None


else:
    if sys.byteorder == 'big':
        _OTHER_ENDIAN = '__ctype_le__'
        BigEndianStructure = Structure

        class LittleEndianStructure(Structure, metaclass=_swapped_meta):
            __doc__ = 'Structure with little endian byte order'
            __slots__ = ()
            _swappedbytes_ = None


    else:
        raise RuntimeError('Invalid byteorder')