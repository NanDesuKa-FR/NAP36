# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\extension.py
import re, functools, distutils.core, distutils.errors, distutils.extension
from setuptools.extern.six.moves import map
from .monkey import get_unpatched

def _have_cython():
    """
    Return True if Cython can be imported.
    """
    cython_impl = 'Cython.Distutils.build_ext'
    try:
        __import__(cython_impl, fromlist=['build_ext']).build_ext
        return True
    except Exception:
        pass

    return False


have_pyrex = _have_cython
_Extension = get_unpatched(distutils.core.Extension)

class Extension(_Extension):
    __doc__ = "Extension that uses '.c' files in place of '.pyx' files"

    def __init__(self, name, sources, *args, **kw):
        self.py_limited_api = kw.pop('py_limited_api', False)
        (_Extension.__init__)(self, name, sources, *args, **kw)

    def _convert_pyx_sources_to_lang(self):
        """
        Replace sources with .pyx extensions to sources with the target
        language extension. This mechanism allows language authors to supply
        pre-converted sources but to prefer the .pyx sources.
        """
        if _have_cython():
            return
        lang = self.language or ''
        target_ext = '.cpp' if lang.lower() == 'c++' else '.c'
        sub = functools.partial(re.sub, '.pyx$', target_ext)
        self.sources = list(map(sub, self.sources))


class Library(Extension):
    __doc__ = 'Just like a regular Extension, but built as a library instead'