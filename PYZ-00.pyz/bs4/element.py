# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\bs4\element.py
__license__ = 'MIT'
try:
    from collections.abc import Callable
except ImportError as e:
    from collections import Callable

import re, sys, warnings
try:
    import soupsieve
except ImportError as e:
    soupsieve = None
    warnings.warn('The soupsieve package is not installed. CSS selectors cannot be used.')

from bs4.dammit import EntitySubstitution
DEFAULT_OUTPUT_ENCODING = 'utf-8'
PY3K = sys.version_info[0] > 2
nonwhitespace_re = re.compile('\\S+')
whitespace_re = re.compile('\\s+')

def _alias(attr):
    """Alias one attribute name to another for backward compatibility"""

    @property
    def alias(self):
        return getattr(self, attr)

    @alias.setter
    def alias(self):
        return setattr(self, attr)

    return alias


class NamespacedAttribute(str):

    def __new__(cls, prefix, name, namespace=None):
        if name is None:
            obj = str.__new__(cls, prefix)
        else:
            if prefix is None:
                obj = str.__new__(cls, name)
            else:
                obj = str.__new__(cls, prefix + ':' + name)
        obj.prefix = prefix
        obj.name = name
        obj.namespace = namespace
        return obj


class AttributeValueWithCharsetSubstitution(str):
    __doc__ = 'A stand-in object for a character encoding specified in HTML.'


class CharsetMetaAttributeValue(AttributeValueWithCharsetSubstitution):
    __doc__ = 'A generic stand-in for the value of a meta tag\'s \'charset\' attribute.\n\n    When Beautiful Soup parses the markup \'<meta charset="utf8">\', the\n    value of the \'charset\' attribute will be one of these objects.\n    '

    def __new__(cls, original_value):
        obj = str.__new__(cls, original_value)
        obj.original_value = original_value
        return obj

    def encode(self, encoding):
        return encoding


class ContentMetaAttributeValue(AttributeValueWithCharsetSubstitution):
    __doc__ = 'A generic stand-in for the value of a meta tag\'s \'content\' attribute.\n\n    When Beautiful Soup parses the markup:\n     <meta http-equiv="content-type" content="text/html; charset=utf8">\n\n    The value of the \'content\' attribute will be one of these objects.\n    '
    CHARSET_RE = re.compile('((^|;)\\s*charset=)([^;]*)', re.M)

    def __new__(cls, original_value):
        match = cls.CHARSET_RE.search(original_value)
        if match is None:
            return str.__new__(str, original_value)
        else:
            obj = str.__new__(cls, original_value)
            obj.original_value = original_value
            return obj

    def encode(self, encoding):

        def rewrite(match):
            return match.group(1) + encoding

        return self.CHARSET_RE.sub(rewrite, self.original_value)


class HTMLAwareEntitySubstitution(EntitySubstitution):
    __doc__ = "Entity substitution rules that are aware of some HTML quirks.\n\n    Specifically, the contents of <script> and <style> tags should not\n    undergo entity substitution.\n\n    Incoming NavigableString objects are checked to see if they're the\n    direct children of a <script> or <style> tag.\n    "
    cdata_containing_tags = set(['script', 'style'])
    preformatted_tags = set(['pre'])
    preserve_whitespace_tags = set(['pre', 'textarea'])

    @classmethod
    def _substitute_if_appropriate(cls, ns, f):
        if isinstance(ns, NavigableString):
            if ns.parent is not None:
                if ns.parent.name in cls.cdata_containing_tags:
                    return ns
        return f(ns)

    @classmethod
    def substitute_html(cls, ns):
        return cls._substitute_if_appropriate(ns, EntitySubstitution.substitute_html)

    @classmethod
    def substitute_xml(cls, ns):
        return cls._substitute_if_appropriate(ns, EntitySubstitution.substitute_xml)


class Formatter(object):
    __doc__ = 'Contains information about how to format a parse tree.'
    void_element_close_prefix = '/'

    def substitute_entities(self, *args, **kwargs):
        """Transform certain characters into named entities."""
        raise NotImplementedError()


class HTMLFormatter(Formatter):
    __doc__ = 'The default HTML formatter.'

    def substitute(self, *args, **kwargs):
        return (HTMLAwareEntitySubstitution.substitute_html)(*args, **kwargs)


class MinimalHTMLFormatter(Formatter):
    __doc__ = 'A minimal HTML formatter.'

    def substitute(self, *args, **kwargs):
        return (HTMLAwareEntitySubstitution.substitute_xml)(*args, **kwargs)


class HTML5Formatter(HTMLFormatter):
    __doc__ = 'An HTML formatter that omits the slash in a void tag.'
    void_element_close_prefix = None


class XMLFormatter(Formatter):
    __doc__ = 'Substitute only the essential XML entities.'

    def substitute(self, *args, **kwargs):
        return (EntitySubstitution.substitute_xml)(*args, **kwargs)


class HTMLXMLFormatter(Formatter):
    __doc__ = 'Format XML using HTML rules.'

    def substitute(self, *args, **kwargs):
        return (HTMLAwareEntitySubstitution.substitute_html)(*args, **kwargs)


