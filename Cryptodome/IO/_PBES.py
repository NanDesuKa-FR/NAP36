# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\IO\_PBES.py
from Cryptodome.Util.py3compat import *
from Cryptodome import Random
from Cryptodome.Util.asn1 import DerSequence, DerOctetString, DerObjectId, DerInteger
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Hash import MD5, SHA1
from Cryptodome.Cipher import DES, ARC2, DES3, AES
from Cryptodome.Protocol.KDF import PBKDF1, PBKDF2, scrypt

class PbesError(ValueError):
    pass


class PBES1(object):
    __doc__ = 'Deprecated encryption scheme with password-based key derivation\n    (originally defined in PKCS#5 v1.5, but still present in `v2.0`__).\n\n    .. __: http://www.ietf.org/rfc/rfc2898.txt\n    '

    @staticmethod
    def decrypt(data, passphrase):
        """Decrypt a piece of data using a passphrase and *PBES1*.

        The algorithm to use is automatically detected.

        :Parameters:
          data : byte string
            The piece of data to decrypt.
          passphrase : byte string
            The passphrase to use for decrypting the data.
        :Returns:
          The decrypted data, as a binary string.
        """
        enc_private_key_info = DerSequence().decode(data)
        encrypted_algorithm = DerSequence().decode(enc_private_key_info[0])
        encrypted_data = DerOctetString().decode(enc_private_key_info[1]).payload
        pbe_oid = DerObjectId().decode(encrypted_algorithm[0]).value
        cipher_params = {}
        if pbe_oid == '1.2.840.113549.1.5.3':
            hashmod = MD5
            ciphermod = DES
        else:
            if pbe_oid == '1.2.840.113549.1.5.6':
                hashmod = MD5
                ciphermod = ARC2
                cipher_params['effective_keylen'] = 64
            else:
                if pbe_oid == '1.2.840.113549.1.5.10':
                    hashmod = SHA1
                    ciphermod = DES
                else:
                    if pbe_oid == '1.2.840.113549.1.5.11':
                        hashmod = SHA1
                        ciphermod = ARC2
                        cipher_params['effective_keylen'] = 64
                    else:
                        raise PbesError('Unknown OID for PBES1')
        pbe_params = DerSequence().decode((encrypted_algorithm[1]), nr_elements=2)
        salt = DerOctetString().decode(pbe_params[0]).payload
        iterations = pbe_params[1]
        key_iv = PBKDF1(passphrase, salt, 16, iterations, hashmod)
        key, iv = key_iv[:8], key_iv[8:]
        cipher = (ciphermod.new)(key, (ciphermod.MODE_CBC), iv, **cipher_params)
        pt = cipher.decrypt(encrypted_data)
        return unpad(pt, cipher.block_size)


