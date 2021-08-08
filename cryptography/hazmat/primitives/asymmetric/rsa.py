# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\primitives\asymmetric\rsa.py
from __future__ import absolute_import, division, print_function
import abc
try:
    from math import gcd
except ImportError:
    from fractions import gcd

import six
from cryptography import utils
from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.interfaces import RSABackend

@six.add_metaclass(abc.ABCMeta)
class RSAPrivateKey(object):

    @abc.abstractmethod
    def signer(self, padding, algorithm):
        """
        Returns an AsymmetricSignatureContext used for signing data.
        """
        pass

    @abc.abstractmethod
    def decrypt(self, ciphertext, padding):
        """
        Decrypts the provided ciphertext.
        """
        pass

    @abc.abstractproperty
    def key_size(self):
        """
        The bit length of the public modulus.
        """
        pass

    @abc.abstractmethod
    def public_key(self):
        """
        The RSAPublicKey associated with this private key.
        """
        pass

    @abc.abstractmethod
    def sign(self, data, padding, algorithm):
        """
        Signs the data.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class RSAPrivateKeyWithSerialization(RSAPrivateKey):

    @abc.abstractmethod
    def private_numbers(self):
        """
        Returns an RSAPrivateNumbers.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding, format, encryption_algorithm):
        """
        Returns the key serialized as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class RSAPublicKey(object):

    @abc.abstractmethod
    def verifier(self, signature, padding, algorithm):
        """
        Returns an AsymmetricVerificationContext used for verifying signatures.
        """
        pass

    @abc.abstractmethod
    def encrypt(self, plaintext, padding):
        """
        Encrypts the given plaintext.
        """
        pass

    @abc.abstractproperty
    def key_size(self):
        """
        The bit length of the public modulus.
        """
        pass

    @abc.abstractmethod
    def public_numbers(self):
        """
        Returns an RSAPublicNumbers
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding, format):
        """
        Returns the key serialized as bytes.
        """
        pass

    @abc.abstractmethod
    def verify(self, signature, data, padding, algorithm):
        """
        Verifies the signature of the data.
        """
        pass


RSAPublicKeyWithSerialization = RSAPublicKey

def generate_private_key(public_exponent, key_size, backend):
    if not isinstance(backend, RSABackend):
        raise UnsupportedAlgorithm('Backend object does not implement RSABackend.', _Reasons.BACKEND_MISSING_INTERFACE)
    _verify_rsa_parameters(public_exponent, key_size)
    return backend.generate_rsa_private_key(public_exponent, key_size)


def _verify_rsa_parameters(public_exponent, key_size):
    if public_exponent < 3:
        raise ValueError('public_exponent must be >= 3.')
    else:
        if public_exponent & 1 == 0:
            raise ValueError('public_exponent must be odd.')
        if key_size < 512:
            raise ValueError('key_size must be at least 512-bits.')


def _check_private_key_components(p, q, private_exponent, dmp1, dmq1, iqmp, public_exponent, modulus):
    if modulus < 3:
        raise ValueError('modulus must be >= 3.')
    else:
        if p >= modulus:
            raise ValueError('p must be < modulus.')
        else:
            if q >= modulus:
                raise ValueError('q must be < modulus.')
            else:
                if dmp1 >= modulus:
                    raise ValueError('dmp1 must be < modulus.')
                else:
                    if dmq1 >= modulus:
                        raise ValueError('dmq1 must be < modulus.')
                    else:
                        if iqmp >= modulus:
                            raise ValueError('iqmp must be < modulus.')
                        if private_exponent >= modulus:
                            raise ValueError('private_exponent must be < modulus.')
                        if public_exponent < 3 or public_exponent >= modulus:
                            raise ValueError('public_exponent must be >= 3 and < modulus.')
                    if public_exponent & 1 == 0:
                        raise ValueError('public_exponent must be odd.')
                if dmp1 & 1 == 0:
                    raise ValueError('dmp1 must be odd.')
            if dmq1 & 1 == 0:
                raise ValueError('dmq1 must be odd.')
        if p * q != modulus:
            raise ValueError('p*q must equal modulus.')


def _check_public_key_components(e, n):
    if n < 3:
        raise ValueError('n must be >= 3.')
    else:
        if e < 3 or e >= n:
            raise ValueError('e must be >= 3 and < n.')
        if e & 1 == 0:
            raise ValueError('e must be odd.')


