# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\primitives\serialization\base.py
from __future__ import absolute_import, division, print_function
import abc
from enum import Enum
import six
from cryptography import utils

def load_pem_private_key(data, password, backend):
    return backend.load_pem_private_key(data, password)


def load_pem_public_key(data, backend):
    return backend.load_pem_public_key(data)


def load_pem_parameters(data, backend):
    return backend.load_pem_parameters(data)


def load_der_private_key(data, password, backend):
    return backend.load_der_private_key(data, password)


def load_der_public_key(data, backend):
    return backend.load_der_public_key(data)


def load_der_parameters(data, backend):
    return backend.load_der_parameters(data)


class Encoding(Enum):
    PEM = 'PEM'
    DER = 'DER'
    OpenSSH = 'OpenSSH'
    Raw = 'Raw'
    X962 = 'ANSI X9.62'


class PrivateFormat(Enum):
    PKCS8 = 'PKCS8'
    TraditionalOpenSSL = 'TraditionalOpenSSL'
    Raw = 'Raw'


class PublicFormat(Enum):
    SubjectPublicKeyInfo = 'X.509 subjectPublicKeyInfo with PKCS#1'
    PKCS1 = 'Raw PKCS#1'
    OpenSSH = 'OpenSSH'
    Raw = 'Raw'
    CompressedPoint = 'X9.62 Compressed Point'
    UncompressedPoint = 'X9.62 Uncompressed Point'


class ParameterFormat(Enum):
    PKCS3 = 'PKCS3'


@six.add_metaclass(abc.ABCMeta)
class KeySerializationEncryption(object):
    pass


@utils.register_interface(KeySerializationEncryption)
class BestAvailableEncryption(object):

    def __init__(self, password):
        if not isinstance(password, bytes) or len(password) == 0:
            raise ValueError('Password must be 1 or more bytes.')
        self.password = password


@utils.register_interface(KeySerializationEncryption)
class NoEncryption(object):
    pass