# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Math\_IntegerGMP.py
import sys
from Cryptodome.Util.py3compat import tobytes, is_native_int
from Cryptodome.Util._raw_api import backend, load_lib, get_raw_buffer, get_c_string, null_pointer, create_string_buffer, c_ulong, c_size_t
from ._IntegerBase import IntegerBase
gmp_defs = 'typedef unsigned long UNIX_ULONG;\n        typedef struct { int a; int b; void *c; } MPZ;\n        typedef MPZ mpz_t[1];\n        typedef UNIX_ULONG mp_bitcnt_t;\n        void __gmpz_init (mpz_t x);\n        void __gmpz_init_set (mpz_t rop, const mpz_t op);\n        void __gmpz_init_set_ui (mpz_t rop, UNIX_ULONG op);\n        int __gmp_sscanf (const char *s, const char *fmt, ...);\n        void __gmpz_set (mpz_t rop, const mpz_t op);\n        int __gmp_snprintf (uint8_t *buf, size_t size, const char *fmt, ...);\n        void __gmpz_add (mpz_t rop, const mpz_t op1, const mpz_t op2);\n        void __gmpz_add_ui (mpz_t rop, const mpz_t op1, UNIX_ULONG op2);\n        void __gmpz_sub_ui (mpz_t rop, const mpz_t op1, UNIX_ULONG op2);\n        void __gmpz_addmul (mpz_t rop, const mpz_t op1, const mpz_t op2);\n        void __gmpz_addmul_ui (mpz_t rop, const mpz_t op1, UNIX_ULONG op2);\n        void __gmpz_submul_ui (mpz_t rop, const mpz_t op1, UNIX_ULONG op2);\n        void __gmpz_import (mpz_t rop, size_t count, int order, size_t size,\n                            int endian, size_t nails, const void *op);\n        void * __gmpz_export (void *rop, size_t *countp, int order,\n                              size_t size,\n                              int endian, size_t nails, const mpz_t op);\n        size_t __gmpz_sizeinbase (const mpz_t op, int base);\n        void __gmpz_sub (mpz_t rop, const mpz_t op1, const mpz_t op2);\n        void __gmpz_mul (mpz_t rop, const mpz_t op1, const mpz_t op2);\n        void __gmpz_mul_ui (mpz_t rop, const mpz_t op1, UNIX_ULONG op2);\n        int __gmpz_cmp (const mpz_t op1, const mpz_t op2);\n        void __gmpz_powm (mpz_t rop, const mpz_t base, const mpz_t exp, const\n                          mpz_t mod);\n        void __gmpz_powm_ui (mpz_t rop, const mpz_t base, UNIX_ULONG exp,\n                             const mpz_t mod);\n        void __gmpz_pow_ui (mpz_t rop, const mpz_t base, UNIX_ULONG exp);\n        void __gmpz_sqrt(mpz_t rop, const mpz_t op);\n        void __gmpz_mod (mpz_t r, const mpz_t n, const mpz_t d);\n        void __gmpz_neg (mpz_t rop, const mpz_t op);\n        void __gmpz_abs (mpz_t rop, const mpz_t op);\n        void __gmpz_and (mpz_t rop, const mpz_t op1, const mpz_t op2);\n        void __gmpz_ior (mpz_t rop, const mpz_t op1, const mpz_t op2);\n        void __gmpz_clear (mpz_t x);\n        void __gmpz_tdiv_q_2exp (mpz_t q, const mpz_t n, mp_bitcnt_t b);\n        void __gmpz_fdiv_q (mpz_t q, const mpz_t n, const mpz_t d);\n        void __gmpz_mul_2exp (mpz_t rop, const mpz_t op1, mp_bitcnt_t op2);\n        int __gmpz_tstbit (const mpz_t op, mp_bitcnt_t bit_index);\n        int __gmpz_perfect_square_p (const mpz_t op);\n        int __gmpz_jacobi (const mpz_t a, const mpz_t b);\n        void __gmpz_gcd (mpz_t rop, const mpz_t op1, const mpz_t op2);\n        UNIX_ULONG __gmpz_gcd_ui (mpz_t rop, const mpz_t op1,\n                                     UNIX_ULONG op2);\n        void __gmpz_lcm (mpz_t rop, const mpz_t op1, const mpz_t op2);\n        int __gmpz_invert (mpz_t rop, const mpz_t op1, const mpz_t op2);\n        int __gmpz_divisible_p (const mpz_t n, const mpz_t d);\n        int __gmpz_divisible_ui_p (const mpz_t n, UNIX_ULONG d);\n        '
lib = load_lib('gmp', gmp_defs)
implementation = {'library':'gmp',  'api':backend}
if hasattr(lib, '__mpir_version'):
    raise ImportError('MPIR library detected')