class PageElement(object):
    __doc__ = 'Contains the navigational information for some part of the page\n    (either a tag or a piece of text)'
    HTML_FORMATTERS = {'html':HTMLFormatter(), 
     'html5':HTML5Formatter(), 
     'minimal':MinimalHTMLFormatter(), 
     None:None}
    XML_FORMATTERS = {'html':HTMLXMLFormatter(), 
     'minimal':XMLFormatter(), 
     None:None}

    def format_string(self, s, formatter='minimal'):
        """Format the given string using the given formatter."""
        if isinstance(formatter, str):
            formatter = self._formatter_for_name(formatter)
        else:
            if formatter is None:
                output = s
            else:
                if isinstance(formatter, Callable):
                    output = formatter(s)
                else:
                    output = formatter.substitute(s)
        return output

    @property
    def _is_xml(self):
        """Is this element part of an XML tree or an HTML tree?

        This is used when mapping a formatter name ("minimal") to an
        appropriate function (one that performs entity-substitution on
        the contents of <script> and <style> tags, or not). It can be
        inefficient, but it should be called very rarely.
        """
        if self.known_xml is not None:
            return self.known_xml
        else:
            if self.parent is None:
                return getattr(self, 'is_xml', False)
            return self.parent._is_xml

    def _formatter_for_name(self, name):
        """Look up a formatter function based on its name and the tree."""
        if self._is_xml:
            return self.XML_FORMATTERS.get(name, XMLFormatter())
        else:
            return self.HTML_FORMATTERS.get(name, HTMLFormatter())

    def setup(self, parent=None, previous_element=None, next_element=None, previous_sibling=None, next_sibling=None):
        """Sets up the initial relations between this element and
        other elements."""
        self.parent = parent
        self.previous_element = previous_element
        if previous_element is not None:
            self.previous_element.next_element = self
        self.next_element = next_element
        if self.next_element is not None:
            self.next_element.previous_element = self
        self.next_sibling = next_sibling
        if self.next_sibling is not None:
            self.next_sibling.previous_sibling = self
        if previous_sibling is None:
            if self.parent is not None:
                if self.parent.contents:
                    previous_sibling = self.parent.contents[(-1)]
        self.previous_sibling = previous_sibling
        if previous_sibling is not None:
            self.previous_sibling.next_sibling = self

    nextSibling = _alias('next_sibling')
    previousSibling = _alias('previous_sibling')

    def replace_with(self, replace_with):
        if self.parent is None:
            raise ValueError('Cannot replace one element with another when theelement to be replaced is not part of a tree.')
        if replace_with is self:
            return
        else:
            if replace_with is self.parent:
                raise ValueError('Cannot replace a Tag with its parent.')
            old_parent = self.parent
            my_index = self.parent.index(self)
            self.extract()
            old_parent.insert(my_index, replace_with)
            return self

    replaceWith = replace_with

    def unwrap(self):
        my_parent = self.parent
        if self.parent is None:
            raise ValueError('Cannot replace an element with its contents when thatelement is not part of a tree.')
        my_index = self.parent.index(self)
        self.extract()
        for child in reversed(self.contents[:]):
            my_parent.insert(my_index, child)

        return self

    replace_with_children = unwrap
    replaceWithChildren = unwrap

    def wrap(self, wrap_inside):
        me = self.replace_with(wrap_inside)
        wrap_inside.append(me)
        return wrap_inside

    def extract(self):
        """Destructively rips this element out of the tree."""
        if self.parent is not None:
            del self.parent.contents[self.parent.index(self)]
        else:
            last_child = self._last_descendant()
            next_element = last_child.next_element
            if self.previous_element is not None:
                if self.previous_element is not next_element:
                    self.previous_element.next_element = next_element
            if next_element is not None:
                if next_element is not self.previous_element:
                    next_element.previous_element = self.previous_element
            self.previous_element = None
            last_child.next_element = None
            self.parent = None
            if self.previous_sibling is not None:
                if self.previous_sibling is not self.next_sibling:
                    self.previous_sibling.next_sibling = self.next_sibling
            if self.next_sibling is not None:
                if self.next_sibling is not self.previous_sibling:
                    self.next_sibling.previous_sibling = self.previous_sibling
        self.previous_sibling = self.next_sibling = None
        return self

    def _last_descendant(self, is_initialized=True, accept_self=True):
        """Finds the last element beneath this object to be parsed."""
        if is_initialized:
            if self.next_sibling is not None:
                last_child = self.next_sibling.previous_element
        else:
            last_child = self
            while isinstance(last_child, Tag) and last_child.contents:
                last_child = last_child.contents[(-1)]

        if not accept_self:
            if last_child is self:
                last_child = None
        return last_child

    _lastRecursiveChild = _last_descendant

    def insert(self, position, new_child):
        if new_child is None:
            raise ValueError('Cannot insert None into a tag.')
        else:
            if new_child is self:
                raise ValueError('Cannot insert a tag into itself.')
            else:
                if isinstance(new_child, str):
                    if not isinstance(new_child, NavigableString):
                        new_child = NavigableString(new_child)
                    else:
                        from bs4 import BeautifulSoup
                        if isinstance(new_child, BeautifulSoup):
                            for subchild in list(new_child.contents):
                                self.insert(position, subchild)
                                position += 1

                            return
                        position = min(position, len(self.contents))
                        if hasattr(new_child, 'parent'):
                            if new_child.parent is not None:
                                if new_child.parent is self:
                                    current_index = self.index(new_child)
                                    if current_index < position:
                                        position -= 1
                                new_child.extract()
                    new_child.parent = self
                    previous_child = None
                    if position == 0:
                        new_child.previous_sibling = None
                        new_child.previous_element = self
                    else:
                        previous_child = self.contents[(position - 1)]
                        new_child.previous_sibling = previous_child
                        new_child.previous_sibling.next_sibling = new_child
                        new_child.previous_element = previous_child._last_descendant(False)
                else:
                    if new_child.previous_element is not None:
                        new_child.previous_element.next_element = new_child
                    new_childs_last_element = new_child._last_descendant(False)
                    if position >= len(self.contents):
                        new_child.next_sibling = None
                        parent = self
                        parents_next_sibling = None
                        while parents_next_sibling is None and parent is not None:
                            parents_next_sibling = parent.next_sibling
                            parent = parent.parent
                            if parents_next_sibling is not None:
                                break

                        if parents_next_sibling is not None:
                            new_childs_last_element.next_element = parents_next_sibling
                        else:
                            new_childs_last_element.next_element = None
                    else:
                        next_child = self.contents[position]
                        new_child.next_sibling = next_child
                        if new_child.next_sibling is not None:
                            new_child.next_sibling.previous_sibling = new_child
                new_childs_last_element.next_element = next_child
            if new_childs_last_element.next_element is not None:
                new_childs_last_element.next_element.previous_element = new_childs_last_element
        self.contents.insert(position, new_child)

    def append(self, tag):
        """Appends the given tag to the contents of this tag."""
        self.insert(len(self.contents), tag)

    def extend(self, tags):
        """Appends the given tags to the contents of this tag."""
        for tag in tags:
            self.append(tag)

    def insert_before(self, *args):
        """Makes the given element(s) the immediate predecessor of this one.

        The elements will have the same parent, and the given elements
        will be immediately before this one.
        """
        parent = self.parent
        if parent is None:
            raise ValueError("Element has no parent, so 'before' has no meaning.")
        if any(x is self for x in args):
            raise ValueError("Can't insert an element before itself.")
        for predecessor in args:
            if isinstance(predecessor, PageElement):
                predecessor.extract()
            index = parent.index(self)
            parent.insert(index, predecessor)

    def insert_after(self, *args):
        """Makes the given element(s) the immediate successor of this one.

        The elements will have the same parent, and the given elements
        will be immediately after this one.
        """
        parent = self.parent
        if parent is None:
            raise ValueError("Element has no parent, so 'after' has no meaning.")
        if any(x is self for x in args):
            raise ValueError("Can't insert an element after itself.")
        offset = 0
        for successor in args:
            if isinstance(successor, PageElement):
                successor.extract()
            index = parent.index(self)
            parent.insert(index + 1 + offset, successor)
            offset += 1

    def find_next(self, name=None, attrs={}, text=None, **kwargs):
        """Returns the first item that matches the given criteria and
        appears after this Tag in the document."""
        return (self._find_one)((self.find_all_next), name, attrs, text, **kwargs)

    findNext = find_next

    def find_all_next(self, name=None, attrs={}, text=None, limit=None, **kwargs):
        """Returns all items that match the given criteria and appear
        after this Tag in the document."""
        return (self._find_all)(name, attrs, text, limit, (self.next_elements), **kwargs)

    findAllNext = find_all_next

    def find_next_sibling(self, name=None, attrs={}, text=None, **kwargs):
        """Returns the closest sibling to this Tag that matches the
        given criteria and appears after this Tag in the document."""
        return (self._find_one)((self.find_next_siblings), name, attrs, text, **kwargs)

    findNextSibling = find_next_sibling

    def find_next_siblings(self, name=None, attrs={}, text=None, limit=None, **kwargs):
        """Returns the siblings of this Tag that match the given
        criteria and appear after this Tag in the document."""
        return (self._find_all)(name, attrs, text, limit, 
         (self.next_siblings), **kwargs)

    findNextSiblings = find_next_siblings
    fetchNextSiblings = find_next_siblings

    def find_previous(self, name=None, attrs={}, text=None, **kwargs):
        """Returns the first item that matches the given criteria and
        appears before this Tag in the document."""
        return (self._find_one)(
         (self.find_all_previous), name, attrs, text, **kwargs)

    findPrevious = find_previous

    def find_all_previous(self, name=None, attrs={}, text=None, limit=None, **kwargs):
        """Returns all items that match the given criteria and appear
        before this Tag in the document."""
        return (self._find_all)(name, attrs, text, limit, (self.previous_elements), **kwargs)

    findAllPrevious = find_all_previous
    fetchPrevious = find_all_previous

    def find_previous_sibling(self, name=None, attrs={}, text=None, **kwargs):
        """Returns the closest sibling to this Tag that matches the
        given criteria and appears before this Tag in the document."""
        return (self._find_one)((self.find_previous_siblings), name, attrs, text, **kwargs)

    findPreviousSibling = find_previous_sibling

    def find_previous_siblings(self, name=None, attrs={}, text=None, limit=None, **kwargs):
        """Returns the siblings of this Tag that match the given
        criteria and appear before this Tag in the document."""
        return (self._find_all)(name, attrs, text, limit, 
         (self.previous_siblings), **kwargs)

    findPreviousSiblings = find_previous_siblings
    fetchPreviousSiblings = find_previous_siblings

    def find_parent(self, name=None, attrs={}, **kwargs):
        """Returns the closest parent of this Tag that matches the given
        criteria."""
        r = None
        l = (self.find_parents)(name, attrs, 1, **kwargs)
        if l:
            r = l[0]
        return r

    findParent = find_parent

    def find_parents(self, name=None, attrs={}, limit=None, **kwargs):
        """Returns the parents of this Tag that match the given
        criteria."""
        return (self._find_all)(name, attrs, None, limit, (self.parents), **kwargs)

    findParents = find_parents
    fetchParents = find_parents

    @property
    def next(self):
        return self.next_element

    @property
    def previous(self):
        return self.previous_element

    def _find_one(self, method, name, attrs, text, **kwargs):
        r = None
        l = method(name, attrs, text, 1, **kwargs)
        if l:
            r = l[0]
        return r

    def _find_all(self, name, attrs, text, limit, generator, **kwargs):
        """Iterates over a generator looking for things that match."""
        if text is None:
            if 'string' in kwargs:
                text = kwargs['string']
                del kwargs['string']
        else:
            if isinstance(name, SoupStrainer):
                strainer = name
            else:
                strainer = SoupStrainer(name, attrs, text, **kwargs)
        if text is None:
            if not limit:
                if not attrs:
                    if not kwargs:
                        if name is True or name is None:
                            result = (element for element in generator if isinstance(element, Tag))
                            return ResultSet(strainer, result)
                        if isinstance(name, str):
                            if name.count(':') == 1:
                                prefix, local_name = name.split(':', 1)
                            else:
                                prefix = None
                                local_name = name
                            result = (element for element in generator if isinstance(element, Tag) and element.name == name or element.name == local_name and (prefix is None or element.prefix == prefix))
                            return ResultSet(strainer, result)
        results = ResultSet(strainer)
        while 1:
            try:
                i = next(generator)
            except StopIteration:
                break

            if i:
                found = strainer.search(i)
                if found:
                    results.append(found)
                    if limit:
                        if len(results) >= limit:
                            break

        return results

    @property
    def next_elements(self):
        i = self.next_element
        while i is not None:
            yield i
            i = i.next_element

    @property
    def next_siblings(self):
        i = self.next_sibling
        while i is not None:
            yield i
            i = i.next_sibling

    @property
    def previous_elements(self):
        i = self.previous_element
        while i is not None:
            yield i
            i = i.previous_element

    @property
    def previous_siblings(self):
        i = self.previous_sibling
        while i is not None:
            yield i
            i = i.previous_sibling

    @property
    def parents(self):
        i = self.parent
        while i is not None:
            yield i
            i = i.parent

    def nextGenerator(self):
        return self.next_elements

    def nextSiblingGenerator(self):
        return self.next_siblings

    def previousGenerator(self):
        return self.previous_elements

    def previousSiblingGenerator(self):
        return self.previous_siblings

    def parentGenerator(self):
        return self.parents


