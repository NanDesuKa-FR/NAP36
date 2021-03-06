# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\pycountry\db.py
from io import open
import json, logging, threading
logger = logging.getLogger('pycountry.db')
try:
    unicode
except NameError:
    unicode = str

class Data(object):

    def __init__(self, **fields):
        self._fields = fields

    def __getattr__(self, key):
        if key not in self._fields:
            raise AttributeError
        return self._fields[key]

    def __setattr__(self, key, value):
        if key != '_fields':
            self._fields[key] = value
        super(Data, self).__setattr__(key, value)

    def __repr__(self):
        cls_name = self.__class__.__name__
        fields = ', '.join('%s=%r' % i for i in sorted(self._fields.items()))
        return '%s(%s)' % (cls_name, fields)

    def __dir__(self):
        return dir(self.__class__) + list(self._fields)


def lazy_load(f):

    def load_if_needed(self, *args, **kw):
        if not self._is_loaded:
            with self._load_lock:
                self._load()
        return f(self, *args, **kw)

    return load_if_needed


class Database(object):
    data_class_base = Data
    data_class_name = None
    root_key = None
    no_index = []

    def __init__(self, filename):
        self.filename = filename
        self._is_loaded = False
        self._load_lock = threading.Lock()

    def _load(self):
        if self._is_loaded:
            return
        self.objects = []
        self.index_names = set()
        self.indices = {}
        self.data_class = type(self.data_class_name, (self.data_class_base,), {})
        with open((self.filename), 'r', encoding='utf-8') as (f):
            tree = json.load(f)
        for entry in tree[self.root_key]:
            obj = (self.data_class)(**entry)
            self.objects.append(obj)
            for key, value in entry.items():
                if key in self.no_index:
                    pass
                else:
                    index = self.indices.setdefault(key, {})
                    if value in index:
                        logger.debug('%s %r already taken in index %r and will be ignored. This is an error in the databases.' % (
                         self.data_class_name, value, key))
                    index[value] = obj

        self._is_loaded = True

    @lazy_load
    def __iter__(self):
        return iter(self.objects)

    @lazy_load
    def __len__(self):
        return len(self.objects)

    @lazy_load
    def get(self, **kw):
        kw.setdefault('default', None)
        default = kw.pop('default')
        if len(kw) != 1:
            raise TypeError('Only one criteria may be given')
        field, value = kw.popitem()
        index = self.indices[field]
        try:
            return index[value]
        except KeyError:
            return default

    @lazy_load
    def lookup(self, value):
        if isinstance(value, (str, unicode)):
            value = value.lower()
        for key in self.indices:
            try:
                return self.indices[key][value]
            except LookupError:
                pass

        for candidate in self:
            for v in candidate._fields.values():
                if v is None:
                    pass
                else:
                    if v.lower() == value:
                        return candidate

        raise LookupError('Could not find a record for %r' % value)