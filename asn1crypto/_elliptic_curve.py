# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\asn1crypto\_elliptic_curve.py
"""
Classes and objects to represent prime-field elliptic curves and points on them.
Exports the following items:

 - PrimeCurve()
 - PrimePoint()
 - SECP192R1_CURVE
 - SECP192R1_BASE_POINT
 - SECP224R1_CURVE
 - SECP224R1_BASE_POINT
 - SECP256R1_CURVE
 - SECP256R1_BASE_POINT
 - SECP384R1_CURVE
 - SECP384R1_BASE_POINT
 - SECP521R1_CURVE
 - SECP521R1_BASE_POINT

The curve constants are all PrimeCurve() objects and the base point constants
are all PrimePoint() objects.

Some of the following source code is derived from
http://webpages.charter.net/curryfans/peter/downloads.html, but has been heavily
modified to fit into this projects lint settings. The original project license
is listed below:

Copyright (c) 2014 Peter Pearson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from __future__ import unicode_literals, division, absolute_import, print_function
from ._int import inverse_mod

class PrimeCurve:
    __doc__ = '\n    Elliptic curve over a prime field. Characteristic two field curves are not\n    supported.\n    '

    def __init__(self, p, a, b):
        """
        The curve of points satisfying y^2 = x^3 + a*x + b (mod p)

        :param p:
            The prime number as an integer

        :param a:
            The component a as an integer

        :param b:
            The component b as an integer
        """
        self.p = p
        self.a = a
        self.b = b

    def contains(self, point):
        """
        :param point:
            A Point object

        :return:
            Boolean if the point is on this curve
        """
        y2 = point.y * point.y
        x3 = point.x * point.x * point.x
        return (y2 - (x3 + self.a * point.x + self.b)) % self.p == 0


class PrimePoint:
    __doc__ = '\n    A point on a prime-field elliptic curve\n    '

    def __init__(self, curve, x, y, order=None):
        """
        :param curve:
            A PrimeCurve object

        :param x:
            The x coordinate of the point as an integer

        :param y:
            The y coordinate of the point as an integer

        :param order:
            The order of the point, as an integer - optional
        """
        self.curve = curve
        self.x = x
        self.y = y
        self.order = order
        if self.curve:
            if not self.curve.contains(self):
                raise ValueError('Invalid EC point')
        if self.order:
            if self * self.order != INFINITY:
                raise ValueError('Invalid EC point')

    def __cmp__(self, other):
        """
        :param other:
            A PrimePoint object

        :return:
            0 if identical, 1 otherwise
        """
        if self.curve == other.curve:
            if self.x == other.x:
                if self.y == other.y:
                    return 0
        return 1

    def __add__(self, other):
        """
        :param other:
            A PrimePoint object

        :return:
            A PrimePoint object
        """
        if other == INFINITY:
            return self
        else:
            if self == INFINITY:
                return other
            else:
                assert self.curve == other.curve
                if self.x == other.x:
                    if (self.y + other.y) % self.curve.p == 0:
                        return INFINITY
                    else:
                        return self.double()
            p = self.curve.p
            l_ = (other.y - self.y) * inverse_mod(other.x - self.x, p) % p
            x3 = (l_ * l_ - self.x - other.x) % p
            y3 = (l_ * (self.x - x3) - self.y) % p
            return PrimePoint(self.curve, x3, y3)

    def __mul__(self, other):
        """
        :param other:
            An integer to multiple the Point by

        :return:
            A PrimePoint object
        """

        def leftmost_bit(x):
            assert x > 0
            result = 1
            while result <= x:
                result = 2 * result

            return result // 2

        e = other
        if self.order:
            e = e % self.order
        if e == 0:
            return INFINITY
        else:
            if self == INFINITY:
                return INFINITY
            elif not e > 0:
                raise AssertionError
            e3 = 3 * e
            negative_self = PrimePoint(self.curve, self.x, -self.y, self.order)
            i = leftmost_bit(e3) // 2
            result = self
            while i > 1:
                result = result.double()
                if e3 & i != 0:
                    if e & i == 0:
                        result = result + self
                if e3 & i == 0:
                    if e & i != 0:
                        result = result + negative_self
                i = i // 2

            return result

    def __rmul__(self, other):
        """
        :param other:
            An integer to multiple the Point by

        :return:
            A PrimePoint object
        """
        return self * other

    def double(self):
        """
        :return:
            A PrimePoint object that is twice this point
        """
        p = self.curve.p
        a = self.curve.a
        l_ = (3 * self.x * self.x + a) * inverse_mod(2 * self.y, p) % p
        x3 = (l_ * l_ - 2 * self.x) % p
        y3 = (l_ * (self.x - x3) - self.y) % p
        return PrimePoint(self.curve, x3, y3)


INFINITY = PrimePoint(None, None, None)
SECP192R1_CURVE = PrimeCurve(6277101735386680763835789423207666416083908700390324961279, -3, 2455155546008943817740293915197451784769108058161191238065)
SECP192R1_BASE_POINT = PrimePoint(SECP192R1_CURVE, 602046282375688656758213480587526111916698976636884684818, 174050332293622031404857552280219410364023488927386650641, 6277101735386680763835789423176059013767194773182842284081)
SECP224R1_CURVE = PrimeCurve(26959946667150639794667015087019630673557916260026308143510066298881, -3, 18958286285566608000408668544493926415504680968679321075787234672564)
SECP224R1_BASE_POINT = PrimePoint(SECP224R1_CURVE, 19277929113566293071110308034699488026831934219452440156649784352033, 19926808758034470970197974370888749184205991990603949537637343198772, 26959946667150639794667015087019625940457807714424391721682722368061)
SECP256R1_CURVE = PrimeCurve(115792089210356248762697446949407573530086143415290314195533631308867097853951, -3, 41058363725152142129326129780047268409114441015993725554835256314039467401291)
SECP256R1_BASE_POINT = PrimePoint(SECP256R1_CURVE, 48439561293906451759052585252797914202762949526041747995844080717082404635286, 36134250956749795798585127919587881956611106672985015071877198253568414405109, 115792089210356248762697446949407573529996955224135760342422259061068512044369)
SECP384R1_CURVE = PrimeCurve(39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319, -3, 27580193559959705877849011840389048093056905856361568521428707301988689241309860865136260764883745107765439761230575)
SECP384R1_BASE_POINT = PrimePoint(SECP384R1_CURVE, 26247035095799689268623156744566981891852923491109213387815615900925518854738050089022388053975719786650872476732087, 8325710961489029985546751289520108179287853048861315594709205902480503199884419224438643760392947333078086511627871, 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643)
SECP521R1_CURVE = PrimeCurve(6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151, -3, 1093849038073734274511112390766805569936207598951683748994586394495953116150735016013708737573759623248592132296706313309438452531591012912142327488478985984)
SECP521R1_BASE_POINT = PrimePoint(SECP521R1_CURVE, 2661740802050217063228768716723360960729859168756973147706671368418802944996427808491545080627771902352094241225065558662157113545570916814161637315895999846, 3757180025770020463545507224491183603594455134769762486694567779615544477440556316691234405012945539562144444537289428522585666729196580810124344277578376784, 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449)