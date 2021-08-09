# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Cipher\_mode_gcm.py
"""
Galois/Counter Mode (GCM).
"""
__all__ = [
 'GcmMode']
from binascii import unhexlify
from Cryptodome.Util.py3compat import bord, _copy_bytes
from Cryptodome.Util._raw_api import is_buffer
from Cryptodome.Util.number import long_to_bytes, bytes_to_long
from Cryptodome.Hash import BLAKE2s
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, create_string_buffer, get_raw_buffer, SmartPointer, c_size_t, c_uint8_ptr
from Cryptodome.Util import _cpu_features
_ghash_api_template = '\n    int ghash_%imp%(uint8_t y_out[16],\n                    const uint8_t block_data[],\n                    size_t len,\n                    const uint8_t y_in[16],\n                    const void *exp_key);\n    int ghash_expand_%imp%(const uint8_t h[16],\n                           void **ghash_tables);\n    int ghash_destroy_%imp%(void *ghash_tables);\n'

def _build_impl(lib, postfix):
    from collections import namedtuple
    funcs = ('ghash', 'ghash_expand', 'ghash_destroy')
    GHASH_Imp = namedtuple('_GHash_Imp', funcs)
    try:
        imp_funcs = [getattr(lib, x + '_' + postfix) for x in funcs]
    except AttributeError:
        imp_funcs = [
         None] * 3

    params = dict(zip(funcs, imp_funcs))
    return GHASH_Imp(**params)


def _get_ghash_portable():
    api = _ghash_api_template.replace('%imp%', 'portable')
    lib = load_pycryptodome_raw_lib('Cryptodome.Hash._ghash_portable', api)
    result = _build_impl(lib, 'portable')
    return result


_ghash_portable = _get_ghash_portable()

def _get_ghash_clmul():
    """Return None if CLMUL implementation is not available"""
    if not _cpu_features.have_clmul():
        return
    else:
        try:
            api = _ghash_api_template.replace('%imp%', 'clmul')
            lib = load_pycryptodome_raw_lib('Cryptodome.Hash._ghash_clmul', api)
            result = _build_impl(lib, 'clmul')
        except OSError:
            result = None

        return result


_ghash_clmul = _get_ghash_clmul()

class _GHASH(object):
    __doc__ = 'GHASH function defined in NIST SP 800-38D, Algorithm 2.\n\n    If X_1, X_2, .. X_m are the blocks of input data, the function\n    computes:\n\n       X_1*H^{m} + X_2*H^{m-1} + ... + X_m*H\n\n    in the Galois field GF(2^256) using the reducing polynomial\n    (x^128 + x^7 + x^2 + x + 1).\n    '

    def __init__(self, subkey, ghash_c):
        assert len(subkey) == 16
        self.ghash_c = ghash_c
        self._exp_key = VoidPointer()
        result = ghash_c.ghash_expand(c_uint8_ptr(subkey), self._exp_key.address_of())
        if result:
            raise ValueError('Error %d while expanding the GHASH key' % result)
        self._exp_key = SmartPointer(self._exp_key.get(), ghash_c.ghash_destroy)
        self._last_y = create_string_buffer(16)

    def update(self, block_data):
        assert len(block_data) % 16 == 0
        result = self.ghash_c.ghash(self._last_y, c_uint8_ptr(block_data), c_size_t(len(block_data)), self._last_y, self._exp_key.get())
        if result:
            raise ValueError('Error %d while updating GHASH' % result)
        return self

    def digest(self):
        return get_raw_buffer(self._last_y)


def enum(**enums):
    return type('Enum', (), enums)


MacStatus = enum(PROCESSING_AUTH_DATA=1, PROCESSING_CIPHERTEXT=2)

