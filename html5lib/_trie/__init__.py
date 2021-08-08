# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\_trie\__init__.py
from __future__ import absolute_import, division, unicode_literals
from .py import Trie as PyTrie
Trie = PyTrie
try:
    from .datrie import Trie as DATrie
except ImportError:
    pass
else:
    Trie = DATrie