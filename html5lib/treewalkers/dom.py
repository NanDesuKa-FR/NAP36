# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\treewalkers\dom.py
from __future__ import absolute_import, division, unicode_literals
from xml.dom import Node
from . import base

class TreeWalker(base.NonRecursiveTreeWalker):

    def getNodeDetails(self, node):
        if node.nodeType == Node.DOCUMENT_TYPE_NODE:
            return (base.DOCTYPE, node.name, node.publicId, node.systemId)
        else:
            if node.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
                return (
                 base.TEXT, node.nodeValue)
            else:
                if node.nodeType == Node.ELEMENT_NODE:
                    attrs = {}
                    for attr in list(node.attributes.keys()):
                        attr = node.getAttributeNode(attr)
                        if attr.namespaceURI:
                            attrs[(attr.namespaceURI, attr.localName)] = attr.value
                        else:
                            attrs[(None, attr.name)] = attr.value

                    return (
                     base.ELEMENT, node.namespaceURI, node.nodeName,
                     attrs, node.hasChildNodes())
                if node.nodeType == Node.COMMENT_NODE:
                    return (
                     base.COMMENT, node.nodeValue)
                if node.nodeType in (Node.DOCUMENT_NODE, Node.DOCUMENT_FRAGMENT_NODE):
                    return (
                     base.DOCUMENT,)
            return (base.UNKNOWN, node.nodeType)

    def getFirstChild(self, node):
        return node.firstChild

    def getNextSibling(self, node):
        return node.nextSibling

    def getParentNode(self, node):
        return node.parentNode