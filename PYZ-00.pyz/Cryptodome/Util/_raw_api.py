# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Util\_raw_api.py
import abc, sys, platform
from Cryptodome.Util.py3compat import byte_string
from Cryptodome.Util._file_system import pycryptodome_filename
if sys.version_info[0] < 3:
    import imp
    extension_suffixes = []
    for ext, mod, typ in imp.get_suffixes():
        if typ == imp.C_EXTENSION:
            extension_suffixes.append(ext)

else:
    from importlib import machinery
    extension_suffixes = machinery.EXTENSION_SUFFIXES
if sys.version_info[0] == 2:
    if sys.version_info[1] < 7:
        _buffer_type = bytearray
    else:
        _buffer_type = (
         bytearray, memoryview)
else:

    class _VoidPointer(object):

        @abc.abstractmethod
        def get(self):
            """Return the memory location we point to"""
            pass

        @abc.abstractmethod
        def address_of(self):
            """Return a raw pointer to this pointer"""
            pass


    try:
        if sys.version_info[0] == 2:
            if sys.version_info[1] < 7:
                raise ImportError('CFFI is only supported with Python 2.7+')
        if platform.python_implementation() != 'PyPy':
            if sys.flags.optimize == 2:
                raise ImportError('CFFI with optimize=2 fails due to pycparser bug.')
        from cffi import FFI
        ffi = FFI()
        null_pointer = ffi.NULL
        uint8_t_type = ffi.typeof(ffi.new('const uint8_t*'))
        _Array = ffi.new('uint8_t[1]').__class__.__bases__

        def load_lib(name, cdecl):
            """Load a shared library and return a handle to it.

        @name,  either an absolute path or the name of a library
                in the system search path.

        @cdecl, the C function declarations.
        """
            lib = ffi.dlopen(name)
            ffi.cdef(cdecl)
            return lib


        def c_ulong(x):
            """Convert a Python integer to unsigned long"""
            return x


        c_ulonglong = c_ulong

        def c_size_t(x):
            """Convert a Python integer to size_t"""
            return x


        def create_string_buffer(init_or_size, size=None):
            """Allocate the given amount of bytes (initially set to 0)"""
            if isinstance(init_or_size, bytes):
                size = max(len(init_or_size) + 1, size)
                result = ffi.new('uint8_t[]', size)
                result[:] = init_or_size
            else:
                if size:
                    raise ValueError('Size must be specified once only')
                result = ffi.new('uint8_t[]', init_or_size)
            return result


        def get_c_string(c_string):
            """Convert a C string into a Python byte sequence"""
            return ffi.string(c_string)


        def get_raw_buffer(buf):
            """Convert a C buffer into a Python byte sequence"""
            return ffi.buffer(buf)[:]


        def c_uint8_ptr(data):
            if isinstance(data, _buffer_type):
                return ffi.cast(uint8_t_type, ffi.from_buffer(data))
            if byte_string(data) or isinstance(data, _Array):
                return data
            raise TypeError('Object type %s cannot be passed to C code' % type(data))


        class VoidPointer_cffi(_VoidPointer):
            __doc__ = 'Model a newly allocated pointer to void'

            def __init__(self):
                self._pp = ffi.new('void *[1]')

            def get(self):
                return self._pp[0]

            def address_of(self):
                return self._pp


        def VoidPointer():
            return VoidPointer_cffi()


        backend = 'cffi'
    except ImportError:
        import ctypes
        from ctypes import CDLL, c_void_p, byref, c_ulong, c_ulonglong, c_size_t, create_string_buffer, c_ubyte
        from ctypes.util import find_library
        from ctypes import Array as _Array
        null_pointer = None

        def load_lib(name, cdecl):
            import platform
            bits, linkage = platform.architecture()
            if '.' not in name:
                if not linkage.startswith('Win'):
                    full_name = find_library(name)
                    if full_name is None:
                        raise OSError("Cannot load library '%s'" % name)
                    name = full_name
            return CDLL(name)


        def get_c_string(c_string):
            return c_string.value


        def get_raw_buffer(buf):
            return buf.raw


        if sys.version_info[0] == 2:
            if sys.version_info[1] == 6:
                _c_ssize_t = c_size_t
        else:
            _c_ssize_t = ctypes.c_ssize_t
        _PyBUF_SIMPLE = 0
        _PyObject_GetBuffer = ctypes.pythonapi.PyObject_GetBuffer
        _py_object = ctypes.py_object
        _c_ssize_p = ctypes.POINTER(_c_ssize_t)

        class _Py_buffer(ctypes.Structure):
            _fields_ = [
             (
              'buf', c_void_p),
             (
              'obj', ctypes.py_object),
             (
              'len', _c_ssize_t),
             (
              'itemsize', _c_ssize_t),
             (
              'readonly', ctypes.c_int),
             (
              'ndim', ctypes.c_int),
             (
              'format', ctypes.c_char_p),
             (
              'shape', _c_ssize_p),
             (
              'strides', _c_ssize_p),
             (
              'suboffsets', _c_ssize_p),
             (
              'internal', c_void_p)]
            if sys.version_info[0] == 2:
                _fields_.insert(-1, ('smalltable', _c_ssize_t * 2))


        def c_uint8_ptr(data):
            if byte_string(data) or isinstance(data, _Array):
                return data
            if isinstance(data, _buffer_type):
                obj = _py_object(data)
                buf = _Py_buffer()
                _PyObject_GetBuffer(obj, byref(buf), _PyBUF_SIMPLE)
                buffer_type = c_ubyte * buf.len
                return buffer_type.from_address(buf.buf)
            raise TypeError('Object type %s cannot be passed to C code' % type(data))


        class VoidPointer_ctypes(_VoidPointer):
            __doc__ = 'Model a newly allocated pointer to void'

            def __init__(self):
                self._p = c_void_p()

            def get(self):
                return self._p

            def address_of(self):
                return byref(self._p)


        def VoidPointer():
            return VoidPointer_ctypes()


        backend = 'ctypes'
        del ctypes

    class SmartPointer(object):
        __doc__ = 'Class to hold a non-managed piece of memory'

        def __init__(self, raw_pointer, destructor):
            self._raw_pointer = raw_pointer
            self._destructor = destructor

        def get(self):
            return self._raw_pointer

        def release(self):
            rp, self._raw_pointer = self._raw_pointer, None
            return rp

        def __del__(self):
            try:
                if self._raw_pointer is not None:
                    self._destructor(self._raw_pointer)
                    self._raw_pointer = None
            except AttributeError:
                pass


    def load_pycryptodome_raw_lib(name, cdecl):
        """Load a shared library and return a handle to it.

    @name,  the name of the library expressed as a PyCryptodome module,
            for instance Cryptodome.Cipher._raw_cbc.

    @cdecl, the C function declarations.
    """
        split = name.split('.')
        dir_comps, basename = split[:-1], split[(-1)]
        attempts = []
        for ext in extension_suffixes:
            try:
                filename = basename + ext
                return load_lib(pycryptodome_filename(dir_comps, filename), cdecl)
            except OSError as exp:
                attempts.append("Trying '%s': %s" % (filename, str(exp)))

        raise OSError("Cannot load native module '%s': %s" % (name, ', '.join(attempts)))


    if sys.version_info[:2] != (2, 6):

        def is_buffer(x):
            """Return True if object x supports the buffer interface"""
            return isinstance(x, (bytes, bytearray, memoryview))


        def is_writeable_buffer(x):
            return isinstance(x, bytearray) or isinstance(x, memoryview) and not x.readonly


    else:

        def is_buffer(x):
            return isinstance(x, (bytes, bytearray))


    def is_writeable_buffer(x):
        return isinstance(x, bytearray)