# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\PyInstaller\fake-modules\site.py
"""
This is a fake 'site' module available in default Python Library.

The real 'site' does some magic to find paths to other possible
Python modules. We do not want this behaviour for frozen applications.

Fake 'site' makes PyInstaller to work with distutils and to work inside
virtualenv environment.
"""
__pyinstaller__faked__site__module__ = True
PREFIXES = []
ENABLE_USER_SITE = False
USER_SITE = ''
USER_BASE = None

class _Helper(object):
    __doc__ = "\n     Define the builtin 'help'.\n     This is a wrapper around pydoc.help (with a twist).\n     "

    def __repr__(self):
        return 'Type help() for interactive help, or help(object) for help about object.'

    def __call__(self, *args, **kwds):
        pydoc = __import__(''.join('pydoc'))
        return (pydoc.help)(*args, **kwds)