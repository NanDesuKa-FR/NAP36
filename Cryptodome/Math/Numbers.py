# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Math\Numbers.py
__all__ = [
 'Integer']
try:
    from Cryptodome.Math._IntegerGMP import IntegerGMP as Integer
    from Cryptodome.Math._IntegerGMP import implementation as _implementation
except (ImportError, OSError, AttributeError):
    try:
        from Cryptodome.Math._IntegerCustom import IntegerCustom as Integer
        from Cryptodome.Math._IntegerCustom import implementation as _implementation
    except (ImportError, OSError):
        from Cryptodome.Math._IntegerNative import IntegerNative as Integer
        _implementation = {}