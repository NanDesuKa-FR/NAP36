# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\bs4\builder\_html5lib.py
__license__ = 'MIT'
__all__ = [
 'HTML5TreeBuilder']
import warnings, re
from bs4.builder import PERMISSIVE, HTML, HTML_5, HTMLTreeBuilder
from bs4.element import NamespacedAttribute, nonwhitespace_re
import html5lib
from html5lib.constants import namespaces, prefixes
from bs4.element import Comment, Doctype, NavigableString, Tag
try:
    from html5lib.treebuilders import _base as treebuilder_base
    new_html5lib = False
except ImportError as e:
    from html5lib.treebuilders import base as treebuilder_base
    new_html5lib = True

class HTML5TreeBuilder(HTMLTreeBuilder):
    __doc__ = 'Use html5lib to build a tree.'
    NAME = 'html5lib'
    features = [
     NAME, PERMISSIVE, HTML_5, HTML]

    def prepare_markup(self, markup, user_specified_encoding, document_declared_encoding=None, exclude_encodings=None):
        self.user_specified_encoding = user_specified_encoding
        if exclude_encodings:
            warnings.warn("You provided a value for exclude_encoding, but the html5lib tree builder doesn't support exclude_encoding.")
        yield (
         markup, None, None, False)

    def feed(self, markup):
        if self.soup.parse_only is not None:
            warnings.warn("You provided a value for parse_only, but the html5lib tree builder doesn't support parse_only. The entire document will be parsed.")
        else:
            parser = html5lib.HTMLParser(tree=(self.create_treebuilder))
            extra_kwargs = dict()
            if not isinstance(markup, str):
                if new_html5lib:
                    extra_kwargs['override_encoding'] = self.user_specified_encoding
                else:
                    extra_kwargs['encoding'] = self.user_specified_encoding
            doc = (parser.parse)(markup, **extra_kwargs)
            if isinstance(markup, str):
                doc.original_encoding = None
            else:
                original_encoding = parser.tokenizer.stream.charEncoding[0]
            if not isinstance(original_encoding, str):
                original_encoding = original_encoding.name
            doc.original_encoding = original_encoding

    def create_treebuilder(self, namespaceHTMLElements):
        self.underlying_builder = TreeBuilderForHtml5lib(namespaceHTMLElements, self.soup)
        return self.underlying_builder

    def test_fragment_to_document(self, fragment):
        """See `TreeBuilder`."""
        return '<html><head></head><body>%s</body></html>' % fragment


class TreeBuilderForHtml5lib(treebuilder_base.TreeBuilder):

    def __init__(self, namespaceHTMLElements, soup=None):
        if soup:
            self.soup = soup
        else:
            from bs4 import BeautifulSoup
            self.soup = BeautifulSoup('', 'html.parser')
        super(TreeBuilderForHtml5lib, self).__init__(namespaceHTMLElements)

    def documentClass(self):
        self.soup.reset()
        return Element(self.soup, self.soup, None)

    def insertDoctype(self, token):
        name = token['name']
        publicId = token['publicId']
        systemId = token['systemId']
        doctype = Doctype.for_name_and_ids(name, publicId, systemId)
        self.soup.object_was_parsed(doctype)

    def elementClass(self, name, namespace):
        tag = self.soup.new_tag(name, namespace)
        return Element(tag, self.soup, namespace)

    def commentClass(self, data):
        return TextNode(Comment(data), self.soup)

    def fragmentClass(self):
        from bs4 import BeautifulSoup
        self.soup = BeautifulSoup('', 'html.parser')
        self.soup.name = '[document_fragment]'
        return Element(self.soup, self.soup, None)

    def appendChild(self, node):
        self.soup.append(node.element)

    def getDocument(self):
        return self.soup

    def getFragment(self):
        return treebuilder_base.TreeBuilder.getFragment(self).element

    def testSerializer(self, element):
        from bs4 import BeautifulSoup
        rv = []
        doctype_re = re.compile('^(.*?)(?: PUBLIC "(.*?)"(?: "(.*?)")?| SYSTEM "(.*?)")?$')

        def serializeElement(element, indent=0):
            if isinstance(element, BeautifulSoup):
                pass
            if isinstance(element, Doctype):
                m = doctype_re.match(element)
                if m:
                    name = m.group(1)
                    if m.lastindex > 1:
                        publicId = m.group(2) or ''
                        systemId = m.group(3) or m.group(4) or ''
                        rv.append('|%s<!DOCTYPE %s "%s" "%s">' % (
                         ' ' * indent, name, publicId, systemId))
                    else:
                        rv.append('|%s<!DOCTYPE %s>' % (' ' * indent, name))
                else:
                    rv.append('|%s<!DOCTYPE >' % (' ' * indent,))
            else:
                if isinstance(element, Comment):
                    rv.append('|%s<!-- %s -->' % (' ' * indent, element))
                else:
                    if isinstance(element, NavigableString):
                        rv.append('|%s"%s"' % (' ' * indent, element))
                    else:
                        if element.namespace:
                            name = '%s %s' % (prefixes[element.namespace],
                             element.name)
                        else:
                            name = element.name
                        rv.append('|%s<%s>' % (' ' * indent, name))
                        if element.attrs:
                            attributes = []
                            for name, value in list(element.attrs.items()):
                                if isinstance(name, NamespacedAttribute):
                                    name = '%s %s' % (prefixes[name.namespace], name.name)
                                if isinstance(value, list):
                                    value = ' '.join(value)
                                attributes.append((name, value))

                            for name, value in sorted(attributes):
                                rv.append('|%s%s="%s"' % (' ' * (indent + 2), name, value))

                        indent += 2
                        for child in element.children:
                            serializeElement(child, indent)

        serializeElement(element, 0)
        return '\n'.join(rv)


