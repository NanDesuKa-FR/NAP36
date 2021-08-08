# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\filters\optionaltags.py
from __future__ import absolute_import, division, unicode_literals
from . import base

class Filter(base.Filter):
    __doc__ = 'Removes optional tags from the token stream'

    def slider(self):
        previous1 = previous2 = None
        for token in self.source:
            if previous1 is not None:
                yield (
                 previous2, previous1, token)
            previous2 = previous1
            previous1 = token

        if previous1 is not None:
            yield (
             previous2, previous1, None)

    def __iter__(self):
        for previous, token, next in self.slider():
            type = token['type']
            if type == 'StartTag':
                if token['data'] or not self.is_optional_start(token['name'], previous, next):
                    yield token
            else:
                if type == 'EndTag':
                    if not self.is_optional_end(token['name'], next):
                        yield token
                else:
                    yield token

    def is_optional_start(self, tagname, previous, next):
        type = next and next['type'] or None
        if tagname in 'html':
            return type not in ('Comment', 'SpaceCharacters')
        if tagname == 'head':
            if type in ('StartTag', 'EmptyTag'):
                return True
            if type == 'EndTag':
                return next['name'] == 'head'
        else:
            if tagname == 'body':
                if type in ('Comment', 'SpaceCharacters'):
                    return False
                else:
                    if type == 'StartTag':
                        return next['name'] not in ('script', 'style')
                    return True
            else:
                if tagname == 'colgroup':
                    if type in ('StartTag', 'EmptyTag'):
                        return next['name'] == 'col'
                    else:
                        return False
                else:
                    if tagname == 'tbody':
                        if type == 'StartTag':
                            if previous:
                                if previous['type'] == 'EndTag':
                                    if previous['name'] in ('tbody', 'thead', 'tfoot'):
                                        return False
                            return next['name'] == 'tr'
                        else:
                            return False
            return False

    def is_optional_end(self, tagname, next):
        type = next and next['type'] or None
        if tagname in ('html', 'head', 'body'):
            return type not in ('Comment', 'SpaceCharacters')
        else:
            if tagname in ('li', 'optgroup', 'tr'):
                if type == 'StartTag':
                    return next['name'] == tagname
                else:
                    return type == 'EndTag' or type is None
            else:
                if tagname in ('dt', 'dd'):
                    if type == 'StartTag':
                        return next['name'] in ('dt', 'dd')
                    else:
                        if tagname == 'dd':
                            return type == 'EndTag' or type is None
                        return False
                else:
                    if tagname == 'p':
                        if type in ('StartTag', 'EmptyTag'):
                            return next['name'] in ('address', 'article', 'aside',
                                                    'blockquote', 'datagrid', 'dialog',
                                                    'dir', 'div', 'dl', 'fieldset',
                                                    'footer', 'form', 'h1', 'h2',
                                                    'h3', 'h4', 'h5', 'h6', 'header',
                                                    'hr', 'menu', 'nav', 'ol', 'p',
                                                    'pre', 'section', 'table', 'ul')
                        else:
                            return type == 'EndTag' or type is None
                    else:
                        if tagname == 'option':
                            if type == 'StartTag':
                                return next['name'] in ('option', 'optgroup')
                            else:
                                return type == 'EndTag' or type is None
                        else:
                            if tagname in ('rt', 'rp'):
                                if type == 'StartTag':
                                    return next['name'] in ('rt', 'rp')
                                else:
                                    return type == 'EndTag' or type is None
                            else:
                                if tagname == 'colgroup':
                                    if type in ('Comment', 'SpaceCharacters'):
                                        return False
                                    else:
                                        if type == 'StartTag':
                                            return next['name'] != 'colgroup'
                                        return True
                                else:
                                    if tagname in ('thead', 'tbody'):
                                        if type == 'StartTag':
                                            return next['name'] in ('tbody', 'tfoot')
                                        else:
                                            if tagname == 'tbody':
                                                return type == 'EndTag' or type is None
                                            return False
                                    else:
                                        if tagname == 'tfoot':
                                            if type == 'StartTag':
                                                return next['name'] == 'tbody'
                                            else:
                                                return type == 'EndTag' or type is None
                                        else:
                                            if tagname in ('td', 'th'):
                                                if type == 'StartTag':
                                                    return next['name'] in ('td', 'th')
                                                else:
                                                    return type == 'EndTag' or type is None
            return False