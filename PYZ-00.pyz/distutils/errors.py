# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: distutils\errors.py
"""distutils.errors

Provides exceptions used by the Distutils modules.  Note that Distutils
modules may raise standard exceptions; in particular, SystemExit is
usually raised for errors that are obviously the end-user's fault
(eg. bad command-line arguments).

This module is safe to use in "from ... import *" mode; it only exports
symbols whose names start with "Distutils" and end with "Error"."""

class DistutilsError(Exception):
    __doc__ = 'The root of all Distutils evil.'


class DistutilsModuleError(DistutilsError):
    __doc__ = 'Unable to load an expected module, or to find an expected class\n    within some module (in particular, command modules and classes).'


class DistutilsClassError(DistutilsError):
    __doc__ = 'Some command class (or possibly distribution class, if anyone\n    feels a need to subclass Distribution) is found not to be holding\n    up its end of the bargain, ie. implementing some part of the\n    "command "interface.'


class DistutilsGetoptError(DistutilsError):
    __doc__ = "The option table provided to 'fancy_getopt()' is bogus."


class DistutilsArgError(DistutilsError):
    __doc__ = 'Raised by fancy_getopt in response to getopt.error -- ie. an\n    error in the command line usage.'


class DistutilsFileError(DistutilsError):
    __doc__ = 'Any problems in the filesystem: expected file not found, etc.\n    Typically this is for problems that we detect before OSError\n    could be raised.'


class DistutilsOptionError(DistutilsError):
    __doc__ = "Syntactic/semantic errors in command options, such as use of\n    mutually conflicting options, or inconsistent options,\n    badly-spelled values, etc.  No distinction is made between option\n    values originating in the setup script, the command line, config\n    files, or what-have-you -- but if we *know* something originated in\n    the setup script, we'll raise DistutilsSetupError instead."


class DistutilsSetupError(DistutilsError):
    __doc__ = "For errors that can be definitely blamed on the setup script,\n    such as invalid keyword arguments to 'setup()'."


class DistutilsPlatformError(DistutilsError):
    __doc__ = "We don't know how to do something on the current platform (but\n    we do know how to do it on some platform) -- eg. trying to compile\n    C files on a platform not supported by a CCompiler subclass."


class DistutilsExecError(DistutilsError):
    __doc__ = 'Any problems executing an external program (such as the C\n    compiler, when compiling C files).'


class DistutilsInternalError(DistutilsError):
    __doc__ = 'Internal inconsistencies or impossibilities (obviously, this\n    should never be seen if the code is working!).'


class DistutilsTemplateError(DistutilsError):
    __doc__ = 'Syntax error in a file list template.'


class DistutilsByteCompileError(DistutilsError):
    __doc__ = 'Byte compile error.'


class CCompilerError(Exception):
    __doc__ = 'Some compile/link operation failed.'


class PreprocessError(CCompilerError):
    __doc__ = 'Failure to preprocess one or more C/C++ files.'


class CompileError(CCompilerError):
    __doc__ = 'Failure to compile one or more C/C++ source files.'


class LibError(CCompilerError):
    __doc__ = 'Failure to create a static library from one or more C/C++ object\n    files.'


class LinkError(CCompilerError):
    __doc__ = 'Failure to link one or more C/C++ object files into an executable\n    or shared library file.'


class UnknownFileError(CCompilerError):
    __doc__ = 'Attempt to process an unknown file type.'