# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\compat.py
import sys
if sys.version_info < (3, 0):
    PY2 = True
    PY3 = False
    base_str = (str, unicode)
    text_type = unicode
else:
    PY2 = False
    PY3 = True
    base_str = (bytes, str)
    text_type = str