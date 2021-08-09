# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\IO\PEM.py
__all__ = [
 'encode', 'decode']
import re
from binascii import a2b_base64, b2a_base64, hexlify, unhexlify
from Cryptodome.Hash import MD5
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Cipher import DES, DES3, AES
from Cryptodome.Protocol.KDF import PBKDF1
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.py3compat import tobytes, tostr

def encode(data, marker, passphrase=None, randfunc=None):
    """Encode a piece of binary data into PEM format.

    Args:
      data (byte string):
        The piece of binary data to encode.
      marker (string):
        The marker for the PEM block (e.g. "PUBLIC KEY").
        Note that there is no official master list for all allowed markers.
        Still, you can refer to the OpenSSL_ source code.
      passphrase (byte string):
        If given, the PEM block will be encrypted. The key is derived from
        the passphrase.
      randfunc (callable):
        Random number generation function; it accepts an integer N and returns
        a byte string of random data, N bytes long. If not given, a new one is
        instantiated.

    Returns:
      The PEM block, as a string.

    .. _OpenSSL: https://github.com/openssl/openssl/blob/master/include/openssl/pem.h
    """
    if randfunc is None:
        randfunc = get_random_bytes
    out = '-----BEGIN %s-----\n' % marker
    if passphrase:
        salt = randfunc(8)
        key = PBKDF1(passphrase, salt, 16, 1, MD5)
        key += PBKDF1(key + passphrase, salt, 8, 1, MD5)
        objenc = DES3.new(key, DES3.MODE_CBC, salt)
        out += 'Proc-Type: 4,ENCRYPTED\nDEK-Info: DES-EDE3-CBC,%s\n\n' % tostr(hexlify(salt).upper())
        data = objenc.encrypt(pad(data, objenc.block_size))
    else:
        if passphrase is not None:
            raise ValueError('Empty password')
    chunks = [tostr(b2a_base64(data[i:i + 48])) for i in range(0, len(data), 48)]
    out += ''.join(chunks)
    out += '-----END %s-----' % marker
    return out


def decode(pem_data, passphrase=None):
    """Decode a PEM block into binary.

    Args:
      pem_data (string):
        The PEM block.
      passphrase (byte string):
        If given and the PEM block is encrypted,
        the key will be derived from the passphrase.

    Returns:
      A tuple with the binary data, the marker string, and a boolean to
      indicate if decryption was performed.

    Raises:
      ValueError: if decoding fails, if the PEM file is encrypted and no passphrase has
                  been provided or if the passphrase is incorrect.
    """
    r = re.compile('\\s*-----BEGIN (.*)-----\\s+')
    m = r.match(pem_data)
    if not m:
        raise ValueError('Not a valid PEM pre boundary')
    else:
        marker = m.group(1)
        r = re.compile('-----END (.*)-----\\s*$')
        m = r.search(pem_data)
        if not m or m.group(1) != marker:
            raise ValueError('Not a valid PEM post boundary')
        lines = pem_data.replace(' ', '').split()
        if lines[1].startswith('Proc-Type:4,ENCRYPTED'):
            if not passphrase:
                raise ValueError('PEM is encrypted, but no passphrase available')
            else:
                DEK = lines[2].split(':')
                if len(DEK) != 2 or DEK[0] != 'DEK-Info':
                    raise ValueError('PEM encryption format not supported.')
                algo, salt = DEK[1].split(',')
                salt = unhexlify(tobytes(salt))
                if algo == 'DES-CBC':
                    key = PBKDF1(passphrase, salt, 8, 1, MD5)
                    objdec = DES.new(key, DES.MODE_CBC, salt)
                else:
                    if algo == 'DES-EDE3-CBC':
                        key = PBKDF1(passphrase, salt, 16, 1, MD5)
                        key += PBKDF1(key + passphrase, salt, 8, 1, MD5)
                        objdec = DES3.new(key, DES3.MODE_CBC, salt)
                    else:
                        if algo == 'AES-128-CBC':
                            key = PBKDF1(passphrase, salt[:8], 16, 1, MD5)
                            objdec = AES.new(key, AES.MODE_CBC, salt)
                        else:
                            raise ValueError('Unsupport PEM encryption algorithm (%s).' % algo)
            lines = lines[2:]
        else:
            objdec = None
    data = a2b_base64(''.join(lines[1:-1]))
    enc_flag = False
    if objdec:
        data = unpad(objdec.decrypt(data), objdec.block_size)
        enc_flag = True
    return (data, marker, enc_flag)