# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\_tokenizer.py
from __future__ import absolute_import, division, unicode_literals
from six import unichr as chr
from collections import deque
from .constants import spaceCharacters
from .constants import entities
from .constants import asciiLetters, asciiUpper2Lower
from .constants import digits, hexDigits, EOF
from .constants import tokenTypes, tagTokenTypes
from .constants import replacementCharacters
from ._inputstream import HTMLInputStream
from ._trie import Trie
entitiesTrie = Trie(entities)

class HTMLTokenizer(object):
    __doc__ = ' This class takes care of tokenizing HTML.\n\n    * self.currentToken\n      Holds the token that is currently being processed.\n\n    * self.state\n      Holds a reference to the method to be invoked... XXX\n\n    * self.stream\n      Points to HTMLInputStream object.\n    '

    def __init__(self, stream, parser=None, **kwargs):
        self.stream = HTMLInputStream(stream, **kwargs)
        self.parser = parser
        self.escapeFlag = False
        self.lastFourChars = []
        self.state = self.dataState
        self.escape = False
        self.currentToken = None
        super(HTMLTokenizer, self).__init__()

    def __iter__(self):
        """ This is where the magic happens.

        We do our usually processing through the states and when we have a token
        to return we yield the token which pauses processing until the next token
        is requested.
        """
        self.tokenQueue = deque([])
        while self.state():
            while self.stream.errors:
                yield {'type':tokenTypes['ParseError'],  'data':self.stream.errors.pop(0)}

            while self.tokenQueue:
                yield self.tokenQueue.popleft()

    def consumeNumberEntity(self, isHex):
        """This function returns either U+FFFD or the character based on the
        decimal or hexadecimal representation. It also discards ";" if present.
        If not present self.tokenQueue.append({"type": tokenTypes["ParseError"]}) is invoked.
        """
        allowed = digits
        radix = 10
        if isHex:
            allowed = hexDigits
            radix = 16
        charStack = []
        c = self.stream.char()
        while c in allowed and c is not EOF:
            charStack.append(c)
            c = self.stream.char()

        charAsInt = int(''.join(charStack), radix)
        if charAsInt in replacementCharacters:
            char = replacementCharacters[charAsInt]
            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'illegal-codepoint-for-numeric-entity', 
             'datavars':{'charAsInt': charAsInt}})
        else:
            if 55296 <= charAsInt <= 57343 or charAsInt > 1114111:
                char = '�'
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'illegal-codepoint-for-numeric-entity', 
                 'datavars':{'charAsInt': charAsInt}})
            else:
                if 1 <= charAsInt <= 8 or 14 <= charAsInt <= 31 or 127 <= charAsInt <= 159 or 64976 <= charAsInt <= 65007 or charAsInt in frozenset([11, 65534, 65535, 131070,
                 131071, 196606, 196607, 262142,
                 262143, 327678, 327679, 393214,
                 393215, 458750, 458751, 524286,
                 524287, 589822, 589823, 655358,
                 655359, 720894, 720895, 786430,
                 786431, 851966, 851967, 917502,
                 917503, 983038, 983039, 1048574,
                 1048575, 1114110, 1114111]):
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'illegal-codepoint-for-numeric-entity', 
                     'datavars':{'charAsInt': charAsInt}})
        try:
            char = chr(charAsInt)
        except ValueError:
            v = charAsInt - 65536
            char = chr(55296 | v >> 10) + chr(56320 | v & 1023)

        if c != ';':
            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'numeric-entity-without-semicolon'})
            self.stream.unget(c)
        return char

    def consumeEntity(self, allowedChar=None, fromAttribute=False):
        output = '&'
        charStack = [
         self.stream.char()]
        if charStack[0] in spaceCharacters or charStack[0] in (EOF, '<', '&') or allowedChar is not None and allowedChar == charStack[0]:
            self.stream.unget(charStack[0])
        else:
            if charStack[0] == '#':
                hex = False
                charStack.append(self.stream.char())
                if charStack[(-1)] in ('x', 'X'):
                    hex = True
                    charStack.append(self.stream.char())
                if hex and charStack[(-1)] in hexDigits or not hex and charStack[(-1)] in digits:
                    self.stream.unget(charStack[(-1)])
                    output = self.consumeNumberEntity(hex)
                else:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-numeric-entity'})
                    self.stream.unget(charStack.pop())
                    output = '&' + ''.join(charStack)
            else:
                while charStack[(-1)] is not EOF:
                    if not entitiesTrie.has_keys_with_prefix(''.join(charStack)):
                        break
                    charStack.append(self.stream.char())

        try:
            entityName = entitiesTrie.longest_prefix(''.join(charStack[:-1]))
            entityLength = len(entityName)
        except KeyError:
            entityName = None

        if entityName is not None:
            if entityName[(-1)] != ';':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'named-entity-without-semicolon'})
        else:
            if entityName[(-1)] != ';' and fromAttribute:
                if charStack[entityLength] in asciiLetters or charStack[entityLength] in digits or charStack[entityLength] == '=':
                    self.stream.unget(charStack.pop())
                    output = '&' + ''.join(charStack)
                else:
                    output = entities[entityName]
                    self.stream.unget(charStack.pop())
                    output += ''.join(charStack[entityLength:])
            else:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-named-entity'})
                self.stream.unget(charStack.pop())
                output = '&' + ''.join(charStack)
            if fromAttribute:
                self.currentToken['data'][(-1)][1] += output
            else:
                if output in spaceCharacters:
                    tokenType = 'SpaceCharacters'
                else:
                    tokenType = 'Characters'
                self.tokenQueue.append({'type':tokenTypes[tokenType],  'data':output})

    def processEntityInAttribute(self, allowedChar):
        """This method replaces the need for "entityInAttributeValueState".
        """
        self.consumeEntity(allowedChar=allowedChar, fromAttribute=True)

    def emitCurrentToken(self):
        """This method is a generic handler for emitting the tags. It also sets
        the state to "data" because that's what's needed after a token has been
        emitted.
        """
        token = self.currentToken
        if token['type'] in tagTokenTypes:
            token['name'] = token['name'].translate(asciiUpper2Lower)
            if token['type'] == tokenTypes['EndTag']:
                if token['data']:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'attributes-in-end-tag'})
                if token['selfClosing']:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'self-closing-flag-on-end-tag'})
        self.tokenQueue.append(token)
        self.state = self.dataState

    def dataState(self):
        data = self.stream.char()
        if data == '&':
            self.state = self.entityDataState
        else:
            if data == '<':
                self.state = self.tagOpenState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'\x00'})
                else:
                    if data is EOF:
                        return False
                    if data in spaceCharacters:
                        self.tokenQueue.append({'type':tokenTypes['SpaceCharacters'],  'data':data + self.stream.charsUntil(spaceCharacters, True)})
                    else:
                        chars = self.stream.charsUntil(('&', '<', '\x00'))
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + chars})
        return True

    def entityDataState(self):
        self.consumeEntity()
        self.state = self.dataState
        return True

    def rcdataState(self):
        data = self.stream.char()
        if data == '&':
            self.state = self.characterReferenceInRcdata
        else:
            if data == '<':
                self.state = self.rcdataLessThanSignState
            else:
                if data == EOF:
                    return False
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                else:
                    if data in spaceCharacters:
                        self.tokenQueue.append({'type':tokenTypes['SpaceCharacters'],  'data':data + self.stream.charsUntil(spaceCharacters, True)})
                    else:
                        chars = self.stream.charsUntil(('&', '<', '\x00'))
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + chars})
        return True

    def characterReferenceInRcdata(self):
        self.consumeEntity()
        self.state = self.rcdataState
        return True

    def rawtextState(self):
        data = self.stream.char()
        if data == '<':
            self.state = self.rawtextLessThanSignState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
            else:
                if data == EOF:
                    return False
                chars = self.stream.charsUntil(('<', '\x00'))
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + chars})
        return True

    def scriptDataState(self):
        data = self.stream.char()
        if data == '<':
            self.state = self.scriptDataLessThanSignState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
            else:
                if data == EOF:
                    return False
                chars = self.stream.charsUntil(('<', '\x00'))
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + chars})
        return True

    def plaintextState(self):
        data = self.stream.char()
        if data == EOF:
            return False
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
            else:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + self.stream.charsUntil('\x00')})
            return True

    def tagOpenState(self):
        data = self.stream.char()
        if data == '!':
            self.state = self.markupDeclarationOpenState
        else:
            if data == '/':
                self.state = self.closeTagOpenState
            else:
                if data in asciiLetters:
                    self.currentToken = {'type':tokenTypes['StartTag'], 
                     'name':data, 
                     'data':[],  'selfClosing':False, 
                     'selfClosingAcknowledged':False}
                    self.state = self.tagNameState
                else:
                    if data == '>':
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-tag-name-but-got-right-bracket'})
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<>'})
                        self.state = self.dataState
                    else:
                        if data == '?':
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-tag-name-but-got-question-mark'})
                            self.stream.unget(data)
                            self.state = self.bogusCommentState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-tag-name'})
                            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                            self.stream.unget(data)
                            self.state = self.dataState
        return True

    def closeTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':data,  'data':[],  'selfClosing':False}
            self.state = self.tagNameState
        else:
            if data == '>':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-closing-tag-but-got-right-bracket'})
                self.state = self.dataState
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-closing-tag-but-got-eof'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</'})
                    self.state = self.dataState
                else:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-closing-tag-but-got-char', 
                     'datavars':{'data': data}})
                    self.stream.unget(data)
                    self.state = self.bogusCommentState
        return True

    def tagNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeAttributeNameState
        else:
            if data == '>':
                self.emitCurrentToken()
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-tag-name'})
                    self.state = self.dataState
                else:
                    if data == '/':
                        self.state = self.selfClosingStartTagState
                    else:
                        if data == '\x00':
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                            self.currentToken['name'] += '�'
                        else:
                            self.currentToken['name'] += data
        return True

    def rcdataLessThanSignState(self):
        data = self.stream.char()
        if data == '/':
            self.temporaryBuffer = ''
            self.state = self.rcdataEndTagOpenState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
            self.stream.unget(data)
            self.state = self.rcdataState
        return True

    def rcdataEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer += data
            self.state = self.rcdataEndTagNameState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</'})
            self.stream.unget(data)
            self.state = self.rcdataState
        return True

    def rcdataEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken['name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters:
            if appropriate:
                self.currentToken = {'type':tokenTypes['EndTag'], 
                 'name':self.temporaryBuffer, 
                 'data':[],  'selfClosing':False}
                self.state = self.beforeAttributeNameState
        if data == '/' and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.state = self.selfClosingStartTagState
        elif data == '>' and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.emitCurrentToken()
            self.state = self.dataState
        else:
            if data in asciiLetters:
                self.temporaryBuffer += data
            else:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</' + self.temporaryBuffer})
                self.stream.unget(data)
                self.state = self.rcdataState
        return True

    def rawtextLessThanSignState(self):
        data = self.stream.char()
        if data == '/':
            self.temporaryBuffer = ''
            self.state = self.rawtextEndTagOpenState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
            self.stream.unget(data)
            self.state = self.rawtextState
        return True

    def rawtextEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer += data
            self.state = self.rawtextEndTagNameState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</'})
            self.stream.unget(data)
            self.state = self.rawtextState
        return True

    def rawtextEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken['name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters:
            if appropriate:
                self.currentToken = {'type':tokenTypes['EndTag'], 
                 'name':self.temporaryBuffer, 
                 'data':[],  'selfClosing':False}
                self.state = self.beforeAttributeNameState
        if data == '/' and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.state = self.selfClosingStartTagState
        elif data == '>' and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.emitCurrentToken()
            self.state = self.dataState
        else:
            if data in asciiLetters:
                self.temporaryBuffer += data
            else:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</' + self.temporaryBuffer})
                self.stream.unget(data)
                self.state = self.rawtextState
        return True

    def scriptDataLessThanSignState(self):
        data = self.stream.char()
        if data == '/':
            self.temporaryBuffer = ''
            self.state = self.scriptDataEndTagOpenState
        else:
            if data == '!':
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<!'})
                self.state = self.scriptDataEscapeStartState
            else:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                self.stream.unget(data)
                self.state = self.scriptDataState
        return True

    def scriptDataEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer += data
            self.state = self.scriptDataEndTagNameState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</'})
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken['name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters:
            if appropriate:
                self.currentToken = {'type':tokenTypes['EndTag'], 
                 'name':self.temporaryBuffer, 
                 'data':[],  'selfClosing':False}
                self.state = self.beforeAttributeNameState
        if data == '/' and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.state = self.selfClosingStartTagState
        elif data == '>' and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.emitCurrentToken()
            self.state = self.dataState
        else:
            if data in asciiLetters:
                self.temporaryBuffer += data
            else:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</' + self.temporaryBuffer})
                self.stream.unget(data)
                self.state = self.scriptDataState
        return True

    def scriptDataEscapeStartState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataEscapeStartDashState
        else:
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEscapeStartDashState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataEscapedDashDashState
        else:
            self.stream.unget(data)
            self.state = self.scriptDataState
        return True

    def scriptDataEscapedState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataEscapedDashState
        else:
            if data == '<':
                self.state = self.scriptDataEscapedLessThanSignState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                else:
                    if data == EOF:
                        self.state = self.dataState
                    else:
                        chars = self.stream.charsUntil(('<', '-', '\x00'))
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data + chars})
        return True

    def scriptDataEscapedDashState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataEscapedDashDashState
        else:
            if data == '<':
                self.state = self.scriptDataEscapedLessThanSignState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                    self.state = self.scriptDataEscapedState
                else:
                    if data == EOF:
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
                        self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedDashDashState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
        else:
            if data == '<':
                self.state = self.scriptDataEscapedLessThanSignState
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'>'})
                    self.state = self.scriptDataState
                else:
                    if data == '\x00':
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                        self.state = self.scriptDataEscapedState
                    else:
                        if data == EOF:
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
                            self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedLessThanSignState(self):
        data = self.stream.char()
        if data == '/':
            self.temporaryBuffer = ''
            self.state = self.scriptDataEscapedEndTagOpenState
        else:
            if data in asciiLetters:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<' + data})
                self.temporaryBuffer = data
                self.state = self.scriptDataDoubleEscapeStartState
            else:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                self.stream.unget(data)
                self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedEndTagOpenState(self):
        data = self.stream.char()
        if data in asciiLetters:
            self.temporaryBuffer = data
            self.state = self.scriptDataEscapedEndTagNameState
        else:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</'})
            self.stream.unget(data)
            self.state = self.scriptDataEscapedState
        return True

    def scriptDataEscapedEndTagNameState(self):
        appropriate = self.currentToken and self.currentToken['name'].lower() == self.temporaryBuffer.lower()
        data = self.stream.char()
        if data in spaceCharacters:
            if appropriate:
                self.currentToken = {'type':tokenTypes['EndTag'], 
                 'name':self.temporaryBuffer, 
                 'data':[],  'selfClosing':False}
                self.state = self.beforeAttributeNameState
        if data == '/' and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.state = self.selfClosingStartTagState
        elif data == '>' and appropriate:
            self.currentToken = {'type':tokenTypes['EndTag'], 
             'name':self.temporaryBuffer, 
             'data':[],  'selfClosing':False}
            self.emitCurrentToken()
            self.state = self.dataState
        else:
            if data in asciiLetters:
                self.temporaryBuffer += data
            else:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'</' + self.temporaryBuffer})
                self.stream.unget(data)
                self.state = self.scriptDataEscapedState
        return True

    def scriptDataDoubleEscapeStartState(self):
        data = self.stream.char()
        if data in spaceCharacters | frozenset(('/', '>')):
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
            if self.temporaryBuffer.lower() == 'script':
                self.state = self.scriptDataDoubleEscapedState
            else:
                self.state = self.scriptDataEscapedState
        else:
            if data in asciiLetters:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
                self.temporaryBuffer += data
            else:
                self.stream.unget(data)
                self.state = self.scriptDataEscapedState
        return True

    def scriptDataDoubleEscapedState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataDoubleEscapedDashState
        else:
            if data == '<':
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                self.state = self.scriptDataDoubleEscapedLessThanSignState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                else:
                    if data == EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-script-in-script'})
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
        return True

    def scriptDataDoubleEscapedDashState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
            self.state = self.scriptDataDoubleEscapedDashDashState
        else:
            if data == '<':
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                self.state = self.scriptDataDoubleEscapedLessThanSignState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                    self.state = self.scriptDataDoubleEscapedState
                else:
                    if data == EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-script-in-script'})
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
                        self.state = self.scriptDataDoubleEscapedState
        return True

    def scriptDataDoubleEscapedDashDashState(self):
        data = self.stream.char()
        if data == '-':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'-'})
        else:
            if data == '<':
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'<'})
                self.state = self.scriptDataDoubleEscapedLessThanSignState
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'>'})
                    self.state = self.scriptDataState
                else:
                    if data == '\x00':
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                        self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'�'})
                        self.state = self.scriptDataDoubleEscapedState
                    else:
                        if data == EOF:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-script-in-script'})
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
                            self.state = self.scriptDataDoubleEscapedState
        return True

    def scriptDataDoubleEscapedLessThanSignState(self):
        data = self.stream.char()
        if data == '/':
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':'/'})
            self.temporaryBuffer = ''
            self.state = self.scriptDataDoubleEscapeEndState
        else:
            self.stream.unget(data)
            self.state = self.scriptDataDoubleEscapedState
        return True

    def scriptDataDoubleEscapeEndState(self):
        data = self.stream.char()
        if data in spaceCharacters | frozenset(('/', '>')):
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
            if self.temporaryBuffer.lower() == 'script':
                self.state = self.scriptDataEscapedState
            else:
                self.state = self.scriptDataDoubleEscapedState
        else:
            if data in asciiLetters:
                self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
                self.temporaryBuffer += data
            else:
                self.stream.unget(data)
                self.state = self.scriptDataDoubleEscapedState
        return True

    def beforeAttributeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.stream.charsUntil(spaceCharacters, True)
        else:
            if data in asciiLetters:
                self.currentToken['data'].append([data, ''])
                self.state = self.attributeNameState
            else:
                if data == '>':
                    self.emitCurrentToken()
                else:
                    if data == '/':
                        self.state = self.selfClosingStartTagState
                    else:
                        if data in ("'", '"', '=', '<'):
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-character-in-attribute-name'})
                            self.currentToken['data'].append([data, ''])
                            self.state = self.attributeNameState
                        else:
                            if data == '\x00':
                                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                                self.currentToken['data'].append(['�', ''])
                                self.state = self.attributeNameState
                            else:
                                if data is EOF:
                                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-attribute-name-but-got-eof'})
                                    self.state = self.dataState
                                else:
                                    self.currentToken['data'].append([data, ''])
                                    self.state = self.attributeNameState
        return True

    def attributeNameState(self):
        data = self.stream.char()
        leavingThisState = True
        emitToken = False
        if data == '=':
            self.state = self.beforeAttributeValueState
        else:
            if data in asciiLetters:
                self.currentToken['data'][(-1)][0] += data + self.stream.charsUntil(asciiLetters, True)
                leavingThisState = False
            else:
                if data == '>':
                    emitToken = True
                else:
                    if data in spaceCharacters:
                        self.state = self.afterAttributeNameState
                    else:
                        if data == '/':
                            self.state = self.selfClosingStartTagState
                        else:
                            if data == '\x00':
                                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                                self.currentToken['data'][(-1)][0] += '�'
                                leavingThisState = False
                            else:
                                if data in ("'", '"', '<'):
                                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-character-in-attribute-name'})
                                    self.currentToken['data'][(-1)][0] += data
                                    leavingThisState = False
                                else:
                                    if data is EOF:
                                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-attribute-name'})
                                        self.state = self.dataState
                                    else:
                                        self.currentToken['data'][(-1)][0] += data
                                        leavingThisState = False
        if leavingThisState:
            self.currentToken['data'][(-1)][0] = self.currentToken['data'][(-1)][0].translate(asciiUpper2Lower)
            for name, _ in self.currentToken['data'][:-1]:
                if self.currentToken['data'][(-1)][0] == name:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'duplicate-attribute'})
                    break

            if emitToken:
                self.emitCurrentToken()
        return True

    def afterAttributeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.stream.charsUntil(spaceCharacters, True)
        else:
            if data == '=':
                self.state = self.beforeAttributeValueState
            else:
                if data == '>':
                    self.emitCurrentToken()
                else:
                    if data in asciiLetters:
                        self.currentToken['data'].append([data, ''])
                        self.state = self.attributeNameState
                    else:
                        if data == '/':
                            self.state = self.selfClosingStartTagState
                        else:
                            if data == '\x00':
                                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                                self.currentToken['data'].append(['�', ''])
                                self.state = self.attributeNameState
                            else:
                                if data in ("'", '"', '<'):
                                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-character-after-attribute-name'})
                                    self.currentToken['data'].append([data, ''])
                                    self.state = self.attributeNameState
                                else:
                                    if data is EOF:
                                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-end-of-tag-but-got-eof'})
                                        self.state = self.dataState
                                    else:
                                        self.currentToken['data'].append([data, ''])
                                        self.state = self.attributeNameState
        return True

    def beforeAttributeValueState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.stream.charsUntil(spaceCharacters, True)
        else:
            if data == '"':
                self.state = self.attributeValueDoubleQuotedState
            else:
                if data == '&':
                    self.state = self.attributeValueUnQuotedState
                    self.stream.unget(data)
                else:
                    if data == "'":
                        self.state = self.attributeValueSingleQuotedState
                    else:
                        if data == '>':
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-attribute-value-but-got-right-bracket'})
                            self.emitCurrentToken()
                        else:
                            if data == '\x00':
                                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                                self.currentToken['data'][(-1)][1] += '�'
                                self.state = self.attributeValueUnQuotedState
                            else:
                                if data in ('=', '<', '`'):
                                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'equals-in-unquoted-attribute-value'})
                                    self.currentToken['data'][(-1)][1] += data
                                    self.state = self.attributeValueUnQuotedState
                                else:
                                    if data is EOF:
                                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-attribute-value-but-got-eof'})
                                        self.state = self.dataState
                                    else:
                                        self.currentToken['data'][(-1)][1] += data
                                        self.state = self.attributeValueUnQuotedState
        return True

    def attributeValueDoubleQuotedState(self):
        data = self.stream.char()
        if data == '"':
            self.state = self.afterAttributeValueState
        else:
            if data == '&':
                self.processEntityInAttribute('"')
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.currentToken['data'][(-1)][1] += '�'
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-attribute-value-double-quote'})
                        self.state = self.dataState
                    else:
                        self.currentToken['data'][(-1)][1] += data + self.stream.charsUntil(('"',
                                                                                             '&',
                                                                                             '\x00'))
        return True

    def attributeValueSingleQuotedState(self):
        data = self.stream.char()
        if data == "'":
            self.state = self.afterAttributeValueState
        else:
            if data == '&':
                self.processEntityInAttribute("'")
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.currentToken['data'][(-1)][1] += '�'
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-attribute-value-single-quote'})
                        self.state = self.dataState
                    else:
                        self.currentToken['data'][(-1)][1] += data + self.stream.charsUntil(("'",
                                                                                             '&',
                                                                                             '\x00'))
        return True

    def attributeValueUnQuotedState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeAttributeNameState
        else:
            if data == '&':
                self.processEntityInAttribute('>')
            else:
                if data == '>':
                    self.emitCurrentToken()
                else:
                    if data in ('"', "'", '=', '<', '`'):
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-character-in-unquoted-attribute-value'})
                        self.currentToken['data'][(-1)][1] += data
                    else:
                        if data == '\x00':
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                            self.currentToken['data'][(-1)][1] += '�'
                        else:
                            if data is EOF:
                                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-attribute-value-no-quotes'})
                                self.state = self.dataState
                            else:
                                self.currentToken['data'][(-1)][1] += data + self.stream.charsUntil(frozenset(('&',
                                                                                                               '>',
                                                                                                               '"',
                                                                                                               "'",
                                                                                                               '=',
                                                                                                               '<',
                                                                                                               '`',
                                                                                                               '\x00')) | spaceCharacters)
        return True

    def afterAttributeValueState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeAttributeNameState
        else:
            if data == '>':
                self.emitCurrentToken()
            else:
                if data == '/':
                    self.state = self.selfClosingStartTagState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-EOF-after-attribute-value'})
                        self.stream.unget(data)
                        self.state = self.dataState
                    else:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-character-after-attribute-value'})
                        self.stream.unget(data)
                        self.state = self.beforeAttributeNameState
        return True

    def selfClosingStartTagState(self):
        data = self.stream.char()
        if data == '>':
            self.currentToken['selfClosing'] = True
            self.emitCurrentToken()
        else:
            if data is EOF:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-EOF-after-solidus-in-tag'})
                self.stream.unget(data)
                self.state = self.dataState
            else:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-character-after-solidus-in-tag'})
                self.stream.unget(data)
                self.state = self.beforeAttributeNameState
        return True

    def bogusCommentState(self):
        data = self.stream.charsUntil('>')
        data = data.replace('\x00', '�')
        self.tokenQueue.append({'type':tokenTypes['Comment'], 
         'data':data})
        self.stream.char()
        self.state = self.dataState
        return True

    def markupDeclarationOpenState(self):
        charStack = [
         self.stream.char()]
        if charStack[(-1)] == '-':
            charStack.append(self.stream.char())
            if charStack[(-1)] == '-':
                self.currentToken = {'type':tokenTypes['Comment'], 
                 'data':''}
                self.state = self.commentStartState
                return True
        elif charStack[(-1)] in ('d', 'D'):
            matched = True
            for expected in (('o', 'O'), ('c', 'C'), ('t', 'T'), ('y', 'Y'), ('p', 'P'),
                             ('e', 'E')):
                charStack.append(self.stream.char())
                if charStack[(-1)] not in expected:
                    matched = False
                    break

            if matched:
                self.currentToken = {'type':tokenTypes['Doctype'], 
                 'name':'', 
                 'publicId':None, 
                 'systemId':None,  'correct':True}
                self.state = self.doctypeState
                return True
        else:
            if charStack[(-1)] == '[':
                if self.parser is not None:
                    if self.parser.tree.openElements:
                        if self.parser.tree.openElements[(-1)].namespace != self.parser.tree.defaultNamespace:
                            matched = True
                            for expected in ('C', 'D', 'A', 'T', 'A', '['):
                                charStack.append(self.stream.char())
                                if charStack[(-1)] != expected:
                                    matched = False
                                    break

                            if matched:
                                self.state = self.cdataSectionState
                                return True
            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-dashes-or-doctype'})
            while charStack:
                self.stream.unget(charStack.pop())

            self.state = self.bogusCommentState
            return True

    def commentStartState(self):
        data = self.stream.char()
        if data == '-':
            self.state = self.commentStartDashState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['data'] += '�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'incorrect-comment'})
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment'})
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['data'] += data
                        self.state = self.commentState
        return True

    def commentStartDashState(self):
        data = self.stream.char()
        if data == '-':
            self.state = self.commentEndState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['data'] += '-�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'incorrect-comment'})
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment'})
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['data'] += '-' + data
                        self.state = self.commentState
        return True

    def commentState(self):
        data = self.stream.char()
        if data == '-':
            self.state = self.commentEndDashState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['data'] += '�'
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment'})
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    self.currentToken['data'] += data + self.stream.charsUntil(('-',
                                                                                '\x00'))
        return True

    def commentEndDashState(self):
        data = self.stream.char()
        if data == '-':
            self.state = self.commentEndState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['data'] += '-�'
                self.state = self.commentState
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment-end-dash'})
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    self.currentToken['data'] += '-' + data
                    self.state = self.commentState
        return True

    def commentEndState(self):
        data = self.stream.char()
        if data == '>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['data'] += '--�'
                self.state = self.commentState
            else:
                if data == '!':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-bang-after-double-dash-in-comment'})
                    self.state = self.commentEndBangState
                else:
                    if data == '-':
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-dash-after-double-dash-in-comment'})
                        self.currentToken['data'] += data
                    else:
                        if data is EOF:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment-double-dash'})
                            self.tokenQueue.append(self.currentToken)
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-comment'})
                            self.currentToken['data'] += '--' + data
                            self.state = self.commentState
        return True

    def commentEndBangState(self):
        data = self.stream.char()
        if data == '>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        else:
            if data == '-':
                self.currentToken['data'] += '--!'
                self.state = self.commentEndDashState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.currentToken['data'] += '--!�'
                    self.state = self.commentState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-comment-end-bang-state'})
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['data'] += '--!' + data
                        self.state = self.commentState
        return True

    def doctypeState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeDoctypeNameState
        else:
            if data is EOF:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-doctype-name-but-got-eof'})
                self.currentToken['correct'] = False
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'need-space-after-doctype'})
                self.stream.unget(data)
                self.state = self.beforeDoctypeNameState
        return True

    def beforeDoctypeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        else:
            if data == '>':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-doctype-name-but-got-right-bracket'})
                self.currentToken['correct'] = False
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.currentToken['name'] = '�'
                    self.state = self.doctypeNameState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-doctype-name-but-got-eof'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['name'] = data
                        self.state = self.doctypeNameState
            return True

    def doctypeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.currentToken['name'] = self.currentToken['name'].translate(asciiUpper2Lower)
            self.state = self.afterDoctypeNameState
        else:
            if data == '>':
                self.currentToken['name'] = self.currentToken['name'].translate(asciiUpper2Lower)
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                if data == '\x00':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                    self.currentToken['name'] += '�'
                    self.state = self.doctypeNameState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype-name'})
                        self.currentToken['correct'] = False
                        self.currentToken['name'] = self.currentToken['name'].translate(asciiUpper2Lower)
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['name'] += data
        return True

    def afterDoctypeNameState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        else:
            if data == '>':
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                if data is EOF:
                    self.currentToken['correct'] = False
                    self.stream.unget(data)
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data in ('p', 'P'):
                        matched = True
                        for expected in (('u', 'U'), ('b', 'B'), ('l', 'L'), ('i', 'I'),
                                         ('c', 'C')):
                            data = self.stream.char()
                            if data not in expected:
                                matched = False
                                break

                        if matched:
                            self.state = self.afterDoctypePublicKeywordState
                            return True
                    else:
                        if data in ('s', 'S'):
                            matched = True
                            for expected in (('y', 'Y'), ('s', 'S'), ('t', 'T'), ('e', 'E'),
                                             ('m', 'M')):
                                data = self.stream.char()
                                if data not in expected:
                                    matched = False
                                    break

                            if matched:
                                self.state = self.afterDoctypeSystemKeywordState
                                return True
                        self.stream.unget(data)
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'expected-space-or-right-bracket-in-doctype', 
                         'datavars':{'data': data}})
                        self.currentToken['correct'] = False
                        self.state = self.bogusDoctypeState
            return True

    def afterDoctypePublicKeywordState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeDoctypePublicIdentifierState
        else:
            if data in ("'", '"'):
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                self.stream.unget(data)
                self.state = self.beforeDoctypePublicIdentifierState
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    self.stream.unget(data)
                    self.state = self.beforeDoctypePublicIdentifierState
        return True

    def beforeDoctypePublicIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        else:
            if data == '"':
                self.currentToken['publicId'] = ''
                self.state = self.doctypePublicIdentifierDoubleQuotedState
            else:
                if data == "'":
                    self.currentToken['publicId'] = ''
                    self.state = self.doctypePublicIdentifierSingleQuotedState
                else:
                    if data == '>':
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-end-of-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        if data is EOF:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                            self.currentToken['correct'] = False
                            self.tokenQueue.append(self.currentToken)
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                            self.currentToken['correct'] = False
                            self.state = self.bogusDoctypeState
            return True

    def doctypePublicIdentifierDoubleQuotedState(self):
        data = self.stream.char()
        if data == '"':
            self.state = self.afterDoctypePublicIdentifierState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['publicId'] += '�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-end-of-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['publicId'] += data
        return True

    def doctypePublicIdentifierSingleQuotedState(self):
        data = self.stream.char()
        if data == "'":
            self.state = self.afterDoctypePublicIdentifierState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['publicId'] += '�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-end-of-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['publicId'] += data
        return True

    def afterDoctypePublicIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.betweenDoctypePublicAndSystemIdentifiersState
        else:
            if data == '>':
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                if data == '"':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                    self.currentToken['systemId'] = ''
                    self.state = self.doctypeSystemIdentifierDoubleQuotedState
                else:
                    if data == "'":
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                        self.currentToken['systemId'] = ''
                        self.state = self.doctypeSystemIdentifierSingleQuotedState
                    else:
                        if data is EOF:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                            self.currentToken['correct'] = False
                            self.tokenQueue.append(self.currentToken)
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                            self.currentToken['correct'] = False
                            self.state = self.bogusDoctypeState
        return True

    def betweenDoctypePublicAndSystemIdentifiersState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        else:
            if data == '>':
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                if data == '"':
                    self.currentToken['systemId'] = ''
                    self.state = self.doctypeSystemIdentifierDoubleQuotedState
                else:
                    if data == "'":
                        self.currentToken['systemId'] = ''
                        self.state = self.doctypeSystemIdentifierSingleQuotedState
                    else:
                        if data == EOF:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                            self.currentToken['correct'] = False
                            self.tokenQueue.append(self.currentToken)
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                            self.currentToken['correct'] = False
                            self.state = self.bogusDoctypeState
            return True

    def afterDoctypeSystemKeywordState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            self.state = self.beforeDoctypeSystemIdentifierState
        else:
            if data in ("'", '"'):
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                self.stream.unget(data)
                self.state = self.beforeDoctypeSystemIdentifierState
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    self.stream.unget(data)
                    self.state = self.beforeDoctypeSystemIdentifierState
        return True

    def beforeDoctypeSystemIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        else:
            if data == '"':
                self.currentToken['systemId'] = ''
                self.state = self.doctypeSystemIdentifierDoubleQuotedState
            else:
                if data == "'":
                    self.currentToken['systemId'] = ''
                    self.state = self.doctypeSystemIdentifierSingleQuotedState
                else:
                    if data == '>':
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        if data is EOF:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                            self.currentToken['correct'] = False
                            self.tokenQueue.append(self.currentToken)
                            self.state = self.dataState
                        else:
                            self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                            self.currentToken['correct'] = False
                            self.state = self.bogusDoctypeState
            return True

    def doctypeSystemIdentifierDoubleQuotedState(self):
        data = self.stream.char()
        if data == '"':
            self.state = self.afterDoctypeSystemIdentifierState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['systemId'] += '�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-end-of-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['systemId'] += data
        return True

    def doctypeSystemIdentifierSingleQuotedState(self):
        data = self.stream.char()
        if data == "'":
            self.state = self.afterDoctypeSystemIdentifierState
        else:
            if data == '\x00':
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})
                self.currentToken['systemId'] += '�'
            else:
                if data == '>':
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-end-of-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    if data is EOF:
                        self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                        self.currentToken['correct'] = False
                        self.tokenQueue.append(self.currentToken)
                        self.state = self.dataState
                    else:
                        self.currentToken['systemId'] += data
        return True

    def afterDoctypeSystemIdentifierState(self):
        data = self.stream.char()
        if data in spaceCharacters:
            pass
        else:
            if data == '>':
                self.tokenQueue.append(self.currentToken)
                self.state = self.dataState
            else:
                if data is EOF:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'eof-in-doctype'})
                    self.currentToken['correct'] = False
                    self.tokenQueue.append(self.currentToken)
                    self.state = self.dataState
                else:
                    self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'unexpected-char-in-doctype'})
                    self.state = self.bogusDoctypeState
            return True

    def bogusDoctypeState(self):
        data = self.stream.char()
        if data == '>':
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        elif data is EOF:
            self.stream.unget(data)
            self.tokenQueue.append(self.currentToken)
            self.state = self.dataState
        return True

    def cdataSectionState(self):
        data = []
        while True:
            data.append(self.stream.charsUntil(']'))
            data.append(self.stream.charsUntil('>'))
            char = self.stream.char()
            if char == EOF:
                break
            else:
                assert char == '>'
                if data[(-1)][-2:] == ']]':
                    data[-1] = data[(-1)][:-2]
                    break
                else:
                    data.append(char)

        data = ''.join(data)
        nullCount = data.count('\x00')
        if nullCount > 0:
            for _ in range(nullCount):
                self.tokenQueue.append({'type':tokenTypes['ParseError'],  'data':'invalid-codepoint'})

            data = data.replace('\x00', '�')
        if data:
            self.tokenQueue.append({'type':tokenTypes['Characters'],  'data':data})
        self.state = self.dataState
        return True