# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Random\random.py
__all__ = [
 'StrongRandom', 'getrandbits', 'randrange', 'randint', 'choice', 'shuffle', 'sample']
from Cryptodome import Random
from Cryptodome.Util.py3compat import is_native_int

class StrongRandom(object):

    def __init__(self, rng=None, randfunc=None):
        if randfunc is None:
            if rng is None:
                self._randfunc = None
        elif randfunc is not None:
            if rng is None:
                self._randfunc = randfunc
        elif randfunc is None:
            if rng is not None:
                self._randfunc = rng.read
        else:
            raise ValueError("Cannot specify both 'rng' and 'randfunc'")

    def getrandbits(self, k):
        """Return an integer with k random bits."""
        if self._randfunc is None:
            self._randfunc = Random.new().read
        mask = (1 << k) - 1
        return mask & bytes_to_long(self._randfunc(ceil_div(k, 8)))

    def randrange(self, *args):
        """randrange([start,] stop[, step]):
        Return a randomly-selected element from range(start, stop, step)."""
        if len(args) == 3:
            start, stop, step = args
        else:
            if len(args) == 2:
                start, stop = args
                step = 1
            else:
                if len(args) == 1:
                    stop, = args
                    start = 0
                    step = 1
                else:
                    raise TypeError('randrange expected at most 3 arguments, got %d' % (len(args),))
                if not is_native_int(start) or not is_native_int(stop) or not is_native_int(step):
                    raise TypeError('randrange requires integer arguments')
                if step == 0:
                    raise ValueError('randrange step argument must not be zero')
                num_choices = ceil_div(stop - start, step)
                if num_choices < 0:
                    num_choices = 0
            if num_choices < 1:
                raise ValueError('empty range for randrange(%r, %r, %r)' % (start, stop, step))
        r = num_choices
        while r >= num_choices:
            r = self.getrandbits(size(num_choices))

        return start + step * r

    def randint(self, a, b):
        """Return a random integer N such that a <= N <= b."""
        if not is_native_int(a) or not is_native_int(b):
            raise TypeError('randint requires integer arguments')
        else:
            N = self.randrange(a, b + 1)
            assert a <= N <= b
        return N

    def choice(self, seq):
        """Return a random element from a (non-empty) sequence.

        If the seqence is empty, raises IndexError.
        """
        if len(seq) == 0:
            raise IndexError('empty sequence')
        return seq[self.randrange(len(seq))]

    def shuffle(self, x):
        """Shuffle the sequence in place."""
        for i in range(len(x) - 1, 0, -1):
            j = self.randrange(0, i + 1)
            x[i], x[j] = x[j], x[i]

    def sample(self, population, k):
        """Return a k-length list of unique elements chosen from the population sequence."""
        num_choices = len(population)
        if k > num_choices:
            raise ValueError('sample larger than population')
        retval = []
        selected = {}
        for i in range(k):
            r = None
            while r is None or r in selected:
                r = self.randrange(num_choices)

            retval.append(population[r])
            selected[r] = 1

        return retval


_r = StrongRandom()
getrandbits = _r.getrandbits
randrange = _r.randrange
randint = _r.randint
choice = _r.choice
shuffle = _r.shuffle
sample = _r.sample
from Cryptodome.Util.number import ceil_div, bytes_to_long, long_to_bytes, size