# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: cgi.py
"""Support module for CGI (Common Gateway Interface) scripts.

This module defines a number of utilities for use by CGI scripts
written in Python.
"""
__version__ = '2.6'
from io import StringIO, BytesIO, TextIOWrapper
from collections import Mapping
import sys, os, urllib.parse
from email.parser import FeedParser
from email.message import Message
from warnings import warn
import html, locale, tempfile
__all__ = [
 'MiniFieldStorage', 'FieldStorage',
 'parse', 'parse_qs', 'parse_qsl', 'parse_multipart',
 'parse_header', 'test', 'print_exception', 'print_environ',
 'print_form', 'print_directory', 'print_arguments',
 'print_environ_usage', 'escape']
logfile = ''
logfp = None

def initlog(*allargs):
    """Write a log message, if there is a log file.

    Even though this function is called initlog(), you should always
    use log(); log is a variable that is set either to initlog
    (initially), to dolog (once the log file has been opened), or to
    nolog (when logging is disabled).

    The first argument is a format string; the remaining arguments (if
    any) are arguments to the % operator, so e.g.
        log("%s: %s", "a", "b")
    will write "a: b" to the log file, followed by a newline.

    If the global logfp is not None, it should be a file object to
    which log data is written.

    If the global logfp is None, the global logfile may be a string
    giving a filename to open, in append mode.  This file should be
    world writable!!!  If the file can't be opened, logging is
    silently disabled (since there is no safe place where we could
    send an error message).

    """
    global log
    global logfile
    global logfp
    if logfile:
        if not logfp:
            try:
                logfp = open(logfile, 'a')
            except OSError:
                pass

        log = logfp or nolog
    else:
        log = dolog
    log(*allargs)


def dolog(fmt, *args):
    """Write a log message to the log file.  See initlog() for docs."""
    logfp.write(fmt % args + '\n')


def nolog(*allargs):
    """Dummy function, assigned to log when logging is disabled."""
    pass


def closelog():
    """Close the log file."""
    global log
    global logfile
    global logfp
    logfile = ''
    if logfp:
        logfp.close()
        logfp = None
    log = initlog


log = initlog
maxlen = 0

def parse(fp=None, environ=os.environ, keep_blank_values=0, strict_parsing=0):
    """Parse a query in the environment or from a file (default stdin)

        Arguments, all optional:

        fp              : file pointer; default: sys.stdin.buffer

        environ         : environment dictionary; default: os.environ

        keep_blank_values: flag indicating whether blank values in
            percent-encoded forms should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.

        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.
    """
    global maxlen
    if fp is None:
        fp = sys.stdin
    else:
        if hasattr(fp, 'encoding'):
            encoding = fp.encoding
        else:
            encoding = 'latin-1'
        if isinstance(fp, TextIOWrapper):
            fp = fp.buffer
        if 'REQUEST_METHOD' not in environ:
            environ['REQUEST_METHOD'] = 'GET'
        if environ['REQUEST_METHOD'] == 'POST':
            ctype, pdict = parse_header(environ['CONTENT_TYPE'])
            if ctype == 'multipart/form-data':
                return parse_multipart(fp, pdict)
            if ctype == 'application/x-www-form-urlencoded':
                clength = int(environ['CONTENT_LENGTH'])
                if maxlen:
                    if clength > maxlen:
                        raise ValueError('Maximum content length exceeded')
                qs = fp.read(clength).decode(encoding)
            else:
                qs = ''
            if 'QUERY_STRING' in environ:
                if qs:
                    qs = qs + '&'
                qs = qs + environ['QUERY_STRING']
            else:
                if sys.argv[1:]:
                    if qs:
                        qs = qs + '&'
                    qs = qs + sys.argv[1]
            environ['QUERY_STRING'] = qs
        else:
            if 'QUERY_STRING' in environ:
                qs = environ['QUERY_STRING']
            else:
                if sys.argv[1:]:
                    qs = sys.argv[1]
                else:
                    qs = ''
                environ['QUERY_STRING'] = qs
    return urllib.parse.parse_qs(qs, keep_blank_values, strict_parsing, encoding=encoding)


