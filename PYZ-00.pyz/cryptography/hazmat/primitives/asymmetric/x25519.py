# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\primitives\asymmetric\x25519.py
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons

@six.add_metaclass(abc.ABCMeta)
class X25519PublicKey(object):

    @classmethod
    def from_public_bytes(cls, data):
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.x25519_supported():
            raise UnsupportedAlgorithm('X25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM)
        return backend.x25519_load_public_bytes(data)

    @abc.abstractmethod
    def public_bytes(self, encoding=None, format=None):
        """
        The serialized bytes of the public key.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class X25519PrivateKey(object):

    @classmethod
    def generate(cls):
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.x25519_supported():
            raise UnsupportedAlgorithm('X25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM)
        return backend.x25519_generate_key()

    @classmethod
    def from_private_bytes(cls, data):
        from cryptography.hazmat.backends.openssl.backend import backend
        if not backend.x25519_supported():
            raise UnsupportedAlgorithm('X25519 is not supported by this version of OpenSSL.', _Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM)
        return backend.x25519_load_private_bytes(data)

    @abc.abstractmethod
    def public_key(self):
        """
        The serialized bytes of the public key.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding, format, encryption_algorithm):
        """
        The serialized bytes of the private key.
        """
        pass

    @abc.abstractmethod
    def exchange(self, peer_public_key):
        """
        Performs a key exchange operation using the provided peer's public key.
        """
        pass