class GcmMode(object):
    __doc__ = 'Galois Counter Mode (GCM).\n\n    This is an Authenticated Encryption with Associated Data (`AEAD`_) mode.\n    It provides both confidentiality and authenticity.\n\n    The header of the message may be left in the clear, if needed, and it will\n    still be subject to authentication. The decryption step tells the receiver\n    if the message comes from a source that really knowns the secret key.\n    Additionally, decryption detects if any part of the message - including the\n    header - has been modified or corrupted.\n\n    This mode requires a *nonce*.\n\n    This mode is only available for ciphers that operate on 128 bits blocks\n    (e.g. AES but not TDES).\n\n    See `NIST SP800-38D`_.\n\n    .. _`NIST SP800-38D`: http://csrc.nist.gov/publications/nistpubs/800-38D/SP-800-38D.pdf\n    .. _AEAD: http://blog.cryptographyengineering.com/2012/05/how-to-choose-authenticated-encryption.html\n\n    :undocumented: __init__\n    '

    def __init__(self, factory, key, nonce, mac_len, cipher_params, ghash_c):
        self.block_size = factory.block_size
        if self.block_size != 16:
            raise ValueError('GCM mode is only available for ciphers that operate on 128 bits blocks')
        if len(nonce) == 0:
            raise ValueError('Nonce cannot be empty')
        if not is_buffer(nonce):
            raise TypeError('Nonce must be bytes, bytearray or memoryview')
        if len(nonce) > 18446744073709551615:
            raise ValueError('Nonce exceeds maximum length')
        else:
            self.nonce = _copy_bytes(None, None, nonce)
            self._factory = factory
            self._key = _copy_bytes(None, None, key)
            self._tag = None
            self._mac_len = mac_len
            if not 4 <= mac_len <= 16:
                raise ValueError("Parameter 'mac_len' must be in the range 4..16")
            self._next = [
             self.update, self.encrypt, self.decrypt,
             self.digest, self.verify]
            self._no_more_assoc_data = False
            self._auth_len = 0
            self._msg_len = 0
            hash_subkey = (factory.new)(key, 
             (self._factory.MODE_ECB), **cipher_params).encrypt(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            if len(self.nonce) == 12:
                self._j0 = bytes_to_long(self.nonce + b'\x00\x00\x00\x01')
            else:
                fill = (16 - len(nonce) % 16) % 16 + 8
            ghash_in = self.nonce + b'\x00' * fill + long_to_bytes(8 * len(nonce), 8)
            self._j0 = bytes_to_long(_GHASH(hash_subkey, ghash_c).update(ghash_in).digest())
        nonce_ctr = long_to_bytes(self._j0 >> 32, 12)
        iv_ctr = self._j0 + 1 & 4294967295
        self._cipher = (factory.new)(key,
 self._factory.MODE_CTR, initial_value=iv_ctr, 
         nonce=nonce_ctr, **cipher_params)
        self._signer = _GHASH(hash_subkey, ghash_c)
        self._tag_cipher = (factory.new)(key,
 self._factory.MODE_CTR, initial_value=self._j0, 
         nonce=b'', **cipher_params)
        self._cache = b''
        self._status = MacStatus.PROCESSING_AUTH_DATA

    def update(self, assoc_data):
        """Protect associated data

        If there is any associated data, the caller has to invoke
        this function one or more times, before using
        ``decrypt`` or ``encrypt``.

        By *associated data* it is meant any data (e.g. packet headers) that
        will not be encrypted and will be transmitted in the clear.
        However, the receiver is still able to detect any modification to it.
        In GCM, the *associated data* is also called
        *additional authenticated data* (AAD).

        If there is no associated data, this method must not be called.

        The caller may split associated data in segments of any size, and
        invoke this method multiple times, each time with the next segment.

        :Parameters:
          assoc_data : bytes/bytearray/memoryview
            A piece of associated data. There are no restrictions on its size.
        """
        if self.update not in self._next:
            raise TypeError('update() can only be called immediately after initialization')
        self._next = [
         self.update, self.encrypt, self.decrypt,
         self.digest, self.verify]
        self._update(assoc_data)
        self._auth_len += len(assoc_data)
        if self._auth_len > 18446744073709551615:
            raise ValueError('Additional Authenticated Data exceeds maximum length')
        return self

    def _update(self, data):
        if not len(self._cache) < 16:
            raise AssertionError
        else:
            if len(self._cache) > 0:
                filler = min(16 - len(self._cache), len(data))
                self._cache += _copy_bytes(None, filler, data)
                data = data[filler:]
                if len(self._cache) < 16:
                    return
                self._signer.update(self._cache)
                self._cache = b''
            update_len = len(data) // 16 * 16
            self._cache = _copy_bytes(update_len, None, data)
            if update_len > 0:
                self._signer.update(data[:update_len])

    def _pad_cache_and_update(self):
        assert len(self._cache) < 16
        len_cache = len(self._cache)
        if len_cache > 0:
            self._update(b'\x00' * (16 - len_cache))

    def encrypt(self, plaintext, output=None):
        """Encrypt data with the key and the parameters set at initialization.

        A cipher object is stateful: once you have encrypted a message
        you cannot encrypt (or decrypt) another message using the same
        object.

        The data to encrypt can be broken up in two or
        more pieces and `encrypt` can be called multiple times.

        That is, the statement:

            >>> c.encrypt(a) + c.encrypt(b)

        is equivalent to:

             >>> c.encrypt(a+b)

        This function does not add any padding to the plaintext.

        :Parameters:
          plaintext : bytes/bytearray/memoryview
            The piece of data to encrypt.
            It can be of any length.
        :Keywords:
          output : bytearray/memoryview
            The location where the ciphertext must be written to.
            If ``None``, the ciphertext is returned.
        :Return:
          If ``output`` is ``None``, the ciphertext as ``bytes``.
          Otherwise, ``None``.
        """
        if self.encrypt not in self._next:
            raise TypeError('encrypt() can only be called after initialization or an update()')
        else:
            self._next = [
             self.encrypt, self.digest]
            ciphertext = self._cipher.encrypt(plaintext, output=output)
            if self._status == MacStatus.PROCESSING_AUTH_DATA:
                self._pad_cache_and_update()
                self._status = MacStatus.PROCESSING_CIPHERTEXT
            self._update(ciphertext if output is None else output)
            self._msg_len += len(plaintext)
            if self._msg_len > 549755813632:
                raise ValueError('Plaintext exceeds maximum length')
        return ciphertext

    def decrypt(self, ciphertext, output=None):
        """Decrypt data with the key and the parameters set at initialization.

        A cipher object is stateful: once you have decrypted a message
        you cannot decrypt (or encrypt) another message with the same
        object.

        The data to decrypt can be broken up in two or
        more pieces and `decrypt` can be called multiple times.

        That is, the statement:

            >>> c.decrypt(a) + c.decrypt(b)

        is equivalent to:

             >>> c.decrypt(a+b)

        This function does not remove any padding from the plaintext.

        :Parameters:
          ciphertext : bytes/bytearray/memoryview
            The piece of data to decrypt.
            It can be of any length.
        :Keywords:
          output : bytearray/memoryview
            The location where the plaintext must be written to.
            If ``None``, the plaintext is returned.
        :Return:
          If ``output`` is ``None``, the plaintext as ``bytes``.
          Otherwise, ``None``.
        """
        if self.decrypt not in self._next:
            raise TypeError('decrypt() can only be called after initialization or an update()')
        self._next = [self.decrypt, self.verify]
        if self._status == MacStatus.PROCESSING_AUTH_DATA:
            self._pad_cache_and_update()
            self._status = MacStatus.PROCESSING_CIPHERTEXT
        self._update(ciphertext)
        self._msg_len += len(ciphertext)
        return self._cipher.decrypt(ciphertext, output=output)

    def digest(self):
        """Compute the *binary* MAC tag in an AEAD mode.

        The caller invokes this function at the very end.

        This method returns the MAC that shall be sent to the receiver,
        together with the ciphertext.

        :Return: the MAC, as a byte string.
        """
        if self.digest not in self._next:
            raise TypeError('digest() cannot be called when decrypting or validating a message')
        self._next = [self.digest]
        return self._compute_mac()

    def _compute_mac(self):
        """Compute MAC without any FSM checks."""
        if self._tag:
            return self._tag
        else:
            self._pad_cache_and_update()
            self._update(long_to_bytes(8 * self._auth_len, 8))
            self._update(long_to_bytes(8 * self._msg_len, 8))
            s_tag = self._signer.digest()
            self._tag = self._tag_cipher.encrypt(s_tag)[:self._mac_len]
            return self._tag

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
        self._next = [self.verify]
        secret = get_random_bytes(16)
        mac1 = BLAKE2s.new(digest_bits=160, key=secret, data=(self._compute_mac()))
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
        return (
         self.encrypt(plaintext, output=output), self.digest())

    def decrypt_and_verify(self, ciphertext, received_mac_tag, output=None):
        """Perform decrypt() and verify() in one step.

        :Parameters:
          ciphertext : bytes/bytearray/memoryview
            The piece of data to decrypt.
          received_mac_tag : byte string
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
        plaintext = self.decrypt(ciphertext, output=output)
        self.verify(received_mac_tag)
        return plaintext


def _create_gcm_cipher(factory, **kwargs):
    """Create a new block cipher, configured in Galois Counter Mode (GCM).

    :Parameters:
      factory : module
        A block cipher module, taken from `Cryptodome.Cipher`.
        The cipher must have block length of 16 bytes.
        GCM has been only defined for `Cryptodome.Cipher.AES`.

    :Keywords:
      key : bytes/bytearray/memoryview
        The secret key to use in the symmetric cipher.
        It must be 16 (e.g. *AES-128*), 24 (e.g. *AES-192*)
        or 32 (e.g. *AES-256*) bytes long.

      nonce : bytes/bytearray/memoryview
        A value that must never be reused for any other encryption.

        There are no restrictions on its length,
        but it is recommended to use at least 16 bytes.

        The nonce shall never repeat for two
        different messages encrypted with the same key,
        but it does not need to be random.

        If not provided, a 16 byte nonce will be randomly created.

      mac_len : integer
        Length of the MAC, in bytes.
        It must be no larger than 16 bytes (which is the default).
    """
    try:
        key = kwargs.pop('key')
    except KeyError as e:
        raise TypeError('Missing parameter:' + str(e))

    nonce = kwargs.pop('nonce', None)
    if nonce is None:
        nonce = get_random_bytes(16)
    else:
        mac_len = kwargs.pop('mac_len', 16)
        use_clmul = kwargs.pop('use_clmul', True)
        if use_clmul:
            if _ghash_clmul:
                ghash_c = _ghash_clmul
        ghash_c = _ghash_portable
    return GcmMode(factory, key, nonce, mac_len, kwargs, ghash_c)