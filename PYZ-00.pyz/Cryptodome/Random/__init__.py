# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Random\__init__.py
__all__ = [
 'new', 'get_random_bytes']
from os import urandom

class _UrandomRNG(object):

    def read(self, n):
        """Return a random byte string of the desired size."""
        return urandom(n)

    def flush(self):
        """Method provided for backward compatibility only."""
        pass

    def reinit(self):
        """Method provided for backward compatibility only."""
        pass

    def close(self):
        """Method provided for backward compatibility only."""
        pass


def new(*args, **kwargs):
    """Return a file-like object that outputs cryptographically random bytes."""
    return _UrandomRNG()


def atfork():
    pass


get_random_bytes = urandom