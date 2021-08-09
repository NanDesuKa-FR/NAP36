# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\_vendor\packaging\version.py
from __future__ import absolute_import, division, print_function
import collections, itertools, re
from ._structures import Infinity
__all__ = [
 'parse', 'Version', 'LegacyVersion', 'InvalidVersion', 'VERSION_PATTERN']
_Version = collections.namedtuple('_Version', [
 'epoch', 'release', 'dev', 'pre', 'post', 'local'])

def parse(version):
    """
    Parse the given version string and return either a :class:`Version` object
    or a :class:`LegacyVersion` object depending on if the given version is
    a valid PEP 440 version or a legacy version.
    """
    try:
        return Version(version)
    except InvalidVersion:
        return LegacyVersion(version)


class InvalidVersion(ValueError):
    __doc__ = '\n    An invalid version was found, users should refer to PEP 440.\n    '


class _BaseVersion(object):

    def __hash__(self):
        return hash(self._key)

    def __lt__(self, other):
        return self._compare(other, lambda s, o: s < o)

    def __le__(self, other):
        return self._compare(other, lambda s, o: s <= o)

    def __eq__(self, other):
        return self._compare(other, lambda s, o: s == o)

    def __ge__(self, other):
        return self._compare(other, lambda s, o: s >= o)

    def __gt__(self, other):
        return self._compare(other, lambda s, o: s > o)

    def __ne__(self, other):
        return self._compare(other, lambda s, o: s != o)

    def _compare(self, other, method):
        if not isinstance(other, _BaseVersion):
            return NotImplemented
        else:
            return method(self._key, other._key)


class LegacyVersion(_BaseVersion):

    def __init__(self, version):
        self._version = str(version)
        self._key = _legacy_cmpkey(self._version)

    def __str__(self):
        return self._version

    def __repr__(self):
        return '<LegacyVersion({0})>'.format(repr(str(self)))

    @property
    def public(self):
        return self._version

    @property
    def base_version(self):
        return self._version

    @property
    def local(self):
        pass

    @property
    def is_prerelease(self):
        return False

    @property
    def is_postrelease(self):
        return False


_legacy_version_component_re = re.compile('(\\d+ | [a-z]+ | \\.| -)', re.VERBOSE)
_legacy_version_replacement_map = {'pre':'c', 
 'preview':'c',  '-':'final-',  'rc':'c',  'dev':'@'}

def _parse_version_parts(s):
    for part in _legacy_version_component_re.split(s):
        part = _legacy_version_replacement_map.get(part, part)
        if not not part:
            if part == '.':
                pass
            else:
                if part[:1] in '0123456789':
                    yield part.zfill(8)
                else:
                    yield '*' + part

    yield '*final'


def _legacy_cmpkey(version):
    epoch = -1
    parts = []
    for part in _parse_version_parts(version.lower()):
        if part.startswith('*'):
            if part < '*final':
                while parts and parts[(-1)] == '*final-':
                    parts.pop()

            while parts and parts[(-1)] == '00000000':
                parts.pop()

        parts.append(part)

    parts = tuple(parts)
    return (
     epoch, parts)


VERSION_PATTERN = '\n    v?\n    (?:\n        (?:(?P<epoch>[0-9]+)!)?                           # epoch\n        (?P<release>[0-9]+(?:\\.[0-9]+)*)                  # release segment\n        (?P<pre>                                          # pre-release\n            [-_\\.]?\n            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))\n            [-_\\.]?\n            (?P<pre_n>[0-9]+)?\n        )?\n        (?P<post>                                         # post release\n            (?:-(?P<post_n1>[0-9]+))\n            |\n            (?:\n                [-_\\.]?\n                (?P<post_l>post|rev|r)\n                [-_\\.]?\n                (?P<post_n2>[0-9]+)?\n            )\n        )?\n        (?P<dev>                                          # dev release\n            [-_\\.]?\n            (?P<dev_l>dev)\n            [-_\\.]?\n            (?P<dev_n>[0-9]+)?\n        )?\n    )\n    (?:\\+(?P<local>[a-z0-9]+(?:[-_\\.][a-z0-9]+)*))?       # local version\n'

