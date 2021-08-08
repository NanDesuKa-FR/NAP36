# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\treewalkers\etree_lxml.py
from __future__ import absolute_import, division, unicode_literals
from six import text_type
from lxml import etree
from ..treebuilders.etree import tag_regexp
from . import base
from .. import _ihatexml

def ensure_str(s):
    if s is None:
        return
    else:
        if isinstance(s, text_type):
            return s
        return s.decode('ascii', 'strict')


class Root(object):

    def __init__(self, et):
        self.elementtree = et
        self.children = []
        try:
            if et.docinfo.internalDTD:
                self.children.append(Doctype(self, ensure_str(et.docinfo.root_name), ensure_str(et.docinfo.public_id), ensure_str(et.docinfo.system_url)))
        except AttributeError:
            pass

        try:
            node = et.getroot()
        except AttributeError:
            node = et

        while node.getprevious() is not None:
            node = node.getprevious()

        while node is not None:
            self.children.append(node)
            node = node.getnext()

        self.text = None
        self.tail = None

    def __getitem__(self, key):
        return self.children[key]

    def getnext(self):
        pass

    def __len__(self):
        return 1


class Doctype(object):

    def __init__(self, root_node, name, public_id, system_id):
        self.root_node = root_node
        self.name = name
        self.public_id = public_id
        self.system_id = system_id
        self.text = None
        self.tail = None

    def getnext(self):
        return self.root_node.children[1]


class FragmentRoot(Root):

    def __init__(self, children):
        self.children = [FragmentWrapper(self, child) for child in children]
        self.text = self.tail = None

    def getnext(self):
        pass


class FragmentWrapper(object):

    def __init__(self, fragment_root, obj):
        self.root_node = fragment_root
        self.obj = obj
        if hasattr(self.obj, 'text'):
            self.text = ensure_str(self.obj.text)
        else:
            self.text = None
        if hasattr(self.obj, 'tail'):
            self.tail = ensure_str(self.obj.tail)
        else:
            self.tail = None

    def __getattr__(self, name):
        return getattr(self.obj, name)

    def getnext(self):
        siblings = self.root_node.children
        idx = siblings.index(self)
        if idx < len(siblings) - 1:
            return siblings[(idx + 1)]
        else:
            return

    def __getitem__(self, key):
        return self.obj[key]

    def __bool__(self):
        return bool(self.obj)

    def getparent(self):
        pass

    def __str__(self):
        return str(self.obj)

    def __unicode__(self):
        return str(self.obj)

    def __len__(self):
        return len(self.obj)


class TreeWalker(base.NonRecursiveTreeWalker):

    def __init__(self, tree):
        if isinstance(tree, list):
            self.fragmentChildren = set(tree)
            tree = FragmentRoot(tree)
        else:
            self.fragmentChildren = set()
            tree = Root(tree)
        base.NonRecursiveTreeWalker.__init__(self, tree)
        self.filter = _ihatexml.InfosetFilter()

    def getNodeDetails(self, node):
        if isinstance(node, tuple):
            node, key = node
            assert key in ('text', 'tail'), 'Text nodes are text or tail, found %s' % key
            return (
             base.TEXT, ensure_str(getattr(node, key)))
        else:
            if isinstance(node, Root):
                return (
                 base.DOCUMENT,)
            else:
                if isinstance(node, Doctype):
                    return (
                     base.DOCTYPE, node.name, node.public_id, node.system_id)
                else:
                    if isinstance(node, FragmentWrapper):
                        if not hasattr(node, 'tag'):
                            return (
                             base.TEXT, ensure_str(node.obj))
                    if node.tag == etree.Comment:
                        return (
                         base.COMMENT, ensure_str(node.text))
                    if node.tag == etree.Entity:
                        return (
                         base.ENTITY, ensure_str(node.text)[1:-1])
                match = tag_regexp.match(ensure_str(node.tag))
                if match:
                    namespace, tag = match.groups()
                else:
                    namespace = None
                tag = ensure_str(node.tag)
            attrs = {}
            for name, value in list(node.attrib.items()):
                name = ensure_str(name)
                value = ensure_str(value)
                match = tag_regexp.match(name)
                if match:
                    attrs[(match.group(1), match.group(2))] = value
                else:
                    attrs[(None, name)] = value

            return (
             base.ELEMENT, namespace, self.filter.fromXmlName(tag),
             attrs, len(node) > 0 or node.text)

    def getFirstChild(self, node):
        assert not isinstance(node, tuple), 'Text nodes have no children'
        if not len(node):
            if not node.text:
                raise AssertionError('Node has no children')
        if node.text:
            return (node, 'text')
        else:
            return node[0]

    def getNextSibling(self, node):
        if isinstance(node, tuple):
            node, key = node
            assert key in ('text', 'tail'), 'Text nodes are text or tail, found %s' % key
            if key == 'text':
                if len(node):
                    return node[0]
                else:
                    return
            else:
                return node.getnext()
        if node.tail:
            return (node, 'tail')
        else:
            return node.getnext()

    def getParentNode(self, node):
        if isinstance(node, tuple):
            node, key = node
            assert key in ('text', 'tail'), 'Text nodes are text or tail, found %s' % key
            if key == 'text':
                return node
        else:
            if node in self.fragmentChildren:
                return
        return node.getparent()