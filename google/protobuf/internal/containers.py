# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\google\protobuf\internal\containers.py
"""Contains container classes to represent different protocol buffer types.

This file defines container classes which represent categories of protocol
buffer field types which need extra maintenance. Currently these categories
are:
  - Repeated scalar fields - These are all repeated fields which aren't
    composite (e.g. they are of simple types like int32, string, etc).
  - Repeated composite fields - Repeated fields which are composite. This
    includes groups and nested messages.
"""
__author__ = 'petar@google.com (Petar Petrov)'
import collections, sys
if sys.version_info[0] < 3:

    class Mapping(object):
        __slots__ = ()

        def get(self, key, default=None):
            try:
                return self[key]
            except KeyError:
                return default

        def __contains__(self, key):
            try:
                self[key]
            except KeyError:
                return False
            else:
                return True

        def iterkeys(self):
            return iter(self)

        def itervalues(self):
            for key in self:
                yield self[key]

        def iteritems(self):
            for key in self:
                yield (
                 key, self[key])

        def keys(self):
            return list(self)

        def items(self):
            return [(key, self[key]) for key in self]

        def values(self):
            return [self[key] for key in self]

        __hash__ = None

        def __eq__(self, other):
            if not isinstance(other, collections.Mapping):
                return NotImplemented
            else:
                return dict(list(self.items())) == dict(list(other.items()))

        def __ne__(self, other):
            return not self == other


    class MutableMapping(Mapping):
        __slots__ = ()
        _MutableMapping__marker = object()

        def pop(self, key, default=_MutableMapping__marker):
            try:
                value = self[key]
            except KeyError:
                if default is self._MutableMapping__marker:
                    raise
                return default
            else:
                del self[key]
                return value

        def popitem(self):
            try:
                key = next(iter(self))
            except StopIteration:
                raise KeyError

            value = self[key]
            del self[key]
            return (key, value)

        def clear(self):
            try:
                while True:
                    self.popitem()

            except KeyError:
                pass

        def update(*args, **kwds):
            if len(args) > 2:
                raise TypeError('update() takes at most 2 positional arguments ({} given)'.format(len(args)))
            elif not args:
                raise TypeError('update() takes at least 1 argument (0 given)')
            else:
                self = args[0]
                other = args[1] if len(args) >= 2 else ()
                if isinstance(other, Mapping):
                    for key in other:
                        self[key] = other[key]

                else:
                    if hasattr(other, 'keys'):
                        for key in list(other.keys()):
                            self[key] = other[key]

                    else:
                        for key, value in other:
                            self[key] = value

            for key, value in list(kwds.items()):
                self[key] = value

        def setdefault(self, key, default=None):
            try:
                return self[key]
            except KeyError:
                self[key] = default

            return default


    collections.Mapping.register(Mapping)
    collections.MutableMapping.register(MutableMapping)
else:
    MutableMapping = collections.MutableMapping

class BaseContainer(object):
    __doc__ = 'Base container class.'
    __slots__ = [
     '_message_listener', '_values']

    def __init__(self, message_listener):
        """
    Args:
      message_listener: A MessageListener implementation.
        The RepeatedScalarFieldContainer will call this object's
        Modified() method when it is modified.
    """
        self._message_listener = message_listener
        self._values = []

    def __getitem__(self, key):
        """Retrieves item by the specified key."""
        return self._values[key]

    def __len__(self):
        """Returns the number of elements in the container."""
        return len(self._values)

    def __ne__(self, other):
        """Checks if another instance isn't equal to this one."""
        return not self == other

    def __hash__(self):
        raise TypeError('unhashable object')

    def __repr__(self):
        return repr(self._values)

    def sort(self, *args, **kwargs):
        if 'sort_function' in kwargs:
            kwargs['cmp'] = kwargs.pop('sort_function')
        (self._values.sort)(*args, **kwargs)