class Version(_BaseVersion):
    _regex = re.compile('^\\s*' + VERSION_PATTERN + '\\s*$', re.VERBOSE | re.IGNORECASE)

    def __init__(self, version):
        match = self._regex.search(version)
        if not match:
            raise InvalidVersion("Invalid version: '{0}'".format(version))
        self._version = _Version(epoch=(int(match.group('epoch')) if match.group('epoch') else 0),
          release=(tuple(int(i) for i in match.group('release').split('.'))),
          pre=(_parse_letter_version(match.group('pre_l'), match.group('pre_n'))),
          post=(_parse_letter_version(match.group('post_l'), match.group('post_n1') or match.group('post_n2'))),
          dev=(_parse_letter_version(match.group('dev_l'), match.group('dev_n'))),
          local=(_parse_local_version(match.group('local'))))
        self._key = _cmpkey(self._version.epoch, self._version.release, self._version.pre, self._version.post, self._version.dev, self._version.local)

    def __repr__(self):
        return '<Version({0})>'.format(repr(str(self)))

    def __str__(self):
        parts = []
        if self._version.epoch != 0:
            parts.append('{0}!'.format(self._version.epoch))
        parts.append('.'.join(str(x) for x in self._version.release))
        if self._version.pre is not None:
            parts.append(''.join(str(x) for x in self._version.pre))
        if self._version.post is not None:
            parts.append('.post{0}'.format(self._version.post[1]))
        if self._version.dev is not None:
            parts.append('.dev{0}'.format(self._version.dev[1]))
        if self._version.local is not None:
            parts.append('+{0}'.format('.'.join(str(x) for x in self._version.local)))
        return ''.join(parts)

    @property
    def public(self):
        return str(self).split('+', 1)[0]

    @property
    def base_version(self):
        parts = []
        if self._version.epoch != 0:
            parts.append('{0}!'.format(self._version.epoch))
        parts.append('.'.join(str(x) for x in self._version.release))
        return ''.join(parts)

    @property
    def local(self):
        version_string = str(self)
        if '+' in version_string:
            return version_string.split('+', 1)[1]

    @property
    def is_prerelease(self):
        return bool(self._version.dev or self._version.pre)

    @property
    def is_postrelease(self):
        return bool(self._version.post)


def _parse_letter_version(letter, number):
    if letter:
        if number is None:
            number = 0
        letter = letter.lower()
        if letter == 'alpha':
            letter = 'a'
        else:
            if letter == 'beta':
                letter = 'b'
            else:
                if letter in ('c', 'pre', 'preview'):
                    letter = 'rc'
                else:
                    if letter in ('rev', 'r'):
                        letter = 'post'
        return (
         letter, int(number))
    if not letter:
        if number:
            letter = 'post'
            return (
             letter, int(number))


_local_version_seperators = re.compile('[\\._-]')

def _parse_local_version(local):
    """
    Takes a string like abc.1.twelve and turns it into ("abc", 1, "twelve").
    """
    if local is not None:
        return tuple((part.lower() if not part.isdigit() else int(part)) for part in _local_version_seperators.split(local))


def _cmpkey(epoch, release, pre, post, dev, local):
    release = tuple(reversed(list(itertools.dropwhile(lambda x: x == 0, reversed(release)))))
    if pre is None:
        if post is None:
            if dev is not None:
                pre = -Infinity
    if pre is None:
        pre = Infinity
    else:
        if post is None:
            post = -Infinity
        if dev is None:
            dev = Infinity
        if local is None:
            local = -Infinity
        else:
            local = tuple(((i, '') if isinstance(i, int) else (-Infinity, i)) for i in local)
    return (epoch, release, pre, post, dev, local)