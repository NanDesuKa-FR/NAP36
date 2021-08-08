# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Util\py3compat.py
"""Compatibility code for handling string/bytes changes from Python 2.x to Py3k

In Python 2.x, strings (of type ''str'') contain binary data, including encoded
Unicode text (e.g. UTF-8).  The separate type ''unicode'' holds Unicode text.
Unicode literals are specified via the u'...' prefix.  Indexing or slicing
either type always produces a string of the same type as the original.
Data read from a file is always of '''str'' type.

In Python 3.x, strings (type ''str'') may only contain Unicode text. The u'...'
prefix and the ''unicode'' type are now redundant.  A new type (called
''bytes'') has to be used for binary data (including any particular
''encoding'' of a string).  The b'...' prefix allows one to specify a binary
literal.  Indexing or slicing a string produces another string.  Slicing a byte
string produces another byte string, but the indexing operation produces an
integer.  Data read from a file is of '''str'' type if the file was opened in
text mode, or of ''bytes'' type otherwise.

Since PyCryptodome aims at supporting both Python 2.x and 3.x, the following helper
functions are used to keep the rest of the library as independent as possible
from the actual Python version.

In general, the code should always deal with binary strings, and use integers
instead of 1-byte character strings.

b(s)
    Take a text string literal (with no prefix or with u'...' prefix) and
    make a byte string.
bchr(c)
    Take an integer and make a 1-character byte string.
bord(c)
    Take the result of indexing on a byte string and make an integer.
tobytes(s)
    Take a text string, a byte string, or a sequence of character taken from
    a byte string and make a byte string.
"""
import sys, abc
if sys.version_info[0] == 2:

    def b(s):
        return s


    def bchr(s):
        return chr(s)


    def bstr(s):
        return str(s)


    def bord(s):
        return ord(s)


    def tobytes(s):
        if isinstance(s, unicode):
            return s.encode('latin-1')
        else:
            return ''.join(s)


    def tostr(bs):
        return bs


    def byte_string(s):
        return isinstance(s, str)


    from StringIO import StringIO as BytesIO
    from sys import maxint
    if sys.version_info[1] < 7:
        import types
        _memoryview = types.NoneType
    else:
        _memoryview = memoryview
    iter_range = xrange

    def is_native_int(x):
        return isinstance(x, (int, long))


    def is_string(x):
        return isinstance(x, basestring)


    ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})
else:

    def b(s):
        return s.encode('latin-1')


    def bchr(s):
        return bytes([s])


    def bstr(s):
        if isinstance(s, str):
            return bytes(s, 'latin-1')
        else:
            return bytes(s)


    def bord(s):
        return s


    def tobytes(s):
        if isinstance(s, bytes):
            return s
        else:
            if isinstance(s, str):
                return s.encode('latin-1')
            return bytes([s])


    def tostr(bs):
        return bs.decode('latin-1')


    def byte_string(s):
        return isinstance(s, bytes)


    from io import BytesIO
    from sys import maxsize as maxint
    _memoryview = memoryview
    iter_range = range

    def is_native_int(x):
        return isinstance(x, int)


    def is_string(x):
        return isinstance(x, str)


    from abc import ABC

def _copy_bytes(start, end, seq):
    """Return an immutable copy of a sequence (byte string, byte array, memoryview)
    in a certain interval [start:seq]"""
    if isinstance(seq, _memoryview):
        return seq[start:end].tobytes()
    else:
        if isinstance(seq, bytearray):
            return bytes(seq[start:end])
        return seq[start:end]


del sys
del abc