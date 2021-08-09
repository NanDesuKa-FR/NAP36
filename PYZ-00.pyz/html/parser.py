# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: html\parser.py
"""A parser for HTML and XHTML."""
import re, warnings, _markupbase
from html import unescape
__all__ = [
 'HTMLParser']
interesting_normal = re.compile('[&<]')
incomplete = re.compile('&[a-zA-Z#]')
entityref = re.compile('&([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]')
charref = re.compile('&#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]')
starttagopen = re.compile('<[a-zA-Z]')
piclose = re.compile('>')
commentclose = re.compile('--\\s*>')
tagfind_tolerant = re.compile('([a-zA-Z][^\\t\\n\\r\\f />\\x00]*)(?:\\s|/(?!>))*')
attrfind_tolerant = re.compile('((?<=[\\\'"\\s/])[^\\s/>][^\\s/=>]*)(\\s*=+\\s*(\\\'[^\\\']*\\\'|"[^"]*"|(?![\\\'"])[^>\\s]*))?(?:\\s|/(?!>))*')
locatestarttagend_tolerant = re.compile('\n  <[a-zA-Z][^\\t\\n\\r\\f />\\x00]*       # tag name\n  (?:[\\s/]*                          # optional whitespace before attribute name\n    (?:(?<=[\'"\\s/])[^\\s/>][^\\s/=>]*  # attribute name\n      (?:\\s*=+\\s*                    # value indicator\n        (?:\'[^\']*\'                   # LITA-enclosed value\n          |"[^"]*"                   # LIT-enclosed value\n          |(?![\'"])[^>\\s]*           # bare value\n         )\n         (?:\\s*,)*                   # possibly followed by a comma\n       )?(?:\\s|/(?!>))*\n     )*\n   )?\n  \\s*                                # trailing whitespace\n', re.VERBOSE)
endendtag = re.compile('>')
endtagfind = re.compile('</\\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\\s*>')

