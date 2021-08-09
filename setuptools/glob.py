# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\glob.py
"""
Filename globbing utility. Mostly a copy of `glob` from Python 3.5.

Changes include:
 * `yield from` and PEP3102 `*` removed.
 * `bytes` changed to `six.binary_type`.
 * Hidden files are not ignored.
"""
import os, re, fnmatch
from setuptools.extern.six import binary_type
__all__ = [
 'glob', 'iglob', 'escape']

def glob(pathname, recursive=False):
    """Return a list of paths matching a pathname pattern.

    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.

    If recursive is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    return list(iglob(pathname, recursive=recursive))


def iglob(pathname, recursive=False):
    """Return an iterator which yields the paths matching a pathname pattern.

    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.

    If recursive is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    it = _iglob(pathname, recursive)
    if recursive:
        if _isrecursive(pathname):
            s = next(it)
            assert not s
    return it


def _iglob(pathname, recursive):
    dirname, basename = os.path.split(pathname)
    if not has_magic(pathname):
        if basename:
            if os.path.lexists(pathname):
                yield pathname
        else:
            if os.path.isdir(dirname):
                yield pathname
        return
    else:
        if dirname or recursive and _isrecursive(basename):
            for x in glob2(dirname, basename):
                yield x

        else:
            for x in glob1(dirname, basename):
                yield x

        return
    if dirname != pathname:
        if has_magic(dirname):
            dirs = _iglob(dirname, recursive)
        else:
            dirs = [
             dirname]
    else:
        if has_magic(basename):
            if recursive:
                if _isrecursive(basename):
                    glob_in_dir = glob2
            glob_in_dir = glob1
        else:
            glob_in_dir = glob0
    for dirname in dirs:
        for name in glob_in_dir(dirname, basename):
            yield os.path.join(dirname, name)


def glob1(dirname, pattern):
    if not dirname:
        if isinstance(pattern, binary_type):
            dirname = os.curdir.encode('ASCII')
        else:
            dirname = os.curdir
    try:
        names = os.listdir(dirname)
    except OSError:
        return []
    else:
        return fnmatch.filter(names, pattern)


def glob0(dirname, basename):
    if basename or os.path.isdir(dirname):
        return [
         basename]
    else:
        if os.path.lexists(os.path.join(dirname, basename)):
            return [
             basename]
        return []


def glob2(dirname, pattern):
    assert _isrecursive(pattern)
    yield pattern[:0]
    for x in _rlistdir(dirname):
        yield x


def _rlistdir(dirname):
    if not dirname:
        if isinstance(dirname, binary_type):
            dirname = binary_type(os.curdir, 'ASCII')
        else:
            dirname = os.curdir
    try:
        names = os.listdir(dirname)
    except os.error:
        return
    else:
        for x in names:
            yield x
            path = os.path.join(dirname, x) if dirname else x
            for y in _rlistdir(path):
                yield os.path.join(x, y)


magic_check = re.compile('([*?[])')
magic_check_bytes = re.compile(b'([*?[])')

def has_magic(s):
    if isinstance(s, binary_type):
        match = magic_check_bytes.search(s)
    else:
        match = magic_check.search(s)
    return match is not None


def _isrecursive(pattern):
    if isinstance(pattern, binary_type):
        return pattern == b'**'
    else:
        return pattern == '**'


def escape(pathname):
    """Escape all special characters.
    """
    drive, pathname = os.path.splitdrive(pathname)
    if isinstance(pathname, binary_type):
        pathname = magic_check_bytes.sub(b'[\\1]', pathname)
    else:
        pathname = magic_check.sub('[\\1]', pathname)
    return drive + pathname