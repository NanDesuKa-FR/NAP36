# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: ctypes\macholib\dylib.py
"""
Generic dylib path manipulation
"""
import re
__all__ = [
 'dylib_info']
DYLIB_RE = re.compile('(?x)\n(?P<location>^.*)(?:^|/)\n(?P<name>\n    (?P<shortname>\\w+?)\n    (?:\\.(?P<version>[^._]+))?\n    (?:_(?P<suffix>[^._]+))?\n    \\.dylib$\n)\n')

def dylib_info(filename):
    """
    A dylib name can take one of the following four forms:
        Location/Name.SomeVersion_Suffix.dylib
        Location/Name.SomeVersion.dylib
        Location/Name_Suffix.dylib
        Location/Name.dylib

    returns None if not found or a mapping equivalent to:
        dict(
            location='Location',
            name='Name.SomeVersion_Suffix.dylib',
            shortname='Name',
            version='SomeVersion',
            suffix='Suffix',
        )

    Note that SomeVersion and Suffix are optional and may be None
    if not present.
    """
    is_dylib = DYLIB_RE.match(filename)
    if not is_dylib:
        return
    else:
        return is_dylib.groupdict()


def test_dylib_info():

    def d(location=None, name=None, shortname=None, version=None, suffix=None):
        return dict(location=location,
          name=name,
          shortname=shortname,
          version=version,
          suffix=suffix)

    if not dylib_info('completely/invalid') is None:
        raise AssertionError
    else:
        if not dylib_info('completely/invalide_debug') is None:
            raise AssertionError
        else:
            if not dylib_info('P/Foo.dylib') == d('P', 'Foo.dylib', 'Foo'):
                raise AssertionError
            else:
                assert dylib_info('P/Foo_debug.dylib') == d('P', 'Foo_debug.dylib', 'Foo', suffix='debug')
                assert dylib_info('P/Foo.A.dylib') == d('P', 'Foo.A.dylib', 'Foo', 'A')
            assert dylib_info('P/Foo_debug.A.dylib') == d('P', 'Foo_debug.A.dylib', 'Foo_debug', 'A')
        assert dylib_info('P/Foo.A_debug.dylib') == d('P', 'Foo.A_debug.dylib', 'Foo', 'A', 'debug')


if __name__ == '__main__':
    test_dylib_info()