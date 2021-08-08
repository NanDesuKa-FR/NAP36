# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cryptography\x509\certificate_transparency.py
from __future__ import absolute_import, division, print_function
import abc
from enum import Enum
import six

class LogEntryType(Enum):
    X509_CERTIFICATE = 0
    PRE_CERTIFICATE = 1


class Version(Enum):
    v1 = 0


@six.add_metaclass(abc.ABCMeta)
class SignedCertificateTimestamp(object):

    @abc.abstractproperty
    def version(self):
        """
        Returns the SCT version.
        """
        pass

    @abc.abstractproperty
    def log_id(self):
        """
        Returns an identifier indicating which log this SCT is for.
        """
        pass

    @abc.abstractproperty
    def timestamp(self):
        """
        Returns the timestamp for this SCT.
        """
        pass

    @abc.abstractproperty
    def entry_type(self):
        """
        Returns whether this is an SCT for a certificate or pre-certificate.
        """
        pass