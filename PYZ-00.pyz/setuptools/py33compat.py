# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\py33compat.py
import dis, array, collections
try:
    import html
except ImportError:
    html = None

from setuptools.extern import six
from setuptools.extern.six.moves import html_parser
OpArg = collections.namedtuple('OpArg', 'opcode arg')

class Bytecode_compat(object):

    def __init__(self, code):
        self.code = code

    def __iter__(self):
        """Yield '(op,arg)' pair for each operation in code object 'code'"""
        bytes = array.array('b', self.code.co_code)
        eof = len(self.code.co_code)
        ptr = 0
        extended_arg = 0
        while ptr < eof:
            op = bytes[ptr]
            if op >= dis.HAVE_ARGUMENT:
                arg = bytes[(ptr + 1)] + bytes[(ptr + 2)] * 256 + extended_arg
                ptr += 3
                if op == dis.EXTENDED_ARG:
                    long_type = six.integer_types[(-1)]
                    extended_arg = arg * long_type(65536)
                    continue
            else:
                arg = None
                ptr += 1
            yield OpArg(op, arg)


Bytecode = getattr(dis, 'Bytecode', Bytecode_compat)
unescape = getattr(html, 'unescape', html_parser.HTMLParser().unescape)