class RepeatedScalarFieldContainer(BaseContainer):
    __doc__ = 'Simple, type-checked, list-like container for holding repeated scalars.'
    __slots__ = [
     '_type_checker']

    def __init__(self, message_listener, type_checker):
        super(RepeatedScalarFieldContainer, self).__init__(message_listener)
        self._type_checker = type_checker

    def append(self, value):
        """Appends an item to the list. Similar to list.append()."""
        self._values.append(self._type_checker.CheckValue(value))
        if not self._message_listener.dirty:
            self._message_listener.Modified()

    def insert(self, key, value):
        """Inserts the item at the specified position. Similar to list.insert()."""
        self._values.insert(key, self._type_checker.CheckValue(value))
        if not self._message_listener.dirty:
            self._message_listener.Modified()

    def extend(self, elem_seq):
        """Extends by appending the given iterable. Similar to list.extend()."""
        if elem_seq is None:
            return
        try:
            elem_seq_iter = iter(elem_seq)
        except TypeError:
            if not elem_seq:
                return
            raise

        new_values = [self._type_checker.CheckValue(elem) for elem in elem_seq_iter]
        if new_values:
            self._values.extend(new_values)
        self._message_listener.Modified()

    def MergeFrom(self, other):
        """Appends the contents of another repeated field of the same type to this
    one. We do not check the types of the individual fields.
    """
        self._values.extend(other._values)
        self._message_listener.Modified()

    def remove(self, elem):
        """Removes an item from the list. Similar to list.remove()."""
        self._values.remove(elem)
        self._message_listener.Modified()

    def pop(self, key=-1):
        """Removes and returns an item at a given index. Similar to list.pop()."""
        value = self._values[key]
        self.__delitem__(key)
        return value

    def __setitem__(self, key, value):
        """Sets the item on the specified position."""
        if isinstance(key, slice):
            if key.step is not None:
                raise ValueError('Extended slices not supported')
            self.__setslice__(key.start, key.stop, value)
        else:
            self._values[key] = self._type_checker.CheckValue(value)
            self._message_listener.Modified()

    def __getslice__(self, start, stop):
        """Retrieves the subset of items from between the specified indices."""
        return self._values[start:stop]

    def __setslice__(self, start, stop, values):
        """Sets the subset of items from between the specified indices."""
        new_values = []
        for value in values:
            new_values.append(self._type_checker.CheckValue(value))

        self._values[start:stop] = new_values
        self._message_listener.Modified()

    def __delitem__(self, key):
        """Deletes the item at the specified position."""
        del self._values[key]
        self._message_listener.Modified()

    def __delslice__(self, start, stop):
        """Deletes the subset of items from between the specified indices."""
        del self._values[start:stop]
        self._message_listener.Modified()

    def __eq__(self, other):
        """Compares the current instance with another one."""
        if self is other:
            return True
        else:
            if isinstance(other, self.__class__):
                return other._values == self._values
            return other == self._values


collections.MutableSequence.register(BaseContainer)

class RepeatedCompositeFieldContainer(BaseContainer):
    __doc__ = 'Simple, list-like container for holding repeated composite fields.'
    __slots__ = [
     '_message_descriptor']

    def __init__(self, message_listener, message_descriptor):
        super(RepeatedCompositeFieldContainer, self).__init__(message_listener)
        self._message_descriptor = message_descriptor

    def add(self, **kwargs):
        """Adds a new element at the end of the list and returns it. Keyword
    arguments may be used to initialize the element.
    """
        new_element = (self._message_descriptor._concrete_class)(**kwargs)
        new_element._SetListener(self._message_listener)
        self._values.append(new_element)
        if not self._message_listener.dirty:
            self._message_listener.Modified()
        return new_element

    def extend(self, elem_seq):
        """Extends by appending the given sequence of elements of the same type
    as this one, copying each individual message.
    """
        message_class = self._message_descriptor._concrete_class
        listener = self._message_listener
        values = self._values
        for message in elem_seq:
            new_element = message_class()
            new_element._SetListener(listener)
            new_element.MergeFrom(message)
            values.append(new_element)

        listener.Modified()

    def MergeFrom(self, other):
        """Appends the contents of another repeated field of the same type to this
    one, copying each individual message.
    """
        self.extend(other._values)

    def remove(self, elem):
        """Removes an item from the list. Similar to list.remove()."""
        self._values.remove(elem)
        self._message_listener.Modified()

    def pop(self, key=-1):
        """Removes and returns an item at a given index. Similar to list.pop()."""
        value = self._values[key]
        self.__delitem__(key)
        return value

    def __getslice__(self, start, stop):
        """Retrieves the subset of items from between the specified indices."""
        return self._values[start:stop]

    def __delitem__(self, key):
        """Deletes the item at the specified position."""
        del self._values[key]
        self._message_listener.Modified()

    def __delslice__(self, start, stop):
        """Deletes the subset of items from between the specified indices."""
        del self._values[start:stop]
        self._message_listener.Modified()

    def __eq__(self, other):
        """Compares the current instance with another one."""
        if self is other:
            return True
        else:
            if not isinstance(other, self.__class__):
                raise TypeError('Can only compare repeated composite fields against other repeated composite fields.')
            return self._values == other._values


