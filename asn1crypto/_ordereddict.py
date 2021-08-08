# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\asn1crypto\_ordereddict.py
import sys
if not sys.version_info < (2, 7):
    from collections import OrderedDict
else:
    from UserDict import DictMixin

    class OrderedDict(dict, DictMixin):

        def __init__(self, *args, **kwds):
            if len(args) > 1:
                raise TypeError('expected at most 1 arguments, got %d' % len(args))
            try:
                self._OrderedDict__end
            except AttributeError:
                self.clear()

            (self.update)(*args, **kwds)

        def clear(self):
            self._OrderedDict__end = end = []
            end += [None, end, end]
            self._OrderedDict__map = {}
            dict.clear(self)

        def __setitem__(self, key, value):
            if key not in self:
                end = self._OrderedDict__end
                curr = end[1]
                curr[2] = end[1] = self._OrderedDict__map[key] = [key, curr, end]
            dict.__setitem__(self, key, value)

        def __delitem__(self, key):
            dict.__delitem__(self, key)
            key, prev, next_ = self._OrderedDict__map.pop(key)
            prev[2] = next_
            next_[1] = prev

        def __iter__(self):
            end = self._OrderedDict__end
            curr = end[2]
            while curr is not end:
                yield curr[0]
                curr = curr[2]

        def __reversed__(self):
            end = self._OrderedDict__end
            curr = end[1]
            while curr is not end:
                yield curr[0]
                curr = curr[1]

        def popitem(self, last=True):
            if not self:
                raise KeyError('dictionary is empty')
            else:
                if last:
                    key = reversed(self).next()
                else:
                    key = iter(self).next()
            value = self.pop(key)
            return (key, value)

        def __reduce__(self):
            items = [[k, self[k]] for k in self]
            tmp = (self._OrderedDict__map, self._OrderedDict__end)
            del self._OrderedDict__map
            del self._OrderedDict__end
            inst_dict = vars(self).copy()
            self._OrderedDict__map, self._OrderedDict__end = tmp
            if inst_dict:
                return (self.__class__, (items,), inst_dict)
            else:
                return (
                 self.__class__, (items,))

        def keys(self):
            return list(self)

        setdefault = DictMixin.setdefault
        update = DictMixin.update
        pop = DictMixin.pop
        values = DictMixin.values
        items = DictMixin.items
        iterkeys = DictMixin.iterkeys
        itervalues = DictMixin.itervalues
        iteritems = DictMixin.iteritems

        def __repr__(self):
            if not self:
                return '%s()' % (self.__class__.__name__,)
            else:
                return '%s(%r)' % (self.__class__.__name__, self.items())

        def copy(self):
            return self.__class__(self)

        @classmethod
        def fromkeys(cls, iterable, value=None):
            d = cls()
            for key in iterable:
                d[key] = value

            return d

        def __eq__(self, other):
            if isinstance(other, OrderedDict):
                if len(self) != len(other):
                    return False
                for p, q in zip(self.items(), other.items()):
                    if p != q:
                        return False

                return True
            else:
                return dict.__eq__(self, other)

        def __ne__(self, other):
            return not self == other