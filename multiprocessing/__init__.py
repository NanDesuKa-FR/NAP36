# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: multiprocessing\__init__.py
import sys
from . import context
globals().update((name, getattr(context._default_context, name)) for name in context._default_context.__all__)
__all__ = context._default_context.__all__
SUBDEBUG = 5
SUBWARNING = 25
if '__main__' in sys.modules:
    sys.modules['__mp_main__'] = sys.modules['__main__']