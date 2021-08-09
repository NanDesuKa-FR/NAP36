# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\google\protobuf\internal\api_implementation.py
"""Determine which implementation of the protobuf API is used in this process.
"""
import os, warnings, sys
try:
    from google.protobuf.internal import _api_implementation
    _api_version = _api_implementation.api_version
    _proto_extension_modules_exist_in_build = True
except ImportError:
    _api_version = -1
    _proto_extension_modules_exist_in_build = False

if _api_version == 1:
    raise ValueError('api_version=1 is no longer supported.')
if _api_version < 0:
    try:
        from google.protobuf import _use_fast_cpp_protos
        if not _use_fast_cpp_protos:
            raise ImportError('_use_fast_cpp_protos import succeeded but was None')
        del _use_fast_cpp_protos
        _api_version = 2
    except ImportError:
        try:
            from google.protobuf.internal import use_pure_python
            del use_pure_python
        except ImportError:
            pass

_default_implementation_type = 'python' if _api_version <= 0 else 'cpp'
_implementation_type = os.getenv('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION', _default_implementation_type)
if _implementation_type != 'python':
    _implementation_type = 'cpp'
if 'PyPy' in sys.version:
    if _implementation_type == 'cpp':
        warnings.warn('PyPy does not work yet with cpp protocol buffers. Falling back to the python implementation.')
        _implementation_type = 'python'
_implementation_version_str = os.getenv('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION', '2')
if _implementation_version_str != '2':
    raise ValueError('unsupported PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION: "' + _implementation_version_str + '" (supported versions: 2)')
_implementation_version = int(_implementation_version_str)
try:
    from google.protobuf import enable_deterministic_proto_serialization
    _python_deterministic_proto_serialization = True
except ImportError:
    _python_deterministic_proto_serialization = False

def Type():
    return _implementation_type


def Version():
    return _implementation_version


def IsPythonDefaultSerializationDeterministic():
    return _python_deterministic_proto_serialization


if _implementation_type == 'cpp':
    try:
        from google.protobuf.pyext import _message

        def GetPythonProto3PreserveUnknownsDefault():
            return _message.GetPythonProto3PreserveUnknownsDefault()


        def SetPythonProto3PreserveUnknownsDefault(preserve):
            _message.SetPythonProto3PreserveUnknownsDefault(preserve)


    except ImportError:
        pass

else:
    _python_proto3_preserve_unknowns_default = True

    def GetPythonProto3PreserveUnknownsDefault():
        global _python_proto3_preserve_unknowns_default
        return _python_proto3_preserve_unknowns_default


    def SetPythonProto3PreserveUnknownsDefault(preserve):
        global _python_proto3_preserve_unknowns_default
        _python_proto3_preserve_unknowns_default = preserve