def parse_qs(qs, keep_blank_values=0, strict_parsing=0):
    """Parse a query given as a string argument."""
    warn('cgi.parse_qs is deprecated, use urllib.parse.parse_qs instead', DeprecationWarning, 2)
    return urllib.parse.parse_qs(qs, keep_blank_values, strict_parsing)


def parse_qsl(qs, keep_blank_values=0, strict_parsing=0):
    """Parse a query given as a string argument."""
    warn('cgi.parse_qsl is deprecated, use urllib.parse.parse_qsl instead', DeprecationWarning, 2)
    return urllib.parse.parse_qsl(qs, keep_blank_values, strict_parsing)


def parse_multipart(fp, pdict):
    """Parse multipart input.

    Arguments:
    fp   : input file
    pdict: dictionary containing other parameters of content-type header

    Returns a dictionary just like parse_qs(): keys are the field names, each
    value is a list of values for that field.  This is easy to use but not
    much good if you are expecting megabytes to be uploaded -- in that case,
    use the FieldStorage class instead which is much more flexible.  Note
    that content-type is the raw, unparsed contents of the content-type
    header.

    XXX This does not parse nested multipart parts -- use FieldStorage for
    that.

    XXX This should really be subsumed by FieldStorage altogether -- no
    point in having two implementations of the same parsing algorithm.
    Also, FieldStorage protects itself better against certain DoS attacks
    by limiting the size of the data read in one chunk.  The API here
    does not support that kind of protection.  This also affects parse()
    since it can call parse_multipart().

    """
    import http.client
    boundary = b''
    if 'boundary' in pdict:
        boundary = pdict['boundary']
    if not valid_boundary(boundary):
        raise ValueError('Invalid boundary in multipart form: %r' % (
         boundary,))
    nextpart = b'--' + boundary
    lastpart = b'--' + boundary + b'--'
    partdict = {}
    terminator = b''
    while terminator != lastpart:
        bytes = -1
        data = None
        if terminator:
            headers = http.client.parse_headers(fp)
            clength = headers.get('content-length')
            if clength:
                try:
                    bytes = int(clength)
                except ValueError:
                    pass

            if bytes > 0:
                if maxlen:
                    if bytes > maxlen:
                        raise ValueError('Maximum content length exceeded')
                data = fp.read(bytes)
            else:
                data = b''
        lines = []
        while True:
            line = fp.readline()
            if not line:
                terminator = lastpart
                break
            if line.startswith(b'--'):
                terminator = line.rstrip()
                if terminator in (nextpart, lastpart):
                    break
            lines.append(line)

        if data is None:
            continue
        if bytes < 0:
            if lines:
                line = lines[(-1)]
                if line[-2:] == b'\r\n':
                    line = line[:-2]
                else:
                    if line[-1:] == b'\n':
                        line = line[:-1]
                    lines[-1] = line
                    data = (b'').join(lines)
                line = headers['content-disposition']
                if not line:
                    continue
                key, params = parse_header(line)
                if key != 'form-data':
                    continue
                if 'name' in params:
                    name = params['name']
            else:
                continue
        if name in partdict:
            partdict[name].append(data)
        else:
            partdict[name] = [
             data]

    return partdict


