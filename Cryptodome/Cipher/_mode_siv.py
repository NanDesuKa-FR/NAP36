# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Cipher\_mode_siv.py
"""
Synthetic Initialization Vector (SIV) mode.
"""
__all__ = [
 'SivMode']
from binascii import hexlify, unhexlify
from Cryptodome.Util.py3compat import bord, _copy_bytes
from Cryptodome.Util._raw_api import is_buffer
from Cryptodome.Util.number import long_to_bytes, bytes_to_long
from Cryptodome.Protocol.KDF import _S2V
from Cryptodome.Hash import BLAKE2s
from Cryptodome.Random import get_random_bytes

class SivMode(object):
    __doc__ = 'Synthetic Initialization Vector (SIV).\n\n    This is an Authenticated Encryption with Associated Data (`AEAD`_) mode.\n    It provides both confidentiality and authenticity.\n\n    The header of the message may be left in the clear, if needed, and it will\n    still be subject to authentication. The decryption step tells the receiver\n    if the message comes from a source that really knowns the secret key.\n    Additionally, decryption detects if any part of the message - including the\n    header - has been modified or corrupted.\n\n    Unlike other AEAD modes such as CCM, EAX or GCM, accidental reuse of a\n    nonce is not catastrophic for the confidentiality of the message. The only\n    effect is that an attacker can tell when the same plaintext (and same\n    associated data) is protected with the same key.\n\n    The length of the MAC is fixed to the block size of the underlying cipher.\n    The key size is twice the length of the key of the underlying cipher.\n\n    This mode is only available for AES ciphers.\n\n    +--------------------+---------------+-------------------+\n    |      Cipher        | SIV MAC size  |   SIV key length  |\n    |                    |    (bytes)    |     (bytes)       |\n    +====================+===============+===================+\n    |    AES-128         |      16       |        32         |\n    +--------------------+---------------+-------------------+\n    |    AES-192         |      16       |        48         |\n    +--------------------+---------------+-------------------+\n    |    AES-256         |      16       |        64         |\n    +--------------------+---------------+-------------------+\n\n    See `RFC5297`_ and the `original paper`__.\n\n    .. _RFC5297: https://tools.ietf.org/html/rfc5297\n    .. _AEAD: http://blog.cryptographyengineering.com/2012/05/how-to-choose-authenticated-encryption.html\n    .. __: http://www.cs.ucdavis.edu/~rogaway/papers/keywrap.pdf\n\n    :undocumented: __init__\n    '

    def __init__(self, factory, key, nonce, kwargs):
        self.block_size = factory.block_size
        self._factory = factory
        self._cipher_params = kwargs
        if len(key) not in (32, 48, 64):
            raise ValueError('Incorrect key length (%d bytes)' % len(key))
        if nonce is not None:
            if not is_buffer(nonce):
                raise TypeError('When provided, the nonce must be bytes, bytearray or memoryview')
            if len(nonce) == 0:
                raise ValueError('When provided, the nonce must be non-empty')
            self.nonce = _copy_bytes(None, None, nonce)
        subkey_size = len(key) // 2
        self._mac_tag = None
        self._kdf = _S2V((key[:subkey_size]), ciphermod=factory,
          cipher_params=(self._cipher_params))
        self._subkey_cipher = key[subkey_size:]
        (factory.new)((key[:subkey_size]), (factory.MODE_ECB), **kwargs)
        self._next = [
         self.update, self.encrypt, self.decrypt,
         self.digest, self.verify]

    def _create_ctr_cipher(self, v):
        """Create a new CTR cipher from V in SIV mode"""
        v_int = bytes_to_long(v)
        q = v_int & 340282366920938463454151235392765951999
        return (self._factory.new)(
 self._subkey_cipher,
 self._factory.MODE_CTR, initial_value=q, 
         nonce=b'', **self._cipher_params)

    def update(self, component):
        """Protect one associated data component

        For SIV, the associated data is a sequence (*vector*) of non-empty
        byte strings (*components*).

        This method consumes the next component. It must be called
        once for each of the components that constitue the associated data.

        Note that the components have clear boundaries, so that:

            >>> cipher.update(b"builtin")
            >>> cipher.update(b"securely")

        is not equivalent to:

            >>> cipher.update(b"built")
            >>> cipher.update(b"insecurely")

        If there is no associated data, this method must not be called.

        :Parameters:
          component : bytes/bytearray/memoryview
            The next associated data component.
        """
        if self.update not in self._next:
            raise TypeError('update() can only be called immediately after initialization')
        self._next = [
         self.update, self.encrypt, self.decrypt,
         self.digest, self.verify]
        return self._kdf.update(component)

    def encrypt(self, plaintext):
        """
        For SIV, encryption and MAC authentication must take place at the same
        point. This method shall not be used.

        Use `encrypt_and_digest` instead.
        """
        raise TypeError('encrypt() not allowed for SIV mode. Use encrypt_and_digest() instead.')

    def decrypt(self, ciphertext):
        """
        For SIV, decryption and verification must take place at the same
        point. This method shall not be used.

        Use `decrypt_and_verify` instead.
        """
        raise TypeError('decrypt() not allowed for SIV mode. Use decrypt_and_verify() instead.')

    def digest(self):
        """Compute the *binary* MAC tag.

        The caller invokes this function at the very end.

        This method returns the MAC that shall be sent to the receiver,
        together with the ciphertext.

        :Return: the MAC, as a byte string.
        """
        if self.digest not in self._next:
            raise TypeError('digest() cannot be called when decrypting or validating a message')
        self._next = [self.digest]
        if self._mac_tag is None:
            self._mac_tag = self._kdf.derive()
        return self._mac_tag

    def hexdigest(self):
        """Compute the *printable* MAC tag.

        This method is like `digest`.

        :Return: the MAC, as a hexadecimal string.
        """
        return ''.join(['%02x' % bord(x) for x in self.digest()])

    def verify(self, received_mac_tag):
        """Validate the *binary* MAC tag.

        The caller invokes this function at the very end.

        This method checks if the decrypted message is indeed valid
        (that is, if the key is correct) and it has not been
        tampered with while in transit.

        :Parameters:
          received_mac_tag : bytes/bytearray/memoryview
            This is the *binary* MAC, as received from the sender.
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        if self.verify not in self._next:
            raise TypeError('verify() cannot be called when encrypting a message')
        else:
            self._next = [
             self.verify]
            if self._mac_tag is None:
                self._mac_tag = self._kdf.derive()
            secret = get_random_bytes(16)
            mac1 = BLAKE2s.new(digest_bits=160, key=secret, data=(self._mac_tag))
            mac2 = BLAKE2s.new(digest_bits=160, key=secret, data=received_mac_tag)
            if mac1.digest() != mac2.digest():
                raise ValueError('MAC check failed')

    def hexverify(self, hex_mac_tag):
        """Validate the *printable* MAC tag.

        This method is like `verify`.

        :Parameters:
          hex_mac_tag : string
            This is the *printable* MAC, as received from the sender.
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        self.verify(unhexlify(hex_mac_tag))

    def encrypt_and_digest(self, plaintext, output=None):
        """Perform encrypt() and digest() in one step.

        :Parameters:
          plaintext : bytes/bytearray/memoryview
            The piece of data to encrypt.
        :Keywords:
          output : bytearray/memoryview
            The location where the ciphertext must be written to.
            If ``None``, the ciphertext is returned.
        :Return:
            a tuple with two items:

            - the ciphertext, as ``bytes``
            - the MAC tag, as ``bytes``

            The first item becomes ``None`` when the ``output`` parameter
            specified a location for the result.
        """
        if self.encrypt not in self._next:
            raise TypeError('encrypt() can only be called after initialization or an update()')
        self._next = [
         self.digest]
        if hasattr(self, 'nonce'):
            self._kdf.update(self.nonce)
        self._kdf.update(plaintext)
        self._mac_tag = self._kdf.derive()
        cipher = self._create_ctr_cipher(self._mac_tag)
        return (
         cipher.encrypt(plaintext, output=output), self._mac_tag)

    def decrypt_and_verify(self, ciphertext, mac_tag, output=None):
        """Perform decryption and verification in one step.

        A cipher object is stateful: once you have decrypted a message
        you cannot decrypt (or encrypt) another message with the same
        object.

        You cannot reuse an object for encrypting
        or decrypting other data with the same key.

        This function does not remove any padding from the plaintext.

        :Parameters:
          ciphertext : bytes/bytearray/memoryview
            The piece of data to decrypt.
            It can be of any length.
          mac_tag : bytes/bytearray/memoryview
            This is the *binary* MAC, as received from the sender.
        :Keywords:
          output : bytearray/memoryview
            The location where the plaintext must be written to.
            If ``None``, the plaintext is returned.
        :Return: the plaintext as ``bytes`` or ``None`` when the ``output``
            parameter specified a location for the result.
        :Raises ValueError:
            if the MAC does not match. The message has been tampered with
            or the key is incorrect.
        """
        if self.decrypt not in self._next:
            raise TypeError('decrypt() can only be called after initialization or an update()')
        self._next = [self.verify]
        self._cipher = self._create_ctr_cipher(mac_tag)
        plaintext = self._cipher.decrypt(ciphertext, output=output)
        if hasattr(self, 'nonce'):
            self._kdf.update(self.nonce)
        self._kdf.update(plaintext if output is None else output)
        self.verify(mac_tag)
        return plaintext


def _create_siv_cipher(factory, **kwargs):
    """Create a new block cipher, configured in
    Synthetic Initializaton Vector (SIV) mode.

    :Parameters:

      factory : object
        A symmetric cipher module from `Cryptodome.Cipher`
        (like `Cryptodome.Cipher.AES`).

    :Keywords:

      key : bytes/bytearray/memoryview
        The secret key to use in the symmetric cipher.
        It must be 32, 48 or 64 bytes long.
        If AES is the chosen cipher, the variants *AES-128*,
        *AES-192* and or *AES-256* will be used internally.

      nonce : bytes/bytearray/memoryview
        For deterministic encryption, it is not present.

        Otherwise, it is a value that must never be reused
        for encrypting message under this key.

        There are no restrictions on its length,
        but it is recommended to use at least 16 bytes.
    """
    try:
        key = kwargs.pop('key')
    except KeyError as e:
        raise TypeError('Missing parameter: ' + str(e))

    nonce = kwargs.pop('nonce', None)
    return SivMode(factory, key, nonce, kwargs)