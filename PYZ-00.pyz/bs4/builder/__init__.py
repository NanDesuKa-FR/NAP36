# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\bs4\builder\__init__.py
__license__ = 'MIT'
from collections import defaultdict
import itertools, sys
from bs4.element import CharsetMetaAttributeValue, ContentMetaAttributeValue, HTMLAwareEntitySubstitution, nonwhitespace_re
__all__ = [
 'HTMLTreeBuilder',
 'SAXTreeBuilder',
 'TreeBuilder',
 'TreeBuilderRegistry']
FAST = 'fast'
PERMISSIVE = 'permissive'
STRICT = 'strict'
XML = 'xml'
HTML = 'html'
HTML_5 = 'html5'

class TreeBuilderRegistry(object):

    def __init__(self):
        self.builders_for_feature = defaultdict(list)
        self.builders = []

    def register(self, treebuilder_class):
        """Register a treebuilder based on its advertised features."""
        for feature in treebuilder_class.features:
            self.builders_for_feature[feature].insert(0, treebuilder_class)

        self.builders.insert(0, treebuilder_class)

    def lookup(self, *features):
        if len(self.builders) == 0:
            return
        else:
            if len(features) == 0:
                return self.builders[0]
            features = list(features)
            features.reverse()
            candidates = None
            candidate_set = None
            while len(features) > 0:
                feature = features.pop()
                we_have_the_feature = self.builders_for_feature.get(feature, [])
                if len(we_have_the_feature) > 0:
                    if candidates is None:
                        candidates = we_have_the_feature
                        candidate_set = set(candidates)
                    else:
                        candidate_set = candidate_set.intersection(set(we_have_the_feature))

            if candidate_set is None:
                return
        for candidate in candidates:
            if candidate in candidate_set:
                return candidate


builder_registry = TreeBuilderRegistry()

class TreeBuilder(object):
    __doc__ = 'Turn a document into a Beautiful Soup object tree.'
    NAME = '[Unknown tree builder]'
    ALTERNATE_NAMES = []
    features = []
    is_xml = False
    picklable = False
    preserve_whitespace_tags = set()
    empty_element_tags = None
    cdata_list_attributes = {}

    def __init__(self):
        self.soup = None

    def initialize_soup(self, soup):
        """The BeautifulSoup object has been initialized and is now
        being associated with the TreeBuilder.
        """
        self.soup = soup

    def reset(self):
        pass

    def can_be_empty_element(self, tag_name):
        """Might a tag with this name be an empty-element tag?

        The final markup may or may not actually present this tag as
        self-closing.

        For instance: an HTMLBuilder does not consider a <p> tag to be
        an empty-element tag (it's not in
        HTMLBuilder.empty_element_tags). This means an empty <p> tag
        will be presented as "<p></p>", not "<p />".

        The default implementation has no opinion about which tags are
        empty-element tags, so a tag will be presented as an
        empty-element tag if and only if it has no contents.
        "<foo></foo>" will become "<foo />", and "<foo>bar</foo>" will
        be left alone.
        """
        if self.empty_element_tags is None:
            return True
        else:
            return tag_name in self.empty_element_tags

    def feed(self, markup):
        raise NotImplementedError()

    def prepare_markup(self, markup, user_specified_encoding=None, document_declared_encoding=None):
        return (
         markup, None, None, False)

    def test_fragment_to_document(self, fragment):
        """Wrap an HTML fragment to make it look like a document.

        Different parsers do this differently. For instance, lxml
        introduces an empty <head> tag, and html5lib
        doesn't. Abstracting this away lets us write simple tests
        which run HTML fragments through the parser and compare the
        results against other HTML fragments.

        This method should not be used outside of tests.
        """
        return fragment

    def set_up_substitutions(self, tag):
        return False

    def _replace_cdata_list_attribute_values(self, tag_name, attrs):
        """Replaces class="foo bar" with class=["foo", "bar"]

        Modifies its input in place.
        """
        if not attrs:
            return attrs
        else:
            if self.cdata_list_attributes:
                universal = self.cdata_list_attributes.get('*', [])
                tag_specific = self.cdata_list_attributes.get(tag_name.lower(), None)
                for attr in list(attrs.keys()):
                    if attr in universal or tag_specific and attr in tag_specific:
                        value = attrs[attr]
                        if isinstance(value, str):
                            values = nonwhitespace_re.findall(value)
                        else:
                            values = value
                        attrs[attr] = values

            return attrs


