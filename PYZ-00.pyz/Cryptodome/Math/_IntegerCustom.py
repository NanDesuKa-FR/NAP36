# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Math\_IntegerCustom.py
from ._IntegerNative import IntegerNative
from Cryptodome.Util.number import long_to_bytes, bytes_to_long
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib, create_string_buffer, get_raw_buffer, backend, c_size_t, c_ulonglong
from Cryptodome.Random.random import getrandbits
c_defs = '\nint monty_pow(const uint8_t *base,\n               const uint8_t *exp,\n               const uint8_t *modulus,\n               uint8_t       *out,\n               size_t len,\n               uint64_t seed);\n'
_raw_montgomery = load_pycryptodome_raw_lib('Cryptodome.Math._montgomery', c_defs)
implementation = {'library':'custom',  'api':backend}

class IntegerCustom(IntegerNative):

    @staticmethod
    def from_bytes(byte_string):
        return IntegerCustom(bytes_to_long(byte_string))

    def inplace_pow(self, exponent, modulus=None):
        exp_value = int(exponent)
        if exp_value < 0:
            raise ValueError('Exponent must not be negative')
        if modulus is None:
            self._value = pow(self._value, exp_value)
            return self
        mod_value = int(modulus)
        if mod_value < 0:
            raise ValueError('Modulus must be positive')
        if mod_value == 0:
            raise ZeroDivisionError('Modulus cannot be zero')
        if mod_value & 1 == 0:
            self._value = pow(self._value, exp_value, mod_value)
            return self
        else:
            max_len = len(long_to_bytes(max(self._value, exp_value, mod_value)))
            base_b = long_to_bytes(self._value, max_len)
            exp_b = long_to_bytes(exp_value, max_len)
            modulus_b = long_to_bytes(mod_value, max_len)
            out = create_string_buffer(max_len)
            error = _raw_montgomery.monty_pow(base_b, exp_b, modulus_b, out, c_size_t(max_len), c_ulonglong(getrandbits(64)))
            if error:
                raise ValueError('monty_pow failed with error: %d' % error)
            result = bytes_to_long(get_raw_buffer(out))
            self._value = result
            return self