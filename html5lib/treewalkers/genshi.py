# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\treewalkers\genshi.py
from __future__ import absolute_import, division, unicode_literals
from genshi.core import QName
from genshi.core import START, END, XML_NAMESPACE, DOCTYPE, TEXT
from genshi.core import START_NS, END_NS, START_CDATA, END_CDATA, PI, COMMENT
from . import base
from ..constants import voidElements, namespaces

class TreeWalker(base.TreeWalker):

    def __iter__(self):
        previous = None
        for event in self.tree:
            if previous is not None:
                for token in self.tokens(previous, event):
                    yield token

            previous = event

        if previous is not None:
            for token in self.tokens(previous, None):
                yield token

    def tokens(self, event, next):
        kind, data, _ = event
        if kind == START:
            tag, attribs = data
            name = tag.localname
            namespace = tag.namespace
            converted_attribs = {}
            for k, v in attribs:
                if isinstance(k, QName):
                    converted_attribs[(k.namespace, k.localname)] = v
                else:
                    converted_attribs[(None, k)] = v

            if namespace == namespaces['html']:
                if name in voidElements:
                    for token in self.emptyTag(namespace, name, converted_attribs, not next or next[0] != END or next[1] != tag):
                        yield token

            else:
                yield self.startTag(namespace, name, converted_attribs)
        else:
            if kind == END:
                name = data.localname
                namespace = data.namespace
                if namespace != namespaces['html'] or name not in voidElements:
                    yield self.endTag(namespace, name)
            else:
                if kind == COMMENT:
                    yield self.comment(data)
                else:
                    if kind == TEXT:
                        for token in self.text(data):
                            yield token

                    else:
                        if kind == DOCTYPE:
                            yield (self.doctype)(*data)
                        else:
                            if kind in (XML_NAMESPACE, DOCTYPE, START_NS, END_NS,
                             START_CDATA, END_CDATA, PI):
                                pass
                            else:
                                yield self.unknown(kind)