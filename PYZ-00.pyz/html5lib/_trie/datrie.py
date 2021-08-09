# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\_trie\datrie.py
from __future__ import absolute_import, division, unicode_literals
from datrie import Trie as DATrie
from six import text_type
from ._base import Trie as ABCTrie

class Trie(ABCTrie):

    def __init__(self, data):
        chars = set()
        for key in data.keys():
            if not isinstance(key, text_type):
                raise TypeError('All keys must be strings')
            for char in key:
                chars.add(char)

        self._data = DATrie(''.join(chars))
        for key, value in data.items():
            self._data[key] = value

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, key):
        return self._data[key]

    def keys(self, prefix=None):
        return self._data.keys(prefix)

    def has_keys_with_prefix(self, prefix):
        return self._data.has_keys_with_prefix(prefix)

    def longest_prefix(self, prefix):
        return self._data.longest_prefix(prefix)

    def longest_prefix_item(self, prefix):
        return self._data.longest_prefix_item(prefix)