class NavigableString(str, PageElement):
    PREFIX = ''
    SUFFIX = ''
    known_xml = None

    def __new__(cls, value):
        """Create a new NavigableString.

        When unpickling a NavigableString, this method is called with
        the string in DEFAULT_OUTPUT_ENCODING. That encoding needs to be
        passed in to the superclass's __new__ or the superclass won't know
        how to handle non-ASCII characters.
        """
        if isinstance(value, str):
            u = str.__new__(cls, value)
        else:
            u = str.__new__(cls, value, DEFAULT_OUTPUT_ENCODING)
        u.setup()
        return u

    def __copy__(self):
        """A copy of a NavigableString has the same contents and class
        as the original, but it is not connected to the parse tree.
        """
        return type(self)(self)

    def __getnewargs__(self):
        return (
         str(self),)

    def __getattr__(self, attr):
        """text.string gives you text. This is for backwards
        compatibility for Navigable*String, but for CData* it lets you
        get the string without the CData wrapper."""
        if attr == 'string':
            return self
        raise AttributeError("'%s' object has no attribute '%s'" % (
         self.__class__.__name__, attr))

    def output_ready(self, formatter='minimal'):
        output = self.format_string(self, formatter)
        return self.PREFIX + output + self.SUFFIX

    @property
    def name(self):
        pass

    @name.setter
    def name(self, name):
        raise AttributeError('A NavigableString cannot be given a name.')


