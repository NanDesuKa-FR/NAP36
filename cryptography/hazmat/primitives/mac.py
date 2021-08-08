# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\hazmat\primitives\mac.py
from __future__ import absolute_import, division, print_function
import abc, six

@six.add_metaclass(abc.ABCMeta)
class MACContext(object):

    @abc.abstractmethod
    def update(self, data):
        """
        Processes the provided bytes.
        """
        pass

    @abc.abstractmethod
    def finalize(self):
        """
        Returns the message authentication code as bytes.
        """
        pass

    @abc.abstractmethod
    def copy(self):
        """
        Return a MACContext that is a copy of the current context.
        """
        pass

    @abc.abstractmethod
    def verify(self, signature):
        """
        Checks if the generated message authentication code matches the
        signature.
        """
        pass