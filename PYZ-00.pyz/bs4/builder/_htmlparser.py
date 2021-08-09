# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\bs4\builder\_htmlparser.py
"""Use the HTMLParser library to parse HTML files that aren't too bad."""
__license__ = 'MIT'
__all__ = [
 'HTMLParserTreeBuilder']
from html.parser import HTMLParser
try:
    from html.parser import HTMLParseError
except ImportError as e:

    class HTMLParseError(Exception):
        pass


import sys, warnings
major, minor, release = sys.version_info[:3]
CONSTRUCTOR_TAKES_STRICT = major == 3 and minor == 2 and release >= 3
CONSTRUCTOR_STRICT_IS_DEPRECATED = major == 3 and minor == 3
CONSTRUCTOR_TAKES_CONVERT_CHARREFS = major == 3 and minor >= 4
from bs4.element import CData, Comment, Declaration, Doctype, ProcessingInstruction
from bs4.dammit import EntitySubstitution, UnicodeDammit
from bs4.builder import HTML, HTMLTreeBuilder, STRICT
HTMLPARSER = 'html.parser'

class BeautifulSoupHTMLParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        (HTMLParser.__init__)(self, *args, **kwargs)
        self.already_closed_empty_element = []

    def error(self, msg):
        """In Python 3, HTMLParser subclasses must implement error(), although this
        requirement doesn't appear to be documented.

        In Python 2, HTMLParser implements error() as raising an exception.

        In any event, this method is called only on very strange markup and our best strategy
        is to pretend it didn't happen and keep going.
        """
        warnings.warn(msg)

    def handle_startendtag(self, name, attrs):
        tag = self.handle_starttag(name, attrs, handle_empty_element=False)
        self.handle_endtag(name)

    def handle_starttag(self, name, attrs, handle_empty_element=True):
        attr_dict = {}
        for key, value in attrs:
            if value is None:
                value = ''
            attr_dict[key] = value
            attrvalue = '""'

        tag = self.soup.handle_starttag(name, None, None, attr_dict)
        if tag:
            if tag.is_empty_element:
                if handle_empty_element:
                    self.handle_endtag(name, check_already_closed=False)
                    self.already_closed_empty_element.append(name)

    def handle_endtag(self, name, check_already_closed=True):
        if check_already_closed:
            if name in self.already_closed_empty_element:
                self.already_closed_empty_element.remove(name)
        else:
            self.soup.handle_endtag(name)

    def handle_data(self, data):
        self.soup.handle_data(data)

    def handle_charref(self, name):
        if name.startswith('x'):
            real_name = int(name.lstrip('x'), 16)
        else:
            if name.startswith('X'):
                real_name = int(name.lstrip('X'), 16)
            else:
                real_name = int(name)
        data = None
        if real_name < 256:
            for encoding in (self.soup.original_encoding, 'windows-1252'):
                if not encoding:
                    pass
                else:
                    try:
                        data = bytearray([real_name]).decode(encoding)
                    except UnicodeDecodeError as e:
                        pass

        if not data:
            try:
                data = chr(real_name)
            except (ValueError, OverflowError) as e:
                pass

        data = data or '�'
        self.handle_data(data)

    def handle_entityref(self, name):
        character = EntitySubstitution.HTML_ENTITY_TO_CHARACTER.get(name)
        if character is not None:
            data = character
        else:
            data = '&%s' % name
        self.handle_data(data)

    def handle_comment(self, data):
        self.soup.endData()
        self.soup.handle_data(data)
        self.soup.endData(Comment)

    def handle_decl(self, data):
        self.soup.endData()
        if data.startswith('DOCTYPE '):
            data = data[len('DOCTYPE '):]
        else:
            if data == 'DOCTYPE':
                data = ''
        self.soup.handle_data(data)
        self.soup.endData(Doctype)

    def unknown_decl(self, data):
        if data.upper().startswith('CDATA['):
            cls = CData
            data = data[len('CDATA['):]
        else:
            cls = Declaration
        self.soup.endData()
        self.soup.handle_data(data)
        self.soup.endData(cls)

    def handle_pi(self, data):
        self.soup.endData()
        self.soup.handle_data(data)
        self.soup.endData(ProcessingInstruction)


