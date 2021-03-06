# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\primitives\ciphers\modes.py
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography import utils

@six.add_metaclass(abc.ABCMeta)
class Mode(object):

    @abc.abstractproperty
    def name(self):
        """
        A string naming this mode (e.g. "ECB", "CBC").
        """
        pass

    @abc.abstractmethod
    def validate_for_algorithm(self, algorithm):
        """
        Checks that all the necessary invariants of this (mode, algorithm)
        combination are met.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class ModeWithInitializationVector(object):

    @abc.abstractproperty
    def initialization_vector(self):
        """
        The value of the initialization vector for this mode as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class ModeWithTweak(object):

    @abc.abstractproperty
    def tweak(self):
        """
        The value of the tweak for this mode as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class ModeWithNonce(object):

    @abc.abstractproperty
    def nonce(self):
        """
        The value of the nonce for this mode as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class ModeWithAuthenticationTag(object):

    @abc.abstractproperty
    def tag(self):
        """
        The value of the tag supplied to the constructor of this mode.
        """
        pass


def _check_aes_key_length(self, algorithm):
    if algorithm.key_size > 256:
        if algorithm.name == 'AES':
            raise ValueError('Only 128, 192, and 256 bit keys are allowed for this AES mode')


def _check_iv_length(self, algorithm):
    if len(self.initialization_vector) * 8 != algorithm.block_size:
        raise ValueError('Invalid IV size ({0}) for {1}.'.format(len(self.initialization_vector), self.name))


def _check_iv_and_key_length(self, algorithm):
    _check_aes_key_length(self, algorithm)
    _check_iv_length(self, algorithm)


@utils.register_interface(Mode)
@utils.register_interface(ModeWithInitializationVector)
class CBC(object):
    name = 'CBC'

    def __init__(self, initialization_vector):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    initialization_vector = utils.read_only_property('_initialization_vector')
    validate_for_algorithm = _check_iv_and_key_length


@utils.register_interface(Mode)
@utils.register_interface(ModeWithTweak)
class XTS(object):
    name = 'XTS'

    def __init__(self, tweak):
        utils._check_byteslike('tweak', tweak)
        if len(tweak) != 16:
            raise ValueError('tweak must be 128-bits (16 bytes)')
        self._tweak = tweak

    tweak = utils.read_only_property('_tweak')

    def validate_for_algorithm(self, algorithm):
        if algorithm.key_size not in (256, 512):
            raise ValueError('The XTS specification requires a 256-bit key for AES-128-XTS and 512-bit key for AES-256-XTS')


@utils.register_interface(Mode)
class ECB(object):
    name = 'ECB'
    validate_for_algorithm = _check_aes_key_length


@utils.register_interface(Mode)
@utils.register_interface(ModeWithInitializationVector)
class OFB(object):
    name = 'OFB'

    def __init__(self, initialization_vector):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    initialization_vector = utils.read_only_property('_initialization_vector')
    validate_for_algorithm = _check_iv_and_key_length


@utils.register_interface(Mode)
@utils.register_interface(ModeWithInitializationVector)
class CFB(object):
    name = 'CFB'

    def __init__(self, initialization_vector):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    initialization_vector = utils.read_only_property('_initialization_vector')
    validate_for_algorithm = _check_iv_and_key_length


@utils.register_interface(Mode)
@utils.register_interface(ModeWithInitializationVector)
class CFB8(object):
    name = 'CFB8'

    def __init__(self, initialization_vector):
        utils._check_byteslike('initialization_vector', initialization_vector)
        self._initialization_vector = initialization_vector

    initialization_vector = utils.read_only_property('_initialization_vector')
    validate_for_algorithm = _check_iv_and_key_length


@utils.register_interface(Mode)
@utils.register_interface(ModeWithNonce)
class CTR(object):
    name = 'CTR'

    def __init__(self, nonce):
        utils._check_byteslike('nonce', nonce)
        self._nonce = nonce

    nonce = utils.read_only_property('_nonce')

    def validate_for_algorithm(self, algorithm):
        _check_aes_key_length(self, algorithm)
        if len(self.nonce) * 8 != algorithm.block_size:
            raise ValueError('Invalid nonce size ({0}) for {1}.'.format(len(self.nonce), self.name))


@utils.register_interface(Mode)
@utils.register_interface(ModeWithInitializationVector)
@utils.register_interface(ModeWithAuthenticationTag)
class GCM(object):
    name = 'GCM'
    _MAX_ENCRYPTED_BYTES = 68719476704
    _MAX_AAD_BYTES = 2305843009213693952

    def __init__(self, initialization_vector, tag=None, min_tag_length=16):
        utils._check_byteslike('initialization_vector', initialization_vector)
        if len(initialization_vector) == 0:
            raise ValueError('initialization_vector must be at least 1 byte')
        self._initialization_vector = initialization_vector
        if tag is not None:
            utils._check_bytes('tag', tag)
            if min_tag_length < 4:
                raise ValueError('min_tag_length must be >= 4')
            if len(tag) < min_tag_length:
                raise ValueError('Authentication tag must be {0} bytes or longer.'.format(min_tag_length))
        self._tag = tag
        self._min_tag_length = min_tag_length

    tag = utils.read_only_property('_tag')
    initialization_vector = utils.read_only_property('_initialization_vector')

    def validate_for_algorithm(self, algorithm):
        _check_aes_key_length(self, algorithm)