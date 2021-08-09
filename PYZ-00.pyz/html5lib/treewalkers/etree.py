# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\treewalkers\etree.py
from __future__ import absolute_import, division, unicode_literals
from collections import OrderedDict
import re
from six import string_types
from . import base
from .._utils import moduleFactoryFactory
tag_regexp = re.compile('{([^}]*)}(.*)')

def getETreeBuilder(ElementTreeImplementation):
    ElementTree = ElementTreeImplementation
    ElementTreeCommentType = ElementTree.Comment('asd').tag

    class TreeWalker(base.NonRecursiveTreeWalker):
        __doc__ = 'Given the particular ElementTree representation, this implementation,\n        to avoid using recursion, returns "nodes" as tuples with the following\n        content:\n\n        1. The current element\n\n        2. The index of the element relative to its parent\n\n        3. A stack of ancestor elements\n\n        4. A flag "text", "tail" or None to indicate if the current node is a\n           text node; either the text or tail of the current element (1)\n        '

        def getNodeDetails(self, node):
            if isinstance(node, tuple):
                elt, _, _, flag = node
                if flag in ('text', 'tail'):
                    return (
                     base.TEXT, getattr(elt, flag))
                node = elt
            else:
                if not hasattr(node, 'tag'):
                    node = node.getroot()
                if node.tag in ('DOCUMENT_ROOT', 'DOCUMENT_FRAGMENT'):
                    return (
                     base.DOCUMENT,)
            if node.tag == '<!DOCTYPE>':
                return (base.DOCTYPE, node.text,
                 node.get('publicId'), node.get('systemId'))
            else:
                if node.tag == ElementTreeCommentType:
                    return (
                     base.COMMENT, node.text)
                else:
                    assert isinstance(node.tag, string_types), type(node.tag)
                    match = tag_regexp.match(node.tag)
                    if match:
                        namespace, tag = match.groups()
                    else:
                        namespace = None
                    tag = node.tag
                attrs = OrderedDict()
                for name, value in list(node.attrib.items()):
                    match = tag_regexp.match(name)
                    if match:
                        attrs[(match.group(1), match.group(2))] = value
                    else:
                        attrs[(None, name)] = value

                return (
                 base.ELEMENT, namespace, tag,
                 attrs, len(node) or node.text)

        def getFirstChild(self, node):
            if isinstance(node, tuple):
                element, key, parents, flag = node
            else:
                element, key, parents, flag = (
                 node, None, [], None)
            if flag in ('text', 'tail'):
                return
            if element.text:
                return (element, key, parents, 'text')
            else:
                if len(element):
                    parents.append(element)
                    return (element[0], 0, parents, None)
                return

        def getNextSibling(self, node):
            if isinstance(node, tuple):
                element, key, parents, flag = node
            else:
                return
                if flag == 'text':
                    if len(element):
                        parents.append(element)
                        return (
                         element[0], 0, parents, None)
                    else:
                        return
                else:
                    if element.tail:
                        if flag != 'tail':
                            return (
                             element, key, parents, 'tail')
                    if key < len(parents[(-1)]) - 1:
                        return (parents[(-1)][(key + 1)], key + 1, parents, None)
                    else:
                        return

        def getParentNode(self, node):
            if isinstance(node, tuple):
                element, key, parents, flag = node
            else:
                return
                if flag == 'text':
                    if not parents:
                        return element
                    else:
                        return (
                         element, key, parents, None)
                else:
                    parent = parents.pop()
                    if not parents:
                        return parent
                    else:
                        assert list(parents[(-1)]).count(parent) == 1
                        return (parent, list(parents[(-1)]).index(parent), parents, None)

    return locals()


getETreeModule = moduleFactoryFactory(getETreeBuilder)