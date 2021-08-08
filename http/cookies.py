# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: http\cookies.py
r"""
Here's a sample session to show how to use this module.
At the moment, this is the only documentation.

The Basics
----------

Importing is easy...

   >>> from http import cookies

Most of the time you start by creating a cookie.

   >>> C = cookies.SimpleCookie()

Once you've created your Cookie, you can add values just as if it were
a dictionary.

   >>> C = cookies.SimpleCookie()
   >>> C["fig"] = "newton"
   >>> C["sugar"] = "wafer"
   >>> C.output()
   'Set-Cookie: fig=newton\r\nSet-Cookie: sugar=wafer'

Notice that the printable representation of a Cookie is the
appropriate format for a Set-Cookie: header.  This is the
default behavior.  You can change the header and printed
attributes by using the .output() function

   >>> C = cookies.SimpleCookie()
   >>> C["rocky"] = "road"
   >>> C["rocky"]["path"] = "/cookie"
   >>> print(C.output(header="Cookie:"))
   Cookie: rocky=road; Path=/cookie
   >>> print(C.output(attrs=[], header="Cookie:"))
   Cookie: rocky=road

The load() method of a Cookie extracts cookies from a string.  In a
CGI script, you would use this method to extract the cookies from the
HTTP_COOKIE environment variable.

   >>> C = cookies.SimpleCookie()
   >>> C.load("chips=ahoy; vienna=finger")
   >>> C.output()
   'Set-Cookie: chips=ahoy\r\nSet-Cookie: vienna=finger'

The load() method is darn-tootin smart about identifying cookies
within a string.  Escaped quotation marks, nested semicolons, and other
such trickeries do not confuse it.

   >>> C = cookies.SimpleCookie()
   >>> C.load('keebler="E=everybody; L=\\"Loves\\"; fudge=\\012;";')
   >>> print(C)
   Set-Cookie: keebler="E=everybody; L=\"Loves\"; fudge=\012;"

Each element of the Cookie also supports all of the RFC 2109
Cookie attributes.  Here's an example which sets the Path
attribute.

   >>> C = cookies.SimpleCookie()
   >>> C["oreo"] = "doublestuff"
   >>> C["oreo"]["path"] = "/"
   >>> print(C)
   Set-Cookie: oreo=doublestuff; Path=/

Each dictionary element has a 'value' attribute, which gives you
back the value associated with the key.

   >>> C = cookies.SimpleCookie()
   >>> C["twix"] = "none for you"
   >>> C["twix"].value
   'none for you'

The SimpleCookie expects that all values should be standard strings.
Just to be sure, SimpleCookie invokes the str() builtin to convert
the value to a string, when the values are set dictionary-style.

   >>> C = cookies.SimpleCookie()
   >>> C["number"] = 7
   >>> C["string"] = "seven"
   >>> C["number"].value
   '7'
   >>> C["string"].value
   'seven'
   >>> C.output()
   'Set-Cookie: number=7\r\nSet-Cookie: string=seven'

Finis.
"""
import re, string
__all__ = [
 'CookieError', 'BaseCookie', 'SimpleCookie']
_nulljoin = ''.join
_semispacejoin = '; '.join
_spacejoin = ' '.join

def _warn_deprecated_setter(setter):
    import warnings
    msg = 'The .%s setter is deprecated. The attribute will be read-only in future releases. Please use the set() method instead.' % setter
    warnings.warn(msg, DeprecationWarning, stacklevel=3)


class CookieError(Exception):
    pass


_LegalChars = string.ascii_letters + string.digits + "!#$%&'*+-.^_`|~:"
_UnescapedChars = _LegalChars + ' ()/<=>?@[]{}'
_Translator = {n:'\\%03o' % n for n in set(range(256)) - set(map(ord, _UnescapedChars))}
_Translator.update({ord('"'): '\\"', 
 ord('\\'): '\\\\'})
_is_legal_key = re.compile('[%s]+' % re.escape(_LegalChars)).fullmatch

def _quote(str):
    r"""Quote a string for use in a cookie header.

    If the string does not need to be double-quoted, then just return the
    string.  Otherwise, surround the string in doublequotes and quote
    (with a \) special characters.
    """
    if str is None or _is_legal_key(str):
        return str
    else:
        return '"' + str.translate(_Translator) + '"'


_OctalPatt = re.compile('\\\\[0-3][0-7][0-7]')
_QuotePatt = re.compile('[\\\\].')

def _unquote(str):
    if str is None or len(str) < 2:
        return str
    else:
        if str[0] != '"' or str[(-1)] != '"':
            return str
        str = str[1:-1]
        i = 0
        n = len(str)
        res = []
        while 0 <= i < n:
            o_match = _OctalPatt.search(str, i)
            q_match = _QuotePatt.search(str, i)
            if not o_match:
                if not q_match:
                    res.append(str[i:])
                    break
            j = k = -1
            if o_match:
                j = o_match.start(0)
            if q_match:
                k = q_match.start(0)
            if q_match and (not o_match or k < j):
                res.append(str[i:k])
                res.append(str[(k + 1)])
                i = k + 2
            else:
                res.append(str[i:j])
                res.append(chr(int(str[j + 1:j + 4], 8)))
                i = j + 4

        return _nulljoin(res)


