# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\treebuilders\base.py
from __future__ import absolute_import, division, unicode_literals
from six import text_type
from ..constants import scopingElements, tableInsertModeElements, namespaces
Marker = None
listElementsMap = {None:(
  frozenset(scopingElements), False), 
 'button':(
  frozenset(scopingElements | set([(namespaces['html'], 'button')])), False), 
 'list':(
  frozenset(scopingElements | set([(namespaces['html'], 'ol'),
   (
    namespaces['html'], 'ul')])), False), 
 'table':(
  frozenset([(namespaces['html'], 'html'),
   (
    namespaces['html'], 'table')]), False), 
 'select':(
  frozenset([(namespaces['html'], 'optgroup'),
   (
    namespaces['html'], 'option')]), True)}

class Node(object):
    __doc__ = 'Represents an item in the tree'

    def __init__(self, name):
        """Creates a Node

        :arg name: The tag name associated with the node

        """
        self.name = name
        self.parent = None
        self.value = None
        self.attributes = {}
        self.childNodes = []
        self._flags = []

    def __str__(self):
        attributesStr = ' '.join(['%s="%s"' % (name, value) for name, value in self.attributes.items()])
        if attributesStr:
            return '<%s %s>' % (self.name, attributesStr)
        else:
            return '<%s>' % self.name

    def __repr__(self):
        return '<%s>' % self.name

    def appendChild(self, node):
        """Insert node as a child of the current node

        :arg node: the node to insert

        """
        raise NotImplementedError

    def insertText(self, data, insertBefore=None):
        """Insert data as text in the current node, positioned before the
        start of node insertBefore or to the end of the node's text.

        :arg data: the data to insert

        :arg insertBefore: True if you want to insert the text before the node
            and False if you want to insert it after the node

        """
        raise NotImplementedError

    def insertBefore(self, node, refNode):
        """Insert node as a child of the current node, before refNode in the
        list of child nodes. Raises ValueError if refNode is not a child of
        the current node

        :arg node: the node to insert

        :arg refNode: the child node to insert the node before

        """
        raise NotImplementedError

    def removeChild(self, node):
        """Remove node from the children of the current node

        :arg node: the child node to remove

        """
        raise NotImplementedError

    def reparentChildren(self, newParent):
        """Move all the children of the current node to newParent.
        This is needed so that trees that don't store text as nodes move the
        text in the correct way

        :arg newParent: the node to move all this node's children to

        """
        for child in self.childNodes:
            newParent.appendChild(child)

        self.childNodes = []

    def cloneNode(self):
        """Return a shallow copy of the current node i.e. a node with the same
        name and attributes but with no parent or child nodes
        """
        raise NotImplementedError

    def hasContent(self):
        """Return true if the node has children or text, false otherwise
        """
        raise NotImplementedError


class ActiveFormattingElements(list):

    def append(self, node):
        equalCount = 0
        if node != Marker:
            for element in self[::-1]:
                if element == Marker:
                    break
                else:
                    if self.nodesEqual(element, node):
                        equalCount += 1
                    if equalCount == 3:
                        self.remove(element)
                        break

        list.append(self, node)

    def nodesEqual(self, node1, node2):
        if not node1.nameTuple == node2.nameTuple:
            return False
        else:
            if not node1.attributes == node2.attributes:
                return False
            return True