class PreformattedString(NavigableString):
    __doc__ = 'A NavigableString not subject to the normal formatting rules.\n\n    The string will be passed into the formatter (to trigger side effects),\n    but the return value will be ignored.\n    '

    def output_ready(self, formatter='minimal'):
        """CData strings are passed into the formatter.
        But the return value is ignored."""
        self.format_string(self, formatter)
        return self.PREFIX + self + self.SUFFIX


class CData(PreformattedString):
    PREFIX = '<![CDATA['
    SUFFIX = ']]>'


class ProcessingInstruction(PreformattedString):
    __doc__ = 'A SGML processing instruction.'
    PREFIX = '<?'
    SUFFIX = '>'


class XMLProcessingInstruction(ProcessingInstruction):
    __doc__ = 'An XML processing instruction.'
    PREFIX = '<?'
    SUFFIX = '?>'


class Comment(PreformattedString):
    PREFIX = '<!--'
    SUFFIX = '-->'


class Declaration(PreformattedString):
    PREFIX = '<?'
    SUFFIX = '?>'


class Doctype(PreformattedString):

    @classmethod
    def for_name_and_ids(cls, name, pub_id, system_id):
        value = name or ''
        if pub_id is not None:
            value += ' PUBLIC "%s"' % pub_id
            if system_id is not None:
                value += ' "%s"' % system_id
        else:
            if system_id is not None:
                value += ' SYSTEM "%s"' % system_id
        return Doctype(value)

    PREFIX = '<!DOCTYPE '
    SUFFIX = '>\n'