else:
    if sys.platform == 'win32':
        raise ImportError('Not using GMP on Windows')
    if implementation['api'] == 'ctypes':
        from ctypes import Structure, c_int, c_void_p, byref

        class _MPZ(Structure):
            _fields_ = [
             (
              '_mp_alloc', c_int),
             (
              '_mp_size', c_int),
             (
              '_mp_d', c_void_p)]


        def new_mpz():
            return byref(_MPZ())


    else:
        from Cryptodome.Util._raw_api import ffi

    def new_mpz():
        return ffi.new('MPZ*')


class _GMP(object):

    def __getattr__(self, name):
        if name.startswith('mpz_'):
            func_name = '__gmpz_' + name[4:]
        else:
            if name.startswith('gmp_'):
                func_name = '__gmp_' + name[4:]
            else:
                raise AttributeError('Attribute %s is invalid' % name)
        func = getattr(lib, func_name)
        setattr(self, name, func)
        return func


_gmp = _GMP()

class IntegerGMP(IntegerBase):
    __doc__ = 'A fast, arbitrary precision integer'
    _zero_mpz_p = new_mpz()
    _gmp.mpz_init_set_ui(_zero_mpz_p, c_ulong(0))

    def __init__(self, value):
        """Initialize the integer to the given value."""
        self._mpz_p = new_mpz()
        self._initialized = False
        if isinstance(value, float):
            raise ValueError('A floating point type is not a natural number')
        else:
            self._initialized = True
            if is_native_int(value):
                _gmp.mpz_init(self._mpz_p)
                result = _gmp.gmp_sscanf(tobytes(str(value)), b'%Zd', self._mpz_p)
                if result != 1:
                    raise ValueError("Error converting '%d'" % value)
            else:
                _gmp.mpz_init_set(self._mpz_p, value._mpz_p)

    def __int__(self):
        buf_len = _gmp.mpz_sizeinbase(self._mpz_p, 2) // 3 + 3
        buf = create_string_buffer(buf_len)
        _gmp.gmp_snprintf(buf, c_size_t(buf_len), b'%Zd', self._mpz_p)
        return int(get_c_string(buf))

    def __str__(self):
        return str(int(self))

    def __repr__(self):
        return 'Integer(%s)' % str(self)

    def to_bytes(self, block_size=0):
        """Convert the number into a byte string.

        This method encodes the number in network order and prepends
        as many zero bytes as required. It only works for non-negative
        values.

        :Parameters:
          block_size : integer
            The exact size the output byte string must have.
            If zero, the string has the minimal length.
        :Returns:
          A byte string.
        :Raise ValueError:
          If the value is negative or if ``block_size`` is
          provided and the length of the byte string would exceed it.
        """
        if self < 0:
            raise ValueError('Conversion only valid for non-negative numbers')
        buf_len = (_gmp.mpz_sizeinbase(self._mpz_p, 2) + 7) // 8
        if buf_len > block_size > 0:
            raise ValueError('Number is too big to convert to byte stringof prescribed length')
        buf = create_string_buffer(buf_len)
        _gmp.mpz_export(buf, null_pointer, 1, c_size_t(1), 0, c_size_t(0), self._mpz_p)
        return b'\x00' * max(0, block_size - buf_len) + get_raw_buffer(buf)

    @staticmethod
    def from_bytes(byte_string):
        """Convert a byte string into a number.

        :Parameters:
          byte_string : byte string
            The input number, encoded in network order.
            It can only be non-negative.
        :Return:
          The ``Integer`` object carrying the same value as the input.
        """
        result = IntegerGMP(0)
        _gmp.mpz_import(result._mpz_p, c_size_t(len(byte_string)), 1, c_size_t(1), 0, c_size_t(0), byte_string)
        return result

    def _apply_and_return(self, func, term):
        if not isinstance(term, IntegerGMP):
            term = IntegerGMP(term)
        return func(self._mpz_p, term._mpz_p)

    def __eq__(self, term):
        if not (isinstance(term, IntegerGMP) or is_native_int(term)):
            return False
        else:
            return self._apply_and_return(_gmp.mpz_cmp, term) == 0

    def __ne__(self, term):
        if not (isinstance(term, IntegerGMP) or is_native_int(term)):
            return True
        else:
            return self._apply_and_return(_gmp.mpz_cmp, term) != 0

    def __lt__(self, term):
        return self._apply_and_return(_gmp.mpz_cmp, term) < 0

    def __le__(self, term):
        return self._apply_and_return(_gmp.mpz_cmp, term) <= 0

    def __gt__(self, term):
        return self._apply_and_return(_gmp.mpz_cmp, term) > 0

    def __ge__(self, term):
        return self._apply_and_return(_gmp.mpz_cmp, term) >= 0

    def __nonzero__(self):
        return _gmp.mpz_cmp(self._mpz_p, self._zero_mpz_p) != 0

    __bool__ = __nonzero__

    def is_negative(self):
        return _gmp.mpz_cmp(self._mpz_p, self._zero_mpz_p) < 0

    def __add__(self, term):
        result = IntegerGMP(0)
        if not isinstance(term, IntegerGMP):
            term = IntegerGMP(term)
        _gmp.mpz_add(result._mpz_p, self._mpz_p, term._mpz_p)
        return result

    def __sub__(self, term):
        result = IntegerGMP(0)
        if not isinstance(term, IntegerGMP):
            term = IntegerGMP(term)
        _gmp.mpz_sub(result._mpz_p, self._mpz_p, term._mpz_p)
        return result

    def __mul__(self, term):
        result = IntegerGMP(0)
        if not isinstance(term, IntegerGMP):
            term = IntegerGMP(term)
        _gmp.mpz_mul(result._mpz_p, self._mpz_p, term._mpz_p)
        return result

    def __floordiv__(self, divisor):
        if not isinstance(divisor, IntegerGMP):
            divisor = IntegerGMP(divisor)
        if _gmp.mpz_cmp(divisor._mpz_p, self._zero_mpz_p) == 0:
            raise ZeroDivisionError('Division by zero')
        result = IntegerGMP(0)
        _gmp.mpz_fdiv_q(result._mpz_p, self._mpz_p, divisor._mpz_p)
        return result

    def __mod__(self, divisor):
        if not isinstance(divisor, IntegerGMP):
            divisor = IntegerGMP(divisor)
        else:
            comp = _gmp.mpz_cmp(divisor._mpz_p, self._zero_mpz_p)
            if comp == 0:
                raise ZeroDivisionError('Division by zero')
            if comp < 0:
                raise ValueError('Modulus must be positive')
        result = IntegerGMP(0)
        _gmp.mpz_mod(result._mpz_p, self._mpz_p, divisor._mpz_p)
        return result

    def inplace_pow(self, exponent, modulus=None):
        if modulus is None:
            if exponent < 0:
                raise ValueError('Exponent must not be negative')
            if exponent > 256:
                raise ValueError('Exponent is too big')
            _gmp.mpz_pow_ui(self._mpz_p, self._mpz_p, c_ulong(int(exponent)))
        elif not isinstance(modulus, IntegerGMP):
            modulus = IntegerGMP(modulus)
        else:
            if not modulus:
                raise ZeroDivisionError('Division by zero')
            if modulus.is_negative():
                raise ValueError('Modulus must be positive')
        if is_native_int(exponent):
            if exponent < 0:
                raise ValueError('Exponent must not be negative')
            if exponent < 65536:
                _gmp.mpz_powm_ui(self._mpz_p, self._mpz_p, c_ulong(exponent), modulus._mpz_p)
                return self
            exponent = IntegerGMP(exponent)
        else:
            if exponent.is_negative():
                raise ValueError('Exponent must not be negative')
            _gmp.mpz_powm(self._mpz_p, self._mpz_p, exponent._mpz_p, modulus._mpz_p)
        return self

    def __pow__(self, exponent, modulus=None):
        result = IntegerGMP(self)
        return result.inplace_pow(exponent, modulus)

    def __abs__(self):
        result = IntegerGMP(0)
        _gmp.mpz_abs(result._mpz_p, self._mpz_p)
        return result

    def sqrt(self, modulus=None):
        """Return the largest Integer that does not
        exceed the square root"""
        if modulus is None:
            if self < 0:
                raise ValueError('Square root of negative value')
            result = IntegerGMP(0)
            _gmp.mpz_sqrt(result._mpz_p, self._mpz_p)
        else:
            if modulus <= 0:
                raise ValueError('Modulus must be positive')
            modulus = int(modulus)
            result = IntegerGMP(self._tonelli_shanks(int(self) % modulus, modulus))
        return result

    def __iadd__(self, term):
        if is_native_int(term):
            if 0 <= term < 65536:
                _gmp.mpz_add_ui(self._mpz_p, self._mpz_p, c_ulong(term))
                return self
            if -65535 < term < 0:
                _gmp.mpz_sub_ui(self._mpz_p, self._mpz_p, c_ulong(-term))
                return self
            term = IntegerGMP(term)
        _gmp.mpz_add(self._mpz_p, self._mpz_p, term._mpz_p)
        return self

    def __isub__(self, term):
        if is_native_int(term):
            if 0 <= term < 65536:
                _gmp.mpz_sub_ui(self._mpz_p, self._mpz_p, c_ulong(term))
                return self
            if -65535 < term < 0:
                _gmp.mpz_add_ui(self._mpz_p, self._mpz_p, c_ulong(-term))
                return self
            term = IntegerGMP(term)
        _gmp.mpz_sub(self._mpz_p, self._mpz_p, term._mpz_p)
        return self

    def __imul__(self, term):
        if is_native_int(term):
            if 0 <= term < 65536:
                _gmp.mpz_mul_ui(self._mpz_p, self._mpz_p, c_ulong(term))
                return self
            if -65535 < term < 0:
                _gmp.mpz_mul_ui(self._mpz_p, self._mpz_p, c_ulong(-term))
                _gmp.mpz_neg(self._mpz_p, self._mpz_p)
                return self
            term = IntegerGMP(term)
        _gmp.mpz_mul(self._mpz_p, self._mpz_p, term._mpz_p)
        return self

    def __imod__(self, divisor):
        if not isinstance(divisor, IntegerGMP):
            divisor = IntegerGMP(divisor)
        else:
            comp = _gmp.mpz_cmp(divisor._mpz_p, divisor._zero_mpz_p)
            if comp == 0:
                raise ZeroDivisionError('Division by zero')
            if comp < 0:
                raise ValueError('Modulus must be positive')
        _gmp.mpz_mod(self._mpz_p, self._mpz_p, divisor._mpz_p)
        return self

    def __and__(self, term):
        result = IntegerGMP(0)
        if not isinstance(term, IntegerGMP):
            term = IntegerGMP(term)
        _gmp.mpz_and(result._mpz_p, self._mpz_p, term._mpz_p)
        return result

    def __or__(self, term):
        result = IntegerGMP(0)
        if not isinstance(term, IntegerGMP):
            term = IntegerGMP(term)
        _gmp.mpz_ior(result._mpz_p, self._mpz_p, term._mpz_p)
        return result

    def __rshift__(self, pos):
        result = IntegerGMP(0)
        if pos < 0:
            raise ValueError('negative shift count')
        if pos > 65536:
            if self < 0:
                return -1
            return 0
        else:
            _gmp.mpz_tdiv_q_2exp(result._mpz_p, self._mpz_p, c_ulong(int(pos)))
            return result

    def __irshift__(self, pos):
        if pos < 0:
            raise ValueError('negative shift count')
        if pos > 65536:
            if self < 0:
                return -1
            return 0
        else:
            _gmp.mpz_tdiv_q_2exp(self._mpz_p, self._mpz_p, c_ulong(int(pos)))
            return self

    def __lshift__(self, pos):
        result = IntegerGMP(0)
        if not 0 <= pos < 65536:
            raise ValueError('Incorrect shift count')
        _gmp.mpz_mul_2exp(result._mpz_p, self._mpz_p, c_ulong(int(pos)))
        return result

    def __ilshift__(self, pos):
        if not 0 <= pos < 65536:
            raise ValueError('Incorrect shift count')
        _gmp.mpz_mul_2exp(self._mpz_p, self._mpz_p, c_ulong(int(pos)))
        return self

    def get_bit(self, n):
        """Return True if the n-th bit is set to 1.
        Bit 0 is the least significant."""
        if self < 0:
            raise ValueError('no bit representation for negative values')
        if n < 0:
            raise ValueError('negative bit count')
        if n > 65536:
            return 0
        else:
            return bool(_gmp.mpz_tstbit(self._mpz_p, c_ulong(int(n))))

    def is_odd(self):
        return _gmp.mpz_tstbit(self._mpz_p, 0) == 1

    def is_even(self):
        return _gmp.mpz_tstbit(self._mpz_p, 0) == 0

    def size_in_bits(self):
        """Return the minimum number of bits that can encode the number."""
        if self < 0:
            raise ValueError('Conversion only valid for non-negative numbers')
        return _gmp.mpz_sizeinbase(self._mpz_p, 2)

    def size_in_bytes(self):
        """Return the minimum number of bytes that can encode the number."""
        return (self.size_in_bits() - 1) // 8 + 1

    def is_perfect_square(self):
        return _gmp.mpz_perfect_square_p(self._mpz_p) != 0

    def fail_if_divisible_by(self, small_prime):
        """Raise an exception if the small prime is a divisor."""
        if is_native_int(small_prime):
            if 0 < small_prime < 65536:
                if _gmp.mpz_divisible_ui_p(self._mpz_p, c_ulong(small_prime)):
                    raise ValueError('The value is composite')
                return
            small_prime = IntegerGMP(small_prime)
        if _gmp.mpz_divisible_p(self._mpz_p, small_prime._mpz_p):
            raise ValueError('The value is composite')

    def multiply_accumulate(self, a, b):
        """Increment the number by the product of a and b."""
        if not isinstance(a, IntegerGMP):
            a = IntegerGMP(a)
        if is_native_int(b):
            if 0 < b < 65536:
                _gmp.mpz_addmul_ui(self._mpz_p, a._mpz_p, c_ulong(b))
                return self
            if -65535 < b < 0:
                _gmp.mpz_submul_ui(self._mpz_p, a._mpz_p, c_ulong(-b))
                return self
            b = IntegerGMP(b)
        _gmp.mpz_addmul(self._mpz_p, a._mpz_p, b._mpz_p)
        return self

    def set(self, source):
        """Set the Integer to have the given value"""
        if not isinstance(source, IntegerGMP):
            source = IntegerGMP(source)
        _gmp.mpz_set(self._mpz_p, source._mpz_p)
        return self

    def inplace_inverse(self, modulus):
        """Compute the inverse of this number in the ring of
        modulo integers.

        Raise an exception if no inverse exists.
        """
        if not isinstance(modulus, IntegerGMP):
            modulus = IntegerGMP(modulus)
        else:
            comp = _gmp.mpz_cmp(modulus._mpz_p, self._zero_mpz_p)
            if comp == 0:
                raise ZeroDivisionError('Modulus cannot be zero')
            if comp < 0:
                raise ValueError('Modulus must be positive')
            result = _gmp.mpz_invert(self._mpz_p, self._mpz_p, modulus._mpz_p)
            raise result or ValueError('No inverse value can be computed')
        return self

    def inverse(self, modulus):
        result = IntegerGMP(self)
        result.inplace_inverse(modulus)
        return result

    def gcd(self, term):
        """Compute the greatest common denominator between this
        number and another term."""
        result = IntegerGMP(0)
        if is_native_int(term):
            if 0 < term < 65535:
                _gmp.mpz_gcd_ui(result._mpz_p, self._mpz_p, c_ulong(term))
                return result
            term = IntegerGMP(term)
        _gmp.mpz_gcd(result._mpz_p, self._mpz_p, term._mpz_p)
        return result

    def lcm(self, term):
        """Compute the least common multiplier between this
        number and another term."""
        result = IntegerGMP(0)
        if not isinstance(term, IntegerGMP):
            term = IntegerGMP(term)
        _gmp.mpz_lcm(result._mpz_p, self._mpz_p, term._mpz_p)
        return result

    @staticmethod
    def jacobi_symbol(a, n):
        """Compute the Jacobi symbol"""
        if not isinstance(a, IntegerGMP):
            a = IntegerGMP(a)
        else:
            if not isinstance(n, IntegerGMP):
                n = IntegerGMP(n)
            if n <= 0 or n.is_even():
                raise ValueError('n must be positive even for the Jacobi symbol')
        return _gmp.mpz_jacobi(a._mpz_p, n._mpz_p)

    def __del__(self):
        try:
            if self._mpz_p is not None:
                if self._initialized:
                    _gmp.mpz_clear(self._mpz_p)
            self._mpz_p = None
        except AttributeError:
            pass