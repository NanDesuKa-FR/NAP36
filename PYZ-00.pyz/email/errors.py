# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: email\errors.py
"""email package exception classes."""

class MessageError(Exception):
    __doc__ = 'Base class for errors in the email package.'


class MessageParseError(MessageError):
    __doc__ = 'Base class for message parsing errors.'


class HeaderParseError(MessageParseError):
    __doc__ = 'Error while parsing headers.'


class BoundaryError(MessageParseError):
    __doc__ = "Couldn't find terminating boundary."


class MultipartConversionError(MessageError, TypeError):
    __doc__ = 'Conversion to a multipart is prohibited.'


class CharsetError(MessageError):
    __doc__ = 'An illegal charset was given.'


class MessageDefect(ValueError):
    __doc__ = 'Base class for a message defect.'

    def __init__(self, line=None):
        if line is not None:
            super().__init__(line)
        self.line = line


class NoBoundaryInMultipartDefect(MessageDefect):
    __doc__ = 'A message claimed to be a multipart but had no boundary parameter.'


class StartBoundaryNotFoundDefect(MessageDefect):
    __doc__ = 'The claimed start boundary was never found.'


class CloseBoundaryNotFoundDefect(MessageDefect):
    __doc__ = 'A start boundary was found, but not the corresponding close boundary.'


class FirstHeaderLineIsContinuationDefect(MessageDefect):
    __doc__ = 'A message had a continuation line as its first header line.'


class MisplacedEnvelopeHeaderDefect(MessageDefect):
    __doc__ = "A 'Unix-from' header was found in the middle of a header block."


class MissingHeaderBodySeparatorDefect(MessageDefect):
    __doc__ = 'Found line with no leading whitespace and no colon before blank line.'


MalformedHeaderDefect = MissingHeaderBodySeparatorDefect

class MultipartInvariantViolationDefect(MessageDefect):
    __doc__ = 'A message claimed to be a multipart but no subparts were found.'


class InvalidMultipartContentTransferEncodingDefect(MessageDefect):
    __doc__ = 'An invalid content transfer encoding was set on the multipart itself.'


class UndecodableBytesDefect(MessageDefect):
    __doc__ = 'Header contained bytes that could not be decoded'


class InvalidBase64PaddingDefect(MessageDefect):
    __doc__ = 'base64 encoded sequence had an incorrect length'


class InvalidBase64CharactersDefect(MessageDefect):
    __doc__ = 'base64 encoded sequence had characters not in base64 alphabet'


class HeaderDefect(MessageDefect):
    __doc__ = 'Base class for a header defect.'

    def __init__(self, *args, **kw):
        (super().__init__)(*args, **kw)


class InvalidHeaderDefect(HeaderDefect):
    __doc__ = 'Header is not valid, message gives details.'


class HeaderMissingRequiredValue(HeaderDefect):
    __doc__ = 'A header that must have a value had none'


class NonPrintableDefect(HeaderDefect):
    __doc__ = 'ASCII characters outside the ascii-printable range found'

    def __init__(self, non_printables):
        super().__init__(non_printables)
        self.non_printables = non_printables

    def __str__(self):
        return 'the following ASCII non-printables found in header: {}'.format(self.non_printables)


class ObsoleteHeaderDefect(HeaderDefect):
    __doc__ = 'Header uses syntax declared obsolete by RFC 5322'


class NonASCIILocalPartDefect(HeaderDefect):
    __doc__ = 'local_part contains non-ASCII characters'