class AttrList(object):

    def __init__(self, element):
        self.element = element
        self.attrs = dict(self.element.attrs)

    def __iter__(self):
        return list(self.attrs.items()).__iter__()

    def __setitem__(self, name, value):
        list_attr = HTML5TreeBuilder.cdata_list_attributes
        if name in list_attr['*'] or self.element.name in list_attr and name in list_attr[self.element.name]:
            if not isinstance(value, list):
                value = nonwhitespace_re.findall(value)
        self.element[name] = value

    def items(self):
        return list(self.attrs.items())

    def keys(self):
        return list(self.attrs.keys())

    def __len__(self):
        return len(self.attrs)

    def __getitem__(self, name):
        return self.attrs[name]

    def __contains__(self, name):
        return name in list(self.attrs.keys())


class Element(treebuilder_base.Node):

    def __init__(self, element, soup, namespace):
        treebuilder_base.Node.__init__(self, element.name)
        self.element = element
        self.soup = soup
        self.namespace = namespace

    def appendChild(self, node):
        string_child = child = None
        if isinstance(node, str):
            string_child = child = node
        else:
            if isinstance(node, Tag):
                child = node
            else:
                if node.element.__class__ == NavigableString:
                    string_child = child = node.element
                    node.parent = self
                else:
                    child = node.element
                    node.parent = self
        if not isinstance(child, str):
            if child.parent is not None:
                node.element.extract()
            if string_child is not None:
                if self.element.contents and self.element.contents[(-1)].__class__ == NavigableString:
                    old_element = self.element.contents[(-1)]
                    new_element = self.soup.new_string(old_element + string_child)
                    old_element.replace_with(new_element)
                    self.soup._most_recent_element = new_element
        else:
            if isinstance(node, str):
                child = self.soup.new_string(node)
            else:
                if self.element.contents:
                    most_recent_element = self.element._last_descendant(False)
                else:
                    if self.element.next_element is not None:
                        most_recent_element = self.soup._last_descendant()
                    else:
                        most_recent_element = self.element
            self.soup.object_was_parsed(child,
              parent=(self.element), most_recent_element=most_recent_element)

    def getAttributes(self):
        if isinstance(self.element, Comment):
            return {}
        else:
            return AttrList(self.element)

    def setAttributes(self, attributes):
        if attributes is not None:
            if len(attributes) > 0:
                converted_attributes = []
                for name, value in list(attributes.items()):
                    if isinstance(name, tuple):
                        new_name = NamespacedAttribute(*name)
                        del attributes[name]
                        attributes[new_name] = value

                self.soup.builder._replace_cdata_list_attribute_values(self.name, attributes)
                for name, value in list(attributes.items()):
                    self.element[name] = value

                self.soup.builder.set_up_substitutions(self.element)

    attributes = property(getAttributes, setAttributes)

    def insertText(self, data, insertBefore=None):
        text = TextNode(self.soup.new_string(data), self.soup)
        if insertBefore:
            self.insertBefore(text, insertBefore)
        else:
            self.appendChild(text)

    def insertBefore(self, node, refNode):
        index = self.element.index(refNode.element)
        if node.element.__class__ == NavigableString:
            if self.element.contents:
                if self.element.contents[(index - 1)].__class__ == NavigableString:
                    old_node = self.element.contents[(index - 1)]
                    new_str = self.soup.new_string(old_node + node.element)
                    old_node.replace_with(new_str)
        else:
            self.element.insert(index, node.element)
            node.parent = self

    def removeChild(self, node):
        node.element.extract()

    def reparentChildren(self, new_parent):
        """Move all of this tag's children into another tag."""
        element = self.element
        new_parent_element = new_parent.element
        final_next_element = element.next_sibling
        new_parents_last_descendant = new_parent_element._last_descendant(False, False)
        if len(new_parent_element.contents) > 0:
            new_parents_last_child = new_parent_element.contents[(-1)]
            new_parents_last_descendant_next_element = new_parents_last_descendant.next_element
        else:
            new_parents_last_child = None
            new_parents_last_descendant_next_element = new_parent_element.next_element
        to_append = element.contents
        if len(to_append) > 0:
            first_child = to_append[0]
            if new_parents_last_descendant is not None:
                first_child.previous_element = new_parents_last_descendant
            else:
                first_child.previous_element = new_parent_element
            first_child.previous_sibling = new_parents_last_child
            if new_parents_last_descendant is not None:
                new_parents_last_descendant.next_element = first_child
            else:
                new_parent_element.next_element = first_child
            if new_parents_last_child is not None:
                new_parents_last_child.next_sibling = first_child
            last_childs_last_descendant = to_append[(-1)]._last_descendant(False, True)
            last_childs_last_descendant.next_element = new_parents_last_descendant_next_element
            if new_parents_last_descendant_next_element is not None:
                new_parents_last_descendant_next_element.previous_element = last_childs_last_descendant
            last_childs_last_descendant.next_sibling = None
        for child in to_append:
            child.parent = new_parent_element
            new_parent_element.contents.append(child)

        element.contents = []
        element.next_element = final_next_element

    def cloneNode(self):
        tag = self.soup.new_tag(self.element.name, self.namespace)
        node = Element(tag, self.soup, self.namespace)
        for key, value in self.attributes:
            node.attributes[key] = value

        return node

    def hasContent(self):
        return self.element.contents

    def getNameTuple(self):
        if self.namespace == None:
            return (namespaces['html'], self.name)
        else:
            return (
             self.namespace, self.name)

    nameTuple = property(getNameTuple)


class TextNode(Element):

    def __init__(self, element, soup):
        treebuilder_base.Node.__init__(self, None)
        self.element = element
        self.soup = soup

    def cloneNode(self):
        raise NotImplementedError