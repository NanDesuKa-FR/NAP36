# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\primitives\ciphers\algorithms.py
from __future__ import absolute_import, division, print_function
from cryptography import utils
from cryptography.hazmat.primitives.ciphers import BlockCipherAlgorithm, CipherAlgorithm
from cryptography.hazmat.primitives.ciphers.modes import ModeWithNonce

def _verify_key_size(algorithm, key):
    utils._check_byteslike('key', key)
    if len(key) * 8 not in algorithm.key_sizes:
        raise ValueError('Invalid key size ({0}) for {1}.'.format(len(key) * 8, algorithm.name))
    return key


@utils.register_interface(BlockCipherAlgorithm)
@utils.register_interface(CipherAlgorithm)
class AES(object):
    name = 'AES'
    block_size = 128
    key_sizes = frozenset([128, 192, 256, 512])

    def __init__(self, key):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self):
        return len(self.key) * 8


@utils.register_interface(BlockCipherAlgorithm)
@utils.register_interface(CipherAlgorithm)
class Camellia(object):
    name = 'camellia'
    block_size = 128
    key_sizes = frozenset([128, 192, 256])

    def __init__(self, key):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self):
        return len(self.key) * 8


@utils.register_interface(BlockCipherAlgorithm)
@utils.register_interface(CipherAlgorithm)
class TripleDES(object):
    name = '3DES'
    block_size = 64
    key_sizes = frozenset([64, 128, 192])

    def __init__(self, key):
        if len(key) == 8:
            key += key + key
        else:
            if len(key) == 16:
                key += key[:8]
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self):
        return len(self.key) * 8


@utils.register_interface(BlockCipherAlgorithm)
@utils.register_interface(CipherAlgorithm)
class Blowfish(object):
    name = 'Blowfish'
    block_size = 64
    key_sizes = frozenset(range(32, 449, 8))

    def __init__(self, key):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self):
        return len(self.key) * 8


@utils.register_interface(BlockCipherAlgorithm)
@utils.register_interface(CipherAlgorithm)
class CAST5(object):
    name = 'CAST5'
    block_size = 64
    key_sizes = frozenset(range(40, 129, 8))

    def __init__(self, key):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self):
        return len(self.key) * 8


@utils.register_interface(CipherAlgorithm)
class ARC4(object):
    name = 'RC4'
    key_sizes = frozenset([40, 56, 64, 80, 128, 160, 192, 256])

    def __init__(self, key):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self):
        return len(self.key) * 8


@utils.register_interface(CipherAlgorithm)
class IDEA(object):
    name = 'IDEA'
    block_size = 64
    key_sizes = frozenset([128])

    def __init__(self, key):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self):
        return len(self.key) * 8


@utils.register_interface(BlockCipherAlgorithm)
@utils.register_interface(CipherAlgorithm)
class SEED(object):
    name = 'SEED'
    block_size = 128
    key_sizes = frozenset([128])

    def __init__(self, key):
        self.key = _verify_key_size(self, key)

    @property
    def key_size(self):
        return len(self.key) * 8


@utils.register_interface(CipherAlgorithm)
@utils.register_interface(ModeWithNonce)
class ChaCha20(object):
    name = 'ChaCha20'
    key_sizes = frozenset([256])

    def __init__(self, key, nonce):
        self.key = _verify_key_size(self, key)
        utils._check_byteslike('nonce', nonce)
        if len(nonce) != 16:
            raise ValueError('nonce must be 128-bits (16 bytes)')
        self._nonce = nonce

    nonce = utils.read_only_property('_nonce')

    @property
    def key_size(self):
        return len(self.key) * 8