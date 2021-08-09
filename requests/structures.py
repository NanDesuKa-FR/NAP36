# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\requests\structures.py
"""
requests.structures
~~~~~~~~~~~~~~~~~~~

Data structures that power Requests.
"""
from .compat import OrderedDict, Mapping, MutableMapping

class CaseInsensitiveDict(MutableMapping):
    __doc__ = "A case-insensitive ``dict``-like object.\n\n    Implements all methods and operations of\n    ``MutableMapping`` as well as dict's ``copy``. Also\n    provides ``lower_items``.\n\n    All keys are expected to be strings. The structure remembers the\n    case of the last key to be set, and ``iter(instance)``,\n    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``\n    will contain case-sensitive keys. However, querying and contains\n    testing is case insensitive::\n\n        cid = CaseInsensitiveDict()\n        cid['Accept'] = 'application/json'\n        cid['aCCEPT'] == 'application/json'  # True\n        list(cid) == ['Accept']  # True\n\n    For example, ``headers['content-encoding']`` will return the\n    value of a ``'Content-Encoding'`` response header, regardless\n    of how the header name was originally stored.\n\n    If the constructor, ``.update``, or equality comparison\n    operations are given keys that have equal ``.lower()``s, the\n    behavior is undefined.\n    "

    def __init__(self, data=None, **kwargs):
        self._store = OrderedDict()
        if data is None:
            data = {}
        (self.update)(data, **kwargs)

    def __setitem__(self, key, value):
        self._store[key.lower()] = (
         key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return ((lowerkey, keyval[1]) for lowerkey, keyval in self._store.items())

    def __eq__(self, other):
        if isinstance(other, Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        return dict(self.lower_items()) == dict(other.lower_items())

    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return str(dict(self.items()))


class LookupDict(dict):
    __doc__ = 'Dictionary lookup object.'

    def __init__(self, name=None):
        self.name = name
        super(LookupDict, self).__init__()

    def __repr__(self):
        return "<lookup '%s'>" % self.name

    def __getitem__(self, key):
        return self.__dict__.get(key, None)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)