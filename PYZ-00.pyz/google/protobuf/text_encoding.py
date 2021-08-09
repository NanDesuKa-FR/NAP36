# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\google\protobuf\text_encoding.py
"""Encoding related utilities."""
import re, six
_cescape_utf8_to_str = [chr(i) for i in range(0, 256)]
_cescape_utf8_to_str[9] = '\\t'
_cescape_utf8_to_str[10] = '\\n'
_cescape_utf8_to_str[13] = '\\r'
_cescape_utf8_to_str[39] = "\\'"
_cescape_utf8_to_str[34] = '\\"'
_cescape_utf8_to_str[92] = '\\\\'
_cescape_byte_to_str = ['\\%03o' % i for i in range(0, 32)] + [chr(i) for i in range(32, 127)] + ['\\%03o' % i for i in range(127, 256)]
_cescape_byte_to_str[9] = '\\t'
_cescape_byte_to_str[10] = '\\n'
_cescape_byte_to_str[13] = '\\r'
_cescape_byte_to_str[39] = "\\'"
_cescape_byte_to_str[34] = '\\"'
_cescape_byte_to_str[92] = '\\\\'

def CEscape(text, as_utf8):
    """Escape a bytes string for use in an ascii protocol buffer.

  text.encode('string_escape') does not seem to satisfy our needs as it
  encodes unprintable characters using two-digit hex escapes whereas our
  C++ unescaping function allows hex escapes to be any length.  So,
  "\x011".encode('string_escape') ends up being "\\x011", which will be
  decoded in C++ as a single-character string with char code 0x11.

  Args:
    text: A byte string to be escaped
    as_utf8: Specifies if result should be returned in UTF-8 encoding
  Returns:
    Escaped string
  """
    Ord = ord if isinstance(text, six.string_types) else (lambda x: x)
    if as_utf8:
        return ''.join(_cescape_utf8_to_str[Ord(c)] for c in text)
    else:
        return ''.join(_cescape_byte_to_str[Ord(c)] for c in text)


_CUNESCAPE_HEX = re.compile('(\\\\+)x([0-9a-fA-F])(?![0-9a-fA-F])')
_cescape_highbit_to_str = [chr(i) for i in range(0, 127)] + ['\\%03o' % i for i in range(127, 256)]

def CUnescape(text):
    """Unescape a text string with C-style escape sequences to UTF-8 bytes."""

    def ReplaceHex(m):
        if len(m.group(1)) & 1:
            return m.group(1) + 'x0' + m.group(2)
        else:
            return m.group(0)

    result = _CUNESCAPE_HEX.sub(ReplaceHex, text)
    if str is bytes:
        return result.decode('string_escape')
    else:
        result = ''.join(_cescape_highbit_to_str[ord(c)] for c in result)
        return result.encode('ascii').decode('unicode_escape').encode('raw_unicode_escape')