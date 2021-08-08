# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\utils.py
from __future__ import absolute_import, division, print_function
import abc, binascii, inspect, sys, warnings

class CryptographyDeprecationWarning(UserWarning):
    pass


PersistentlyDeprecated = CryptographyDeprecationWarning
DeprecatedIn21 = CryptographyDeprecationWarning
DeprecatedIn23 = CryptographyDeprecationWarning
DeprecatedIn25 = CryptographyDeprecationWarning

def _check_bytes(name, value):
    if not isinstance(value, bytes):
        raise TypeError('{0} must be bytes'.format(name))


def _check_byteslike(name, value):
    try:
        memoryview(value)
    except TypeError:
        raise TypeError('{0} must be bytes-like'.format(name))


def read_only_property(name):
    return property(lambda self: getattr(self, name))


def register_interface(iface):

    def register_decorator(klass):
        verify_interface(iface, klass)
        iface.register(klass)
        return klass

    return register_decorator


def register_interface_if(predicate, iface):

    def register_decorator(klass):
        if predicate:
            verify_interface(iface, klass)
            iface.register(klass)
        return klass

    return register_decorator


if hasattr(int, 'from_bytes'):
    int_from_bytes = int.from_bytes
else:

    def int_from_bytes(data, byteorder, signed=False):
        if not byteorder == 'big':
            raise AssertionError
        elif not not signed:
            raise AssertionError
        return int(binascii.hexlify(data), 16)


if hasattr(int, 'to_bytes'):

    def int_to_bytes(integer, length=None):
        return integer.to_bytes(length or (integer.bit_length() + 7) // 8 or 1, 'big')


else:

    def int_to_bytes(integer, length=None):
        hex_string = '%x' % integer
        if length is None:
            n = len(hex_string)
        else:
            n = length * 2
        return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


class InterfaceNotImplemented(Exception):
    pass


if hasattr(inspect, 'signature'):
    signature = inspect.signature
else:
    signature = inspect.getargspec

def verify_interface(iface, klass):
    for method in iface.__abstractmethods__:
        if not hasattr(klass, method):
            raise InterfaceNotImplemented('{0} is missing a {1!r} method'.format(klass, method))
        if isinstance(getattr(iface, method), abc.abstractproperty):
            continue
        sig = signature(getattr(iface, method))
        actual = signature(getattr(klass, method))
        if sig != actual:
            raise InterfaceNotImplemented("{0}.{1}'s signature differs from the expected. Expected: {2!r}. Received: {3!r}".format(klass, method, sig, actual))


def bit_length(x):
    return x.bit_length()


class _DeprecatedValue(object):

    def __init__(self, value, message, warning_class):
        self.value = value
        self.message = message
        self.warning_class = warning_class


class _ModuleWithDeprecations(object):

    def __init__(self, module):
        self.__dict__['_module'] = module

    def __getattr__(self, attr):
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn((obj.message), (obj.warning_class), stacklevel=2)
            obj = obj.value
        return obj

    def __setattr__(self, attr, value):
        setattr(self._module, attr, value)

    def __delattr__(self, attr):
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn((obj.message), (obj.warning_class), stacklevel=2)
        delattr(self._module, attr)

    def __dir__(self):
        return [
         '_module'] + dir(self._module)


def deprecated(value, module_name, message, warning_class):
    module = sys.modules[module_name]
    if not isinstance(module, _ModuleWithDeprecations):
        sys.modules[module_name] = _ModuleWithDeprecations(module)
    return _DeprecatedValue(value, message, warning_class)


def cached_property(func):
    cached_name = '_cached_{0}'.format(func)
    sentinel = object()

    def inner(instance):
        cache = getattr(instance, cached_name, sentinel)
        if cache is not sentinel:
            return cache
        else:
            result = func(instance)
            setattr(instance, cached_name, result)
            return result

    return property(inner)