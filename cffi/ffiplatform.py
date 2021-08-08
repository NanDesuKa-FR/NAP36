# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cffi\ffiplatform.py
import sys, os
from .error import VerificationError
LIST_OF_FILE_NAMES = [
 'sources', 'include_dirs', 'library_dirs',
 'extra_objects', 'depends']

def get_extension(srcfilename, modname, sources=(), **kwds):
    _hack_at_distutils()
    from distutils.core import Extension
    allsources = [srcfilename]
    for src in sources:
        allsources.append(os.path.normpath(src))

    return Extension(name=modname, sources=allsources, **kwds)


def compile(tmpdir, ext, compiler_verbose=0, debug=None):
    """Compile a C extension module using distutils."""
    _hack_at_distutils()
    saved_environ = os.environ.copy()
    try:
        outputfilename = _build(tmpdir, ext, compiler_verbose, debug)
        outputfilename = os.path.abspath(outputfilename)
    finally:
        for key, value in saved_environ.items():
            if os.environ.get(key) != value:
                os.environ[key] = value

    return outputfilename


def _build(tmpdir, ext, compiler_verbose=0, debug=None):
    from distutils.core import Distribution
    import distutils.errors, distutils.log
    dist = Distribution({'ext_modules': [ext]})
    dist.parse_config_files()
    options = dist.get_option_dict('build_ext')
    if debug is None:
        debug = sys.flags.debug
    options['debug'] = (
     'ffiplatform', debug)
    options['force'] = ('ffiplatform', True)
    options['build_lib'] = ('ffiplatform', tmpdir)
    options['build_temp'] = ('ffiplatform', tmpdir)
    try:
        old_level = distutils.log.set_threshold(0) or 0
        try:
            distutils.log.set_verbosity(compiler_verbose)
            dist.run_command('build_ext')
            cmd_obj = dist.get_command_obj('build_ext')
            soname, = cmd_obj.get_outputs()
        finally:
            distutils.log.set_threshold(old_level)

    except (distutils.errors.CompileError,
     distutils.errors.LinkError) as e:
        raise VerificationError('%s: %s' % (e.__class__.__name__, e))

    return soname


try:
    from os.path import samefile
except ImportError:

    def samefile(f1, f2):
        return os.path.abspath(f1) == os.path.abspath(f2)


def maybe_relative_path(path):
    if not os.path.isabs(path):
        return path
    dir = path
    names = []
    while True:
        prevdir = dir
        dir, name = os.path.split(prevdir)
        if dir == prevdir or not dir:
            return path
        names.append(name)
        try:
            if samefile(dir, os.curdir):
                names.reverse()
                return (os.path.join)(*names)
        except OSError:
            pass


try:
    int_or_long = (
     int, long)
    import cStringIO
except NameError:
    int_or_long = int
    import io as cStringIO

def _flatten(x, f):
    if isinstance(x, str):
        f.write('%ds%s' % (len(x), x))
    else:
        if isinstance(x, dict):
            keys = sorted(x.keys())
            f.write('%dd' % len(keys))
            for key in keys:
                _flatten(key, f)
                _flatten(x[key], f)

        else:
            if isinstance(x, (list, tuple)):
                f.write('%dl' % len(x))
                for value in x:
                    _flatten(value, f)

            else:
                if isinstance(x, int_or_long):
                    f.write('%di' % (x,))
                else:
                    raise TypeError('the keywords to verify() contains unsupported object %r' % (x,))


def flatten(x):
    f = cStringIO.StringIO()
    _flatten(x, f)
    return f.getvalue()


def _hack_at_distutils():
    if sys.platform == 'win32':
        try:
            import setuptools
        except ImportError:
            pass