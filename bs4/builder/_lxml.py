# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\bs4\builder\_lxml.py
__license__ = 'MIT'
__all__ = [
 'LXMLTreeBuilderForXML',
 'LXMLTreeBuilder']
try:
    from collections.abc import Callable
except ImportError as e:
    from collections import Callable

from io import BytesIO
from io import StringIO
from lxml import etree
from bs4.element import Comment, Doctype, NamespacedAttribute, ProcessingInstruction, XMLProcessingInstruction
from bs4.builder import FAST, HTML, HTMLTreeBuilder, PERMISSIVE, ParserRejectedMarkup, TreeBuilder, XML
from bs4.dammit import EncodingDetector
LXML = 'lxml'

def _invert(d):
    """Invert a dictionary."""
    return dict((v, k) for k, v in list(d.items()))


class LXMLTreeBuilderForXML(TreeBuilder):
    DEFAULT_PARSER_CLASS = etree.XMLParser
    is_xml = True
    processing_instruction_class = XMLProcessingInstruction
    NAME = 'lxml-xml'
    ALTERNATE_NAMES = ['xml']
    features = [
     NAME, LXML, XML, FAST, PERMISSIVE]
    CHUNK_SIZE = 512
    DEFAULT_NSMAPS = dict(xml='http://www.w3.org/XML/1998/namespace')
    DEFAULT_NSMAPS_INVERTED = _invert(DEFAULT_NSMAPS)

    def initialize_soup(self, soup):
        super(LXMLTreeBuilderForXML, self).initialize_soup(soup)
        self._register_namespaces(self.DEFAULT_NSMAPS)

    def _register_namespaces(self, mapping):
        """Let the BeautifulSoup object know about namespaces encountered
        while parsing the document.

        This might be useful later on when creating CSS selectors.
        """
        for key, value in list(mapping.items()):
            if key and key not in self.soup._namespaces:
                self.soup._namespaces[key] = value

    def default_parser(self, encoding):
        if self._default_parser is not None:
            return self._default_parser
        else:
            return etree.XMLParser(target=self,
              strip_cdata=False,
              recover=True,
              encoding=encoding)

    def parser_for(self, encoding):
        parser = self.default_parser(encoding)
        if isinstance(parser, Callable):
            parser = parser(target=self, strip_cdata=False, encoding=encoding)
        return parser

    def __init__(self, parser=None, empty_element_tags=None):
        self._default_parser = parser
        if empty_element_tags is not None:
            self.empty_element_tags = set(empty_element_tags)
        self.soup = None
        self.nsmaps = [self.DEFAULT_NSMAPS_INVERTED]

    def _getNsTag(self, tag):
        if tag[0] == '{':
            return tuple(tag[1:].split('}', 1))
        else:
            return (
             None, tag)

    def prepare_markup(self, markup, user_specified_encoding=None, exclude_encodings=None, document_declared_encoding=None):
        """
        :yield: A series of 4-tuples.
         (markup, encoding, declared encoding,
          has undergone character replacement)

        Each 4-tuple represents a strategy for parsing the document.
        """
        is_html = not self.is_xml
        if is_html:
            self.processing_instruction_class = ProcessingInstruction
        else:
            self.processing_instruction_class = XMLProcessingInstruction
        if isinstance(markup, str):
            yield (
             markup, None, document_declared_encoding, False)
        if isinstance(markup, str):
            yield (
             markup.encode('utf8'), 'utf8',
             document_declared_encoding, False)
        try_encodings = [user_specified_encoding, document_declared_encoding]
        detector = EncodingDetector(markup, try_encodings, is_html, exclude_encodings)
        for encoding in detector.encodings:
            yield (
             detector.markup, encoding, document_declared_encoding, False)

    def feed(self, markup):
        if isinstance(markup, bytes):
            markup = BytesIO(markup)
        else:
            if isinstance(markup, str):
                markup = StringIO(markup)
        data = markup.read(self.CHUNK_SIZE)
        try:
            self.parser = self.parser_for(self.soup.original_encoding)
            self.parser.feed(data)
            while len(data) != 0:
                data = markup.read(self.CHUNK_SIZE)
                if len(data) != 0:
                    self.parser.feed(data)

            self.parser.close()
        except (UnicodeDecodeError, LookupError, etree.ParserError) as e:
            raise ParserRejectedMarkup(str(e))

    def close(self):
        self.nsmaps = [self.DEFAULT_NSMAPS_INVERTED]

    def start(self, name, attrs, nsmap={}):
        attrs = dict(attrs)
        nsprefix = None
        if len(nsmap) == 0:
            if len(self.nsmaps) > 1:
                self.nsmaps.append(None)
        if len(nsmap) > 0:
            self._register_namespaces(nsmap)
            self.nsmaps.append(_invert(nsmap))
            attrs = attrs.copy()
            for prefix, namespace in list(nsmap.items()):
                attribute = NamespacedAttribute('xmlns', prefix, 'http://www.w3.org/2000/xmlns/')
                attrs[attribute] = namespace

        new_attrs = {}
        for attr, value in list(attrs.items()):
            namespace, attr = self._getNsTag(attr)
            if namespace is None:
                new_attrs[attr] = value
            else:
                nsprefix = self._prefix_for_namespace(namespace)
                attr = NamespacedAttribute(nsprefix, attr, namespace)
                new_attrs[attr] = value

        attrs = new_attrs
        namespace, name = self._getNsTag(name)
        nsprefix = self._prefix_for_namespace(namespace)
        self.soup.handle_starttag(name, namespace, nsprefix, attrs)

    def _prefix_for_namespace(self, namespace):
        """Find the currently active prefix for the given namespace."""
        if namespace is None:
            return
        for inverted_nsmap in reversed(self.nsmaps):
            if inverted_nsmap is not None:
                if namespace in inverted_nsmap:
                    return inverted_nsmap[namespace]

    def end(self, name):
        self.soup.endData()
        completed_tag = self.soup.tagStack[(-1)]
        namespace, name = self._getNsTag(name)
        nsprefix = None
        if namespace is not None:
            for inverted_nsmap in reversed(self.nsmaps):
                if inverted_nsmap is not None:
                    if namespace in inverted_nsmap:
                        nsprefix = inverted_nsmap[namespace]
                        break

        self.soup.handle_endtag(name, nsprefix)
        if len(self.nsmaps) > 1:
            self.nsmaps.pop()

    def pi(self, target, data):
        self.soup.endData()
        self.soup.handle_data(target + ' ' + data)
        self.soup.endData(self.processing_instruction_class)

    def data(self, content):
        self.soup.handle_data(content)

    def doctype(self, name, pubid, system):
        self.soup.endData()
        doctype = Doctype.for_name_and_ids(name, pubid, system)
        self.soup.object_was_parsed(doctype)

    def comment(self, content):
        """Handle comments as Comment objects."""
        self.soup.endData()
        self.soup.handle_data(content)
        self.soup.endData(Comment)

    def test_fragment_to_document(self, fragment):
        """See `TreeBuilder`."""
        return '<?xml version="1.0" encoding="utf-8"?>\n%s' % fragment


class LXMLTreeBuilder(HTMLTreeBuilder, LXMLTreeBuilderForXML):
    NAME = LXML
    ALTERNATE_NAMES = ['lxml-html']
    features = ALTERNATE_NAMES + [NAME, HTML, FAST, PERMISSIVE]
    is_xml = False
    processing_instruction_class = ProcessingInstruction

    def default_parser(self, encoding):
        return etree.HTMLParser

    def feed(self, markup):
        encoding = self.soup.original_encoding
        try:
            self.parser = self.parser_for(encoding)
            self.parser.feed(markup)
            self.parser.close()
        except (UnicodeDecodeError, LookupError, etree.ParserError) as e:
            raise ParserRejectedMarkup(str(e))

    def test_fragment_to_document(self, fragment):
        """See `TreeBuilder`."""
        return '<html><body>%s</body></html>' % fragment