_weekdayname = [
 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
_monthname = [
 None,
 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def _getdate(future=0, weekdayname=_weekdayname, monthname=_monthname):
    from time import gmtime, time
    now = time()
    year, month, day, hh, mm, ss, wd, y, z = gmtime(now + future)
    return '%s, %02d %3s %4d %02d:%02d:%02d GMT' % (
     weekdayname[wd], day, monthname[month], year, hh, mm, ss)


class Morsel(dict):
    __doc__ = 'A class to hold ONE (key, value) pair.\n\n    In a cookie, each such pair may have several attributes, so this class is\n    used to keep the attributes associated with the appropriate key,value pair.\n    This class also includes a coded_value attribute, which is used to hold\n    the network representation of the value.  This is most useful when Python\n    objects are pickled for network transit.\n    '
    _reserved = {'expires':'expires', 
     'path':'Path', 
     'comment':'Comment', 
     'domain':'Domain', 
     'max-age':'Max-Age', 
     'secure':'Secure', 
     'httponly':'HttpOnly', 
     'version':'Version'}
    _flags = {
     'secure', 'httponly'}

    def __init__(self):
        self._key = self._value = self._coded_value = None
        for key in self._reserved:
            dict.__setitem__(self, key, '')

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        _warn_deprecated_setter('key')
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        _warn_deprecated_setter('value')
        self._value = value

    @property
    def coded_value(self):
        return self._coded_value

    @coded_value.setter
    def coded_value(self, coded_value):
        _warn_deprecated_setter('coded_value')
        self._coded_value = coded_value

    def __setitem__(self, K, V):
        K = K.lower()
        if K not in self._reserved:
            raise CookieError('Invalid attribute %r' % (K,))
        dict.__setitem__(self, K, V)

    def setdefault(self, key, val=None):
        key = key.lower()
        if key not in self._reserved:
            raise CookieError('Invalid attribute %r' % (key,))
        return dict.setdefault(self, key, val)

    def __eq__(self, morsel):
        if not isinstance(morsel, Morsel):
            return NotImplemented
        else:
            return dict.__eq__(self, morsel) and self._value == morsel._value and self._key == morsel._key and self._coded_value == morsel._coded_value

    __ne__ = object.__ne__

    def copy(self):
        morsel = Morsel()
        dict.update(morsel, self)
        morsel.__dict__.update(self.__dict__)
        return morsel

    def update(self, values):
        data = {}
        for key, val in dict(values).items():
            key = key.lower()
            if key not in self._reserved:
                raise CookieError('Invalid attribute %r' % (key,))
            data[key] = val

        dict.update(self, data)

    def isReservedKey(self, K):
        return K.lower() in self._reserved

    def set(self, key, val, coded_val, LegalChars=_LegalChars):
        if LegalChars != _LegalChars:
            import warnings
            warnings.warn('LegalChars parameter is deprecated, ignored and will be removed in future versions.',
              DeprecationWarning,
              stacklevel=2)
        else:
            if key.lower() in self._reserved:
                raise CookieError('Attempt to set a reserved key %r' % (key,))
            raise _is_legal_key(key) or CookieError('Illegal key %r' % (key,))
        self._key = key
        self._value = val
        self._coded_value = coded_val

    def __getstate__(self):
        return {'key':self._key, 
         'value':self._value, 
         'coded_value':self._coded_value}

    def __setstate__(self, state):
        self._key = state['key']
        self._value = state['value']
        self._coded_value = state['coded_value']

    def output(self, attrs=None, header='Set-Cookie:'):
        return '%s %s' % (header, self.OutputString(attrs))

    __str__ = output

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.OutputString())

    def js_output(self, attrs=None):
        return '\n        <script type="text/javascript">\n        <!-- begin hiding\n        document.cookie = "%s";\n        // end hiding -->\n        </script>\n        ' % self.OutputString(attrs).replace('"', '\\"')

    def OutputString(self, attrs=None):
        result = []
        append = result.append
        append('%s=%s' % (self.key, self.coded_value))
        if attrs is None:
            attrs = self._reserved
        items = sorted(self.items())
        for key, value in items:
            if value == '':
                pass
            elif key not in attrs:
                continue
            if key == 'expires' and isinstance(value, int):
                append('%s=%s' % (self._reserved[key], _getdate(value)))
            elif key == 'max-age':
                if isinstance(value, int):
                    append('%s=%d' % (self._reserved[key], value))
            else:
                if key in self._flags:
                    if value:
                        append(str(self._reserved[key]))
                else:
                    append('%s=%s' % (self._reserved[key], value))

        return _semispacejoin(result)


_LegalKeyChars = "\\w\\d!#%&'~_`><@,:/\\$\\*\\+\\-\\.\\^\\|\\)\\(\\?\\}\\{\\="
_LegalValueChars = _LegalKeyChars + '\\[\\]'
_CookiePattern = re.compile("\n    \\s*                            # Optional whitespace at start of cookie\n    (?P<key>                       # Start of group 'key'\n    [" + _LegalKeyChars + ']+?   # Any word of at least one letter\n    )                              # End of group \'key\'\n    (                              # Optional group: there may not be a value.\n    \\s*=\\s*                          # Equal Sign\n    (?P<val>                         # Start of group \'val\'\n    "(?:[^\\\\"]|\\\\.)*"                  # Any doublequoted string\n    |                                  # or\n    \\w{3},\\s[\\w\\d\\s-]{9,11}\\s[\\d:]{8}\\sGMT  # Special case for "expires" attr\n    |                                  # or\n    [' + _LegalValueChars + "]*      # Any word or empty string\n    )                                # End of group 'val'\n    )?                             # End of optional value group\n    \\s*                            # Any number of spaces.\n    (\\s+|;|$)                      # Ending either at space, semicolon, or EOS.\n    ", re.ASCII | re.VERBOSE)

class BaseCookie(dict):
    __doc__ = 'A container class for a set of Morsels.'

    def value_decode(self, val):
        """real_value, coded_value = value_decode(STRING)
        Called prior to setting a cookie's value from the network
        representation.  The VALUE is the value read from HTTP
        header.
        Override this function to modify the behavior of cookies.
        """
        return (
         val, val)

    def value_encode(self, val):
        """real_value, coded_value = value_encode(VALUE)
        Called prior to setting a cookie's value from the dictionary
        representation.  The VALUE is the value being assigned.
        Override this function to modify the behavior of cookies.
        """
        strval = str(val)
        return (strval, strval)

    def __init__(self, input=None):
        if input:
            self.load(input)

    def __set(self, key, real_value, coded_value):
        """Private method for setting a cookie's value"""
        M = self.get(key, Morsel())
        M.set(key, real_value, coded_value)
        dict.__setitem__(self, key, M)

    def __setitem__(self, key, value):
        """Dictionary style assignment."""
        if isinstance(value, Morsel):
            dict.__setitem__(self, key, value)
        else:
            rval, cval = self.value_encode(value)
            self._BaseCookie__set(key, rval, cval)

    def output(self, attrs=None, header='Set-Cookie:', sep='\r\n'):
        """Return a string suitable for HTTP."""
        result = []
        items = sorted(self.items())
        for key, value in items:
            result.append(value.output(attrs, header))

        return sep.join(result)

    __str__ = output

    def __repr__(self):
        l = []
        items = sorted(self.items())
        for key, value in items:
            l.append('%s=%s' % (key, repr(value.value)))

        return '<%s: %s>' % (self.__class__.__name__, _spacejoin(l))

    def js_output(self, attrs=None):
        """Return a string suitable for JavaScript."""
        result = []
        items = sorted(self.items())
        for key, value in items:
            result.append(value.js_output(attrs))

        return _nulljoin(result)

    def load(self, rawdata):
        """Load cookies from a string (presumably HTTP_COOKIE) or
        from a dictionary.  Loading cookies from a dictionary 'd'
        is equivalent to calling:
            map(Cookie.__setitem__, d.keys(), d.values())
        """
        if isinstance(rawdata, str):
            self._BaseCookie__parse_string(rawdata)
        else:
            for key, value in rawdata.items():
                self[key] = value

    def __parse_string(self, str, patt=_CookiePattern):
        i = 0
        n = len(str)
        parsed_items = []
        morsel_seen = False
        TYPE_ATTRIBUTE = 1
        TYPE_KEYVALUE = 2
        while 0 <= i < n:
            match = patt.match(str, i)
            if not match:
                break
            key, value = match.group('key'), match.group('val')
            i = match.end(0)
            if key[0] == '$':
                if not morsel_seen:
                    pass
                else:
                    parsed_items.append((TYPE_ATTRIBUTE, key[1:], value))
            elif key.lower() in Morsel._reserved:
                if not morsel_seen:
                    return
                else:
                    if value is None:
                        if key.lower() in Morsel._flags:
                            parsed_items.append((TYPE_ATTRIBUTE, key, True))
                        else:
                            return
                    else:
                        parsed_items.append((TYPE_ATTRIBUTE, key, _unquote(value)))
            else:
                if value is not None:
                    parsed_items.append((TYPE_KEYVALUE, key, self.value_decode(value)))
                    morsel_seen = True
                else:
                    return

        M = None
        for tp, key, value in parsed_items:
            if tp == TYPE_ATTRIBUTE:
                assert M is not None
                M[key] = value
            else:
                assert tp == TYPE_KEYVALUE
                rval, cval = value
                self._BaseCookie__set(key, rval, cval)
                M = self[key]


class SimpleCookie(BaseCookie):
    __doc__ = '\n    SimpleCookie supports strings as cookie values.  When setting\n    the value using the dictionary assignment notation, SimpleCookie\n    calls the builtin str() to convert the value to a string.  Values\n    received from HTTP are kept as strings.\n    '

    def value_decode(self, val):
        return (_unquote(val), val)

    def value_encode(self, val):
        strval = str(val)
        return (strval, _quote(strval))