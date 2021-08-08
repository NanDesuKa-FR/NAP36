# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Cipher\_mode_openpgp.py
"""
OpenPGP mode.
"""
__all__ = [
 'OpenPgpMode']
from Cryptodome.Util.py3compat import _copy_bytes
from Cryptodome.Random import get_random_bytes

class OpenPgpMode(object):
    __doc__ = 'OpenPGP mode.\n\n    This mode is a variant of CFB, and it is only used in PGP and\n    OpenPGP_ applications. If in doubt, use another mode.\n\n    An Initialization Vector (*IV*) is required.\n\n    Unlike CFB, the *encrypted* IV (not the IV itself) is\n    transmitted to the receiver.\n\n    The IV is a random data block. For legacy reasons, two of its bytes are\n    duplicated to act as a checksum for the correctness of the key, which is now\n    known to be insecure and is ignored. The encrypted IV is therefore 2 bytes\n    longer than the clean IV.\n\n    .. _OpenPGP: http://tools.ietf.org/html/rfc4880\n\n    :undocumented: __init__\n    '

    def __init__(self, factory, key, iv, cipher_params):
        self.block_size = factory.block_size
        self._done_first_block = False
        IV_cipher = (factory.new)(
 key,
 factory.MODE_CFB, IV=b'\x00' * self.block_size, 
         segment_size=self.block_size * 8, **cipher_params)
        iv = _copy_bytes(None, None, iv)
        if len(iv) == self.block_size:
            self._encrypted_IV = IV_cipher.encrypt(iv + iv[-2:])
        else:
            if len(iv) == self.block_size + 2:
                self._encrypted_IV = iv
                iv = IV_cipher.decrypt(iv)[:-2]
            else:
                raise ValueError('Length of IV must be %d or %d bytes for MODE_OPENPGP' % (
                 self.block_size, self.block_size + 2))
        self.iv = self.IV = iv
        self._cipher = (factory.new)(
 key,
 factory.MODE_CFB, IV=self._encrypted_IV[-self.block_size:], 
         segment_size=self.block_size * 8, **cipher_params)

    def encrypt(self, plaintext):
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

        :Return:
            the encrypted data, as a byte string.
            It is as long as *plaintext* with one exception:
            when encrypting the first message chunk,
            the encypted IV is prepended to the returned ciphertext.
        """
        res = self._cipher.encrypt(plaintext)
        if not self._done_first_block:
            res = self._encrypted_IV + res
            self._done_first_block = True
        return res

    def decrypt(self, ciphertext):
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

        :Return: the decrypted data (byte string).
        """
        return self._cipher.decrypt(ciphertext)


def _create_openpgp_cipher(factory, **kwargs):
    """Create a new block cipher, configured in OpenPGP mode.

    :Parameters:
      factory : module
        The module.

    :Keywords:
      key : bytes/bytearray/memoryview
        The secret key to use in the symmetric cipher.

      IV : bytes/bytearray/memoryview
        The initialization vector to use for encryption or decryption.

        For encryption, the IV must be as long as the cipher block size.

        For decryption, it must be 2 bytes longer (it is actually the
        *encrypted* IV which was prefixed to the ciphertext).
    """
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
    try:
        key = kwargs.pop('key')
    except KeyError as e:
        raise TypeError('Missing component: ' + str(e))

    return OpenPgpMode(factory, key, iv, kwargs)