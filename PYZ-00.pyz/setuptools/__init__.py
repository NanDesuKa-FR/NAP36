# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\__init__.py
"""Extensions to the 'distutils' for large or complex distributions"""
import os, functools, distutils.core, distutils.filelist
from distutils.util import convert_path
from fnmatch import fnmatchcase
from setuptools.extern.six.moves import filter, map
import setuptools.version
from setuptools.extension import Extension
from setuptools.dist import Distribution, Feature
from setuptools.depends import Require
from . import monkey
__all__ = [
 'setup', 'Distribution', 'Feature', 'Command', 'Extension', 'Require',
 'find_packages']
__version__ = setuptools.version.__version__
bootstrap_install_from = None
run_2to3_on_doctests = True
lib2to3_fixer_packages = [
 'lib2to3.fixes']

class PackageFinder(object):
    __doc__ = '\n    Generate a list of all Python packages found within a directory\n    '

    @classmethod
    def find(cls, where='.', exclude=(), include=('*', )):
        """Return a list all Python packages found within directory 'where'

        'where' is the root directory which will be searched for packages.  It
        should be supplied as a "cross-platform" (i.e. URL-style) path; it will
        be converted to the appropriate local path syntax.

        'exclude' is a sequence of package names to exclude; '*' can be used
        as a wildcard in the names, such that 'foo.*' will exclude all
        subpackages of 'foo' (but not 'foo' itself).

        'include' is a sequence of package names to include.  If it's
        specified, only the named packages will be included.  If it's not
        specified, all found packages will be included.  'include' can contain
        shell style wildcard patterns just like 'exclude'.
        """
        return list(cls._find_packages_iter(convert_path(where), (cls._build_filter)(*('ez_setup',
                                                                                       '*__pycache__'), *exclude), (cls._build_filter)(*include)))

    @classmethod
    def _find_packages_iter(cls, where, exclude, include):
        """
        All the packages found in 'where' that pass the 'include' filter, but
        not the 'exclude' filter.
        """
        for root, dirs, files in os.walk(where, followlinks=True):
            all_dirs = dirs[:]
            dirs[:] = []
            for dir in all_dirs:
                full_path = os.path.join(root, dir)
                rel_path = os.path.relpath(full_path, where)
                package = rel_path.replace(os.path.sep, '.')
                if not '.' in dir:
                    if not cls._looks_like_package(full_path):
                        pass
                    else:
                        if include(package):
                            if not exclude(package):
                                yield package
                        dirs.append(dir)

    @staticmethod
    def _looks_like_package(path):
        """Does a directory look like a package?"""
        return os.path.isfile(os.path.join(path, '__init__.py'))

    @staticmethod
    def _build_filter(*patterns):
        """
        Given a list of patterns, return a callable that will be true only if
        the input matches at least one of the patterns.
        """
        return lambda name: any(fnmatchcase(name, pat=pat) for pat in patterns)


class PEP420PackageFinder(PackageFinder):

    @staticmethod
    def _looks_like_package(path):
        return True


find_packages = PackageFinder.find

def _install_setup_requires(attrs):
    dist = distutils.core.Distribution(dict((k, v) for k, v in attrs.items() if k in ('dependency_links',
                                                                                      'setup_requires')))
    dist.parse_config_files(ignore_option_errors=True)
    if dist.setup_requires:
        dist.fetch_build_eggs(dist.setup_requires)


def setup(**attrs):
    _install_setup_requires(attrs)
    return (distutils.core.setup)(**attrs)


setup.__doc__ = distutils.core.setup.__doc__
_Command = monkey.get_unpatched(distutils.core.Command)

class Command(_Command):
    __doc__ = _Command.__doc__
    command_consumes_arguments = False

    def __init__(self, dist, **kw):
        """
        Construct the command for dist, updating
        vars(self) with any keyword parameters.
        """
        _Command.__init__(self, dist)
        vars(self).update(kw)

    def reinitialize_command(self, command, reinit_subcommands=0, **kw):
        cmd = _Command.reinitialize_command(self, command, reinit_subcommands)
        vars(cmd).update(kw)
        return cmd


def _find_all_simple(path):
    """
    Find all files under 'path'
    """
    results = (os.path.join(base, file) for base, dirs, files in os.walk(path, followlinks=True) for file in files)
    return filter(os.path.isfile, results)


def findall(dir=os.curdir):
    """
    Find all files under 'dir' and return the list of full filenames.
    Unless dir is '.', return full filenames with dir prepended.
    """
    files = _find_all_simple(dir)
    if dir == os.curdir:
        make_rel = functools.partial((os.path.relpath), start=dir)
        files = map(make_rel, files)
    return list(files)


monkey.patch_all()