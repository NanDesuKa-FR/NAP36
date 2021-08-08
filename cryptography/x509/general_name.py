# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\x509\general_name.py
from __future__ import absolute_import, division, print_function
import abc, ipaddress, warnings
from email.utils import parseaddr
import six
from six.moves import urllib_parse
from cryptography import utils
from cryptography.x509.name import Name
from cryptography.x509.oid import ObjectIdentifier
_GENERAL_NAMES = {0:'otherName', 
 1:'rfc822Name', 
 2:'dNSName', 
 3:'x400Address', 
 4:'directoryName', 
 5:'ediPartyName', 
 6:'uniformResourceIdentifier', 
 7:'iPAddress', 
 8:'registeredID'}

def _lazy_import_idna():
    try:
        import idna
        return idna
    except ImportError:
        raise ImportError('idna is not installed, but a deprecated feature that requires it was used. See: https://cryptography.io/en/latest/faq/#importerror-idna-is-not-installed')


class UnsupportedGeneralNameType(Exception):

    def __init__(self, msg, type):
        super(UnsupportedGeneralNameType, self).__init__(msg)
        self.type = type


@six.add_metaclass(abc.ABCMeta)
class GeneralName(object):

    @abc.abstractproperty
    def value(self):
        """
        Return the value of the object
        """
        pass


@utils.register_interface(GeneralName)
class RFC822Name(object):

    def __init__(self, value):
        if isinstance(value, six.text_type):
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                value = self._idna_encode(value)
                warnings.warn('RFC822Name values should be passed as an A-label string. This means unicode characters should be encoded via idna. Support for passing unicode strings (aka U-label) will be removed in a future version.',
                  (utils.DeprecatedIn21),
                  stacklevel=2)

        else:
            raise TypeError('value must be string')
        name, address = parseaddr(value)
        if name or not address:
            raise ValueError('Invalid rfc822name value')
        self._value = value

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def _idna_encode(self, value):
        idna = _lazy_import_idna()
        _, address = parseaddr(value)
        parts = address.split('@')
        return parts[0] + '@' + idna.encode(parts[1]).decode('ascii')

    def __repr__(self):
        return '<RFC822Name(value={0!r})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, RFC822Name):
            return NotImplemented
        else:
            return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


def _idna_encode(value):
    idna = _lazy_import_idna()
    for prefix in ('*.', '.'):
        if value.startswith(prefix):
            value = value[len(prefix):]
            return prefix + idna.encode(value).decode('ascii')

    return idna.encode(value).decode('ascii')


@utils.register_interface(GeneralName)
class DNSName(object):

    def __init__(self, value):
        if isinstance(value, six.text_type):
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                value = _idna_encode(value)
                warnings.warn('DNSName values should be passed as an A-label string. This means unicode characters should be encoded via idna. Support for passing unicode strings (aka U-label) will be removed in a future version.',
                  (utils.DeprecatedIn21),
                  stacklevel=2)

        else:
            raise TypeError('value must be string')
        self._value = value

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def __repr__(self):
        return '<DNSName(value={0!r})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, DNSName):
            return NotImplemented
        else:
            return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class UniformResourceIdentifier(object):

    def __init__(self, value):
        if isinstance(value, six.text_type):
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                value = self._idna_encode(value)
                warnings.warn('URI values should be passed as an A-label string. This means unicode characters should be encoded via idna. Support for passing unicode strings (aka U-label)  will be removed in a future version.',
                  (utils.DeprecatedIn21),
                  stacklevel=2)

        else:
            raise TypeError('value must be string')
        self._value = value

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def _idna_encode(self, value):
        idna = _lazy_import_idna()
        parsed = urllib_parse.urlparse(value)
        if parsed.port:
            netloc = (idna.encode(parsed.hostname) + ':{0}'.format(parsed.port).encode('ascii')).decode('ascii')
        else:
            netloc = idna.encode(parsed.hostname).decode('ascii')
        return urllib_parse.urlunparse((
         parsed.scheme,
         netloc,
         parsed.path,
         parsed.params,
         parsed.query,
         parsed.fragment))

    def __repr__(self):
        return '<UniformResourceIdentifier(value={0!r})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, UniformResourceIdentifier):
            return NotImplemented
        else:
            return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class DirectoryName(object):

    def __init__(self, value):
        if not isinstance(value, Name):
            raise TypeError('value must be a Name')
        self._value = value

    value = utils.read_only_property('_value')

    def __repr__(self):
        return '<DirectoryName(value={0})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, DirectoryName):
            return NotImplemented
        else:
            return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class RegisteredID(object):

    def __init__(self, value):
        if not isinstance(value, ObjectIdentifier):
            raise TypeError('value must be an ObjectIdentifier')
        self._value = value

    value = utils.read_only_property('_value')

    def __repr__(self):
        return '<RegisteredID(value={0})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, RegisteredID):
            return NotImplemented
        else:
            return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class IPAddress(object):

    def __init__(self, value):
        if not isinstance(value, (
         ipaddress.IPv4Address,
         ipaddress.IPv6Address,
         ipaddress.IPv4Network,
         ipaddress.IPv6Network)):
            raise TypeError('value must be an instance of ipaddress.IPv4Address, ipaddress.IPv6Address, ipaddress.IPv4Network, or ipaddress.IPv6Network')
        self._value = value

    value = utils.read_only_property('_value')

    def __repr__(self):
        return '<IPAddress(value={0})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, IPAddress):
            return NotImplemented
        else:
            return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class OtherName(object):

    def __init__(self, type_id, value):
        if not isinstance(type_id, ObjectIdentifier):
            raise TypeError('type_id must be an ObjectIdentifier')
        if not isinstance(value, bytes):
            raise TypeError('value must be a binary string')
        self._type_id = type_id
        self._value = value

    type_id = utils.read_only_property('_type_id')
    value = utils.read_only_property('_value')

    def __repr__(self):
        return '<OtherName(type_id={0}, value={1!r})>'.format(self.type_id, self.value)

    def __eq__(self, other):
        if not isinstance(other, OtherName):
            return NotImplemented
        else:
            return self.type_id == other.type_id and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.type_id, self.value))