class HTMLParserTreeBuilder(HTMLTreeBuilder):
    is_xml = False
    picklable = True
    NAME = HTMLPARSER
    features = [NAME, HTML, STRICT]

    def __init__(self, *args, **kwargs):
        if CONSTRUCTOR_TAKES_STRICT:
            if not CONSTRUCTOR_STRICT_IS_DEPRECATED:
                kwargs['strict'] = False
        if CONSTRUCTOR_TAKES_CONVERT_CHARREFS:
            kwargs['convert_charrefs'] = False
        self.parser_args = (
         args, kwargs)

    def prepare_markup(self, markup, user_specified_encoding=None, document_declared_encoding=None, exclude_encodings=None):
        """
        :return: A 4-tuple (markup, original encoding, encoding
        declared within markup, whether any characters had to be
        replaced with REPLACEMENT CHARACTER).
        """
        if isinstance(markup, str):
            yield (
             markup, None, None, False)
            return
        try_encodings = [user_specified_encoding, document_declared_encoding]
        dammit = UnicodeDammit(markup, try_encodings, is_html=True, exclude_encodings=exclude_encodings)
        yield (dammit.markup, dammit.original_encoding,
         dammit.declared_html_encoding,
         dammit.contains_replacement_characters)

    def feed(self, markup):
        args, kwargs = self.parser_args
        parser = BeautifulSoupHTMLParser(*args, **kwargs)
        parser.soup = self.soup
        try:
            parser.feed(markup)
            parser.close()
        except HTMLParseError as e:
            warnings.warn(RuntimeWarning("Python's built-in HTMLParser cannot parse the given document. This is not a bug in Beautiful Soup. The best solution is to install an external parser (lxml or html5lib), and use Beautiful Soup with that parser. See http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser for help."))
            raise e

        parser.already_closed_empty_element = []


if major == 3:
    if minor == 2:
        if not CONSTRUCTOR_TAKES_STRICT:
            import re
            attrfind_tolerant = re.compile('\\s*((?<=[\\\'"\\s])[^\\s/>][^\\s/=>]*)(\\s*=+\\s*(\\\'[^\\\']*\\\'|"[^"]*"|(?![\\\'"])[^>\\s]*))?')
            HTMLParserTreeBuilder.attrfind_tolerant = attrfind_tolerant
            locatestarttagend = re.compile('\n  <[a-zA-Z][-.a-zA-Z0-9:_]*          # tag name\n  (?:\\s+                             # whitespace before attribute name\n    (?:[a-zA-Z_][-.:a-zA-Z0-9_]*     # attribute name\n      (?:\\s*=\\s*                     # value indicator\n        (?:\'[^\']*\'                   # LITA-enclosed value\n          |\\"[^\\"]*\\"                # LIT-enclosed value\n          |[^\'\\">\\s]+                # bare value\n         )\n       )?\n     )\n   )*\n  \\s*                                # trailing whitespace\n', re.VERBOSE)
            BeautifulSoupHTMLParser.locatestarttagend = locatestarttagend
            from html.parser import tagfind, attrfind

            def parse_starttag(self, i):
                self.__starttag_text = None
                endpos = self.check_for_whole_start_tag(i)
                if endpos < 0:
                    return endpos
                else:
                    rawdata = self.rawdata
                    self.__starttag_text = rawdata[i:endpos]
                    attrs = []
                    match = tagfind.match(rawdata, i + 1)
                    assert match, 'unexpected call to parse_starttag()'
                k = match.end()
                self.lasttag = tag = rawdata[i + 1:k].lower()
                while k < endpos:
                    if self.strict:
                        m = attrfind.match(rawdata, k)
                    else:
                        m = attrfind_tolerant.match(rawdata, k)
                    if not m:
                        break
                    attrname, rest, attrvalue = m.group(1, 2, 3)
                    if not rest:
                        attrvalue = None
                    elif not attrvalue[:1] == "'" == attrvalue[-1:]:
                        if attrvalue[:1] == '"' == attrvalue[-1:]:
                            attrvalue = attrvalue[1:-1]
                    if attrvalue:
                        attrvalue = self.unescape(attrvalue)
                    attrs.append((attrname.lower(), attrvalue))
                    k = m.end()

                end = rawdata[k:endpos].strip()
                if end not in ('>', '/>'):
                    lineno, offset = self.getpos()
                    if '\n' in self.__starttag_text:
                        lineno = lineno + self.__starttag_text.count('\n')
                        offset = len(self.__starttag_text) - self.__starttag_text.rfind('\n')
                    else:
                        offset = offset + len(self.__starttag_text)
                    if self.strict:
                        self.error('junk characters in start tag: %r' % (
                         rawdata[k:endpos][:20],))
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


            def set_cdata_mode(self, elem):
                self.cdata_elem = elem.lower()
                self.interesting = re.compile('</\\s*%s\\s*>' % self.cdata_elem, re.I)


            BeautifulSoupHTMLParser.parse_starttag = parse_starttag
            BeautifulSoupHTMLParser.set_cdata_mode = set_cdata_mode
            CONSTRUCTOR_TAKES_STRICT = True