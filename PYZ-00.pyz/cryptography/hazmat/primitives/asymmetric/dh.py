# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\primitives\asymmetric\dh.py
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography import utils

def generate_parameters(generator, key_size, backend):
    return backend.generate_dh_parameters(generator, key_size)


class DHPrivateNumbers(object):

    def __init__(self, x, public_numbers):
        if not isinstance(x, six.integer_types):
            raise TypeError('x must be an integer.')
        if not isinstance(public_numbers, DHPublicNumbers):
            raise TypeError('public_numbers must be an instance of DHPublicNumbers.')
        self._x = x
        self._public_numbers = public_numbers

    def __eq__(self, other):
        if not isinstance(other, DHPrivateNumbers):
            return NotImplemented
        else:
            return self._x == other._x and self._public_numbers == other._public_numbers

    def __ne__(self, other):
        return not self == other

    def private_key(self, backend):
        return backend.load_dh_private_numbers(self)

    public_numbers = utils.read_only_property('_public_numbers')
    x = utils.read_only_property('_x')


class DHPublicNumbers(object):

    def __init__(self, y, parameter_numbers):
        if not isinstance(y, six.integer_types):
            raise TypeError('y must be an integer.')
        if not isinstance(parameter_numbers, DHParameterNumbers):
            raise TypeError('parameters must be an instance of DHParameterNumbers.')
        self._y = y
        self._parameter_numbers = parameter_numbers

    def __eq__(self, other):
        if not isinstance(other, DHPublicNumbers):
            return NotImplemented
        else:
            return self._y == other._y and self._parameter_numbers == other._parameter_numbers

    def __ne__(self, other):
        return not self == other

    def public_key(self, backend):
        return backend.load_dh_public_numbers(self)

    y = utils.read_only_property('_y')
    parameter_numbers = utils.read_only_property('_parameter_numbers')


class DHParameterNumbers(object):

    def __init__(self, p, g, q=None):
        if not isinstance(p, six.integer_types) or not isinstance(g, six.integer_types):
            raise TypeError('p and g must be integers')
        else:
            if q is not None:
                if not isinstance(q, six.integer_types):
                    raise TypeError('q must be integer or None')
            if g < 2:
                raise ValueError('DH generator must be 2 or greater')
        self._p = p
        self._g = g
        self._q = q

    def __eq__(self, other):
        if not isinstance(other, DHParameterNumbers):
            return NotImplemented
        else:
            return self._p == other._p and self._g == other._g and self._q == other._q

    def __ne__(self, other):
        return not self == other

    def parameters(self, backend):
        return backend.load_dh_parameter_numbers(self)

    p = utils.read_only_property('_p')
    g = utils.read_only_property('_g')
    q = utils.read_only_property('_q')


@six.add_metaclass(abc.ABCMeta)
class DHParameters(object):

    @abc.abstractmethod
    def generate_private_key(self):
        """
        Generates and returns a DHPrivateKey.
        """
        pass

    @abc.abstractmethod
    def parameter_bytes(self, encoding, format):
        """
        Returns the parameters serialized as bytes.
        """
        pass

    @abc.abstractmethod
    def parameter_numbers(self):
        """
        Returns a DHParameterNumbers.
        """
        pass


DHParametersWithSerialization = DHParameters

@six.add_metaclass(abc.ABCMeta)
class DHPrivateKey(object):

    @abc.abstractproperty
    def key_size(self):
        """
        The bit length of the prime modulus.
        """
        pass

    @abc.abstractmethod
    def public_key(self):
        """
        The DHPublicKey associated with this private key.
        """
        pass

    @abc.abstractmethod
    def parameters(self):
        """
        The DHParameters object associated with this private key.
        """
        pass

    @abc.abstractmethod
    def exchange(self, peer_public_key):
        """
        Given peer's DHPublicKey, carry out the key exchange and
        return shared key as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class DHPrivateKeyWithSerialization(DHPrivateKey):

    @abc.abstractmethod
    def private_numbers(self):
        """
        Returns a DHPrivateNumbers.
        """
        pass

    @abc.abstractmethod
    def private_bytes(self, encoding, format, encryption_algorithm):
        """
        Returns the key serialized as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class DHPublicKey(object):

    @abc.abstractproperty
    def key_size(self):
        """
        The bit length of the prime modulus.
        """
        pass

    @abc.abstractmethod
    def parameters(self):
        """
        The DHParameters object associated with this public key.
        """
        pass

    @abc.abstractmethod
    def public_numbers(self):
        """
        Returns a DHPublicNumbers.
        """
        pass

    @abc.abstractmethod
    def public_bytes(self, encoding, format):
        """
        Returns the key serialized as bytes.
        """
        pass


DHPublicKeyWithSerialization = DHPublicKey