class HTMLParser(_markupbase.ParserBase):
    __doc__ = 'Find tags and other markup and call handler functions.\n\n    Usage:\n        p = HTMLParser()\n        p.feed(data)\n        ...\n        p.close()\n\n    Start tags are handled by calling self.handle_starttag() or\n    self.handle_startendtag(); end tags by self.handle_endtag().  The\n    data between tags is passed from the parser to the derived class\n    by calling self.handle_data() with the data as argument (the data\n    may be split up in arbitrary chunks).  If convert_charrefs is\n    True the character references are converted automatically to the\n    corresponding Unicode character (and self.handle_data() is no\n    longer split in chunks), otherwise they are passed by calling\n    self.handle_entityref() or self.handle_charref() with the string\n    containing respectively the named or numeric reference as the\n    argument.\n    '
    CDATA_CONTENT_ELEMENTS = ('script', 'style')

    def __init__(self, *, convert_charrefs=True):
        """Initialize and reset this instance.

        If convert_charrefs is True (the default), all character references
        are automatically converted to the corresponding Unicode characters.
        """
        self.convert_charrefs = convert_charrefs
        self.reset()

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.rawdata = ''
        self.lasttag = '???'
        self.interesting = interesting_normal
        self.cdata_elem = None
        _markupbase.ParserBase.reset(self)

    def feed(self, data):
        r"""Feed data to the parser.

        Call this as often as you want, with as little or as much text
        as you want (may include '\n').
        """
        self.rawdata = self.rawdata + data
        self.goahead(0)

    def close(self):
        """Handle any buffered data."""
        self.goahead(1)

    _HTMLParser__starttag_text = None

    def get_starttag_text(self):
        """Return full source of start tag: '<...>'."""
        return self._HTMLParser__starttag_text

    def set_cdata_mode(self, elem):
        self.cdata_elem = elem.lower()
        self.interesting = re.compile('</\\s*%s\\s*>' % self.cdata_elem, re.I)

    def clear_cdata_mode(self):
        self.interesting = interesting_normal
        self.cdata_elem = None

    def goahead(self, end):
        rawdata = self.rawdata
        i = 0
        n = len(rawdata)
        while i < n:
            if self.convert_charrefs:
                if not self.cdata_elem:
                    j = rawdata.find('<', i)
                    if j < 0:
                        amppos = rawdata.rfind('&', max(i, n - 34))
                        if amppos >= 0:
                            if not re.compile('[\\s;]').search(rawdata, amppos):
                                break
                        j = n
                else:
                    match = self.interesting.search(rawdata, i)
                    if match:
                        j = match.start()
                    else:
                        if self.cdata_elem:
                            break
                        j = n
            else:
                if i < j:
                    if self.convert_charrefs:
                        if not self.cdata_elem:
                            self.handle_data(unescape(rawdata[i:j]))
                    else:
                        self.handle_data(rawdata[i:j])
                i = self.updatepos(i, j)
                if i == n:
                    break
            startswith = rawdata.startswith
            if startswith('<', i):
                if starttagopen.match(rawdata, i):
                    k = self.parse_starttag(i)
                else:
                    if startswith('</', i):
                        k = self.parse_endtag(i)
                    else:
                        if startswith('<!--', i):
                            k = self.parse_comment(i)
                        else:
                            if startswith('<?', i):
                                k = self.parse_pi(i)
                            else:
                                if startswith('<!', i):
                                    k = self.parse_html_declaration(i)
                                else:
                                    if i + 1 < n:
                                        self.handle_data('<')
                                        k = i + 1
                                    else:
                                        break
                if k < 0:
                    if not end:
                        break
                    else:
                        k = rawdata.find('>', i + 1)
                        if k < 0:
                            k = rawdata.find('<', i + 1)
                            if k < 0:
                                k = i + 1
                        else:
                            k += 1
                        if self.convert_charrefs and not self.cdata_elem:
                            self.handle_data(unescape(rawdata[i:k]))
                        else:
                            self.handle_data(rawdata[i:k])
                i = self.updatepos(i, k)
            elif startswith('&#', i):
                match = charref.match(rawdata, i)
                if match:
                    name = match.group()[2:-1]
                    self.handle_charref(name)
                    k = match.end()
                    if not startswith(';', k - 1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                else:
                    if ';' in rawdata[i:]:
                        self.handle_data(rawdata[i:i + 2])
                        i = self.updatepos(i, i + 2)
                    break
            elif startswith('&', i):
                match = entityref.match(rawdata, i)
                if match:
                    name = match.group(1)
                    self.handle_entityref(name)
                    k = match.end()
                    if not startswith(';', k - 1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                match = incomplete.match(rawdata, i)
                if match:
                    if end:
                        if match.group() == rawdata[i:]:
                            k = match.end()
                            if k <= i:
                                k = n
                            i = self.updatepos(i, i + 1)
                    break
                else:
                    if i + 1 < n:
                        self.handle_data('&')
                        i = self.updatepos(i, i + 1)
                    else:
                        break
            elif not 0:
                raise AssertionError('interesting.search() lied')

        if end:
            if i < n:
                if not self.cdata_elem:
                    if self.convert_charrefs:
                        if not self.cdata_elem:
                            self.handle_data(unescape(rawdata[i:n]))
                    else:
                        self.handle_data(rawdata[i:n])
                    i = self.updatepos(i, n)
        self.rawdata = rawdata[i:]

    def parse_html_declaration(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] == '<!', 'unexpected call to parse_html_declaration()'
        if rawdata[i:i + 4] == '<!--':
            return self.parse_comment(i)
        if rawdata[i:i + 3] == '<![':
            return self.parse_marked_section(i)
        else:
            if rawdata[i:i + 9].lower() == '<!doctype':
                gtpos = rawdata.find('>', i + 9)
                if gtpos == -1:
                    return -1
                else:
                    self.handle_decl(rawdata[i + 2:gtpos])
                    return gtpos + 1
            return self.parse_bogus_comment(i)

    def parse_bogus_comment(self, i, report=1):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] in ('<!', '</'), 'unexpected call to parse_comment()'
        pos = rawdata.find('>', i + 2)
        if pos == -1:
            return -1
        else:
            if report:
                self.handle_comment(rawdata[i + 2:pos])
            return pos + 1

    def parse_pi(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] == '<?', 'unexpected call to parse_pi()'
        match = piclose.search(rawdata, i + 2)
        if not match:
            return -1
        else:
            j = match.start()
            self.handle_pi(rawdata[i + 2:j])
            j = match.end()
            return j

    def parse_starttag(self, i):
        self._HTMLParser__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        else:
            rawdata = self.rawdata
            self._HTMLParser__starttag_text = rawdata[i:endpos]
            attrs = []
            match = tagfind_tolerant.match(rawdata, i + 1)
            assert match, 'unexpected call to parse_starttag()'
        k = match.end()
        self.lasttag = tag = match.group(1).lower()
        while k < endpos:
            m = attrfind_tolerant.match(rawdata, k)
            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            if not rest:
                attrvalue = None
            else:
                if attrvalue[:1] == "'" == attrvalue[-1:] or attrvalue[:1] == '"' == attrvalue[-1:]:
                    attrvalue = attrvalue[1:-1]
            if attrvalue:
                attrvalue = unescape(attrvalue)
            attrs.append((attrname.lower(), attrvalue))
            k = m.end()

        end = rawdata[k:endpos].strip()
        if end not in ('>', '/>'):
            lineno, offset = self.getpos()
            if '\n' in self._HTMLParser__starttag_text:
                lineno = lineno + self._HTMLParser__starttag_text.count('\n')
                offset = len(self._HTMLParser__starttag_text) - self._HTMLParser__starttag_text.rfind('\n')
            else:
                offset = offset + len(self._HTMLParser__starttag_text)
            self.handle_data(rawdata[i:endpos])
            return endpos
        else:
            if end.endswith('/>'):
                self.handle_startendtag(tag, attrs)
            else:
                self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)
            return endpos

    def check_for_whole_start_tag(self, i):
        rawdata = self.rawdata
        m = locatestarttagend_tolerant.match(rawdata, i)
        if m:
            j = m.end()
            next = rawdata[j:j + 1]
            if next == '>':
                return j + 1
            if next == '/':
                if rawdata.startswith('/>', j):
                    return j + 2
                else:
                    if rawdata.startswith('/', j):
                        return -1
                    if j > i:
                        return j
                    return i + 1
            if next == '':
                return -1
            if next in 'abcdefghijklmnopqrstuvwxyz=/ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                return -1
            else:
                if j > i:
                    return j
                return i + 1
        raise AssertionError('we should not get here!')

    def parse_endtag(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] == '</', 'unexpected call to parse_endtag'
        match = endendtag.search(rawdata, i + 1)
        if not match:
            return -1
        gtpos = match.end()
        match = endtagfind.match(rawdata, i)
        if not match:
            if self.cdata_elem is not None:
                self.handle_data(rawdata[i:gtpos])
                return gtpos
            namematch = tagfind_tolerant.match(rawdata, i + 2)
            if not namematch:
                if rawdata[i:i + 3] == '</>':
                    return i + 3
                else:
                    return self.parse_bogus_comment(i)
            tagname = namematch.group(1).lower()
            gtpos = rawdata.find('>', namematch.end())
            self.handle_endtag(tagname)
            return gtpos + 1
        else:
            elem = match.group(1).lower()
            if self.cdata_elem is not None:
                if elem != self.cdata_elem:
                    self.handle_data(rawdata[i:gtpos])
                    return gtpos
            self.handle_endtag(elem.lower())
            self.clear_cdata_mode()
            return gtpos

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_charref(self, name):
        pass

    def handle_entityref(self, name):
        pass

    def handle_data(self, data):
        pass

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):
        pass

    def unescape(self, s):
        warnings.warn('The unescape method is deprecated and will be removed in 3.5, use html.unescape() instead.', DeprecationWarning,
          stacklevel=2)
        return unescape(s)