class ScalarMap(MutableMapping):
    __doc__ = 'Simple, type-checked, dict-like container for holding repeated scalars.'
    __slots__ = [
     '_key_checker', '_value_checker', '_values', '_message_listener',
     '_entry_descriptor']

    def __init__(self, message_listener, key_checker, value_checker, entry_descriptor):
        """
    Args:
      message_listener: A MessageListener implementation.
        The ScalarMap will call this object's Modified() method when it
        is modified.
      key_checker: A type_checkers.ValueChecker instance to run on keys
        inserted into this container.
      value_checker: A type_checkers.ValueChecker instance to run on values
        inserted into this container.
      entry_descriptor: The MessageDescriptor of a map entry: key and value.
    """
        self._message_listener = message_listener
        self._key_checker = key_checker
        self._value_checker = value_checker
        self._entry_descriptor = entry_descriptor
        self._values = {}

    def __getitem__(self, key):
        try:
            return self._values[key]
        except KeyError:
            key = self._key_checker.CheckValue(key)
            val = self._value_checker.DefaultValue()
            self._values[key] = val
            return val

    def __contains__(self, item):
        self._key_checker.CheckValue(item)
        return item in self._values

    def get(self, key, default=None):
        if key in self:
            return self[key]
        else:
            return default

    def __setitem__(self, key, value):
        checked_key = self._key_checker.CheckValue(key)
        checked_value = self._value_checker.CheckValue(value)
        self._values[checked_key] = checked_value
        self._message_listener.Modified()

    def __delitem__(self, key):
        del self._values[key]
        self._message_listener.Modified()

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def __repr__(self):
        return repr(self._values)

    def MergeFrom(self, other):
        self._values.update(other._values)
        self._message_listener.Modified()

    def InvalidateIterators(self):
        original = self._values
        self._values = original.copy()
        original[None] = None

    def clear(self):
        self._values.clear()
        self._message_listener.Modified()

    def GetEntryClass(self):
        return self._entry_descriptor._concrete_class


class MessageMap(MutableMapping):
    __doc__ = 'Simple, type-checked, dict-like container for with submessage values.'
    __slots__ = [
     '_key_checker', '_values', '_message_listener',
     '_message_descriptor', '_entry_descriptor']

    def __init__(self, message_listener, message_descriptor, key_checker, entry_descriptor):
        """
    Args:
      message_listener: A MessageListener implementation.
        The ScalarMap will call this object's Modified() method when it
        is modified.
      key_checker: A type_checkers.ValueChecker instance to run on keys
        inserted into this container.
      value_checker: A type_checkers.ValueChecker instance to run on values
        inserted into this container.
      entry_descriptor: The MessageDescriptor of a map entry: key and value.
    """
        self._message_listener = message_listener
        self._message_descriptor = message_descriptor
        self._key_checker = key_checker
        self._entry_descriptor = entry_descriptor
        self._values = {}

    def __getitem__(self, key):
        key = self._key_checker.CheckValue(key)
        try:
            return self._values[key]
        except KeyError:
            new_element = self._message_descriptor._concrete_class()
            new_element._SetListener(self._message_listener)
            self._values[key] = new_element
            self._message_listener.Modified()
            return new_element

    def get_or_create(self, key):
        """get_or_create() is an alias for getitem (ie. map[key]).

    Args:
      key: The key to get or create in the map.

    This is useful in cases where you want to be explicit that the call is
    mutating the map.  This can avoid lint errors for statements like this
    that otherwise would appear to be pointless statements:

      msg.my_map[key]
    """
        return self[key]

    def get(self, key, default=None):
        if key in self:
            return self[key]
        else:
            return default

    def __contains__(self, item):
        item = self._key_checker.CheckValue(item)
        return item in self._values

    def __setitem__(self, key, value):
        raise ValueError('May not set values directly, call my_map[key].foo = 5')

    def __delitem__(self, key):
        key = self._key_checker.CheckValue(key)
        del self._values[key]
        self._message_listener.Modified()

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return iter(self._values)

    def __repr__(self):
        return repr(self._values)

    def MergeFrom(self, other):
        for key in other:
            if key in self:
                del self[key]
            self[key].CopyFrom(other[key])

    def InvalidateIterators(self):
        original = self._values
        self._values = original.copy()
        original[None] = None

    def clear(self):
        self._values.clear()
        self._message_listener.Modified()

    def GetEntryClass(self):
        return self._entry_descriptor._concrete_class