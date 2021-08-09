# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\glibc.py
from __future__ import absolute_import
import ctypes, re, warnings

def glibc_version_string():
    """Returns glibc version string, or None if not using glibc."""
    process_namespace = ctypes.CDLL(None)
    try:
        gnu_get_libc_version = process_namespace.gnu_get_libc_version
    except AttributeError:
        return
    else:
        gnu_get_libc_version.restype = ctypes.c_char_p
        version_str = gnu_get_libc_version()
        if not isinstance(version_str, str):
            version_str = version_str.decode('ascii')
        return version_str


def check_glibc_version(version_str, required_major, minimum_minor):
    m = re.match('(?P<major>[0-9]+)\\.(?P<minor>[0-9]+)', version_str)
    if not m:
        warnings.warn('Expected glibc version with 2 components major.minor, got: %s' % version_str, RuntimeWarning)
        return False
    else:
        return int(m.group('major')) == required_major and int(m.group('minor')) >= minimum_minor


def have_compatible_glibc(required_major, minimum_minor):
    version_str = glibc_version_string()
    if version_str is None:
        return False
    else:
        return check_glibc_version(version_str, required_major, minimum_minor)


def libc_ver():
    """Try to determine the glibc version

    Returns a tuple of strings (lib, version) which default to empty strings
    in case the lookup fails.
    """
    glibc_version = glibc_version_string()
    if glibc_version is None:
        return ('', '')
    else:
        return (
         'glibc', glibc_version)