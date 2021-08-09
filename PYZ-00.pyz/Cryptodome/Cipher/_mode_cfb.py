# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Cipher\_mode_cfb.py
"""
Counter Feedback (CFB) mode.
"""
__all__ = [
 'CfbMode']
from Cryptodome.Util.py3compat import _copy_bytes
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib, VoidPointer, create_string_buffer, get_raw_buffer, SmartPointer, c_size_t, c_uint8_ptr, is_writeable_buffer
from Cryptodome.Random import get_random_bytes
raw_cfb_lib = load_pycryptodome_raw_lib('Cryptodome.Cipher._raw_cfb', '\n                    int CFB_start_operation(void *cipher,\n                                            const uint8_t iv[],\n                                            size_t iv_len,\n                                            size_t segment_len, /* In bytes */\n                                            void **pResult);\n                    int CFB_encrypt(void *cfbState,\n                                    const uint8_t *in,\n                                    uint8_t *out,\n                                    size_t data_len);\n                    int CFB_decrypt(void *cfbState,\n                                    const uint8_t *in,\n                                    uint8_t *out,\n                                    size_t data_len);\n                    int CFB_stop_operation(void *state);')

class CfbMode(object):
    __doc__ = '*Cipher FeedBack (CFB)*.\n\n    This mode is similar to CFB, but it transforms\n    the underlying block cipher into a stream cipher.\n\n    Plaintext and ciphertext are processed in *segments*\n    of **s** bits. The mode is therefore sometimes\n    labelled **s**-bit CFB.\n\n    An Initialization Vector (*IV*) is required.\n\n    See `NIST SP800-38A`_ , Section 6.3.\n\n    .. _`NIST SP800-38A` : http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf\n\n    :undocumented: __init__\n    '

    def __init__(self, block_cipher, iv, segment_size):
        """Create a new block cipher, configured in CFB mode.

        :Parameters:
          block_cipher : C pointer
            A smart pointer to the low-level block cipher instance.

          iv : bytes/bytearray/memoryview
            The initialization vector to use for encryption or decryption.
            It is as long as the cipher block.

            **The IV must be unpredictable**. Ideally it is picked randomly.

            Reusing the *IV* for encryptions performed with the same key
            compromises confidentiality.

          segment_size : integer
            The number of bytes the plaintext and ciphertext are segmented in.
        """
        self._state = VoidPointer()
        result = raw_cfb_lib.CFB_start_operation(block_cipher.get(), c_uint8_ptr(iv), c_size_t(len(iv)), c_size_t(segment_size), self._state.address_of())
        if result:
            raise ValueError('Error %d while instatiating the CFB mode' % result)
        self._state = SmartPointer(self._state.get(), raw_cfb_lib.CFB_stop_operation)
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
            result = raw_cfb_lib.CFB_encrypt(self._state.get(), c_uint8_ptr(plaintext), c_uint8_ptr(ciphertext), c_size_t(len(plaintext)))
            if result:
                raise ValueError('Error %d while encrypting in CFB mode' % result)
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
            It can be of any length.
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
            result = raw_cfb_lib.CFB_decrypt(self._state.get(), c_uint8_ptr(ciphertext), c_uint8_ptr(plaintext), c_size_t(len(ciphertext)))
            if result:
                raise ValueError('Error %d while decrypting in CFB mode' % result)
        if output is None:
            return get_raw_buffer(plaintext)
        else:
            return


def _create_cfb_cipher(factory, **kwargs):
    """Instantiate a cipher object that performs CFB encryption/decryption.

    :Parameters:
      factory : module
        The underlying block cipher, a module from ``Cryptodome.Cipher``.

    :Keywords:
      iv : bytes/bytearray/memoryview
        The IV to use for CFB.

      IV : bytes/bytearray/memoryview
        Alias for ``iv``.

      segment_size : integer
        The number of bit the plaintext and ciphertext are segmented in.
        If not present, the default is 8.

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
    segment_size_bytes, rem = divmod(kwargs.pop('segment_size', 8), 8)
    if segment_size_bytes == 0 or rem != 0:
        raise ValueError("'segment_size' must be positive and multiple of 8 bits")
    if kwargs:
        raise TypeError('Unknown parameters for CFB: %s' % str(kwargs))
    return CfbMode(cipher_state, iv, segment_size_bytes)