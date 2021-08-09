# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cffi\lock.py
import sys
if sys.version_info < (3, ):
    try:
        from thread import allocate_lock
    except ImportError:
        from dummy_thread import allocate_lock

try:
    from _thread import allocate_lock
except ImportError:
    from _dummy_thread import allocate_lock