class PBES2(object):
    __doc__ = 'Encryption scheme with password-based key derivation\n    (defined in `PKCS#5 v2.0`__).\n\n    .. __: http://www.ietf.org/rfc/rfc2898.txt.'

    @staticmethod
    def encrypt(data, passphrase, protection, prot_params=None, randfunc=None):
        """Encrypt a piece of data using a passphrase and *PBES2*.

        :Parameters:
          data : byte string
            The piece of data to encrypt.
          passphrase : byte string
            The passphrase to use for encrypting the data.
          protection : string
            The identifier of the encryption algorithm to use.
            The default value is '``PBKDF2WithHMAC-SHA1AndDES-EDE3-CBC``'.
          prot_params : dictionary
            Parameters of the protection algorithm.

            +------------------+-----------------------------------------------+
            | Key              | Description                                   |
            +==================+===============================================+
            | iteration_count  | The KDF algorithm is repeated several times to|
            |                  | slow down brute force attacks on passwords    |
            |                  | (called *N* or CPU/memory cost in scrypt).    |
            |                  |                                               |
            |                  | The default value for PBKDF2 is 1 000.        |
            |                  | The default value for scrypt is 16 384.       |
            +------------------+-----------------------------------------------+
            | salt_size        | Salt is used to thwart dictionary and rainbow |
            |                  | attacks on passwords. The default value is 8  |
            |                  | bytes.                                        |
            +------------------+-----------------------------------------------+
            | block_size       | *(scrypt only)* Memory-cost (r). The default  |
            |                  | value is 8.                                   |
            +------------------+-----------------------------------------------+
            | parallelization  | *(scrypt only)* CPU-cost (p). The default     |
            |                  | value is 1.                                   |
            +------------------+-----------------------------------------------+

          randfunc : callable
            Random number generation function; it should accept
            a single integer N and return a string of random data,
            N bytes long. If not specified, a new RNG will be
            instantiated from ``Cryptodome.Random``.

        :Returns:
          The encrypted data, as a binary string.
        """
        if prot_params is None:
            prot_params = {}
        else:
            if randfunc is None:
                randfunc = Random.new().read
            else:
                if protection == 'PBKDF2WithHMAC-SHA1AndDES-EDE3-CBC':
                    key_size = 24
                    module = DES3
                    cipher_mode = DES3.MODE_CBC
                    enc_oid = '1.2.840.113549.3.7'
                else:
                    if protection in ('PBKDF2WithHMAC-SHA1AndAES128-CBC', 'scryptAndAES128-CBC'):
                        key_size = 16
                        module = AES
                        cipher_mode = AES.MODE_CBC
                        enc_oid = '2.16.840.1.101.3.4.1.2'
                    else:
                        if protection in ('PBKDF2WithHMAC-SHA1AndAES192-CBC', 'scryptAndAES192-CBC'):
                            key_size = 24
                            module = AES
                            cipher_mode = AES.MODE_CBC
                            enc_oid = '2.16.840.1.101.3.4.1.22'
                        else:
                            if protection in ('PBKDF2WithHMAC-SHA1AndAES256-CBC', 'scryptAndAES256-CBC'):
                                key_size = 32
                                module = AES
                                cipher_mode = AES.MODE_CBC
                                enc_oid = '2.16.840.1.101.3.4.1.42'
                            else:
                                raise ValueError('Unknown PBES2 mode')
            iv = randfunc(module.block_size)
            salt = randfunc(prot_params.get('salt_size', 8))
            if protection.startswith('PBKDF2'):
                count = prot_params.get('iteration_count', 1000)
                key = PBKDF2(passphrase, salt, key_size, count)
                kdf_info = DerSequence([
                 DerObjectId('1.2.840.113549.1.5.12'),
                 DerSequence([
                  DerOctetString(salt),
                  DerInteger(count)])])
            else:
                count = prot_params.get('iteration_count', 16384)
            scrypt_r = prot_params.get('block_size', 8)
            scrypt_p = prot_params.get('parallelization', 1)
            key = scrypt(passphrase, salt, key_size, count, scrypt_r, scrypt_p)
            kdf_info = DerSequence([
             DerObjectId('1.3.6.1.4.1.11591.4.11'),
             DerSequence([
              DerOctetString(salt),
              DerInteger(count),
              DerInteger(scrypt_r),
              DerInteger(scrypt_p)])])
        cipher = module.new(key, cipher_mode, iv)
        encrypted_data = cipher.encrypt(pad(data, cipher.block_size))
        enc_info = DerSequence([
         DerObjectId(enc_oid),
         DerOctetString(iv)])
        enc_private_key_info = DerSequence([
         DerSequence([
          DerObjectId('1.2.840.113549.1.5.13'),
          DerSequence([
           kdf_info,
           enc_info])]),
         DerOctetString(encrypted_data)])
        return enc_private_key_info.encode()

    @staticmethod
    def decrypt(data, passphrase):
        """Decrypt a piece of data using a passphrase and *PBES2*.

        The algorithm to use is automatically detected.

        :Parameters:
          data : byte string
            The piece of data to decrypt.
          passphrase : byte string
            The passphrase to use for decrypting the data.
        :Returns:
          The decrypted data, as a binary string.
        """
        enc_private_key_info = DerSequence().decode(data, nr_elements=2)
        enc_algo = DerSequence().decode(enc_private_key_info[0])
        encrypted_data = DerOctetString().decode(enc_private_key_info[1]).payload
        pbe_oid = DerObjectId().decode(enc_algo[0]).value
        if pbe_oid != '1.2.840.113549.1.5.13':
            raise PbesError('Not a PBES2 object')
        pbes2_params = DerSequence().decode((enc_algo[1]), nr_elements=2)
        kdf_info = DerSequence().decode((pbes2_params[0]), nr_elements=2)
        kdf_oid = DerObjectId().decode(kdf_info[0]).value
        if kdf_oid == '1.2.840.113549.1.5.12':
            pbkdf2_params = DerSequence().decode((kdf_info[1]), nr_elements=(2, 3,
                                                                             4))
            salt = DerOctetString().decode(pbkdf2_params[0]).payload
            iteration_count = pbkdf2_params[1]
            if len(pbkdf2_params) > 2:
                kdf_key_length = pbkdf2_params[2]
            else:
                kdf_key_length = None
            if len(pbkdf2_params) > 3:
                raise PbesError('Unsupported PRF for PBKDF2')
        else:
            if kdf_oid == '1.3.6.1.4.1.11591.4.11':
                scrypt_params = DerSequence().decode((kdf_info[1]), nr_elements=(4,
                                                                                 5))
                salt = DerOctetString().decode(scrypt_params[0]).payload
                iteration_count, scrypt_r, scrypt_p = [scrypt_params[x] for x in (1,
                                                                                  2,
                                                                                  3)]
                if len(scrypt_params) > 4:
                    kdf_key_length = scrypt_params[4]
                else:
                    kdf_key_length = None
            else:
                raise PbesError('Unsupported PBES2 KDF')
            enc_info = DerSequence().decode(pbes2_params[1])
            enc_oid = DerObjectId().decode(enc_info[0]).value
            if enc_oid == '1.2.840.113549.3.7':
                ciphermod = DES3
                key_size = 24
            else:
                if enc_oid == '2.16.840.1.101.3.4.1.2':
                    ciphermod = AES
                    key_size = 16
                else:
                    if enc_oid == '2.16.840.1.101.3.4.1.22':
                        ciphermod = AES
                        key_size = 24
                    else:
                        if enc_oid == '2.16.840.1.101.3.4.1.42':
                            ciphermod = AES
                            key_size = 32
                        else:
                            raise PbesError('Unsupported PBES2 cipher')
            if kdf_key_length:
                if kdf_key_length != key_size:
                    raise PbesError('Mismatch between PBES2 KDF parameters and selected cipher')
            else:
                IV = DerOctetString().decode(enc_info[1]).payload
                if kdf_oid == '1.2.840.113549.1.5.12':
                    key = PBKDF2(passphrase, salt, key_size, iteration_count)
                else:
                    key = scrypt(passphrase, salt, key_size, iteration_count, scrypt_r, scrypt_p)
            cipher = ciphermod.new(key, ciphermod.MODE_CBC, IV)
            pt = cipher.decrypt(encrypted_data)
            return unpad(pt, cipher.block_size)