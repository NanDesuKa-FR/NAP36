# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\treewalkers\__init__.py
"""A collection of modules for iterating through different kinds of
tree, generating tokens identical to those produced by the tokenizer
module.

To create a tree walker for a new type of tree, you need to do
implement a tree walker object (called TreeWalker by convention) that
implements a 'serialize' method taking a tree as sole argument and
returning an iterator generating tokens.
"""
from __future__ import absolute_import, division, unicode_literals
from .. import constants
from .._utils import default_etree
__all__ = [
 'getTreeWalker', 'pprint']
treeWalkerCache = {}

def getTreeWalker(treeType, implementation=None, **kwargs):
    """Get a TreeWalker class for various types of tree with built-in support

    :arg str treeType: the name of the tree type required (case-insensitive).
        Supported values are:

        * "dom": The xml.dom.minidom DOM implementation
        * "etree": A generic walker for tree implementations exposing an
          elementtree-like interface (known to work with ElementTree,
          cElementTree and lxml.etree).
        * "lxml": Optimized walker for lxml.etree
        * "genshi": a Genshi stream

    :arg implementation: A module implementing the tree type e.g.
        xml.etree.ElementTree or cElementTree (Currently applies to the "etree"
        tree type only).

    :arg kwargs: keyword arguments passed to the etree walker--for other
        walkers, this has no effect

    :returns: a TreeWalker class

    """
    treeType = treeType.lower()
    if treeType not in treeWalkerCache:
        if treeType == 'dom':
            from . import dom
            treeWalkerCache[treeType] = dom.TreeWalker
        else:
            if treeType == 'genshi':
                from . import genshi
                treeWalkerCache[treeType] = genshi.TreeWalker
            else:
                if treeType == 'lxml':
                    from . import etree_lxml
                    treeWalkerCache[treeType] = etree_lxml.TreeWalker
                elif treeType == 'etree':
                    from . import etree
                    if implementation is None:
                        implementation = default_etree
                    return (etree.getETreeModule)(implementation, **kwargs).TreeWalker
    return treeWalkerCache.get(treeType)


def concatenateCharacterTokens(tokens):
    pendingCharacters = []
    for token in tokens:
        type = token['type']
        if type in ('Characters', 'SpaceCharacters'):
            pendingCharacters.append(token['data'])
        else:
            if pendingCharacters:
                yield {'type':'Characters', 
                 'data':''.join(pendingCharacters)}
                pendingCharacters = []
            yield token

    if pendingCharacters:
        yield {'type':'Characters', 
         'data':''.join(pendingCharacters)}


def pprint(walker):
    """Pretty printer for tree walkers

    Takes a TreeWalker instance and pretty prints the output of walking the tree.

    :arg walker: a TreeWalker instance

    """
    output = []
    indent = 0
    for token in concatenateCharacterTokens(walker):
        type = token['type']
        if type in ('StartTag', 'EmptyTag'):
            if token['namespace'] and token['namespace'] != constants.namespaces['html']:
                if token['namespace'] in constants.prefixes:
                    ns = constants.prefixes[token['namespace']]
                else:
                    ns = token['namespace']
                name = '%s %s' % (ns, token['name'])
            else:
                name = token['name']
        else:
            output.append('%s<%s>' % (' ' * indent, name))
            indent += 2
            attrs = token['data']
            for (namespace, localname), value in sorted(attrs.items()):
                if namespace:
                    if namespace in constants.prefixes:
                        ns = constants.prefixes[namespace]
                    else:
                        ns = namespace
                    name = '%s %s' % (ns, localname)
                else:
                    name = localname
                output.append('%s%s="%s"' % (' ' * indent, name, value))

            if type == 'EmptyTag':
                indent -= 2
            else:
                if type == 'EndTag':
                    indent -= 2
                else:
                    if type == 'Comment':
                        output.append('%s<!-- %s -->' % (' ' * indent, token['data']))
                    else:
                        if type == 'Doctype':
                            if token['name']:
                                if token['publicId']:
                                    output.append('%s<!DOCTYPE %s "%s" "%s">' % (
                                     ' ' * indent,
                                     token['name'],
                                     token['publicId'],
                                     token['systemId'] if token['systemId'] else ''))
                                else:
                                    if token['systemId']:
                                        output.append('%s<!DOCTYPE %s "" "%s">' % (
                                         ' ' * indent,
                                         token['name'],
                                         token['systemId']))
                                    else:
                                        output.append('%s<!DOCTYPE %s>' % (' ' * indent,
                                         token['name']))
                            else:
                                output.append('%s<!DOCTYPE >' % (' ' * indent,))
                        else:
                            if type == 'Characters':
                                output.append('%s"%s"' % (' ' * indent, token['data']))
                            else:
                                if type == 'SpaceCharacters':
                                    assert False, 'concatenateCharacterTokens should have got rid of all Space tokens'
                                else:
                                    raise ValueError('Unknown token type, %s' % type)

    return '\n'.join(output)