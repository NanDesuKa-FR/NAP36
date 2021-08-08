# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\cffi\error.py


class FFIError(Exception):
    pass


class CDefError(Exception):

    def __str__(self):
        try:
            current_decl = self.args[1]
            filename = current_decl.coord.file
            linenum = current_decl.coord.line
            prefix = '%s:%d: ' % (filename, linenum)
        except (AttributeError, TypeError, IndexError):
            prefix = ''

        return '%s%s' % (prefix, self.args[0])


class VerificationError(Exception):
    __doc__ = ' An error raised when verification fails\n    '


class VerificationMissing(Exception):
    __doc__ = ' An error raised when incomplete structures are passed into\n    cdef, but no verification has been done\n    '