class Tag(PageElement):
    __doc__ = 'Represents a found HTML tag with its attributes and contents.'

    def __init__(self, parser=None, builder=None, name=None, namespace=None, prefix=None, attrs=None, parent=None, previous=None, is_xml=None):
        """Basic constructor."""
        if parser is None:
            self.parser_class = None
        else:
            self.parser_class = parser.__class__
        if name is None:
            raise ValueError("No value provided for new tag's name.")
        else:
            self.name = name
            self.namespace = namespace
            self.prefix = prefix
            if builder is not None:
                preserve_whitespace_tags = builder.preserve_whitespace_tags
            else:
                if is_xml:
                    preserve_whitespace_tags = []
                else:
                    preserve_whitespace_tags = HTMLAwareEntitySubstitution.preserve_whitespace_tags
                self.preserve_whitespace_tags = preserve_whitespace_tags
                if attrs is None:
                    attrs = {}
                else:
                    if attrs:
                        if builder is not None:
                            if builder.cdata_list_attributes:
                                attrs = builder._replace_cdata_list_attribute_values(self.name, attrs)
                        attrs = dict(attrs)
                    else:
                        attrs = dict(attrs)
                if builder:
                    self.known_xml = builder.is_xml
                else:
                    self.known_xml = is_xml
            self.attrs = attrs
            self.contents = []
            self.setup(parent, previous)
            self.hidden = False
            if builder is not None:
                builder.set_up_substitutions(self)
                self.can_be_empty_element = builder.can_be_empty_element(name)
            else:
                self.can_be_empty_element = False

    parserClass = _alias('parser_class')

    def __copy__(self):
        """A copy of a Tag is a new Tag, unconnected to the parse tree.
        Its contents are a copy of the old Tag's contents.
        """
        clone = type(self)(None, (self.builder), (self.name), (self.namespace), (self.prefix),
          (self.attrs), is_xml=(self._is_xml))
        for attr in ('can_be_empty_element', 'hidden'):
            setattr(clone, attr, getattr(self, attr))

        for child in self.contents:
            clone.append(child.__copy__())

        return clone

    @property
    def is_empty_element(self):
        """Is this tag an empty-element tag? (aka a self-closing tag)

        A tag that has contents is never an empty-element tag.

        A tag that has no contents may or may not be an empty-element
        tag. It depends on the builder used to create the tag. If the
        builder has a designated list of empty-element tags, then only
        a tag whose name shows up in that list is considered an
        empty-element tag.

        If the builder has no designated list of empty-element tags,
        then any tag with no contents is an empty-element tag.
        """
        return len(self.contents) == 0 and self.can_be_empty_element

    isSelfClosing = is_empty_element

    @property
    def string(self):
        """Convenience property to get the single string within this tag.

        :Return: If this tag has a single string child, return value
         is that string. If this tag has no children, or more than one
         child, return value is None. If this tag has one child tag,
         return value is the 'string' attribute of the child tag,
         recursively.
        """
        if len(self.contents) != 1:
            return
        else:
            child = self.contents[0]
            if isinstance(child, NavigableString):
                return child
            return child.string

    @string.setter
    def string(self, string):
        self.clear()
        self.append(string.__class__(string))

    def _all_strings(self, strip=False, types=(NavigableString, CData)):
        """Yield all strings of certain classes, possibly stripping them.

        By default, yields only NavigableString and CData objects. So
        no comments, processing instructions, etc.
        """
        for descendant in self.descendants:
            if not (types is None and not isinstance(descendant, NavigableString)):
                if types is not None:
                    if type(descendant) not in types:
                        continue
                if strip:
                    descendant = descendant.strip()
                    if len(descendant) == 0:
                        continue
                yield descendant

    strings = property(_all_strings)

    @property
    def stripped_strings(self):
        for string in self._all_strings(True):
            yield string

    def get_text(self, separator='', strip=False, types=(
 NavigableString, CData)):
        """
        Get all child strings, concatenated using the given separator.
        """
        return separator.join([s for s in self._all_strings(strip,
          types=types)])

    getText = get_text
    text = property(get_text)

    def decompose(self):
        """Recursively destroys the contents of this tree."""
        self.extract()
        i = self
        while i is not None:
            next = i.next_element
            i.__dict__.clear()
            i.contents = []
            i = next

    def clear(self, decompose=False):
        """
        Extract all children. If decompose is True, decompose instead.
        """
        if decompose:
            for element in self.contents[:]:
                if isinstance(element, Tag):
                    element.decompose()
                else:
                    element.extract()

        else:
            for element in self.contents[:]:
                element.extract()

    def index(self, element):
        """
        Find the index of a child by identity, not value. Avoids issues with
        tag.contents.index(element) getting the index of equal elements.
        """
        for i, child in enumerate(self.contents):
            if child is element:
                return i

        raise ValueError('Tag.index: element not in tag')

    def get(self, key, default=None):
        """Returns the value of the 'key' attribute for the tag, or
        the value given for 'default' if it doesn't have that
        attribute."""
        return self.attrs.get(key, default)

    def get_attribute_list(self, key, default=None):
        """The same as get(), but always returns a list."""
        value = self.get(key, default)
        if not isinstance(value, list):
            value = [
             value]
        return value

    def has_attr(self, key):
        return key in self.attrs

    def __hash__(self):
        return str(self).__hash__()

    def __getitem__(self, key):
        """tag[key] returns the value of the 'key' attribute for the tag,
        and throws an exception if it's not there."""
        return self.attrs[key]

    def __iter__(self):
        """Iterating over a tag iterates over its contents."""
        return iter(self.contents)

    def __len__(self):
        """The length of a tag is the length of its list of contents."""
        return len(self.contents)

    def __contains__(self, x):
        return x in self.contents

    def __bool__(self):
        """A tag is non-None even if it has no contents."""
        return True

    def __setitem__(self, key, value):
        """Setting tag[key] sets the value of the 'key' attribute for the
        tag."""
        self.attrs[key] = value

    def __delitem__(self, key):
        """Deleting tag[key] deletes all 'key' attributes for the tag."""
        self.attrs.pop(key, None)

    def __call__(self, *args, **kwargs):
        """Calling a tag like a function is the same as calling its
        find_all() method. Eg. tag('a') returns a list of all the A tags
        found within this tag."""
        return (self.find_all)(*args, **kwargs)

    def __getattr__(self, tag):
        if len(tag) > 3:
            if tag.endswith('Tag'):
                tag_name = tag[:-3]
                warnings.warn('.%(name)sTag is deprecated, use .find("%(name)s") instead. If you really were looking for a tag called %(name)sTag, use .find("%(name)sTag")' % dict(name=tag_name))
                return self.find(tag_name)
        if not tag.startswith('__'):
            if not tag == 'contents':
                return self.find(tag)
        raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__, tag))

    def __eq__(self, other):
        """Returns true iff this tag has the same name, the same attributes,
        and the same contents (recursively) as the given tag."""
        if self is other:
            return True
        else:
            if not hasattr(other, 'name') or not hasattr(other, 'attrs') or not hasattr(other, 'contents') or self.name != other.name or self.attrs != other.attrs or len(self) != len(other):
                return False
            for i, my_child in enumerate(self.contents):
                if my_child != other.contents[i]:
                    return False

            return True

    def __ne__(self, other):
        """Returns true iff this tag is not identical to the other tag,
        as defined in __eq__."""
        return not self == other

    def __repr__(self, encoding='unicode-escape'):
        """Renders this tag as a string."""
        if PY3K:
            return self.decode()
        else:
            return self.encode(encoding)

    def __unicode__(self):
        return self.decode()

    def __str__(self):
        if PY3K:
            return self.decode()
        else:
            return self.encode()

    if PY3K:
        __str__ = __repr__ = __unicode__

    def encode(self, encoding=DEFAULT_OUTPUT_ENCODING, indent_level=None, formatter='minimal', errors='xmlcharrefreplace'):
        u = self.decode(indent_level, encoding, formatter)
        return u.encode(encoding, errors)

    def _should_pretty_print(self, indent_level):
        """Should this tag be pretty-printed?"""
        return indent_level is not None and self.name not in self.preserve_whitespace_tags

    def decode(self, indent_level=None, eventual_encoding=DEFAULT_OUTPUT_ENCODING, formatter='minimal'):
        """Returns a Unicode representation of this tag and its contents.

        :param eventual_encoding: The tag is destined to be
           encoded into this encoding. This method is _not_
           responsible for performing that encoding. This information
           is passed in so that it can be substituted in if the
           document contains a <META> tag that mentions the document's
           encoding.
        """
        if not isinstance(formatter, Formatter):
            if not isinstance(formatter, Callable):
                formatter = self._formatter_for_name(formatter)
            else:
                attrs = []
                if self.attrs:
                    for key, val in sorted(self.attrs.items()):
                        if val is None:
                            decoded = key
                        else:
                            if isinstance(val, list) or isinstance(val, tuple):
                                val = ' '.join(val)
                            else:
                                if not isinstance(val, str):
                                    val = str(val)
                                else:
                                    if isinstance(val, AttributeValueWithCharsetSubstitution):
                                        if eventual_encoding is not None:
                                            val = val.encode(eventual_encoding)
                                text = self.format_string(val, formatter)
                                decoded = str(key) + '=' + EntitySubstitution.quoted_attribute_value(text)
                        attrs.append(decoded)

                close = ''
                closeTag = ''
                prefix = ''
                if self.prefix:
                    prefix = self.prefix + ':'
                if self.is_empty_element:
                    close = ''
                    if isinstance(formatter, Formatter):
                        close = formatter.void_element_close_prefix or close
                else:
                    closeTag = '</%s%s>' % (prefix, self.name)
                pretty_print = self._should_pretty_print(indent_level)
                space = ''
                indent_space = ''
                if indent_level is not None:
                    indent_space = ' ' * (indent_level - 1)
                if pretty_print:
                    space = indent_space
                    indent_contents = indent_level + 1
                else:
                    indent_contents = None
                contents = self.decode_contents(indent_contents, eventual_encoding, formatter)
                if self.hidden:
                    s = contents
                else:
                    s = []
                    attribute_string = ''
                    if attrs:
                        attribute_string = ' ' + ' '.join(attrs)
                    if indent_level is not None:
                        s.append(indent_space)
                    s.append('<%s%s%s%s>' % (
                     prefix, self.name, attribute_string, close))
                    if pretty_print:
                        s.append('\n')
                    s.append(contents)
                    if pretty_print:
                        if contents:
                            if contents[(-1)] != '\n':
                                s.append('\n')
                    if pretty_print:
                        if closeTag:
                            s.append(space)
        else:
            s.append(closeTag)
            if indent_level is not None:
                if closeTag:
                    if self.next_sibling:
                        s.append('\n')
            s = ''.join(s)
        return s

    def prettify(self, encoding=None, formatter='minimal'):
        if encoding is None:
            return self.decode(True, formatter=formatter)
        else:
            return self.encode(encoding, True, formatter=formatter)

    def decode_contents(self, indent_level=None, eventual_encoding=DEFAULT_OUTPUT_ENCODING, formatter='minimal'):
        """Renders the contents of this tag as a Unicode string.

        :param indent_level: Each line of the rendering will be
           indented this many spaces.

        :param eventual_encoding: The tag is destined to be
           encoded into this encoding. This method is _not_
           responsible for performing that encoding. This information
           is passed in so that it can be substituted in if the
           document contains a <META> tag that mentions the document's
           encoding.

        :param formatter: The output formatter responsible for converting
           entities to Unicode characters.
        """
        if not isinstance(formatter, Formatter):
            if not isinstance(formatter, Callable):
                formatter = self._formatter_for_name(formatter)
        pretty_print = indent_level is not None
        s = []
        for c in self:
            text = None
            if isinstance(c, NavigableString):
                text = c.output_ready(formatter)
            else:
                if isinstance(c, Tag):
                    s.append(c.decode(indent_level, eventual_encoding, formatter))
            if text:
                if indent_level:
                    if not self.name == 'pre':
                        text = text.strip()
            if text:
                if pretty_print:
                    if not self.name == 'pre':
                        s.append(' ' * (indent_level - 1))
                s.append(text)
                if pretty_print and not self.name == 'pre':
                    s.append('\n')

        return ''.join(s)

    def encode_contents(self, indent_level=None, encoding=DEFAULT_OUTPUT_ENCODING, formatter='minimal'):
        """Renders the contents of this tag as a bytestring.

        :param indent_level: Each line of the rendering will be
           indented this many spaces.

        :param eventual_encoding: The bytestring will be in this encoding.

        :param formatter: The output formatter responsible for converting
           entities to Unicode characters.
        """
        contents = self.decode_contents(indent_level, encoding, formatter)
        return contents.encode(encoding)

    def renderContents(self, encoding=DEFAULT_OUTPUT_ENCODING, prettyPrint=False, indentLevel=0):
        if not prettyPrint:
            indentLevel = None
        return self.encode_contents(indent_level=indentLevel,
          encoding=encoding)

    def find(self, name=None, attrs={}, recursive=True, text=None, **kwargs):
        """Return only the first child of this Tag matching the given
        criteria."""
        r = None
        l = (self.find_all)(name, attrs, recursive, text, 1, **kwargs)
        if l:
            r = l[0]
        return r

    findChild = find

    def find_all(self, name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs):
        """Extracts a list of Tag objects that match the given
        criteria.  You can specify the name of the Tag and any
        attributes you want the Tag to have.

        The value of a key-value pair in the 'attrs' map can be a
        string, a list of strings, a regular expression object, or a
        callable that takes a string and returns whether or not the
        string matches for some custom definition of 'matches'. The
        same is true of the tag name."""
        generator = self.descendants
        if not recursive:
            generator = self.children
        return (self._find_all)(name, attrs, text, limit, generator, **kwargs)

    findAll = find_all
    findChildren = find_all

    @property
    def children(self):
        return iter(self.contents)

    @property
    def descendants(self):
        if not len(self.contents):
            return
        stopNode = self._last_descendant().next_element
        current = self.contents[0]
        while current is not stopNode:
            yield current
            current = current.next_element

    def select_one(self, selector, namespaces=None, **kwargs):
        """Perform a CSS selection operation on the current element."""
        value = (self.select)(selector, namespaces, 1, **kwargs)
        if value:
            return value[0]

    def select(self, selector, namespaces=None, limit=None, **kwargs):
        """Perform a CSS selection operation on the current element.

        This uses the SoupSieve library.

        :param selector: A string containing a CSS selector.

        :param namespaces: A dictionary mapping namespace prefixes
        used in the CSS selector to namespace URIs. By default,
        Beautiful Soup will use the prefixes it encountered while
        parsing the document.

        :param limit: After finding this number of results, stop looking.

        :param kwargs: Any extra arguments you'd like to pass in to
        soupsieve.select().
        """
        if namespaces is None:
            namespaces = self._namespaces
        else:
            if limit is None:
                limit = 0
            if soupsieve is None:
                raise NotImplementedError('Cannot execute CSS selectors because the soupsieve package is not installed.')
        return (soupsieve.select)(selector, self, namespaces, limit, **kwargs)

    def childGenerator(self):
        return self.children

    def recursiveChildGenerator(self):
        return self.descendants

    def has_key(self, key):
        """This was kind of misleading because has_key() (attributes)
        was different from __in__ (contents). has_key() is gone in
        Python 3, anyway."""
        warnings.warn('has_key is deprecated. Use has_attr("%s") instead.' % key)
        return self.has_attr(key)


