# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\primitives\asymmetric\utils.py
from __future__ import absolute_import, division, print_function
import warnings
from asn1crypto.algos import DSASignature
import six
from cryptography import utils
from cryptography.hazmat.primitives import hashes

def decode_rfc6979_signature(signature):
    warnings.warn('decode_rfc6979_signature is deprecated and will be removed in a future version, use decode_dss_signature instead.',
      (utils.PersistentlyDeprecated),
      stacklevel=2)
    return decode_dss_signature(signature)


def decode_dss_signature(signature):
    data = DSASignature.load(signature, strict=True).native
    return (data['r'], data['s'])


def encode_rfc6979_signature(r, s):
    warnings.warn('encode_rfc6979_signature is deprecated and will be removed in a future version, use encode_dss_signature instead.',
      (utils.PersistentlyDeprecated),
      stacklevel=2)
    return encode_dss_signature(r, s)


def encode_dss_signature(r, s):
    if not isinstance(r, six.integer_types) or not isinstance(s, six.integer_types):
        raise ValueError('Both r and s must be integers')
    return DSASignature({'r':r,  's':s}).dump()


class Prehashed(object):

    def __init__(self, algorithm):
        if not isinstance(algorithm, hashes.HashAlgorithm):
            raise TypeError('Expected instance of HashAlgorithm.')
        self._algorithm = algorithm
        self._digest_size = algorithm.digest_size

    digest_size = utils.read_only_property('_digest_size')