def _parseparam(s):
    while s[:1] == ';':
        s = s[1:]
        end = s.find(';')
        while end > 0 and (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
            end = s.find(';', end + 1)

        if end < 0:
            end = len(s)
        f = s[:end]
        yield f.strip()
        s = s[end:]


def parse_header(line):
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    """
    parts = _parseparam(';' + line)
    key = parts.__next__()
    pdict = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1:].strip()
            if len(value) >= 2:
                if value[0] == value[(-1)] == '"':
                    value = value[1:-1]
                    value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value

    return (
     key, pdict)


class MiniFieldStorage:
    __doc__ = 'Like FieldStorage, for use when no file uploads are possible.'
    filename = None
    list = None
    type = None
    file = None
    type_options = {}
    disposition = None
    disposition_options = {}
    headers = {}

    def __init__(self, name, value):
        """Constructor from field name and value."""
        self.name = name
        self.value = value

    def __repr__(self):
        """Return printable representation."""
        return 'MiniFieldStorage(%r, %r)' % (self.name, self.value)


class FieldStorage:
    __doc__ = "Store a sequence of fields, reading multipart/form-data.\n\n    This class provides naming, typing, files stored on disk, and\n    more.  At the top level, it is accessible like a dictionary, whose\n    keys are the field names.  (Note: None can occur as a field name.)\n    The items are either a Python list (if there's multiple values) or\n    another FieldStorage or MiniFieldStorage object.  If it's a single\n    object, it has the following attributes:\n\n    name: the field name, if specified; otherwise None\n\n    filename: the filename, if specified; otherwise None; this is the\n        client side filename, *not* the file name on which it is\n        stored (that's a temporary file you don't deal with)\n\n    value: the value as a *string*; for file uploads, this\n        transparently reads the file every time you request the value\n        and returns *bytes*\n\n    file: the file(-like) object from which you can read the data *as\n        bytes* ; None if the data is stored a simple string\n\n    type: the content-type, or None if not specified\n\n    type_options: dictionary of options specified on the content-type\n        line\n\n    disposition: content-disposition, or None if not specified\n\n    disposition_options: dictionary of corresponding options\n\n    headers: a dictionary(-like) object (sometimes email.message.Message or a\n        subclass thereof) containing *all* headers\n\n    The class is subclassable, mostly for the purpose of overriding\n    the make_file() method, which is called internally to come up with\n    a file open for reading and writing.  This makes it possible to\n    override the default choice of storing all files in a temporary\n    directory and unlinking them as soon as they have been opened.\n\n    "

    def __init__(self, fp=None, headers=None, outerboundary=b'', environ=os.environ, keep_blank_values=0, strict_parsing=0, limit=None, encoding='utf-8', errors='replace'):
        """Constructor.  Read multipart/* until last part.

        Arguments, all optional:

        fp              : file pointer; default: sys.stdin.buffer
            (not used when the request method is GET)
            Can be :
            1. a TextIOWrapper object
            2. an object whose read() and readline() methods return bytes

        headers         : header dictionary-like object; default:
            taken from environ as per CGI spec

        outerboundary   : terminating multipart boundary
            (for internal use only)

        environ         : environment dictionary; default: os.environ

        keep_blank_values: flag indicating whether blank values in
            percent-encoded forms should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.

        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.

        limit : used internally to read parts of multipart/form-data forms,
            to exit from the reading loop when reached. It is the difference
            between the form content-length and the number of bytes already
            read

        encoding, errors : the encoding and error handler used to decode the
            binary stream to strings. Must be the same as the charset defined
            for the page sending the form (content-type : meta http-equiv or
            header)

        """
        method = 'GET'
        self.keep_blank_values = keep_blank_values
        self.strict_parsing = strict_parsing
        if 'REQUEST_METHOD' in environ:
            method = environ['REQUEST_METHOD'].upper()
        self.qs_on_post = None
        if method == 'GET' or method == 'HEAD':
            if 'QUERY_STRING' in environ:
                qs = environ['QUERY_STRING']
            else:
                if sys.argv[1:]:
                    qs = sys.argv[1]
                else:
                    qs = ''
                qs = qs.encode(locale.getpreferredencoding(), 'surrogateescape')
                fp = BytesIO(qs)
                if headers is None:
                    headers = {'content-type': 'application/x-www-form-urlencoded'}
        if headers is None:
            headers = {}
            if method == 'POST':
                headers['content-type'] = 'application/x-www-form-urlencoded'
            if 'CONTENT_TYPE' in environ:
                headers['content-type'] = environ['CONTENT_TYPE']
            if 'QUERY_STRING' in environ:
                self.qs_on_post = environ['QUERY_STRING']
            if 'CONTENT_LENGTH' in environ:
                headers['content-length'] = environ['CONTENT_LENGTH']
        else:
            if not isinstance(headers, (Mapping, Message)):
                raise TypeError('headers must be mapping or an instance of email.message.Message')
            else:
                self.headers = headers
                if fp is None:
                    self.fp = sys.stdin.buffer
                else:
                    if isinstance(fp, TextIOWrapper):
                        self.fp = fp.buffer
                    else:
                        if not (hasattr(fp, 'read') and hasattr(fp, 'readline')):
                            raise TypeError('fp must be file pointer')
                        self.fp = fp
                self.encoding = encoding
                self.errors = errors
                if not isinstance(outerboundary, bytes):
                    raise TypeError('outerboundary must be bytes, not %s' % type(outerboundary).__name__)
                self.outerboundary = outerboundary
                self.bytes_read = 0
                self.limit = limit
                cdisp, pdict = '', {}
                if 'content-disposition' in self.headers:
                    cdisp, pdict = parse_header(self.headers['content-disposition'])
            self.disposition = cdisp
            self.disposition_options = pdict
            self.name = None
        if 'name' in pdict:
            self.name = pdict['name']
        else:
            self.filename = None
            if 'filename' in pdict:
                self.filename = pdict['filename']
            self._binary_file = self.filename is not None
            if 'content-type' in self.headers:
                ctype, pdict = parse_header(self.headers['content-type'])
            else:
                if self.outerboundary or method != 'POST':
                    ctype, pdict = 'text/plain', {}
                else:
                    ctype, pdict = 'application/x-www-form-urlencoded', {}
                self.type = ctype
                self.type_options = pdict
                if 'boundary' in pdict:
                    self.innerboundary = pdict['boundary'].encode(self.encoding)
                else:
                    self.innerboundary = b''
                clen = -1
                if 'content-length' in self.headers:
                    try:
                        clen = int(self.headers['content-length'])
                    except ValueError:
                        pass

                    if maxlen:
                        if clen > maxlen:
                            raise ValueError('Maximum content length exceeded')
                self.length = clen
                if self.limit is None:
                    if clen:
                        self.limit = clen
                self.list = self.file = None
                self.done = 0
                if ctype == 'application/x-www-form-urlencoded':
                    self.read_urlencoded()
                else:
                    if ctype[:10] == 'multipart/':
                        self.read_multi(environ, keep_blank_values, strict_parsing)
                    else:
                        self.read_single()

    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.file.close()

    def __repr__(self):
        """Return a printable representation."""
        return 'FieldStorage(%r, %r, %r)' % (
         self.name, self.filename, self.value)

    def __iter__(self):
        return iter(self.keys())

    def __getattr__(self, name):
        if name != 'value':
            raise AttributeError(name)
        else:
            if self.file:
                self.file.seek(0)
                value = self.file.read()
                self.file.seek(0)
            else:
                if self.list is not None:
                    value = self.list
                else:
                    value = None
        return value

    def __getitem__(self, key):
        """Dictionary style indexing."""
        if self.list is None:
            raise TypeError('not indexable')
        found = []
        for item in self.list:
            if item.name == key:
                found.append(item)

        if not found:
            raise KeyError(key)
        if len(found) == 1:
            return found[0]
        else:
            return found

    def getvalue(self, key, default=None):
        """Dictionary style get() method, including 'value' lookup."""
        if key in self:
            value = self[key]
            if isinstance(value, list):
                return [x.value for x in value]
            else:
                return value.value
        else:
            return default

    def getfirst(self, key, default=None):
        """ Return the first value received."""
        if key in self:
            value = self[key]
            if isinstance(value, list):
                return value[0].value
            else:
                return value.value
        else:
            return default

    def getlist(self, key):
        """ Return list of received values."""
        if key in self:
            value = self[key]
            if isinstance(value, list):
                return [x.value for x in value]
            else:
                return [
                 value.value]
        else:
            return []

    def keys(self):
        """Dictionary style keys() method."""
        if self.list is None:
            raise TypeError('not indexable')
        return list(set(item.name for item in self.list))

    def __contains__(self, key):
        """Dictionary style __contains__ method."""
        if self.list is None:
            raise TypeError('not indexable')
        return any(item.name == key for item in self.list)

    def __len__(self):
        """Dictionary style len(x) support."""
        return len(self.keys())

    def __bool__(self):
        if self.list is None:
            raise TypeError('Cannot be converted to bool.')
        return bool(self.list)

    def read_urlencoded(self):
        """Internal: read data in query string format."""
        qs = self.fp.read(self.length)
        if not isinstance(qs, bytes):
            raise ValueError('%s should return bytes, got %s' % (
             self.fp, type(qs).__name__))
        qs = qs.decode(self.encoding, self.errors)
        if self.qs_on_post:
            qs += '&' + self.qs_on_post
        self.list = []
        query = urllib.parse.parse_qsl(qs,
          (self.keep_blank_values), (self.strict_parsing), encoding=(self.encoding),
          errors=(self.errors))
        for key, value in query:
            self.list.append(MiniFieldStorage(key, value))

        self.skip_lines()

    FieldStorageClass = None

    def read_multi(self, environ, keep_blank_values, strict_parsing):
        """Internal: read a part that is itself multipart."""
        ib = self.innerboundary
        if not valid_boundary(ib):
            raise ValueError('Invalid boundary in multipart form: %r' % (ib,))
        self.list = []
        if self.qs_on_post:
            query = urllib.parse.parse_qsl((self.qs_on_post),
              (self.keep_blank_values), (self.strict_parsing), encoding=(self.encoding),
              errors=(self.errors))
            for key, value in query:
                self.list.append(MiniFieldStorage(key, value))

        klass = self.FieldStorageClass or self.__class__
        first_line = self.fp.readline()
        if not isinstance(first_line, bytes):
            raise ValueError('%s should return bytes, got %s' % (
             self.fp, type(first_line).__name__))
        self.bytes_read += len(first_line)
        while first_line.strip() != b'--' + self.innerboundary and first_line:
            first_line = self.fp.readline()
            self.bytes_read += len(first_line)

        while 1:
            parser = FeedParser()
            hdr_text = b''
            while 1:
                data = self.fp.readline()
                hdr_text += data
                if not data.strip():
                    break

            if not hdr_text:
                break
            self.bytes_read += len(hdr_text)
            parser.feed(hdr_text.decode(self.encoding, self.errors))
            headers = parser.close()
            if 'content-length' in headers:
                del headers['content-length']
            part = klass(self.fp, headers, ib, environ, keep_blank_values, strict_parsing, self.limit - self.bytes_read, self.encoding, self.errors)
            self.bytes_read += part.bytes_read
            self.list.append(part)
            if not part.done:
                if self.bytes_read >= self.length > 0:
                    break

        self.skip_lines()

    def read_single(self):
        """Internal: read an atomic part."""
        if self.length >= 0:
            self.read_binary()
            self.skip_lines()
        else:
            self.read_lines()
        self.file.seek(0)

    bufsize = 8192

    def read_binary(self):
        """Internal: read binary data."""
        self.file = self.make_file()
        todo = self.length
        if todo >= 0:
            while todo > 0:
                data = self.fp.read(min(todo, self.bufsize))
                if not isinstance(data, bytes):
                    raise ValueError('%s should return bytes, got %s' % (
                     self.fp, type(data).__name__))
                self.bytes_read += len(data)
                if not data:
                    self.done = -1
                    break
                self.file.write(data)
                todo = todo - len(data)

    def read_lines(self):
        """Internal: read lines until EOF or outerboundary."""
        if self._binary_file:
            self.file = self._FieldStorage__file = BytesIO()
        else:
            self.file = self._FieldStorage__file = StringIO()
        if self.outerboundary:
            self.read_lines_to_outerboundary()
        else:
            self.read_lines_to_eof()

    def __write(self, line):
        """line is always bytes, not string"""
        if self._FieldStorage__file is not None:
            if self._FieldStorage__file.tell() + len(line) > 1000:
                self.file = self.make_file()
                data = self._FieldStorage__file.getvalue()
                self.file.write(data)
                self._FieldStorage__file = None
        else:
            if self._binary_file:
                self.file.write(line)
            else:
                self.file.write(line.decode(self.encoding, self.errors))

    def read_lines_to_eof(self):
        """Internal: read lines until EOF."""
        while True:
            line = self.fp.readline(65536)
            self.bytes_read += len(line)
            if not line:
                self.done = -1
                break
            self._FieldStorage__write(line)

    def read_lines_to_outerboundary(self):
        """Internal: read lines until outerboundary.
        Data is read as bytes: boundaries and line ends must be converted
        to bytes for comparisons.
        """
        next_boundary = b'--' + self.outerboundary
        last_boundary = next_boundary + b'--'
        delim = b''
        last_line_lfend = True
        _read = 0
        while True:
            if _read >= self.limit:
                break
            else:
                line = self.fp.readline(65536)
                self.bytes_read += len(line)
                _read += len(line)
                if not line:
                    self.done = -1
                    break
                if delim == b'\r':
                    line = delim + line
                    delim = b''
                if line.startswith(b'--'):
                    if last_line_lfend:
                        strippedline = line.rstrip()
                        if strippedline == next_boundary:
                            break
                        if strippedline == last_boundary:
                            self.done = 1
                            break
                odelim = delim
                if line.endswith(b'\r\n'):
                    delim = b'\r\n'
                    line = line[:-2]
                    last_line_lfend = True
                else:
                    if line.endswith(b'\n'):
                        delim = b'\n'
                        line = line[:-1]
                        last_line_lfend = True
                    else:
                        if line.endswith(b'\r'):
                            delim = b'\r'
                            line = line[:-1]
                            last_line_lfend = False
                        else:
                            delim = b''
                            last_line_lfend = False
            self._FieldStorage__write(odelim + line)

    def skip_lines(self):
        """Internal: skip lines until outer boundary if defined."""
        if not self.outerboundary or self.done:
            return
        next_boundary = b'--' + self.outerboundary
        last_boundary = next_boundary + b'--'
        last_line_lfend = True
        while True:
            line = self.fp.readline(65536)
            self.bytes_read += len(line)
            if not line:
                self.done = -1
                break
            if line.endswith(b'--'):
                if last_line_lfend:
                    strippedline = line.strip()
                    if strippedline == next_boundary:
                        break
                    if strippedline == last_boundary:
                        self.done = 1
                        break
            last_line_lfend = line.endswith(b'\n')

    def make_file(self):
        """Overridable: return a readable & writable file.

        The file will be used as follows:
        - data is written to it
        - seek(0)
        - data is read from it

        The file is opened in binary mode for files, in text mode
        for other fields

        This version opens a temporary file for reading and writing,
        and immediately deletes (unlinks) it.  The trick (on Unix!) is
        that the file can still be used, but it can't be opened by
        another process, and it will automatically be deleted when it
        is closed or when the current process terminates.

        If you want a more permanent file, you derive a class which
        overrides this method.  If you want a visible temporary file
        that is nevertheless automatically deleted when the script
        terminates, try defining a __del__ method in a derived class
        which unlinks the temporary files you have created.

        """
        if self._binary_file:
            return tempfile.TemporaryFile('wb+')
        else:
            return tempfile.TemporaryFile('w+', encoding=(self.encoding),
              newline='\n')


def test(environ=os.environ):
    """Robust test CGI script, usable as main program.

    Write minimal HTTP headers and dump all information provided to
    the script in HTML form.

    """
    global maxlen
    print('Content-type: text/html')
    print()
    sys.stderr = sys.stdout
    try:
        form = FieldStorage()
        print_directory()
        print_arguments()
        print_form(form)
        print_environ(environ)
        print_environ_usage()

        def f():
            exec('testing print_exception() -- <I>italics?</I>')

        def g(f=f):
            f()

        print('<H3>What follows is a test, not an actual exception:</H3>')
        g()
    except:
        print_exception()

    print('<H1>Second try with a small maxlen...</H1>')
    maxlen = 50
    try:
        form = FieldStorage()
        print_directory()
        print_arguments()
        print_form(form)
        print_environ(environ)
    except:
        print_exception()


def print_exception(type=None, value=None, tb=None, limit=None):
    if type is None:
        type, value, tb = sys.exc_info()
    import traceback
    print()
    print('<H3>Traceback (most recent call last):</H3>')
    list = traceback.format_tb(tb, limit) + traceback.format_exception_only(type, value)
    print('<PRE>%s<B>%s</B></PRE>' % (
     html.escape(''.join(list[:-1])),
     html.escape(list[(-1)])))
    del tb


def print_environ(environ=os.environ):
    """Dump the shell environment as HTML."""
    keys = sorted(environ.keys())
    print()
    print('<H3>Shell Environment:</H3>')
    print('<DL>')
    for key in keys:
        print('<DT>', html.escape(key), '<DD>', html.escape(environ[key]))

    print('</DL>')
    print()


def print_form(form):
    """Dump the contents of a form as HTML."""
    keys = sorted(form.keys())
    print()
    print('<H3>Form Contents:</H3>')
    if not keys:
        print('<P>No form fields.')
    print('<DL>')
    for key in keys:
        print(('<DT>' + html.escape(key) + ':'), end=' ')
        value = form[key]
        print('<i>' + html.escape(repr(type(value))) + '</i>')
        print('<DD>' + html.escape(repr(value)))

    print('</DL>')
    print()


def print_directory():
    """Dump the current directory as HTML."""
    print()
    print('<H3>Current Working Directory:</H3>')
    try:
        pwd = os.getcwd()
    except OSError as msg:
        print('OSError:', html.escape(str(msg)))
    else:
        print(html.escape(pwd))
    print()


def print_arguments():
    print()
    print('<H3>Command Line Arguments:</H3>')
    print()
    print(sys.argv)
    print()


def print_environ_usage():
    """Dump a list of environment variables used by CGI as HTML."""
    print('\n<H3>These environment variables could have been set:</H3>\n<UL>\n<LI>AUTH_TYPE\n<LI>CONTENT_LENGTH\n<LI>CONTENT_TYPE\n<LI>DATE_GMT\n<LI>DATE_LOCAL\n<LI>DOCUMENT_NAME\n<LI>DOCUMENT_ROOT\n<LI>DOCUMENT_URI\n<LI>GATEWAY_INTERFACE\n<LI>LAST_MODIFIED\n<LI>PATH\n<LI>PATH_INFO\n<LI>PATH_TRANSLATED\n<LI>QUERY_STRING\n<LI>REMOTE_ADDR\n<LI>REMOTE_HOST\n<LI>REMOTE_IDENT\n<LI>REMOTE_USER\n<LI>REQUEST_METHOD\n<LI>SCRIPT_NAME\n<LI>SERVER_NAME\n<LI>SERVER_PORT\n<LI>SERVER_PROTOCOL\n<LI>SERVER_ROOT\n<LI>SERVER_SOFTWARE\n</UL>\nIn addition, HTTP headers sent by the server may be passed in the\nenvironment as well.  Here are some common variable names:\n<UL>\n<LI>HTTP_ACCEPT\n<LI>HTTP_CONNECTION\n<LI>HTTP_HOST\n<LI>HTTP_PRAGMA\n<LI>HTTP_REFERER\n<LI>HTTP_USER_AGENT\n</UL>\n')


def escape(s, quote=None):
    """Deprecated API."""
    warn('cgi.escape is deprecated, use html.escape instead', DeprecationWarning,
      stacklevel=2)
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    if quote:
        s = s.replace('"', '&quot;')
    return s


def valid_boundary(s):
    import re
    if isinstance(s, bytes):
        _vb_pattern = b'^[ -~]{0,200}[!-~]$'
    else:
        _vb_pattern = '^[ -~]{0,200}[!-~]$'
    return re.match(_vb_pattern, s)


if __name__ == '__main__':
    test()