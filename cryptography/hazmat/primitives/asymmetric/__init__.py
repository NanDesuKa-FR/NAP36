# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\primitives\asymmetric\__init__.py
from __future__ import absolute_import, division, print_function
import abc, six

@six.add_metaclass(abc.ABCMeta)
class AsymmetricSignatureContext(object):

    @abc.abstractmethod
    def update(self, data):
        """
        Processes the provided bytes and returns nothing.
        """
        pass

    @abc.abstractmethod
    def finalize(self):
        """
        Returns the signature as bytes.
        """
        pass


@six.add_metaclass(abc.ABCMeta)
class AsymmetricVerificationContext(object):

    @abc.abstractmethod
    def update(self, data):
        """
        Processes the provided bytes and returns nothing.
        """
        pass

    @abc.abstractmethod
    def verify(self):
        """
        Raises an exception if the bytes provided to update do not match the
        signature or the signature does not match the public key.
        """
        pass