def _modinv(e, m):
    """
    Modular Multiplicative Inverse. Returns x such that: (x*e) mod m == 1
    """
    x1, y1, x2, y2 = (1, 0, 0, 1)
    a, b = e, m
    while b > 0:
        q, r = divmod(a, b)
        xn, yn = x1 - q * x2, y1 - q * y2
        a, b, x1, y1, x2, y2 = (b, r, x2, y2, xn, yn)

    return x1 % m


def rsa_crt_iqmp(p, q):
    """
    Compute the CRT (q ** -1) % p value from RSA primes p and q.
    """
    return _modinv(q, p)


def rsa_crt_dmp1(private_exponent, p):
    """
    Compute the CRT private_exponent % (p - 1) value from the RSA
    private_exponent (d) and p.
    """
    return private_exponent % (p - 1)


def rsa_crt_dmq1(private_exponent, q):
    """
    Compute the CRT private_exponent % (q - 1) value from the RSA
    private_exponent (d) and q.
    """
    return private_exponent % (q - 1)


_MAX_RECOVERY_ATTEMPTS = 1000

def rsa_recover_prime_factors(n, e, d):
    """
    Compute factors p and q from the private exponent d. We assume that n has
    no more than two factors. This function is adapted from code in PyCrypto.
    """
    ktot = d * e - 1
    t = ktot
    while t % 2 == 0:
        t = t // 2

    spotted = False
    a = 2
    while not spotted and a < _MAX_RECOVERY_ATTEMPTS:
        k = t
        while k < ktot:
            cand = pow(a, k, n)
            if cand != 1:
                if cand != n - 1:
                    if pow(cand, 2, n) == 1:
                        p = gcd(cand + 1, n)
                        spotted = True
                        break
            k *= 2

        a += 2

    if not spotted:
        raise ValueError('Unable to compute factors p and q from exponent d.')
    else:
        q, r = divmod(n, p)
        assert r == 0
    p, q = sorted((p, q), reverse=True)
    return (p, q)


class RSAPrivateNumbers(object):

    def __init__(self, p, q, d, dmp1, dmq1, iqmp, public_numbers):
        if not isinstance(p, six.integer_types) or not isinstance(q, six.integer_types) or not isinstance(d, six.integer_types) or not isinstance(dmp1, six.integer_types) or not isinstance(dmq1, six.integer_types) or not isinstance(iqmp, six.integer_types):
            raise TypeError('RSAPrivateNumbers p, q, d, dmp1, dmq1, iqmp arguments must all be an integers.')
        if not isinstance(public_numbers, RSAPublicNumbers):
            raise TypeError('RSAPrivateNumbers public_numbers must be an RSAPublicNumbers instance.')
        self._p = p
        self._q = q
        self._d = d
        self._dmp1 = dmp1
        self._dmq1 = dmq1
        self._iqmp = iqmp
        self._public_numbers = public_numbers

    p = utils.read_only_property('_p')
    q = utils.read_only_property('_q')
    d = utils.read_only_property('_d')
    dmp1 = utils.read_only_property('_dmp1')
    dmq1 = utils.read_only_property('_dmq1')
    iqmp = utils.read_only_property('_iqmp')
    public_numbers = utils.read_only_property('_public_numbers')

    def private_key(self, backend):
        return backend.load_rsa_private_numbers(self)

    def __eq__(self, other):
        if not isinstance(other, RSAPrivateNumbers):
            return NotImplemented
        else:
            return self.p == other.p and self.q == other.q and self.d == other.d and self.dmp1 == other.dmp1 and self.dmq1 == other.dmq1 and self.iqmp == other.iqmp and self.public_numbers == other.public_numbers

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((
         self.p,
         self.q,
         self.d,
         self.dmp1,
         self.dmq1,
         self.iqmp,
         self.public_numbers))


class RSAPublicNumbers(object):

    def __init__(self, e, n):
        if not isinstance(e, six.integer_types) or not isinstance(n, six.integer_types):
            raise TypeError('RSAPublicNumbers arguments must be integers.')
        self._e = e
        self._n = n

    e = utils.read_only_property('_e')
    n = utils.read_only_property('_n')

    def public_key(self, backend):
        return backend.load_rsa_public_numbers(self)

    def __repr__(self):
        return '<RSAPublicNumbers(e={0.e}, n={0.n})>'.format(self)

    def __eq__(self, other):
        if not isinstance(other, RSAPublicNumbers):
            return NotImplemented
        else:
            return self.e == other.e and self.n == other.n

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.e, self.n))