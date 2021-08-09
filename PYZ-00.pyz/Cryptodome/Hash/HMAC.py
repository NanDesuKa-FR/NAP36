# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Hash\HMAC.py
from Cryptodome.Util.py3compat import bord, tobytes, _memoryview
from binascii import unhexlify
from Cryptodome.Hash import MD5
from Cryptodome.Hash import BLAKE2s
from Cryptodome.Util.strxor import strxor
from Cryptodome.Random import get_random_bytes
__all__ = [
 'new', 'HMAC']

class HMAC:
    __doc__ = 'An HMAC hash object.\n    Do not instantiate directly. Use the :func:`new` function.\n\n    :ivar digest_size: the size in bytes of the resulting MAC tag\n    :vartype digest_size: integer\n    '

    def __init__(self, key, msg=b'', digestmod=None):
        if digestmod is None:
            digestmod = MD5
        elif msg is None:
            msg = b''
        else:
            self.digest_size = digestmod.digest_size
            self._digestmod = digestmod
            if isinstance(key, _memoryview):
                key = key.tobytes()
            try:
                if len(key) <= digestmod.block_size:
                    key_0 = key + b'\x00' * (digestmod.block_size - len(key))
                else:
                    hash_k = digestmod.new(key).digest()
                    key_0 = hash_k + b'\x00' * (digestmod.block_size - len(hash_k))
            except AttributeError:
                raise ValueError('Hash type incompatible to HMAC')

        key_0_ipad = strxor(key_0, b'6' * len(key_0))
        self._inner = digestmod.new(key_0_ipad)
        self._inner.update(msg)
        key_0_opad = strxor(key_0, b'\\' * len(key_0))
        self._outer = digestmod.new(key_0_opad)

    def update(self, msg):
        """Authenticate the next chunk of message.

        Args:
            data (byte string/byte array/memoryview): The next chunk of data
        """
        self._inner.update(msg)
        return self

    def _pbkdf2_hmac_assist(self, first_digest, iterations):
        """Carry out the expensive inner loop for PBKDF2-HMAC"""
        result = self._digestmod._pbkdf2_hmac_assist(self._inner, self._outer, first_digest, iterations)
        return result

    def copy(self):
        """Return a copy ("clone") of the HMAC object.

        The copy will have the same internal state as the original HMAC
        object.
        This can be used to efficiently compute the MAC tag of byte
        strings that share a common initial substring.

        :return: An :class:`HMAC`
        """
        new_hmac = HMAC(b'fake key', digestmod=(self._digestmod))
        new_hmac._inner = self._inner.copy()
        new_hmac._outer = self._outer.copy()
        return new_hmac

    def digest(self):
        """Return the **binary** (non-printable) MAC tag of the message
        authenticated so far.

        :return: The MAC tag digest, computed over the data processed so far.
                 Binary form.
        :rtype: byte string
        """
        frozen_outer_hash = self._outer.copy()
        frozen_outer_hash.update(self._inner.digest())
        return frozen_outer_hash.digest()

    def verify(self, mac_tag):
        """Verify that a given **binary** MAC (computed by another party)
        is valid.

        Args:
          mac_tag (byte string/byte string/memoryview): the expected MAC of the message.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        """
        secret = get_random_bytes(16)
        mac1 = BLAKE2s.new(digest_bits=160, key=secret, data=mac_tag)
        mac2 = BLAKE2s.new(digest_bits=160, key=secret, data=(self.digest()))
        if mac1.digest() != mac2.digest():
            raise ValueError('MAC check failed')

    def hexdigest(self):
        """Return the **printable** MAC tag of the message authenticated so far.

        :return: The MAC tag, computed over the data processed so far.
                 Hexadecimal encoded.
        :rtype: string
        """
        return ''.join(['%02x' % bord(x) for x in tuple(self.digest())])

    def hexverify(self, hex_mac_tag):
        """Verify that a given **printable** MAC (computed by another party)
        is valid.

        Args:
            hex_mac_tag (string): the expected MAC of the message,
                as a hexadecimal string.

        Raises:
            ValueError: if the MAC does not match. It means that the message
                has been tampered with or that the MAC key is incorrect.
        """
        self.verify(unhexlify(tobytes(hex_mac_tag)))


def new(key, msg=b'', digestmod=None):
    """Create a new MAC object.

    Args:
        key (bytes/bytearray/memoryview):
            key for the MAC object.
            It must be long enough to match the expected security level of the
            MAC.
        msg (bytes/bytearray/memoryview):
            Optional. The very first chunk of the message to authenticate.
            It is equivalent to an early call to :meth:`HMAC.update`.
        digestmod (module):
            The hash to use to implement the HMAC.
            Default is :mod:`Cryptodome.Hash.MD5`.

    Returns:
        An :class:`HMAC` object
    """
    return HMAC(key, msg, digestmod)