class SoupStrainer(object):
    __doc__ = 'Encapsulates a number of ways of matching a markup element (tag or\n    text).'

    def __init__(self, name=None, attrs={}, text=None, **kwargs):
        self.name = self._normalize_search_value(name)
        if not isinstance(attrs, dict):
            kwargs['class'] = attrs
            attrs = None
        if 'class_' in kwargs:
            kwargs['class'] = kwargs['class_']
            del kwargs['class_']
        if kwargs:
            if attrs:
                attrs = attrs.copy()
                attrs.update(kwargs)
            else:
                attrs = kwargs
        normalized_attrs = {}
        for key, value in list(attrs.items()):
            normalized_attrs[key] = self._normalize_search_value(value)

        self.attrs = normalized_attrs
        self.text = self._normalize_search_value(text)

    def _normalize_search_value(self, value):
        if isinstance(value, str) or isinstance(value, Callable) or hasattr(value, 'match') or isinstance(value, bool) or value is None:
            return value
        else:
            if isinstance(value, bytes):
                return value.decode('utf8')
            if hasattr(value, '__iter__'):
                new_value = []
                for v in value:
                    if hasattr(v, '__iter__') and not isinstance(v, bytes) and not isinstance(v, str):
                        new_value.append(v)
                    else:
                        new_value.append(self._normalize_search_value(v))

                return new_value
            return str(str(value))

    def __str__(self):
        if self.text:
            return self.text
        else:
            return '%s|%s' % (self.name, self.attrs)

    def search_tag(self, markup_name=None, markup_attrs={}):
        found = None
        markup = None
        if isinstance(markup_name, Tag):
            markup = markup_name
            markup_attrs = markup
        call_function_with_tag_data = isinstance(self.name, Callable) and not isinstance(markup_name, Tag)
        if not self.name or call_function_with_tag_data or markup and self._matches(markup, self.name) or not markup and self._matches(markup_name, self.name):
            if call_function_with_tag_data:
                match = self.name(markup_name, markup_attrs)
            else:
                match = True
                markup_attr_map = None
                for attr, match_against in list(self.attrs.items()):
                    if not markup_attr_map:
                        if hasattr(markup_attrs, 'get'):
                            markup_attr_map = markup_attrs
                        else:
                            markup_attr_map = {}
                            for k, v in markup_attrs:
                                markup_attr_map[k] = v

                        attr_value = markup_attr_map.get(attr)
                        if not self._matches(attr_value, match_against):
                            match = False
                            break

            if match:
                if markup:
                    found = markup
                else:
                    found = markup_name
        if found:
            if self.text:
                if not self._matches(found.string, self.text):
                    found = None
        return found

    searchTag = search_tag

    def search(self, markup):
        found = None
        if hasattr(markup, '__iter__'):
            if not isinstance(markup, (Tag, str)):
                for element in markup:
                    if isinstance(element, NavigableString):
                        if self.search(element):
                            found = element
                            break

        else:
            if isinstance(markup, Tag):
                if not self.text or self.name or self.attrs:
                    found = self.search_tag(markup)
            else:
                if isinstance(markup, NavigableString) or isinstance(markup, str):
                    if not self.name:
                        if not self.attrs:
                            if self._matches(markup, self.text):
                                found = markup
                else:
                    raise Exception("I don't know how to match against a %s" % markup.__class__)
        return found

    def _matches(self, markup, match_against, already_tried=None):
        result = False
        if isinstance(markup, list) or isinstance(markup, tuple):
            for item in markup:
                if self._matches(item, match_against):
                    return True

            if self._matches(' '.join(markup), match_against):
                return True
            else:
                return False
        if match_against is True:
            return markup is not None
        else:
            if isinstance(match_against, Callable):
                return match_against(markup)
            else:
                original_markup = markup
                if isinstance(markup, Tag):
                    markup = markup.name
                markup = self._normalize_search_value(markup)
                if markup is None:
                    return not match_against
                if hasattr(match_against, '__iter__') and not isinstance(match_against, str):
                    if not already_tried:
                        already_tried = set()
                    for item in match_against:
                        if item.__hash__:
                            key = item
                        else:
                            key = id(item)
                        if key in already_tried:
                            continue
                        else:
                            already_tried.add(key)
                        if self._matches(original_markup, item, already_tried):
                            return True
                    else:
                        return False

                match = False
                if not match:
                    if isinstance(match_against, str):
                        match = markup == match_against
                if not match:
                    if hasattr(match_against, 'search'):
                        return match_against.search(markup)
                if not match:
                    if isinstance(original_markup, Tag):
                        if original_markup.prefix:
                            return self._matches(original_markup.prefix + ':' + original_markup.name, match_against)
            return match


class ResultSet(list):
    __doc__ = 'A ResultSet is just a list that keeps track of the SoupStrainer\n    that created it.'

    def __init__(self, source, result=()):
        super(ResultSet, self).__init__(result)
        self.source = source

    def __getattr__(self, key):
        raise AttributeError("ResultSet object has no attribute '%s'. You're probably treating a list of items like a single item. Did you call find_all() when you meant to call find()?" % key)