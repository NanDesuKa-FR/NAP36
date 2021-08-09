# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: ctypes\macholib\framework.py
"""
Generic framework path manipulation
"""
import re
__all__ = [
 'framework_info']
STRICT_FRAMEWORK_RE = re.compile('(?x)\n(?P<location>^.*)(?:^|/)\n(?P<name>\n    (?P<shortname>\\w+).framework/\n    (?:Versions/(?P<version>[^/]+)/)?\n    (?P=shortname)\n    (?:_(?P<suffix>[^_]+))?\n)$\n')

def framework_info(filename):
    """
    A framework name can take one of the following four forms:
        Location/Name.framework/Versions/SomeVersion/Name_Suffix
        Location/Name.framework/Versions/SomeVersion/Name
        Location/Name.framework/Name_Suffix
        Location/Name.framework/Name

    returns None if not found, or a mapping equivalent to:
        dict(
            location='Location',
            name='Name.framework/Versions/SomeVersion/Name_Suffix',
            shortname='Name',
            version='SomeVersion',
            suffix='Suffix',
        )

    Note that SomeVersion and Suffix are optional and may be None
    if not present
    """
    is_framework = STRICT_FRAMEWORK_RE.match(filename)
    if not is_framework:
        return
    else:
        return is_framework.groupdict()


def test_framework_info():

    def d(location=None, name=None, shortname=None, version=None, suffix=None):
        return dict(location=location,
          name=name,
          shortname=shortname,
          version=version,
          suffix=suffix)

    if not framework_info('completely/invalid') is None:
        raise AssertionError
    else:
        if not framework_info('completely/invalid/_debug') is None:
            raise AssertionError
        else:
            if not framework_info('P/F.framework') is None:
                raise AssertionError
            else:
                if not framework_info('P/F.framework/_debug') is None:
                    raise AssertionError
                else:
                    if not framework_info('P/F.framework/F') == d('P', 'F.framework/F', 'F'):
                        raise AssertionError
                    elif not framework_info('P/F.framework/F_debug') == d('P', 'F.framework/F_debug', 'F', suffix='debug'):
                        raise AssertionError
                    assert framework_info('P/F.framework/Versions') is None
                assert framework_info('P/F.framework/Versions/A') is None
            assert framework_info('P/F.framework/Versions/A/F') == d('P', 'F.framework/Versions/A/F', 'F', 'A')
        assert framework_info('P/F.framework/Versions/A/F_debug') == d('P', 'F.framework/Versions/A/F_debug', 'F', 'A', 'debug')


if __name__ == '__main__':
    test_framework_info()