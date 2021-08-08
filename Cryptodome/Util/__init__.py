# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Util\__init__.py
"""Miscellaneous modules

Contains useful modules that don't belong into any of the
other Cryptodome.* subpackages.

========================    =============================================
Module                      Description
========================    =============================================
`Cryptodome.Util.number`        Number-theoretic functions (primality testing, etc.)
`Cryptodome.Util.Counter`       Fast counter functions for CTR cipher modes.
`Cryptodome.Util.RFC1751`       Converts between 128-bit keys and human-readable
                            strings of words.
`Cryptodome.Util.asn1`          Minimal support for ASN.1 DER encoding
`Cryptodome.Util.Padding`       Set of functions for adding and removing padding.
========================    =============================================

:undocumented: _galois, _number_new, cpuid, py3compat, _raw_api
"""
__all__ = [
 'RFC1751', 'number', 'strxor', 'asn1', 'Counter', 'Padding']