class TreeBuilder(object):
    __doc__ = 'Base treebuilder implementation\n\n    * documentClass - the class to use for the bottommost node of a document\n    * elementClass - the class to use for HTML Elements\n    * commentClass - the class to use for comments\n    * doctypeClass - the class to use for doctypes\n\n    '
    documentClass = None
    elementClass = None
    commentClass = None
    doctypeClass = None
    fragmentClass = None

    def __init__(self, namespaceHTMLElements):
        """Create a TreeBuilder

        :arg namespaceHTMLElements: whether or not to namespace HTML elements

        """
        if namespaceHTMLElements:
            self.defaultNamespace = 'http://www.w3.org/1999/xhtml'
        else:
            self.defaultNamespace = None
        self.reset()

    def reset(self):
        self.openElements = []
        self.activeFormattingElements = ActiveFormattingElements()
        self.headPointer = None
        self.formPointer = None
        self.insertFromTable = False
        self.document = self.documentClass()

    def elementInScope(self, target, variant=None):
        exactNode = hasattr(target, 'nameTuple')
        if not exactNode:
            if isinstance(target, text_type):
                target = (
                 namespaces['html'], target)
        else:
            assert isinstance(target, tuple)
            listElements, invert = listElementsMap[variant]
            for node in reversed(self.openElements):
                if exactNode:
                    if node == target:
                        return True
                    else:
                        if not exactNode:
                            if node.nameTuple == target:
                                return True
                        if invert ^ (node.nameTuple in listElements):
                            return False

            assert False

    def reconstructActiveFormattingElements(self):
        if not self.activeFormattingElements:
            return
        i = len(self.activeFormattingElements) - 1
        entry = self.activeFormattingElements[i]
        if entry == Marker or entry in self.openElements:
            return
        while entry != Marker and entry not in self.openElements:
            if i == 0:
                i = -1
                break
            i -= 1
            entry = self.activeFormattingElements[i]

        while 1:
            i += 1
            entry = self.activeFormattingElements[i]
            clone = entry.cloneNode()
            element = self.insertElement({'type':'StartTag',  'name':clone.name, 
             'namespace':clone.namespace, 
             'data':clone.attributes})
            self.activeFormattingElements[i] = element
            if element == self.activeFormattingElements[(-1)]:
                break

    def clearActiveFormattingElements(self):
        entry = self.activeFormattingElements.pop()
        while self.activeFormattingElements and entry != Marker:
            entry = self.activeFormattingElements.pop()

    def elementInActiveFormattingElements(self, name):
        """Check if an element exists between the end of the active
        formatting elements and the last marker. If it does, return it, else
        return false"""
        for item in self.activeFormattingElements[::-1]:
            if item == Marker:
                break
            else:
                if item.name == name:
                    return item

        return False

    def insertRoot(self, token):
        element = self.createElement(token)
        self.openElements.append(element)
        self.document.appendChild(element)

    def insertDoctype(self, token):
        name = token['name']
        publicId = token['publicId']
        systemId = token['systemId']
        doctype = self.doctypeClass(name, publicId, systemId)
        self.document.appendChild(doctype)

    def insertComment(self, token, parent=None):
        if parent is None:
            parent = self.openElements[(-1)]
        parent.appendChild(self.commentClass(token['data']))

    def createElement(self, token):
        """Create an element but don't insert it anywhere"""
        name = token['name']
        namespace = token.get('namespace', self.defaultNamespace)
        element = self.elementClass(name, namespace)
        element.attributes = token['data']
        return element

    def _getInsertFromTable(self):
        return self._insertFromTable

    def _setInsertFromTable(self, value):
        """Switch the function used to insert an element from the
        normal one to the misnested table one and back again"""
        self._insertFromTable = value
        if value:
            self.insertElement = self.insertElementTable
        else:
            self.insertElement = self.insertElementNormal

    insertFromTable = property(_getInsertFromTable, _setInsertFromTable)

    def insertElementNormal(self, token):
        name = token['name']
        assert isinstance(name, text_type), 'Element %s not unicode' % name
        namespace = token.get('namespace', self.defaultNamespace)
        element = self.elementClass(name, namespace)
        element.attributes = token['data']
        self.openElements[(-1)].appendChild(element)
        self.openElements.append(element)
        return element

    def insertElementTable(self, token):
        """Create an element and insert it into the tree"""
        element = self.createElement(token)
        if self.openElements[(-1)].name not in tableInsertModeElements:
            return self.insertElementNormal(token)
        else:
            parent, insertBefore = self.getTableMisnestedNodePosition()
            if insertBefore is None:
                parent.appendChild(element)
            else:
                parent.insertBefore(element, insertBefore)
            self.openElements.append(element)
            return element

    def insertText(self, data, parent=None):
        """Insert text data."""
        if parent is None:
            parent = self.openElements[(-1)]
        else:
            if not self.insertFromTable or self.insertFromTable and self.openElements[(-1)].name not in tableInsertModeElements:
                parent.insertText(data)
            else:
                parent, insertBefore = self.getTableMisnestedNodePosition()
                parent.insertText(data, insertBefore)

    def getTableMisnestedNodePosition(self):
        """Get the foster parent element, and sibling to insert before
        (or None) when inserting a misnested table node"""
        lastTable = None
        fosterParent = None
        insertBefore = None
        for elm in self.openElements[::-1]:
            if elm.name == 'table':
                lastTable = elm
                break

        if lastTable:
            if lastTable.parent:
                fosterParent = lastTable.parent
                insertBefore = lastTable
            else:
                fosterParent = self.openElements[(self.openElements.index(lastTable) - 1)]
        else:
            fosterParent = self.openElements[0]
        return (
         fosterParent, insertBefore)

    def generateImpliedEndTags(self, exclude=None):
        name = self.openElements[(-1)].name
        if name in frozenset(('dd', 'dt', 'li', 'option', 'optgroup', 'p', 'rp', 'rt')):
            if name != exclude:
                self.openElements.pop()
                self.generateImpliedEndTags(exclude)

    def getDocument(self):
        """Return the final tree"""
        return self.document

    def getFragment(self):
        """Return the final fragment"""
        fragment = self.fragmentClass()
        self.openElements[0].reparentChildren(fragment)
        return fragment

    def testSerializer(self, node):
        """Serialize the subtree of node in the format required by unit tests

        :arg node: the node from which to start serializing

        """
        raise NotImplementedError