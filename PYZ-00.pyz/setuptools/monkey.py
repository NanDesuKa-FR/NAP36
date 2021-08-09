# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\monkey.py
"""
Monkey patching of distutils.
"""
import sys, distutils.filelist, platform, types, functools
from importlib import import_module
import inspect
from setuptools.extern import six
import setuptools
__all__ = []

def _get_mro(cls):
    """
    Returns the bases classes for cls sorted by the MRO.

    Works around an issue on Jython where inspect.getmro will not return all
    base classes if multiple classes share the same name. Instead, this
    function will return a tuple containing the class itself, and the contents
    of cls.__bases__. See https://github.com/pypa/setuptools/issues/1024.
    """
    if platform.python_implementation() == 'Jython':
        return (cls,) + cls.__bases__
    else:
        return inspect.getmro(cls)


def get_unpatched(item):
    lookup = get_unpatched_class if isinstance(item, six.class_types) else get_unpatched_function if isinstance(item, types.FunctionType) else (lambda item: None)
    return lookup(item)


def get_unpatched_class(cls):
    """Protect against re-patching the distutils if reloaded

    Also ensures that no other distutils extension monkeypatched the distutils
    first.
    """
    external_bases = (cls for cls in _get_mro(cls) if not cls.__module__.startswith('setuptools'))
    base = next(external_bases)
    if not base.__module__.startswith('distutils'):
        msg = 'distutils has already been patched by %r' % cls
        raise AssertionError(msg)
    return base


def patch_all():
    distutils.core.Command = setuptools.Command
    has_issue_12885 = sys.version_info <= (3, 5, 3)
    if has_issue_12885:
        distutils.filelist.findall = setuptools.findall
    needs_warehouse = sys.version_info < (2, 7, 13) or (3, 0) < sys.version_info < (3,
                                                                                    3,
                                                                                    7) or (3,
                                                                                           4) < sys.version_info < (3,
                                                                                                                    4,
                                                                                                                    6) or (3,
                                                                                                                           5) < sys.version_info <= (3,
                                                                                                                                                     5,
                                                                                                                                                     3)
    if needs_warehouse:
        warehouse = 'https://upload.pypi.org/legacy/'
        distutils.config.PyPIRCCommand.DEFAULT_REPOSITORY = warehouse
    _patch_distribution_metadata_write_pkg_file()
    _patch_distribution_metadata_write_pkg_info()
    for module in (distutils.dist, distutils.core, distutils.cmd):
        module.Distribution = setuptools.dist.Distribution

    distutils.core.Extension = setuptools.extension.Extension
    distutils.extension.Extension = setuptools.extension.Extension
    if 'distutils.command.build_ext' in sys.modules:
        sys.modules['distutils.command.build_ext'].Extension = setuptools.extension.Extension
    patch_for_msvc_specialized_compiler()


def _patch_distribution_metadata_write_pkg_file():
    """Patch write_pkg_file to also write Requires-Python/Requires-External"""
    distutils.dist.DistributionMetadata.write_pkg_file = setuptools.dist.write_pkg_file


def _patch_distribution_metadata_write_pkg_info():
    """
    Workaround issue #197 - Python 3 prior to 3.2.2 uses an environment-local
    encoding to save the pkg_info. Monkey-patch its write_pkg_info method to
    correct this undesirable behavior.
    """
    environment_local = (3, ) <= sys.version_info[:3] < (3, 2, 2)
    if not environment_local:
        return
    distutils.dist.DistributionMetadata.write_pkg_info = setuptools.dist.write_pkg_info


def patch_func(replacement, target_mod, func_name):
    """
    Patch func_name in target_mod with replacement

    Important - original must be resolved by name to avoid
    patching an already patched function.
    """
    original = getattr(target_mod, func_name)
    vars(replacement).setdefault('unpatched', original)
    setattr(target_mod, func_name, replacement)


def get_unpatched_function(candidate):
    return getattr(candidate, 'unpatched')


def patch_for_msvc_specialized_compiler():
    """
    Patch functions in distutils to use standalone Microsoft Visual C++
    compilers.
    """
    msvc = import_module('setuptools.msvc')
    if platform.system() != 'Windows':
        return

    def patch_params(mod_name, func_name):
        repl_prefix = 'msvc9_' if 'msvc9' in mod_name else 'msvc14_'
        repl_name = repl_prefix + func_name.lstrip('_')
        repl = getattr(msvc, repl_name)
        mod = import_module(mod_name)
        if not hasattr(mod, func_name):
            raise ImportError(func_name)
        return (
         repl, mod, func_name)

    msvc9 = functools.partial(patch_params, 'distutils.msvc9compiler')
    msvc14 = functools.partial(patch_params, 'distutils._msvccompiler')
    try:
        patch_func(*msvc9('find_vcvarsall'))
        patch_func(*msvc9('query_vcvarsall'))
    except ImportError:
        pass

    try:
        patch_func(*msvc14('_get_vc_env'))
    except ImportError:
        pass

    try:
        patch_func(*msvc14('gen_lib_options'))
    except ImportError:
        pass