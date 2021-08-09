# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Cipher\_mode_cbc.py
"""
Ciphertext Block Chaining (CBC) mode.
"""
__all__ = [
 'CbcMode']
from Cryptodome.Util.py3compat import _copy_bytes
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, create_string_buffer, get_raw_buffer, SmartPointer, c_size_t, c_uint8_ptr, is_writeable_buffer
from Cryptodome.Random import get_random_bytes
raw_cbc_lib = load_pycryptodome_raw_lib('Cryptodome.Cipher._raw_cbc', '\n                int CBC_start_operation(void *cipher,\n                                        const uint8_t iv[],\n                                        size_t iv_len,\n                                        void **pResult);\n                int CBC_encrypt(void *cbcState,\n                                const uint8_t *in,\n                                uint8_t *out,\n                                size_t data_len);\n                int CBC_decrypt(void *cbcState,\n                                const uint8_t *in,\n                                uint8_t *out,\n                                size_t data_len);\n                int CBC_stop_operation(void *state);\n                ')

class CbcMode(object):
    __doc__ = '*Cipher-Block Chaining (CBC)*.\n\n    Each of the ciphertext blocks depends on the current\n    and all previous plaintext blocks.\n\n    An Initialization Vector (*IV*) is required.\n\n    See `NIST SP800-38A`_ , Section 6.2 .\n\n    .. _`NIST SP800-38A` : http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf\n\n    :undocumented: __init__\n    '

    def __init__(self, block_cipher, iv):
        """Create a new block cipher, configured in CBC mode.

        :Parameters:
          block_cipher : C pointer
            A smart pointer to the low-level block cipher instance.

          iv : bytes/bytearray/memoryview
            The initialization vector to use for encryption or decryption.
            It is as long as the cipher block.

            **The IV must be unpredictable**. Ideally it is picked randomly.

            Reusing the *IV* for encryptions performed with the same key
            compromises confidentiality.
        """
        self._state = VoidPointer()
        result = raw_cbc_lib.CBC_start_operation(block_cipher.get(), c_uint8_ptr(iv), c_size_t(len(iv)), self._state.address_of())
        if result:
            raise ValueError('Error %d while instantiating the CBC mode' % result)
        self._state = SmartPointer(self._state.get(), raw_cbc_lib.CBC_stop_operation)
        block_cipher.release()
        self.block_size = len(iv)
        self.iv = _copy_bytes(None, None, iv)
        self.IV = self.iv
        self._next = [
         self.encrypt, self.decrypt]

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

        That also means that you cannot reuse an object for encrypting
        or decrypting other data with the same key.

        This function does not add any padding to the plaintext.

        :Parameters:
          plaintext : bytes/bytearray/memoryview
            The piece of data to encrypt.
            Its lenght must be multiple of the cipher block size.
        :Keywords:
          output : bytearray/memoryview
            The location where the ciphertext must be written to.
            If ``None``, the ciphertext is returned.
        :Return:
          If ``output`` is ``None``, the ciphertext is returned as ``bytes``.
          Otherwise, ``None``.
        """
        if self.encrypt not in self._next:
            raise TypeError('encrypt() cannot be called after decrypt()')
        else:
            self._next = [
             self.encrypt]
            if output is None:
                ciphertext = create_string_buffer(len(plaintext))
            else:
                ciphertext = output
            if not is_writeable_buffer(output):
                raise TypeError('output must be a bytearray or a writeable memoryview')
            if len(plaintext) != len(output):
                raise ValueError('output must have the same length as the input  (%d bytes)' % len(plaintext))
            result = raw_cbc_lib.CBC_encrypt(self._state.get(), c_uint8_ptr(plaintext), c_uint8_ptr(ciphertext), c_size_t(len(plaintext)))
            if result:
                if result == 3:
                    raise ValueError('Data must be padded to %d byte boundary in CBC mode' % self.block_size)
                raise ValueError('Error %d while encrypting in CBC mode' % result)
        if output is None:
            return get_raw_buffer(ciphertext)
        else:
            return

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
            Its length must be multiple of the cipher block size.
        :Keywords:
          output : bytearray/memoryview
            The location where the plaintext must be written to.
            If ``None``, the plaintext is returned.
        :Return:
          If ``output`` is ``None``, the plaintext is returned as ``bytes``.
          Otherwise, ``None``.
        """
        if self.decrypt not in self._next:
            raise TypeError('decrypt() cannot be called after encrypt()')
        else:
            self._next = [
             self.decrypt]
            if output is None:
                plaintext = create_string_buffer(len(ciphertext))
            else:
                plaintext = output
            if not is_writeable_buffer(output):
                raise TypeError('output must be a bytearray or a writeable memoryview')
            if len(ciphertext) != len(output):
                raise ValueError('output must have the same length as the input  (%d bytes)' % len(plaintext))
            result = raw_cbc_lib.CBC_decrypt(self._state.get(), c_uint8_ptr(ciphertext), c_uint8_ptr(plaintext), c_size_t(len(ciphertext)))
            if result:
                if result == 3:
                    raise ValueError('Data must be padded to %d byte boundary in CBC mode' % self.block_size)
                raise ValueError('Error %d while decrypting in CBC mode' % result)
        if output is None:
            return get_raw_buffer(plaintext)
        else:
            return


def _create_cbc_cipher(factory, **kwargs):
    """Instantiate a cipher object that performs CBC encryption/decryption.

    :Parameters:
      factory : module
        The underlying block cipher, a module from ``Cryptodome.Cipher``.

    :Keywords:
      iv : bytes/bytearray/memoryview
        The IV to use for CBC.

      IV : bytes/bytearray/memoryview
        Alias for ``iv``.

    Any other keyword will be passed to the underlying block cipher.
    See the relevant documentation for details (at least ``key`` will need
    to be present).
    """
    cipher_state = factory._create_base_cipher(kwargs)
    iv = kwargs.pop('IV', None)
    IV = kwargs.pop('iv', None)
    if (None, None) == (iv, IV):
        iv = get_random_bytes(factory.block_size)
    else:
        if iv is not None:
            if IV is not None:
                raise TypeError("You must either use 'iv' or 'IV', not both")
        else:
            iv = IV
    if len(iv) != factory.block_size:
        raise ValueError('Incorrect IV length (it must be %d bytes long)' % factory.block_size)
    if kwargs:
        raise TypeError('Unknown parameters for CBC: %s' % str(kwargs))
    return CbcMode(cipher_state, iv)