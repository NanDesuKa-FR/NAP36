# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cffi\commontypes.py
import sys
from . import model
from .error import FFIError
COMMON_TYPES = {}
try:
    from _cffi_backend import _get_common_types
    _get_common_types(COMMON_TYPES)
except ImportError:
    pass

COMMON_TYPES['FILE'] = model.unknown_type('FILE', '_IO_FILE')
COMMON_TYPES['bool'] = '_Bool'
for _type in model.PrimitiveType.ALL_PRIMITIVE_TYPES:
    if _type.endswith('_t'):
        COMMON_TYPES[_type] = _type

del _type
_CACHE = {}

def resolve_common_type(parser, commontype):
    try:
        return _CACHE[commontype]
    except KeyError:
        cdecl = COMMON_TYPES.get(commontype, commontype)
        if not isinstance(cdecl, str):
            result, quals = cdecl, 0
        else:
            if cdecl in model.PrimitiveType.ALL_PRIMITIVE_TYPES:
                result, quals = model.PrimitiveType(cdecl), 0
            else:
                if cdecl == 'set-unicode-needed':
                    raise FFIError('The Windows type %r is only available after you call ffi.set_unicode()' % (
                     commontype,))
                else:
                    if commontype == cdecl:
                        raise FFIError('Unsupported type: %r.  Please look at http://cffi.readthedocs.io/en/latest/cdef.html#ffi-cdef-limitations and file an issue if you think this type should really be supported.' % (
                         commontype,))
                    result, quals = parser.parse_type_and_quals(cdecl)
        assert isinstance(result, model.BaseTypeByIdentity)
        _CACHE[commontype] = (result, quals)
        return (result, quals)


def win_common_types():
    return {'UNICODE_STRING':model.StructType('_UNICODE_STRING', [
      'Length',
      'MaximumLength',
      'Buffer'], [
      model.PrimitiveType('unsigned short'),
      model.PrimitiveType('unsigned short'),
      model.PointerType(model.PrimitiveType('wchar_t'))], [
      -1, -1, -1]), 
     'PUNICODE_STRING':'UNICODE_STRING *', 
     'PCUNICODE_STRING':'const UNICODE_STRING *', 
     'TBYTE':'set-unicode-needed', 
     'TCHAR':'set-unicode-needed', 
     'LPCTSTR':'set-unicode-needed', 
     'PCTSTR':'set-unicode-needed', 
     'LPTSTR':'set-unicode-needed', 
     'PTSTR':'set-unicode-needed', 
     'PTBYTE':'set-unicode-needed', 
     'PTCHAR':'set-unicode-needed'}


if sys.platform == 'win32':
    COMMON_TYPES.update(win_common_types())