# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\py31compat.py
__all__ = [
 'get_config_vars', 'get_path']
try:
    from sysconfig import get_config_vars, get_path
except ImportError:
    from distutils.sysconfig import get_config_vars, get_python_lib

    def get_path(name):
        if name not in ('platlib', 'purelib'):
            raise ValueError('Name must be purelib or platlib')
        return get_python_lib(name == 'platlib')


try:
    from tempfile import TemporaryDirectory
except ImportError:
    import shutil, tempfile

    class TemporaryDirectory(object):
        __doc__ = '\n        Very simple temporary directory context manager.\n        Will try to delete afterward, but will also ignore OS and similar\n        errors on deletion.\n        '

        def __init__(self):
            self.name = None
            self.name = tempfile.mkdtemp()

        def __enter__(self):
            return self.name

        def __exit__(self, exctype, excvalue, exctrace):
            try:
                shutil.rmtree(self.name, True)
            except OSError:
                pass

            self.name = None