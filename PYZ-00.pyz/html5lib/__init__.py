# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\__init__.py
"""
HTML parsing library based on the `WHATWG HTML specification
<https://whatwg.org/html>`_. The parser is designed to be compatible with
existing HTML found in the wild and implements well-defined error recovery that
is largely compatible with modern desktop web browsers.

Example usage::

    import html5lib
    with open("my_document.html", "rb") as f:
        tree = html5lib.parse(f)

For convenience, this module re-exports the following names:

* :func:`~.html5parser.parse`
* :func:`~.html5parser.parseFragment`
* :class:`~.html5parser.HTMLParser`
* :func:`~.treebuilders.getTreeBuilder`
* :func:`~.treewalkers.getTreeWalker`
* :func:`~.serializer.serialize`
"""
from __future__ import absolute_import, division, unicode_literals
from .html5parser import HTMLParser, parse, parseFragment
from .treebuilders import getTreeBuilder
from .treewalkers import getTreeWalker
from .serializer import serialize
__all__ = [
 'HTMLParser', 'parse', 'parseFragment', 'getTreeBuilder',
 'getTreeWalker', 'serialize']
__version__ = '1.0.1'