class SAXTreeBuilder(TreeBuilder):
    __doc__ = 'A Beautiful Soup treebuilder that listens for SAX events.'

    def feed(self, markup):
        raise NotImplementedError()

    def close(self):
        pass

    def startElement(self, name, attrs):
        attrs = dict((key[1], value) for key, value in list(attrs.items()))
        self.soup.handle_starttag(name, attrs)

    def endElement(self, name):
        self.soup.handle_endtag(name)

    def startElementNS(self, nsTuple, nodeName, attrs):
        self.startElement(nodeName, attrs)

    def endElementNS(self, nsTuple, nodeName):
        self.endElement(nodeName)

    def startPrefixMapping(self, prefix, nodeValue):
        pass

    def endPrefixMapping(self, prefix):
        pass

    def characters(self, content):
        self.soup.handle_data(content)

    def startDocument(self):
        pass

    def endDocument(self):
        pass


class HTMLTreeBuilder(TreeBuilder):
    __doc__ = 'This TreeBuilder knows facts about HTML.\n\n    Such as which tags are empty-element tags.\n    '
    preserve_whitespace_tags = HTMLAwareEntitySubstitution.preserve_whitespace_tags
    empty_element_tags = set([
     'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'menuitem', 'meta', 'param', 'source', 'track', 'wbr',
     'basefont', 'bgsound', 'command', 'frame', 'image', 'isindex', 'nextid', 'spacer'])
    block_elements = set(['address', 'article', 'aside', 'blockquote', 'canvas', 'dd', 'div', 'dl', 'dt', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'li', 'main', 'nav', 'noscript', 'ol', 'output', 'p', 'pre', 'section', 'table', 'tfoot', 'ul', 'video'])
    cdata_list_attributes = {'*':[
      'class', 'accesskey', 'dropzone'], 
     'a':[
      'rel', 'rev'], 
     'link':[
      'rel', 'rev'], 
     'td':[
      'headers'], 
     'th':[
      'headers'], 
     'td':[
      'headers'], 
     'form':[
      'accept-charset'], 
     'object':[
      'archive'], 
     'area':[
      'rel'], 
     'icon':[
      'sizes'], 
     'iframe':[
      'sandbox'], 
     'output':[
      'for']}

    def set_up_substitutions(self, tag):
        if tag.name != 'meta':
            return False
        else:
            http_equiv = tag.get('http-equiv')
            content = tag.get('content')
            charset = tag.get('charset')
            meta_encoding = None
            if charset is not None:
                meta_encoding = charset
                tag['charset'] = CharsetMetaAttributeValue(charset)
            else:
                if content is not None:
                    if http_equiv is not None:
                        if http_equiv.lower() == 'content-type':
                            tag['content'] = ContentMetaAttributeValue(content)
            return meta_encoding is not None


def register_treebuilders_from(module):
    """Copy TreeBuilders from the given module into this module."""
    this_module = sys.modules['bs4.builder']
    for name in module.__all__:
        obj = getattr(module, name)
        if issubclass(obj, TreeBuilder):
            setattr(this_module, name, obj)
            this_module.__all__.append(name)
            this_module.builder_registry.register(obj)


class ParserRejectedMarkup(Exception):
    pass


from . import _htmlparser
register_treebuilders_from(_htmlparser)
try:
    from . import _html5lib
    register_treebuilders_from(_html5lib)
except ImportError:
    pass

try:
    from . import _lxml
    register_treebuilders_from(_lxml)
except ImportError:
    pass