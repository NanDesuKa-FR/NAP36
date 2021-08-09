# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\html5parser.py
from __future__ import absolute_import, division, unicode_literals
from six import with_metaclass, viewkeys
import types
from collections import OrderedDict
from . import _inputstream
from . import _tokenizer
from . import treebuilders
from .treebuilders.base import Marker
from . import _utils
from .constants import spaceCharacters, asciiUpper2Lower, specialElements, headingElements, cdataElements, rcdataElements, tokenTypes, tagTokenTypes, namespaces, htmlIntegrationPointElements, mathmlTextIntegrationPointElements, adjustForeignAttributes as adjustForeignAttributesMap, adjustMathMLAttributes, adjustSVGAttributes, E, _ReparseException

def parse(doc, treebuilder='etree', namespaceHTMLElements=True, **kwargs):
    """Parse an HTML document as a string or file-like object into a tree

    :arg doc: the document to parse as a string or file-like object

    :arg treebuilder: the treebuilder to use when parsing

    :arg namespaceHTMLElements: whether or not to namespace HTML elements

    :returns: parsed tree

    Example:

    >>> from html5lib.html5parser import parse
    >>> parse('<html><body><p>This is a doc</p></body></html>')
    <Element u'{http://www.w3.org/1999/xhtml}html' at 0x7feac4909db0>

    """
    tb = treebuilders.getTreeBuilder(treebuilder)
    p = HTMLParser(tb, namespaceHTMLElements=namespaceHTMLElements)
    return (p.parse)(doc, **kwargs)


def parseFragment(doc, container='div', treebuilder='etree', namespaceHTMLElements=True, **kwargs):
    """Parse an HTML fragment as a string or file-like object into a tree

    :arg doc: the fragment to parse as a string or file-like object

    :arg container: the container context to parse the fragment in

    :arg treebuilder: the treebuilder to use when parsing

    :arg namespaceHTMLElements: whether or not to namespace HTML elements

    :returns: parsed tree

    Example:

    >>> from html5lib.html5libparser import parseFragment
    >>> parseFragment('<b>this is a fragment</b>')
    <Element u'DOCUMENT_FRAGMENT' at 0x7feac484b090>

    """
    tb = treebuilders.getTreeBuilder(treebuilder)
    p = HTMLParser(tb, namespaceHTMLElements=namespaceHTMLElements)
    return (p.parseFragment)(doc, container=container, **kwargs)


def method_decorator_metaclass(function):

    class Decorated(type):

        def __new__(meta, classname, bases, classDict):
            for attributeName, attribute in classDict.items():
                if isinstance(attribute, types.FunctionType):
                    attribute = function(attribute)
                classDict[attributeName] = attribute

            return type.__new__(meta, classname, bases, classDict)

    return Decorated


class HTMLParser(object):
    __doc__ = 'HTML parser\n\n    Generates a tree structure from a stream of (possibly malformed) HTML.\n\n    '

    def __init__(self, tree=None, strict=False, namespaceHTMLElements=True, debug=False):
        """
        :arg tree: a treebuilder class controlling the type of tree that will be
            returned. Built in treebuilders can be accessed through
            html5lib.treebuilders.getTreeBuilder(treeType)

        :arg strict: raise an exception when a parse error is encountered

        :arg namespaceHTMLElements: whether or not to namespace HTML elements

        :arg debug: whether or not to enable debug mode which logs things

        Example:

        >>> from html5lib.html5parser import HTMLParser
        >>> parser = HTMLParser()                     # generates parser with etree builder
        >>> parser = HTMLParser('lxml', strict=True)  # generates parser with lxml builder which is strict

        """
        self.strict = strict
        if tree is None:
            tree = treebuilders.getTreeBuilder('etree')
        self.tree = tree(namespaceHTMLElements)
        self.errors = []
        self.phases = dict([(name, cls(self, self.tree)) for name, cls in getPhases(debug).items()])

    def _parse(self, stream, innerHTML=False, container='div', scripting=False, **kwargs):
        self.innerHTMLMode = innerHTML
        self.container = container
        self.scripting = scripting
        self.tokenizer = (_tokenizer.HTMLTokenizer)(stream, parser=self, **kwargs)
        self.reset()
        try:
            self.mainLoop()
        except _ReparseException:
            self.reset()
            self.mainLoop()

    def reset(self):
        self.tree.reset()
        self.firstStartTag = False
        self.errors = []
        self.log = []
        self.compatMode = 'no quirks'
        if self.innerHTMLMode:
            self.innerHTML = self.container.lower()
            if self.innerHTML in cdataElements:
                self.tokenizer.state = self.tokenizer.rcdataState
            else:
                if self.innerHTML in rcdataElements:
                    self.tokenizer.state = self.tokenizer.rawtextState
                else:
                    if self.innerHTML == 'plaintext':
                        self.tokenizer.state = self.tokenizer.plaintextState
            self.phase = self.phases['beforeHtml']
            self.phase.insertHtmlElement()
            self.resetInsertionMode()
        else:
            self.innerHTML = False
            self.phase = self.phases['initial']
        self.lastPhase = None
        self.beforeRCDataPhase = None
        self.framesetOK = True

    @property
    def documentEncoding(self):
        """Name of the character encoding that was used to decode the input stream, or
        :obj:`None` if that is not determined yet

        """
        if not hasattr(self, 'tokenizer'):
            return
        else:
            return self.tokenizer.stream.charEncoding[0].name

    def isHTMLIntegrationPoint(self, element):
        if element.name == 'annotation-xml':
            if element.namespace == namespaces['mathml']:
                return 'encoding' in element.attributes and element.attributes['encoding'].translate(asciiUpper2Lower) in ('text/html',
                                                                                                                           'application/xhtml+xml')
        return (
         element.namespace, element.name) in htmlIntegrationPointElements

    def isMathMLTextIntegrationPoint(self, element):
        return (
         element.namespace, element.name) in mathmlTextIntegrationPointElements

    def mainLoop--- This code section failed: ---

 L. 197         0  LOAD_GLOBAL              tokenTypes
                2  LOAD_STR                 'Characters'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'CharactersToken'

 L. 198         8  LOAD_GLOBAL              tokenTypes
               10  LOAD_STR                 'SpaceCharacters'
               12  BINARY_SUBSCR    
               14  STORE_FAST               'SpaceCharactersToken'

 L. 199        16  LOAD_GLOBAL              tokenTypes
               18  LOAD_STR                 'StartTag'
               20  BINARY_SUBSCR    
               22  STORE_FAST               'StartTagToken'

 L. 200        24  LOAD_GLOBAL              tokenTypes
               26  LOAD_STR                 'EndTag'
               28  BINARY_SUBSCR    
               30  STORE_FAST               'EndTagToken'

 L. 201        32  LOAD_GLOBAL              tokenTypes
               34  LOAD_STR                 'Comment'
               36  BINARY_SUBSCR    
               38  STORE_FAST               'CommentToken'

 L. 202        40  LOAD_GLOBAL              tokenTypes
               42  LOAD_STR                 'Doctype'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'DoctypeToken'

 L. 203        48  LOAD_GLOBAL              tokenTypes
               50  LOAD_STR                 'ParseError'
               52  BINARY_SUBSCR    
               54  STORE_FAST               'ParseErrorToken'

 L. 205        56  SETUP_LOOP          564  'to 564'
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                normalizedTokens
               64  CALL_FUNCTION_0       0  '0 positional arguments'
               66  GET_ITER         
               68  FOR_ITER            562  'to 562'
               72  STORE_FAST               'token'

 L. 206        74  LOAD_CONST               None
               76  STORE_FAST               'prev_token'

 L. 207        78  LOAD_FAST                'token'
               80  STORE_FAST               'new_token'

 L. 208        82  SETUP_LOOP          514  'to 514'
               86  LOAD_FAST                'new_token'
               88  LOAD_CONST               None
               90  COMPARE_OP               is-not
               92  POP_JUMP_IF_FALSE   512  'to 512'

 L. 209        96  LOAD_FAST                'new_token'
               98  STORE_FAST               'prev_token'

 L. 210       100  LOAD_FAST                'self'
              102  LOAD_ATTR                tree
              104  LOAD_ATTR                openElements
              106  POP_JUMP_IF_FALSE   120  'to 120'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                tree
              112  LOAD_ATTR                openElements
              114  LOAD_CONST               -1
              116  BINARY_SUBSCR    
              118  JUMP_FORWARD        122  'to 122'
              120  ELSE                     '122'
              120  LOAD_CONST               None
            122_0  COME_FROM           118  '118'
              122  STORE_FAST               'currentNode'

 L. 211       124  LOAD_FAST                'currentNode'
              126  POP_JUMP_IF_FALSE   134  'to 134'
              128  LOAD_FAST                'currentNode'
              130  LOAD_ATTR                namespace
              132  JUMP_FORWARD        136  'to 136'
              134  ELSE                     '136'
              134  LOAD_CONST               None
            136_0  COME_FROM           132  '132'
              136  STORE_FAST               'currentNodeNamespace'

 L. 212       138  LOAD_FAST                'currentNode'
              140  POP_JUMP_IF_FALSE   148  'to 148'
              142  LOAD_FAST                'currentNode'
              144  LOAD_ATTR                name
              146  JUMP_FORWARD        150  'to 150'
              148  ELSE                     '150'
              148  LOAD_CONST               None
            150_0  COME_FROM           146  '146'
              150  STORE_FAST               'currentNodeName'

 L. 214       152  LOAD_FAST                'new_token'
              154  LOAD_STR                 'type'
              156  BINARY_SUBSCR    
              158  STORE_FAST               'type'

 L. 216       160  LOAD_FAST                'type'
              162  LOAD_FAST                'ParseErrorToken'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   198  'to 198'

 L. 217       168  LOAD_FAST                'self'
              170  LOAD_ATTR                parseError
              172  LOAD_FAST                'new_token'
              174  LOAD_STR                 'data'
              176  BINARY_SUBSCR    
              178  LOAD_FAST                'new_token'
              180  LOAD_ATTR                get
              182  LOAD_STR                 'datavars'
              184  BUILD_MAP_0           0 
              186  CALL_FUNCTION_2       2  '2 positional arguments'
              188  CALL_FUNCTION_2       2  '2 positional arguments'
              190  POP_TOP          

 L. 218       192  LOAD_CONST               None
              194  STORE_FAST               'new_token'
              196  JUMP_BACK            86  'to 86'
              198  ELSE                     '510'

 L. 220       198  LOAD_GLOBAL              len
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                tree
              204  LOAD_ATTR                openElements
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  LOAD_CONST               0
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_TRUE    364  'to 364'

 L. 221       216  LOAD_FAST                'currentNodeNamespace'
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                tree
              222  LOAD_ATTR                defaultNamespace
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_TRUE    364  'to 364'

 L. 222       230  LOAD_FAST                'self'
              232  LOAD_ATTR                isMathMLTextIntegrationPoint
              234  LOAD_FAST                'currentNode'
              236  CALL_FUNCTION_1       1  '1 positional argument'
              238  POP_JUMP_IF_FALSE   288  'to 288'

 L. 223       242  LOAD_FAST                'type'
              244  LOAD_FAST                'StartTagToken'
              246  COMPARE_OP               ==
              248  POP_JUMP_IF_FALSE   274  'to 274'

 L. 224       252  LOAD_FAST                'token'
              254  LOAD_STR                 'name'
              256  BINARY_SUBSCR    
              258  LOAD_GLOBAL              frozenset
              260  LOAD_STR                 'mglyph'
              262  LOAD_STR                 'malignmark'
              264  BUILD_LIST_2          2 
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  COMPARE_OP               not-in
            270_0  COME_FROM           248  '248'
              270  POP_JUMP_IF_TRUE    364  'to 364'

 L. 225       274  LOAD_FAST                'type'
              276  LOAD_FAST                'CharactersToken'
              278  LOAD_FAST                'SpaceCharactersToken'
              280  BUILD_TUPLE_2         2 
              282  COMPARE_OP               in
            284_0  COME_FROM           270  '270'
            284_1  COME_FROM           238  '238'
              284  POP_JUMP_IF_TRUE    364  'to 364'

 L. 226       288  LOAD_FAST                'currentNodeNamespace'
              290  LOAD_GLOBAL              namespaces
              292  LOAD_STR                 'mathml'
              294  BINARY_SUBSCR    
              296  COMPARE_OP               ==
              298  POP_JUMP_IF_FALSE   336  'to 336'

 L. 227       302  LOAD_FAST                'currentNodeName'
              304  LOAD_STR                 'annotation-xml'
              306  COMPARE_OP               ==
              308  POP_JUMP_IF_FALSE   336  'to 336'

 L. 228       312  LOAD_FAST                'type'
              314  LOAD_FAST                'StartTagToken'
              316  COMPARE_OP               ==
              318  POP_JUMP_IF_FALSE   336  'to 336'

 L. 229       322  LOAD_FAST                'token'
              324  LOAD_STR                 'name'
              326  BINARY_SUBSCR    
              328  LOAD_STR                 'svg'
              330  COMPARE_OP               ==
            332_0  COME_FROM           318  '318'
            332_1  COME_FROM           308  '308'
            332_2  COME_FROM           298  '298'
              332  POP_JUMP_IF_TRUE    364  'to 364'

 L. 230       336  LOAD_FAST                'self'
              338  LOAD_ATTR                isHTMLIntegrationPoint
              340  LOAD_FAST                'currentNode'
              342  CALL_FUNCTION_1       1  '1 positional argument'
              344  POP_JUMP_IF_FALSE   372  'to 372'

 L. 231       348  LOAD_FAST                'type'
              350  LOAD_FAST                'StartTagToken'
              352  LOAD_FAST                'CharactersToken'
              354  LOAD_FAST                'SpaceCharactersToken'
              356  BUILD_TUPLE_3         3 
              358  COMPARE_OP               in
            360_0  COME_FROM           344  '344'
            360_1  COME_FROM           332  '332'
            360_2  COME_FROM           284  '284'
            360_3  COME_FROM           226  '226'
            360_4  COME_FROM           212  '212'
              360  POP_JUMP_IF_FALSE   372  'to 372'

 L. 232       364  LOAD_FAST                'self'
              366  LOAD_ATTR                phase
              368  STORE_FAST               'phase'
              370  JUMP_FORWARD        382  'to 382'
              372  ELSE                     '382'

 L. 234       372  LOAD_FAST                'self'
              374  LOAD_ATTR                phases
              376  LOAD_STR                 'inForeignContent'
              378  BINARY_SUBSCR    
              380  STORE_FAST               'phase'
            382_0  COME_FROM           370  '370'

 L. 236       382  LOAD_FAST                'type'
              384  LOAD_FAST                'CharactersToken'
              386  COMPARE_OP               ==
              388  POP_JUMP_IF_FALSE   404  'to 404'

 L. 237       392  LOAD_FAST                'phase'
              394  LOAD_ATTR                processCharacters
              396  LOAD_FAST                'new_token'
              398  CALL_FUNCTION_1       1  '1 positional argument'
              400  STORE_FAST               'new_token'
              402  JUMP_BACK            86  'to 86'
              404  ELSE                     '510'

 L. 238       404  LOAD_FAST                'type'
              406  LOAD_FAST                'SpaceCharactersToken'
              408  COMPARE_OP               ==
              410  POP_JUMP_IF_FALSE   426  'to 426'

 L. 239       414  LOAD_FAST                'phase'
              416  LOAD_ATTR                processSpaceCharacters
              418  LOAD_FAST                'new_token'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  STORE_FAST               'new_token'
              424  JUMP_BACK            86  'to 86'
              426  ELSE                     '510'

 L. 240       426  LOAD_FAST                'type'
              428  LOAD_FAST                'StartTagToken'
              430  COMPARE_OP               ==
              432  POP_JUMP_IF_FALSE   448  'to 448'

 L. 241       436  LOAD_FAST                'phase'
              438  LOAD_ATTR                processStartTag
              440  LOAD_FAST                'new_token'
              442  CALL_FUNCTION_1       1  '1 positional argument'
              444  STORE_FAST               'new_token'
              446  JUMP_BACK            86  'to 86'
              448  ELSE                     '510'

 L. 242       448  LOAD_FAST                'type'
              450  LOAD_FAST                'EndTagToken'
              452  COMPARE_OP               ==
              454  POP_JUMP_IF_FALSE   470  'to 470'

 L. 243       458  LOAD_FAST                'phase'
              460  LOAD_ATTR                processEndTag
              462  LOAD_FAST                'new_token'
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  STORE_FAST               'new_token'
              468  JUMP_BACK            86  'to 86'
              470  ELSE                     '510'

 L. 244       470  LOAD_FAST                'type'
              472  LOAD_FAST                'CommentToken'
              474  COMPARE_OP               ==
              476  POP_JUMP_IF_FALSE   492  'to 492'

 L. 245       480  LOAD_FAST                'phase'
              482  LOAD_ATTR                processComment
              484  LOAD_FAST                'new_token'
              486  CALL_FUNCTION_1       1  '1 positional argument'
              488  STORE_FAST               'new_token'
              490  JUMP_BACK            86  'to 86'
              492  ELSE                     '510'

 L. 246       492  LOAD_FAST                'type'
              494  LOAD_FAST                'DoctypeToken'
              496  COMPARE_OP               ==
              498  POP_JUMP_IF_FALSE    86  'to 86'

 L. 247       500  LOAD_FAST                'phase'
              502  LOAD_ATTR                processDoctype
              504  LOAD_FAST                'new_token'
              506  CALL_FUNCTION_1       1  '1 positional argument'
              508  STORE_FAST               'new_token'
              510  JUMP_BACK            86  'to 86'
            512_0  COME_FROM            92  '92'
              512  POP_BLOCK        
            514_0  COME_FROM_LOOP       82  '82'

 L. 249       514  LOAD_FAST                'type'
              516  LOAD_FAST                'StartTagToken'
              518  COMPARE_OP               ==
              520  POP_JUMP_IF_FALSE    68  'to 68'
              522  LOAD_FAST                'prev_token'
              524  LOAD_STR                 'selfClosing'
              526  BINARY_SUBSCR    
              528  POP_JUMP_IF_FALSE    68  'to 68'

 L. 250       530  LOAD_FAST                'prev_token'
              532  LOAD_STR                 'selfClosingAcknowledged'
              534  BINARY_SUBSCR    
              536  UNARY_NOT        
              538  POP_JUMP_IF_FALSE    68  'to 68'

 L. 251       540  LOAD_FAST                'self'
              542  LOAD_ATTR                parseError
              544  LOAD_STR                 'non-void-element-with-trailing-solidus'

 L. 252       546  LOAD_STR                 'name'
              548  LOAD_FAST                'prev_token'
              550  LOAD_STR                 'name'
              552  BINARY_SUBSCR    
              554  BUILD_MAP_1           1 
              556  CALL_FUNCTION_2       2  '2 positional arguments'
              558  POP_TOP          
              560  JUMP_BACK            68  'to 68'
              562  POP_BLOCK        
            564_0  COME_FROM_LOOP       56  '56'

 L. 255       564  LOAD_CONST               True
              566  STORE_FAST               'reprocess'

 L. 256       568  BUILD_LIST_0          0 
              570  STORE_FAST               'phases'

 L. 257       572  SETUP_LOOP          630  'to 630'
              574  LOAD_FAST                'reprocess'
              576  POP_JUMP_IF_FALSE   628  'to 628'

 L. 258       580  LOAD_FAST                'phases'
              582  LOAD_ATTR                append
              584  LOAD_FAST                'self'
              586  LOAD_ATTR                phase
              588  CALL_FUNCTION_1       1  '1 positional argument'
              590  POP_TOP          

 L. 259       592  LOAD_FAST                'self'
              594  LOAD_ATTR                phase
              596  LOAD_ATTR                processEOF
              598  CALL_FUNCTION_0       0  '0 positional arguments'
              600  STORE_FAST               'reprocess'

 L. 260       602  LOAD_FAST                'reprocess'
              604  POP_JUMP_IF_FALSE   574  'to 574'

 L. 261       608  LOAD_FAST                'self'
              610  LOAD_ATTR                phase
              612  LOAD_FAST                'phases'
              614  COMPARE_OP               not-in
              616  POP_JUMP_IF_TRUE    574  'to 574'
              620  LOAD_GLOBAL              AssertionError
              622  RAISE_VARARGS_1       1  'exception'
              624  JUMP_BACK           574  'to 574'
            628_0  COME_FROM           576  '576'
              628  POP_BLOCK        
            630_0  COME_FROM_LOOP      572  '572'

Parse error at or near `POP_BLOCK' instruction at offset 628

    def normalizedTokens(self):
        for token in self.tokenizer:
            yield self.normalizeToken(token)

    def parse(self, stream, *args, **kwargs):
        """Parse a HTML document into a well-formed tree

        :arg stream: a file-like object or string containing the HTML to be parsed

            The optional encoding parameter must be a string that indicates
            the encoding.  If specified, that encoding will be used,
            regardless of any BOM or later declaration (such as in a meta
            element).

        :arg scripting: treat noscript elements as if JavaScript was turned on

        :returns: parsed tree

        Example:

        >>> from html5lib.html5parser import HTMLParser
        >>> parser = HTMLParser()
        >>> parser.parse('<html><body><p>This is a doc</p></body></html>')
        <Element u'{http://www.w3.org/1999/xhtml}html' at 0x7feac4909db0>

        """
        (self._parse)(stream, False, None, *args, **kwargs)
        return self.tree.getDocument()

    def parseFragment(self, stream, *args, **kwargs):
        """Parse a HTML fragment into a well-formed tree fragment

        :arg container: name of the element we're setting the innerHTML
            property if set to None, default to 'div'

        :arg stream: a file-like object or string containing the HTML to be parsed

            The optional encoding parameter must be a string that indicates
            the encoding.  If specified, that encoding will be used,
            regardless of any BOM or later declaration (such as in a meta
            element)

        :arg scripting: treat noscript elements as if JavaScript was turned on

        :returns: parsed tree

        Example:

        >>> from html5lib.html5libparser import HTMLParser
        >>> parser = HTMLParser()
        >>> parser.parseFragment('<b>this is a fragment</b>')
        <Element u'DOCUMENT_FRAGMENT' at 0x7feac484b090>

        """
        (self._parse)(stream, True, *args, **kwargs)
        return self.tree.getFragment()

    def parseError(self, errorcode='XXX-undefined-error', datavars=None):
        if datavars is None:
            datavars = {}
        self.errors.append((self.tokenizer.stream.position(), errorcode, datavars))
        if self.strict:
            raise ParseError(E[errorcode] % datavars)

    def normalizeToken(self, token):
        if token['type'] == tokenTypes['StartTag']:
            raw = token['data']
            token['data'] = OrderedDict(raw)
            if len(raw) > len(token['data']):
                token['data'].update(raw[::-1])
        return token

    def adjustMathMLAttributes(self, token):
        adjust_attributes(token, adjustMathMLAttributes)

    def adjustSVGAttributes(self, token):
        adjust_attributes(token, adjustSVGAttributes)

    def adjustForeignAttributes(self, token):
        adjust_attributes(token, adjustForeignAttributesMap)

    def reparseTokenNormal(self, token):
        self.parser.phase()

    def resetInsertionMode(self):
        last = False
        newModes = {'select':'inSelect', 
         'td':'inCell', 
         'th':'inCell', 
         'tr':'inRow', 
         'tbody':'inTableBody', 
         'thead':'inTableBody', 
         'tfoot':'inTableBody', 
         'caption':'inCaption', 
         'colgroup':'inColumnGroup', 
         'table':'inTable', 
         'head':'inBody', 
         'body':'inBody', 
         'frameset':'inFrameset', 
         'html':'beforeHead'}
        for node in self.tree.openElements[::-1]:
            nodeName = node.name
            new_phase = None
            if node == self.tree.openElements[0]:
                assert self.innerHTML
                last = True
                nodeName = self.innerHTML
            if nodeName in ('select', 'colgroup', 'head', 'html'):
                assert self.innerHTML
                if not last:
                    if node.namespace != self.tree.defaultNamespace:
                        continue
                if nodeName in newModes:
                    new_phase = self.phases[newModes[nodeName]]
                    break
                elif last:
                    new_phase = self.phases['inBody']
                    break

        self.phase = new_phase

    def parseRCDataRawtext(self, token, contentType):
        if not contentType in ('RAWTEXT', 'RCDATA'):
            raise AssertionError
        else:
            self.tree.insertElement(token)
            if contentType == 'RAWTEXT':
                self.tokenizer.state = self.tokenizer.rawtextState
            else:
                self.tokenizer.state = self.tokenizer.rcdataState
        self.originalPhase = self.phase
        self.phase = self.phases['text']


@_utils.memoize
def getPhases(debug):

    def log(function):
        """Logger that records which phase processes each token"""
        type_names = dict((value, key) for key, value in tokenTypes.items())

        def wrapped(self, *args, **kwargs):
            if function.__name__.startswith('process') and len(args) > 0:
                token = args[0]
                try:
                    info = {'type': type_names[token['type']]}
                except:
                    raise

                if token['type'] in tagTokenTypes:
                    info['name'] = token['name']
                self.parser.log.append((self.parser.tokenizer.state.__name__,
                 self.parser.phase.__class__.__name__,
                 self.__class__.__name__,
                 function.__name__,
                 info))
                return function(self, *args, **kwargs)
            else:
                return function(self, *args, **kwargs)

        return wrapped

    def getMetaclass(use_metaclass, metaclass_func):
        if use_metaclass:
            return method_decorator_metaclass(metaclass_func)
        else:
            return type

    class Phase(with_metaclass(getMetaclass(debug, log))):
        __doc__ = 'Base class for helper object that implements each phase of processing\n        '

        def __init__(self, parser, tree):
            self.parser = parser
            self.tree = tree

        def processEOF(self):
            raise NotImplementedError

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.openElements[(-1)])

        def processDoctype(self, token):
            self.parser.parseError('unexpected-doctype')

        def processCharacters(self, token):
            self.tree.insertText(token['data'])

        def processSpaceCharacters(self, token):
            self.tree.insertText(token['data'])

        def processStartTag(self, token):
            return self.startTagHandler[token['name']](token)

        def startTagHtml(self, token):
            if not self.parser.firstStartTag:
                if token['name'] == 'html':
                    self.parser.parseError('non-html-root')
            for attr, value in token['data'].items():
                if attr not in self.tree.openElements[0].attributes:
                    self.tree.openElements[0].attributes[attr] = value

            self.parser.firstStartTag = False

        def processEndTag(self, token):
            return self.endTagHandler[token['name']](token)

    class InitialPhase(Phase):

        def processSpaceCharacters(self, token):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processDoctype(self, token):
            name = token['name']
            publicId = token['publicId']
            systemId = token['systemId']
            correct = token['correct']
            if name != 'html' or publicId is not None or systemId is not None and systemId != 'about:legacy-compat':
                self.parser.parseError('unknown-doctype')
            if publicId is None:
                publicId = ''
            self.tree.insertDoctype(token)
            if publicId != '':
                publicId = publicId.translate(asciiUpper2Lower)
            if not correct or token['name'] != 'html' or publicId.startswith(('+//silmaril//dtd html pro v0r11 19970101//',
                                                                              '-//advasoft ltd//dtd html 3.0 aswedit + extensions//',
                                                                              '-//as//dtd html 3.0 aswedit + extensions//',
                                                                              '-//ietf//dtd html 2.0 level 1//',
                                                                              '-//ietf//dtd html 2.0 level 2//',
                                                                              '-//ietf//dtd html 2.0 strict level 1//',
                                                                              '-//ietf//dtd html 2.0 strict level 2//',
                                                                              '-//ietf//dtd html 2.0 strict//',
                                                                              '-//ietf//dtd html 2.0//',
                                                                              '-//ietf//dtd html 2.1e//',
                                                                              '-//ietf//dtd html 3.0//',
                                                                              '-//ietf//dtd html 3.2 final//',
                                                                              '-//ietf//dtd html 3.2//',
                                                                              '-//ietf//dtd html 3//',
                                                                              '-//ietf//dtd html level 0//',
                                                                              '-//ietf//dtd html level 1//',
                                                                              '-//ietf//dtd html level 2//',
                                                                              '-//ietf//dtd html level 3//',
                                                                              '-//ietf//dtd html strict level 0//',
                                                                              '-//ietf//dtd html strict level 1//',
                                                                              '-//ietf//dtd html strict level 2//',
                                                                              '-//ietf//dtd html strict level 3//',
                                                                              '-//ietf//dtd html strict//',
                                                                              '-//ietf//dtd html//',
                                                                              '-//metrius//dtd metrius presentational//',
                                                                              '-//microsoft//dtd internet explorer 2.0 html strict//',
                                                                              '-//microsoft//dtd internet explorer 2.0 html//',
                                                                              '-//microsoft//dtd internet explorer 2.0 tables//',
                                                                              '-//microsoft//dtd internet explorer 3.0 html strict//',
                                                                              '-//microsoft//dtd internet explorer 3.0 html//',
                                                                              '-//microsoft//dtd internet explorer 3.0 tables//',
                                                                              '-//netscape comm. corp.//dtd html//',
                                                                              '-//netscape comm. corp.//dtd strict html//',
                                                                              "-//o'reilly and associates//dtd html 2.0//",
                                                                              "-//o'reilly and associates//dtd html extended 1.0//",
                                                                              "-//o'reilly and associates//dtd html extended relaxed 1.0//",
                                                                              '-//softquad software//dtd hotmetal pro 6.0::19990601::extensions to html 4.0//',
                                                                              '-//softquad//dtd hotmetal pro 4.0::19971010::extensions to html 4.0//',
                                                                              '-//spyglass//dtd html 2.0 extended//',
                                                                              '-//sq//dtd html 2.0 hotmetal + extensions//',
                                                                              '-//sun microsystems corp.//dtd hotjava html//',
                                                                              '-//sun microsystems corp.//dtd hotjava strict html//',
                                                                              '-//w3c//dtd html 3 1995-03-24//',
                                                                              '-//w3c//dtd html 3.2 draft//',
                                                                              '-//w3c//dtd html 3.2 final//',
                                                                              '-//w3c//dtd html 3.2//',
                                                                              '-//w3c//dtd html 3.2s draft//',
                                                                              '-//w3c//dtd html 4.0 frameset//',
                                                                              '-//w3c//dtd html 4.0 transitional//',
                                                                              '-//w3c//dtd html experimental 19960712//',
                                                                              '-//w3c//dtd html experimental 970421//',
                                                                              '-//w3c//dtd w3 html//',
                                                                              '-//w3o//dtd w3 html 3.0//',
                                                                              '-//webtechs//dtd mozilla html 2.0//',
                                                                              '-//webtechs//dtd mozilla html//')) or publicId in ('-//w3o//dtd w3 html strict 3.0//en//',
                                                                                                                                  '-/w3c/dtd html 4.0 transitional/en',
                                                                                                                                  'html') or publicId.startswith(('-//w3c//dtd html 4.01 frameset//',
                                                                                                                                                                  '-//w3c//dtd html 4.01 transitional//')) and systemId is None or systemId and systemId.lower() == 'http://www.ibm.com/data/dtd/v11/ibmxhtml1-transitional.dtd':
                self.parser.compatMode = 'quirks'
            else:
                if publicId.startswith(('-//w3c//dtd xhtml 1.0 frameset//', '-//w3c//dtd xhtml 1.0 transitional//')) or publicId.startswith(('-//w3c//dtd html 4.01 frameset//',
                                                                                                                                             '-//w3c//dtd html 4.01 transitional//')) and systemId is not None:
                    self.parser.compatMode = 'limited quirks'
            self.parser.phase = self.parser.phases['beforeHtml']

        def anythingElse(self):
            self.parser.compatMode = 'quirks'
            self.parser.phase = self.parser.phases['beforeHtml']

        def processCharacters(self, token):
            self.parser.parseError('expected-doctype-but-got-chars')
            self.anythingElse()
            return token

        def processStartTag(self, token):
            self.parser.parseError('expected-doctype-but-got-start-tag', {'name': token['name']})
            self.anythingElse()
            return token

        def processEndTag(self, token):
            self.parser.parseError('expected-doctype-but-got-end-tag', {'name': token['name']})
            self.anythingElse()
            return token

        def processEOF(self):
            self.parser.parseError('expected-doctype-but-got-eof')
            self.anythingElse()
            return True

    class BeforeHtmlPhase(Phase):

        def insertHtmlElement(self):
            self.tree.insertRoot(impliedTagToken('html', 'StartTag'))
            self.parser.phase = self.parser.phases['beforeHead']

        def processEOF(self):
            self.insertHtmlElement()
            return True

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processSpaceCharacters(self, token):
            pass

        def processCharacters(self, token):
            self.insertHtmlElement()
            return token

        def processStartTag(self, token):
            if token['name'] == 'html':
                self.parser.firstStartTag = True
            self.insertHtmlElement()
            return token

        def processEndTag(self, token):
            if token['name'] not in ('head', 'body', 'html', 'br'):
                self.parser.parseError('unexpected-end-tag-before-html', {'name': token['name']})
            else:
                self.insertHtmlElement()
                return token

    class BeforeHeadPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              'head', self.startTagHead)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              ('head', 'body', 'html', 'br'), self.endTagImplyHead)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.startTagHead(impliedTagToken('head', 'StartTag'))
            return True

        def processSpaceCharacters(self, token):
            pass

        def processCharacters(self, token):
            self.startTagHead(impliedTagToken('head', 'StartTag'))
            return token

        def startTagHtml(self, token):
            return self.parser.phases['inBody'].processStartTag(token)

        def startTagHead(self, token):
            self.tree.insertElement(token)
            self.tree.headPointer = self.tree.openElements[(-1)]
            self.parser.phase = self.parser.phases['inHead']

        def startTagOther(self, token):
            self.startTagHead(impliedTagToken('head', 'StartTag'))
            return token

        def endTagImplyHead(self, token):
            self.startTagHead(impliedTagToken('head', 'StartTag'))
            return token

        def endTagOther(self, token):
            self.parser.parseError('end-tag-after-implied-root', {'name': token['name']})

    class InHeadPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              'title', self.startTagTitle),
             (
              ('noframes', 'style'), self.startTagNoFramesStyle),
             (
              'noscript', self.startTagNoscript),
             (
              'script', self.startTagScript),
             (
              ('base', 'basefont', 'bgsound', 'command', 'link'),
              self.startTagBaseLinkCommand),
             (
              'meta', self.startTagMeta),
             (
              'head', self.startTagHead)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'head', self.endTagHead),
             (
              ('br', 'html', 'body'), self.endTagHtmlBodyBr)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.anythingElse()
            return True

        def processCharacters(self, token):
            self.anythingElse()
            return token

        def startTagHtml(self, token):
            return self.parser.phases['inBody'].processStartTag(token)

        def startTagHead(self, token):
            self.parser.parseError('two-heads-are-not-better-than-one')

        def startTagBaseLinkCommand(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token['selfClosingAcknowledged'] = True

        def startTagMeta(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token['selfClosingAcknowledged'] = True
            attributes = token['data']
            if self.parser.tokenizer.stream.charEncoding[1] == 'tentative':
                if 'charset' in attributes:
                    self.parser.tokenizer.stream.changeEncoding(attributes['charset'])
                elif 'content' in attributes:
                    if 'http-equiv' in attributes:
                        if attributes['http-equiv'].lower() == 'content-type':
                            data = _inputstream.EncodingBytes(attributes['content'].encode('utf-8'))
                            parser = _inputstream.ContentAttrParser(data)
                            codec = parser.parse()
                            self.parser.tokenizer.stream.changeEncoding(codec)

        def startTagTitle(self, token):
            self.parser.parseRCDataRawtext(token, 'RCDATA')

        def startTagNoFramesStyle(self, token):
            self.parser.parseRCDataRawtext(token, 'RAWTEXT')

        def startTagNoscript(self, token):
            if self.parser.scripting:
                self.parser.parseRCDataRawtext(token, 'RAWTEXT')
            else:
                self.tree.insertElement(token)
                self.parser.phase = self.parser.phases['inHeadNoscript']

        def startTagScript(self, token):
            self.tree.insertElement(token)
            self.parser.tokenizer.state = self.parser.tokenizer.scriptDataState
            self.parser.originalPhase = self.parser.phase
            self.parser.phase = self.parser.phases['text']

        def startTagOther(self, token):
            self.anythingElse()
            return token

        def endTagHead(self, token):
            node = self.parser.tree.openElements.pop()
            assert node.name == 'head', 'Expected head got %s' % node.name
            self.parser.phase = self.parser.phases['afterHead']

        def endTagHtmlBodyBr(self, token):
            self.anythingElse()
            return token

        def endTagOther(self, token):
            self.parser.parseError('unexpected-end-tag', {'name': token['name']})

        def anythingElse(self):
            self.endTagHead(impliedTagToken('head'))

    class InHeadNoscriptPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              ('basefont', 'bgsound', 'link', 'meta', 'noframes', 'style'), self.startTagBaseLinkCommand),
             (
              ('head', 'noscript'), self.startTagHeadNoscript)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'noscript', self.endTagNoscript),
             (
              'br', self.endTagBr)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.parser.parseError('eof-in-head-noscript')
            self.anythingElse()
            return True

        def processComment(self, token):
            return self.parser.phases['inHead'].processComment(token)

        def processCharacters(self, token):
            self.parser.parseError('char-in-head-noscript')
            self.anythingElse()
            return token

        def processSpaceCharacters(self, token):
            return self.parser.phases['inHead'].processSpaceCharacters(token)

        def startTagHtml(self, token):
            return self.parser.phases['inBody'].processStartTag(token)

        def startTagBaseLinkCommand(self, token):
            return self.parser.phases['inHead'].processStartTag(token)

        def startTagHeadNoscript(self, token):
            self.parser.parseError('unexpected-start-tag', {'name': token['name']})

        def startTagOther(self, token):
            self.parser.parseError('unexpected-inhead-noscript-tag', {'name': token['name']})
            self.anythingElse()
            return token

        def endTagNoscript(self, token):
            node = self.parser.tree.openElements.pop()
            assert node.name == 'noscript', 'Expected noscript got %s' % node.name
            self.parser.phase = self.parser.phases['inHead']

        def endTagBr(self, token):
            self.parser.parseError('unexpected-inhead-noscript-tag', {'name': token['name']})
            self.anythingElse()
            return token

        def endTagOther(self, token):
            self.parser.parseError('unexpected-end-tag', {'name': token['name']})

        def anythingElse(self):
            self.endTagNoscript(impliedTagToken('noscript'))

    class AfterHeadPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              'body', self.startTagBody),
             (
              'frameset', self.startTagFrameset),
             (
              ('base', 'basefont', 'bgsound', 'link', 'meta', 'noframes', 'script', 'style', 'title'),
              self.startTagFromHead),
             (
              'head', self.startTagHead)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (('body', 'html', 'br'),
              self.endTagHtmlBodyBr)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.anythingElse()
            return True

        def processCharacters(self, token):
            self.anythingElse()
            return token

        def startTagHtml(self, token):
            return self.parser.phases['inBody'].processStartTag(token)

        def startTagBody(self, token):
            self.parser.framesetOK = False
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases['inBody']

        def startTagFrameset(self, token):
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases['inFrameset']

        def startTagFromHead(self, token):
            self.parser.parseError('unexpected-start-tag-out-of-my-head', {'name': token['name']})
            self.tree.openElements.append(self.tree.headPointer)
            self.parser.phases['inHead'].processStartTag(token)
            for node in self.tree.openElements[::-1]:
                if node.name == 'head':
                    self.tree.openElements.remove(node)
                    break

        def startTagHead(self, token):
            self.parser.parseError('unexpected-start-tag', {'name': token['name']})

        def startTagOther(self, token):
            self.anythingElse()
            return token

        def endTagHtmlBodyBr(self, token):
            self.anythingElse()
            return token

        def endTagOther(self, token):
            self.parser.parseError('unexpected-end-tag', {'name': token['name']})

        def anythingElse(self):
            self.tree.insertElement(impliedTagToken('body', 'StartTag'))
            self.parser.phase = self.parser.phases['inBody']
            self.parser.framesetOK = True

    class InBodyPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.processSpaceCharacters = self.processSpaceCharactersNonPre
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              ('base', 'basefont', 'bgsound', 'command', 'link', 'meta', 'script', 'style', 'title'),
              self.startTagProcessInHead),
             (
              'body', self.startTagBody),
             (
              'frameset', self.startTagFrameset),
             (
              ('address', 'article', 'aside', 'blockquote', 'center', 'details', 'dir', 'div', 'dl',
 'fieldset', 'figcaption', 'figure', 'footer', 'header', 'hgroup', 'main', 'menu',
 'nav', 'ol', 'p', 'section', 'summary', 'ul'),
              self.startTagCloseP),
             (
              headingElements, self.startTagHeading),
             (
              ('pre', 'listing'), self.startTagPreListing),
             (
              'form', self.startTagForm),
             (
              ('li', 'dd', 'dt'), self.startTagListItem),
             (
              'plaintext', self.startTagPlaintext),
             (
              'a', self.startTagA),
             (
              ('b', 'big', 'code', 'em', 'font', 'i', 's', 'small', 'strike', 'strong', 'tt', 'u'), self.startTagFormatting),
             (
              'nobr', self.startTagNobr),
             (
              'button', self.startTagButton),
             (
              ('applet', 'marquee', 'object'), self.startTagAppletMarqueeObject),
             (
              'xmp', self.startTagXmp),
             (
              'table', self.startTagTable),
             (
              ('area', 'br', 'embed', 'img', 'keygen', 'wbr'),
              self.startTagVoidFormatting),
             (
              ('param', 'source', 'track'), self.startTagParamSource),
             (
              'input', self.startTagInput),
             (
              'hr', self.startTagHr),
             (
              'image', self.startTagImage),
             (
              'isindex', self.startTagIsIndex),
             (
              'textarea', self.startTagTextarea),
             (
              'iframe', self.startTagIFrame),
             (
              'noscript', self.startTagNoscript),
             (
              ('noembed', 'noframes'), self.startTagRawtext),
             (
              'select', self.startTagSelect),
             (
              ('rp', 'rt'), self.startTagRpRt),
             (
              ('option', 'optgroup'), self.startTagOpt),
             (
              'math', self.startTagMath),
             (
              'svg', self.startTagSvg),
             (
              ('caption', 'col', 'colgroup', 'frame', 'head', 'tbody', 'td', 'tfoot', 'th', 'thead',
 'tr'), self.startTagMisplaced)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'body', self.endTagBody),
             (
              'html', self.endTagHtml),
             (
              ('address', 'article', 'aside', 'blockquote', 'button', 'center', 'details', 'dialog',
 'dir', 'div', 'dl', 'fieldset', 'figcaption', 'figure', 'footer', 'header', 'hgroup',
 'listing', 'main', 'menu', 'nav', 'ol', 'pre', 'section', 'summary', 'ul'), self.endTagBlock),
             (
              'form', self.endTagForm),
             (
              'p', self.endTagP),
             (
              ('dd', 'dt', 'li'), self.endTagListItem),
             (
              headingElements, self.endTagHeading),
             (
              ('a', 'b', 'big', 'code', 'em', 'font', 'i', 'nobr', 's', 'small', 'strike', 'strong',
 'tt', 'u'), self.endTagFormatting),
             (
              ('applet', 'marquee', 'object'), self.endTagAppletMarqueeObject),
             (
              'br', self.endTagBr)])
            self.endTagHandler.default = self.endTagOther

        def isMatchingFormattingElement(self, node1, node2):
            return node1.name == node2.name and node1.namespace == node2.namespace and node1.attributes == node2.attributes

        def addFormattingElement(self, token):
            self.tree.insertElement(token)
            element = self.tree.openElements[(-1)]
            matchingElements = []
            for node in self.tree.activeFormattingElements[::-1]:
                if node is Marker:
                    break
                else:
                    if self.isMatchingFormattingElement(node, element):
                        matchingElements.append(node)

            assert len(matchingElements) <= 3
            if len(matchingElements) == 3:
                self.tree.activeFormattingElements.remove(matchingElements[(-1)])
            self.tree.activeFormattingElements.append(element)

        def processEOF(self):
            allowed_elements = frozenset(('dd', 'dt', 'li', 'p', 'tbody', 'td', 'tfoot',
                                          'th', 'thead', 'tr', 'body', 'html'))
            for node in self.tree.openElements[::-1]:
                if node.name not in allowed_elements:
                    self.parser.parseError('expected-closing-tag-but-got-eof')
                    break

        def processSpaceCharactersDropNewline(self, token):
            data = token['data']
            self.processSpaceCharacters = self.processSpaceCharactersNonPre
            if data.startswith('\n'):
                if self.tree.openElements[(-1)].name in ('pre', 'listing', 'textarea'):
                    if not self.tree.openElements[(-1)].hasContent():
                        data = data[1:]
            if data:
                self.tree.reconstructActiveFormattingElements()
                self.tree.insertText(data)

        def processCharacters(self, token):
            if token['data'] == '\x00':
                return
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertText(token['data'])
            if self.parser.framesetOK:
                if any([char not in spaceCharacters for char in token['data']]):
                    self.parser.framesetOK = False

        def processSpaceCharactersNonPre(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertText(token['data'])

        def startTagProcessInHead(self, token):
            return self.parser.phases['inHead'].processStartTag(token)

        def startTagBody(self, token):
            self.parser.parseError('unexpected-start-tag', {'name': 'body'})
            if len(self.tree.openElements) == 1 or self.tree.openElements[1].name != 'body':
                assert self.parser.innerHTML
            else:
                self.parser.framesetOK = False
                for attr, value in token['data'].items():
                    if attr not in self.tree.openElements[1].attributes:
                        self.tree.openElements[1].attributes[attr] = value

        def startTagFrameset(self, token):
            self.parser.parseError('unexpected-start-tag', {'name': 'frameset'})
            if len(self.tree.openElements) == 1 or self.tree.openElements[1].name != 'body':
                assert self.parser.innerHTML
            else:
                if not self.parser.framesetOK:
                    pass
                else:
                    if self.tree.openElements[1].parent:
                        self.tree.openElements[1].parent.removeChild(self.tree.openElements[1])
                    while self.tree.openElements[(-1)].name != 'html':
                        self.tree.openElements.pop()

                    self.tree.insertElement(token)
                    self.parser.phase = self.parser.phases['inFrameset']

        def startTagCloseP(self, token):
            if self.tree.elementInScope('p', variant='button'):
                self.endTagP(impliedTagToken('p'))
            self.tree.insertElement(token)

        def startTagPreListing(self, token):
            if self.tree.elementInScope('p', variant='button'):
                self.endTagP(impliedTagToken('p'))
            self.tree.insertElement(token)
            self.parser.framesetOK = False
            self.processSpaceCharacters = self.processSpaceCharactersDropNewline

        def startTagForm(self, token):
            if self.tree.formPointer:
                self.parser.parseError('unexpected-start-tag', {'name': 'form'})
            else:
                if self.tree.elementInScope('p', variant='button'):
                    self.endTagP(impliedTagToken('p'))
                self.tree.insertElement(token)
                self.tree.formPointer = self.tree.openElements[(-1)]

        def startTagListItem(self, token):
            self.parser.framesetOK = False
            stopNamesMap = {'li':[
              'li'], 
             'dt':[
              'dt', 'dd'], 
             'dd':[
              'dt', 'dd']}
            stopNames = stopNamesMap[token['name']]
            for node in reversed(self.tree.openElements):
                if node.name in stopNames:
                    self.parser.phase.processEndTag(impliedTagToken(node.name, 'EndTag'))
                    break
                if node.nameTuple in specialElements:
                    if node.name not in ('address', 'div', 'p'):
                        break

            if self.tree.elementInScope('p', variant='button'):
                self.parser.phase.processEndTag(impliedTagToken('p', 'EndTag'))
            self.tree.insertElement(token)

        def startTagPlaintext(self, token):
            if self.tree.elementInScope('p', variant='button'):
                self.endTagP(impliedTagToken('p'))
            self.tree.insertElement(token)
            self.parser.tokenizer.state = self.parser.tokenizer.plaintextState

        def startTagHeading(self, token):
            if self.tree.elementInScope('p', variant='button'):
                self.endTagP(impliedTagToken('p'))
            if self.tree.openElements[(-1)].name in headingElements:
                self.parser.parseError('unexpected-start-tag', {'name': token['name']})
                self.tree.openElements.pop()
            self.tree.insertElement(token)

        def startTagA(self, token):
            afeAElement = self.tree.elementInActiveFormattingElements('a')
            if afeAElement:
                self.parser.parseError('unexpected-start-tag-implies-end-tag', {'startName':'a', 
                 'endName':'a'})
                self.endTagFormatting(impliedTagToken('a'))
                if afeAElement in self.tree.openElements:
                    self.tree.openElements.remove(afeAElement)
                if afeAElement in self.tree.activeFormattingElements:
                    self.tree.activeFormattingElements.remove(afeAElement)
            self.tree.reconstructActiveFormattingElements()
            self.addFormattingElement(token)

        def startTagFormatting(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.addFormattingElement(token)

        def startTagNobr(self, token):
            self.tree.reconstructActiveFormattingElements()
            if self.tree.elementInScope('nobr'):
                self.parser.parseError('unexpected-start-tag-implies-end-tag', {'startName':'nobr', 
                 'endName':'nobr'})
                self.processEndTag(impliedTagToken('nobr'))
                self.tree.reconstructActiveFormattingElements()
            self.addFormattingElement(token)

        def startTagButton(self, token):
            if self.tree.elementInScope('button'):
                self.parser.parseError('unexpected-start-tag-implies-end-tag', {'startName':'button', 
                 'endName':'button'})
                self.processEndTag(impliedTagToken('button'))
                return token
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.parser.framesetOK = False

        def startTagAppletMarqueeObject(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.tree.activeFormattingElements.append(Marker)
            self.parser.framesetOK = False

        def startTagXmp(self, token):
            if self.tree.elementInScope('p', variant='button'):
                self.endTagP(impliedTagToken('p'))
            self.tree.reconstructActiveFormattingElements()
            self.parser.framesetOK = False
            self.parser.parseRCDataRawtext(token, 'RAWTEXT')

        def startTagTable(self, token):
            if self.parser.compatMode != 'quirks':
                if self.tree.elementInScope('p', variant='button'):
                    self.processEndTag(impliedTagToken('p'))
            self.tree.insertElement(token)
            self.parser.framesetOK = False
            self.parser.phase = self.parser.phases['inTable']

        def startTagVoidFormatting(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token['selfClosingAcknowledged'] = True
            self.parser.framesetOK = False

        def startTagInput(self, token):
            framesetOK = self.parser.framesetOK
            self.startTagVoidFormatting(token)
            if 'type' in token['data']:
                if token['data']['type'].translate(asciiUpper2Lower) == 'hidden':
                    self.parser.framesetOK = framesetOK

        def startTagParamSource(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token['selfClosingAcknowledged'] = True

        def startTagHr(self, token):
            if self.tree.elementInScope('p', variant='button'):
                self.endTagP(impliedTagToken('p'))
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token['selfClosingAcknowledged'] = True
            self.parser.framesetOK = False

        def startTagImage(self, token):
            self.parser.parseError('unexpected-start-tag-treated-as', {'originalName':'image', 
             'newName':'img'})
            self.processStartTag(impliedTagToken('img', 'StartTag', attributes=(token['data']),
              selfClosing=(token['selfClosing'])))

        def startTagIsIndex(self, token):
            self.parser.parseError('deprecated-tag', {'name': 'isindex'})
            if self.tree.formPointer:
                return
            else:
                form_attrs = {}
                if 'action' in token['data']:
                    form_attrs['action'] = token['data']['action']
                self.processStartTag(impliedTagToken('form', 'StartTag', attributes=form_attrs))
                self.processStartTag(impliedTagToken('hr', 'StartTag'))
                self.processStartTag(impliedTagToken('label', 'StartTag'))
                if 'prompt' in token['data']:
                    prompt = token['data']['prompt']
                else:
                    prompt = 'This is a searchable index. Enter search keywords: '
            self.processCharacters({'type':tokenTypes['Characters'], 
             'data':prompt})
            attributes = token['data'].copy()
            if 'action' in attributes:
                del attributes['action']
            if 'prompt' in attributes:
                del attributes['prompt']
            attributes['name'] = 'isindex'
            self.processStartTag(impliedTagToken('input', 'StartTag', attributes=attributes,
              selfClosing=(token['selfClosing'])))
            self.processEndTag(impliedTagToken('label'))
            self.processStartTag(impliedTagToken('hr', 'StartTag'))
            self.processEndTag(impliedTagToken('form'))

        def startTagTextarea(self, token):
            self.tree.insertElement(token)
            self.parser.tokenizer.state = self.parser.tokenizer.rcdataState
            self.processSpaceCharacters = self.processSpaceCharactersDropNewline
            self.parser.framesetOK = False

        def startTagIFrame(self, token):
            self.parser.framesetOK = False
            self.startTagRawtext(token)

        def startTagNoscript(self, token):
            if self.parser.scripting:
                self.startTagRawtext(token)
            else:
                self.startTagOther(token)

        def startTagRawtext(self, token):
            """iframe, noembed noframes, noscript(if scripting enabled)"""
            self.parser.parseRCDataRawtext(token, 'RAWTEXT')

        def startTagOpt(self, token):
            if self.tree.openElements[(-1)].name == 'option':
                self.parser.phase.processEndTag(impliedTagToken('option'))
            self.tree.reconstructActiveFormattingElements()
            self.parser.tree.insertElement(token)

        def startTagSelect(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.parser.framesetOK = False
            if self.parser.phase in (self.parser.phases['inTable'],
             self.parser.phases['inCaption'],
             self.parser.phases['inColumnGroup'],
             self.parser.phases['inTableBody'],
             self.parser.phases['inRow'],
             self.parser.phases['inCell']):
                self.parser.phase = self.parser.phases['inSelectInTable']
            else:
                self.parser.phase = self.parser.phases['inSelect']

        def startTagRpRt(self, token):
            if self.tree.elementInScope('ruby'):
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[(-1)].name != 'ruby':
                    self.parser.parseError()
            self.tree.insertElement(token)

        def startTagMath(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.parser.adjustMathMLAttributes(token)
            self.parser.adjustForeignAttributes(token)
            token['namespace'] = namespaces['mathml']
            self.tree.insertElement(token)
            if token['selfClosing']:
                self.tree.openElements.pop()
                token['selfClosingAcknowledged'] = True

        def startTagSvg(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.parser.adjustSVGAttributes(token)
            self.parser.adjustForeignAttributes(token)
            token['namespace'] = namespaces['svg']
            self.tree.insertElement(token)
            if token['selfClosing']:
                self.tree.openElements.pop()
                token['selfClosingAcknowledged'] = True

        def startTagMisplaced(self, token):
            """ Elements that should be children of other elements that have a
            different insertion mode; here they are ignored
            "caption", "col", "colgroup", "frame", "frameset", "head",
            "option", "optgroup", "tbody", "td", "tfoot", "th", "thead",
            "tr", "noscript"
            """
            self.parser.parseError('unexpected-start-tag-ignored', {'name': token['name']})

        def startTagOther(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)

        def endTagP(self, token):
            if not self.tree.elementInScope('p', variant='button'):
                self.startTagCloseP(impliedTagToken('p', 'StartTag'))
                self.parser.parseError('unexpected-end-tag', {'name': 'p'})
                self.endTagP(impliedTagToken('p', 'EndTag'))
            else:
                self.tree.generateImpliedEndTags('p')
                if self.tree.openElements[(-1)].name != 'p':
                    self.parser.parseError('unexpected-end-tag', {'name': 'p'})
                node = self.tree.openElements.pop()
                while node.name != 'p':
                    node = self.tree.openElements.pop()

        def endTagBody(self, token):
            if not self.tree.elementInScope('body'):
                self.parser.parseError()
                return
            if self.tree.openElements[(-1)].name != 'body':
                for node in self.tree.openElements[2:]:
                    if node.name not in frozenset(('dd', 'dt', 'li', 'optgroup', 'option',
                                                   'p', 'rp', 'rt', 'tbody', 'td',
                                                   'tfoot', 'th', 'thead', 'tr',
                                                   'body', 'html')):
                        self.parser.parseError('expected-one-end-tag-but-got-another', {'gotName':'body', 
                         'expectedName':node.name})
                        break

            self.parser.phase = self.parser.phases['afterBody']

        def endTagHtml(self, token):
            if self.tree.elementInScope('body'):
                self.endTagBody(impliedTagToken('body'))
                return token

        def endTagBlock(self, token):
            if token['name'] == 'pre':
                self.processSpaceCharacters = self.processSpaceCharactersNonPre
            else:
                inScope = self.tree.elementInScope(token['name'])
                if inScope:
                    self.tree.generateImpliedEndTags()
                if self.tree.openElements[(-1)].name != token['name']:
                    self.parser.parseError('end-tag-too-early', {'name': token['name']})
                if inScope:
                    node = self.tree.openElements.pop()
                    while node.name != token['name']:
                        node = self.tree.openElements.pop()

        def endTagForm(self, token):
            node = self.tree.formPointer
            self.tree.formPointer = None
            if node is None or not self.tree.elementInScope(node):
                self.parser.parseError('unexpected-end-tag', {'name': 'form'})
            else:
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[(-1)] != node:
                    self.parser.parseError('end-tag-too-early-ignored', {'name': 'form'})
                self.tree.openElements.remove(node)

        def endTagListItem(self, token):
            if token['name'] == 'li':
                variant = 'list'
            else:
                variant = None
            if not self.tree.elementInScope((token['name']), variant=variant):
                self.parser.parseError('unexpected-end-tag', {'name': token['name']})
            else:
                self.tree.generateImpliedEndTags(exclude=(token['name']))
                if self.tree.openElements[(-1)].name != token['name']:
                    self.parser.parseError('end-tag-too-early', {'name': token['name']})
                node = self.tree.openElements.pop()
                while node.name != token['name']:
                    node = self.tree.openElements.pop()

        def endTagHeading(self, token):
            for item in headingElements:
                if self.tree.elementInScope(item):
                    self.tree.generateImpliedEndTags()
                    break

            if self.tree.openElements[(-1)].name != token['name']:
                self.parser.parseError('end-tag-too-early', {'name': token['name']})
            for item in headingElements:
                if self.tree.elementInScope(item):
                    item = self.tree.openElements.pop()
                    while item.name not in headingElements:
                        item = self.tree.openElements.pop()

                    break

        def endTagFormatting(self, token):
            """The much-feared adoption agency algorithm"""
            outerLoopCounter = 0
            while outerLoopCounter < 8:
                outerLoopCounter += 1
                formattingElement = self.tree.elementInActiveFormattingElements(token['name'])
                if not formattingElement or formattingElement in self.tree.openElements and not self.tree.elementInScope(formattingElement.name):
                    self.endTagOther(token)
                    return
                if formattingElement not in self.tree.openElements:
                    self.parser.parseError('adoption-agency-1.2', {'name': token['name']})
                    self.tree.activeFormattingElements.remove(formattingElement)
                    return
                if not self.tree.elementInScope(formattingElement.name):
                    self.parser.parseError('adoption-agency-4.4', {'name': token['name']})
                    return
                if formattingElement != self.tree.openElements[(-1)]:
                    self.parser.parseError('adoption-agency-1.3', {'name': token['name']})
                afeIndex = self.tree.openElements.index(formattingElement)
                furthestBlock = None
                for element in self.tree.openElements[afeIndex:]:
                    if element.nameTuple in specialElements:
                        furthestBlock = element
                        break

                if furthestBlock is None:
                    element = self.tree.openElements.pop()
                    while element != formattingElement:
                        element = self.tree.openElements.pop()

                    self.tree.activeFormattingElements.remove(element)
                    return
                commonAncestor = self.tree.openElements[(afeIndex - 1)]
                bookmark = self.tree.activeFormattingElements.index(formattingElement)
                lastNode = node = furthestBlock
                innerLoopCounter = 0
                index = self.tree.openElements.index(node)
                while innerLoopCounter < 3:
                    innerLoopCounter += 1
                    index -= 1
                    node = self.tree.openElements[index]
                    if node not in self.tree.activeFormattingElements:
                        self.tree.openElements.remove(node)
                    else:
                        if node == formattingElement:
                            break
                        else:
                            if lastNode == furthestBlock:
                                bookmark = self.tree.activeFormattingElements.index(node) + 1
                            clone = node.cloneNode()
                            self.tree.activeFormattingElements[self.tree.activeFormattingElements.index(node)] = clone
                            self.tree.openElements[self.tree.openElements.index(node)] = clone
                            node = clone
                            if lastNode.parent:
                                lastNode.parent.removeChild(lastNode)
                        node.appendChild(lastNode)
                    lastNode = node

                if lastNode.parent:
                    lastNode.parent.removeChild(lastNode)
                if commonAncestor.name in frozenset(('table', 'tbody', 'tfoot', 'thead',
                                                     'tr')):
                    parent, insertBefore = self.tree.getTableMisnestedNodePosition()
                    parent.insertBefore(lastNode, insertBefore)
                else:
                    commonAncestor.appendChild(lastNode)
                clone = formattingElement.cloneNode()
                furthestBlock.reparentChildren(clone)
                furthestBlock.appendChild(clone)
                self.tree.activeFormattingElements.remove(formattingElement)
                self.tree.activeFormattingElements.insert(bookmark, clone)
                self.tree.openElements.remove(formattingElement)
                self.tree.openElements.insert(self.tree.openElements.index(furthestBlock) + 1, clone)

        def endTagAppletMarqueeObject(self, token):
            if self.tree.elementInScope(token['name']):
                self.tree.generateImpliedEndTags()
            else:
                if self.tree.openElements[(-1)].name != token['name']:
                    self.parser.parseError('end-tag-too-early', {'name': token['name']})
                if self.tree.elementInScope(token['name']):
                    element = self.tree.openElements.pop()
                    while element.name != token['name']:
                        element = self.tree.openElements.pop()

                    self.tree.clearActiveFormattingElements()

        def endTagBr(self, token):
            self.parser.parseError('unexpected-end-tag-treated-as', {'originalName':'br', 
             'newName':'br element'})
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(impliedTagToken('br', 'StartTag'))
            self.tree.openElements.pop()

        def endTagOther(self, token):
            for node in self.tree.openElements[::-1]:
                if node.name == token['name']:
                    self.tree.generateImpliedEndTags(exclude=(token['name']))
                    if self.tree.openElements[(-1)].name != token['name']:
                        self.parser.parseError('unexpected-end-tag', {'name': token['name']})
                    while self.tree.openElements.pop() != node:
                        pass

                    break
                elif node.nameTuple in specialElements:
                    self.parser.parseError('unexpected-end-tag', {'name': token['name']})
                    break

    class TextPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'script', self.endTagScript)])
            self.endTagHandler.default = self.endTagOther

        def processCharacters(self, token):
            self.tree.insertText(token['data'])

        def processEOF(self):
            self.parser.parseError('expected-named-closing-tag-but-got-eof', {'name': self.tree.openElements[(-1)].name})
            self.tree.openElements.pop()
            self.parser.phase = self.parser.originalPhase
            return True

        def startTagOther(self, token):
            assert False, 'Tried to process start tag %s in RCDATA/RAWTEXT mode' % token['name']

        def endTagScript(self, token):
            node = self.tree.openElements.pop()
            assert node.name == 'script'
            self.parser.phase = self.parser.originalPhase

        def endTagOther(self, token):
            self.tree.openElements.pop()
            self.parser.phase = self.parser.originalPhase

    class InTablePhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              'caption', self.startTagCaption),
             (
              'colgroup', self.startTagColgroup),
             (
              'col', self.startTagCol),
             (
              ('tbody', 'tfoot', 'thead'), self.startTagRowGroup),
             (
              ('td', 'th', 'tr'), self.startTagImplyTbody),
             (
              'table', self.startTagTable),
             (
              ('style', 'script'), self.startTagStyleScript),
             (
              'input', self.startTagInput),
             (
              'form', self.startTagForm)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'table', self.endTagTable),
             (
              ('body', 'caption', 'col', 'colgroup', 'html', 'tbody', 'td', 'tfoot', 'th', 'thead',
 'tr'), self.endTagIgnore)])
            self.endTagHandler.default = self.endTagOther

        def clearStackToTableContext(self):
            while self.tree.openElements[(-1)].name not in ('table', 'html'):
                self.tree.openElements.pop()

        def processEOF(self):
            if self.tree.openElements[(-1)].name != 'html':
                self.parser.parseError('eof-in-table')
            elif not self.parser.innerHTML:
                raise AssertionError

        def processSpaceCharacters(self, token):
            originalPhase = self.parser.phase
            self.parser.phase = self.parser.phases['inTableText']
            self.parser.phase.originalPhase = originalPhase
            self.parser.phase.processSpaceCharacters(token)

        def processCharacters(self, token):
            originalPhase = self.parser.phase
            self.parser.phase = self.parser.phases['inTableText']
            self.parser.phase.originalPhase = originalPhase
            self.parser.phase.processCharacters(token)

        def insertText(self, token):
            self.tree.insertFromTable = True
            self.parser.phases['inBody'].processCharacters(token)
            self.tree.insertFromTable = False

        def startTagCaption(self, token):
            self.clearStackToTableContext()
            self.tree.activeFormattingElements.append(Marker)
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases['inCaption']

        def startTagColgroup(self, token):
            self.clearStackToTableContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases['inColumnGroup']

        def startTagCol(self, token):
            self.startTagColgroup(impliedTagToken('colgroup', 'StartTag'))
            return token

        def startTagRowGroup(self, token):
            self.clearStackToTableContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases['inTableBody']

        def startTagImplyTbody(self, token):
            self.startTagRowGroup(impliedTagToken('tbody', 'StartTag'))
            return token

        def startTagTable(self, token):
            self.parser.parseError('unexpected-start-tag-implies-end-tag', {'startName':'table', 
             'endName':'table'})
            self.parser.phase.processEndTag(impliedTagToken('table'))
            if not self.parser.innerHTML:
                return token

        def startTagStyleScript(self, token):
            return self.parser.phases['inHead'].processStartTag(token)

        def startTagInput(self, token):
            if 'type' in token['data']:
                if token['data']['type'].translate(asciiUpper2Lower) == 'hidden':
                    self.parser.parseError('unexpected-hidden-input-in-table')
                    self.tree.insertElement(token)
                    self.tree.openElements.pop()
            else:
                self.startTagOther(token)

        def startTagForm(self, token):
            self.parser.parseError('unexpected-form-in-table')
            if self.tree.formPointer is None:
                self.tree.insertElement(token)
                self.tree.formPointer = self.tree.openElements[(-1)]
                self.tree.openElements.pop()

        def startTagOther(self, token):
            self.parser.parseError('unexpected-start-tag-implies-table-voodoo', {'name': token['name']})
            self.tree.insertFromTable = True
            self.parser.phases['inBody'].processStartTag(token)
            self.tree.insertFromTable = False

        def endTagTable(self, token):
            if self.tree.elementInScope('table', variant='table'):
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[(-1)].name != 'table':
                    self.parser.parseError('end-tag-too-early-named', {'gotName':'table', 
                     'expectedName':self.tree.openElements[(-1)].name})
                while self.tree.openElements[(-1)].name != 'table':
                    self.tree.openElements.pop()

                self.tree.openElements.pop()
                self.parser.resetInsertionMode()
            else:
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagIgnore(self, token):
            self.parser.parseError('unexpected-end-tag', {'name': token['name']})

        def endTagOther(self, token):
            self.parser.parseError('unexpected-end-tag-implies-table-voodoo', {'name': token['name']})
            self.tree.insertFromTable = True
            self.parser.phases['inBody'].processEndTag(token)
            self.tree.insertFromTable = False

    class InTableTextPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.originalPhase = None
            self.characterTokens = []

        def flushCharacters(self):
            data = ''.join([item['data'] for item in self.characterTokens])
            if any([item not in spaceCharacters for item in data]):
                token = {'type':tokenTypes['Characters'], 
                 'data':data}
                self.parser.phases['inTable'].insertText(token)
            else:
                if data:
                    self.tree.insertText(data)
            self.characterTokens = []

        def processComment(self, token):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return token

        def processEOF(self):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return True

        def processCharacters(self, token):
            if token['data'] == '\x00':
                return
            self.characterTokens.append(token)

        def processSpaceCharacters(self, token):
            self.characterTokens.append(token)

        def processStartTag(self, token):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return token

        def processEndTag(self, token):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return token

    class InCaptionPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              ('caption', 'col', 'colgroup', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'), self.startTagTableElement)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'caption', self.endTagCaption),
             (
              'table', self.endTagTable),
             (
              ('body', 'col', 'colgroup', 'html', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'), self.endTagIgnore)])
            self.endTagHandler.default = self.endTagOther

        def ignoreEndTagCaption(self):
            return not self.tree.elementInScope('caption', variant='table')

        def processEOF(self):
            self.parser.phases['inBody'].processEOF()

        def processCharacters(self, token):
            return self.parser.phases['inBody'].processCharacters(token)

        def startTagTableElement(self, token):
            self.parser.parseError()
            ignoreEndTag = self.ignoreEndTagCaption()
            self.parser.phase.processEndTag(impliedTagToken('caption'))
            if not ignoreEndTag:
                return token

        def startTagOther(self, token):
            return self.parser.phases['inBody'].processStartTag(token)

        def endTagCaption(self, token):
            if not self.ignoreEndTagCaption():
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[(-1)].name != 'caption':
                    self.parser.parseError('expected-one-end-tag-but-got-another', {'gotName':'caption', 
                     'expectedName':self.tree.openElements[(-1)].name})
                while self.tree.openElements[(-1)].name != 'caption':
                    self.tree.openElements.pop()

                self.tree.openElements.pop()
                self.tree.clearActiveFormattingElements()
                self.parser.phase = self.parser.phases['inTable']
            else:
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagTable(self, token):
            self.parser.parseError()
            ignoreEndTag = self.ignoreEndTagCaption()
            self.parser.phase.processEndTag(impliedTagToken('caption'))
            if not ignoreEndTag:
                return token

        def endTagIgnore(self, token):
            self.parser.parseError('unexpected-end-tag', {'name': token['name']})

        def endTagOther(self, token):
            return self.parser.phases['inBody'].processEndTag(token)

    class InColumnGroupPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              'col', self.startTagCol)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'colgroup', self.endTagColgroup),
             (
              'col', self.endTagCol)])
            self.endTagHandler.default = self.endTagOther

        def ignoreEndTagColgroup(self):
            return self.tree.openElements[(-1)].name == 'html'

        def processEOF(self):
            if self.tree.openElements[(-1)].name == 'html':
                assert self.parser.innerHTML
                return
            ignoreEndTag = self.ignoreEndTagColgroup()
            self.endTagColgroup(impliedTagToken('colgroup'))
            if not ignoreEndTag:
                return True

        def processCharacters(self, token):
            ignoreEndTag = self.ignoreEndTagColgroup()
            self.endTagColgroup(impliedTagToken('colgroup'))
            if not ignoreEndTag:
                return token

        def startTagCol(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token['selfClosingAcknowledged'] = True

        def startTagOther(self, token):
            ignoreEndTag = self.ignoreEndTagColgroup()
            self.endTagColgroup(impliedTagToken('colgroup'))
            if not ignoreEndTag:
                return token

        def endTagColgroup(self, token):
            if self.ignoreEndTagColgroup():
                assert self.parser.innerHTML
                self.parser.parseError()
            else:
                self.tree.openElements.pop()
                self.parser.phase = self.parser.phases['inTable']

        def endTagCol(self, token):
            self.parser.parseError('no-end-tag', {'name': 'col'})

        def endTagOther(self, token):
            ignoreEndTag = self.ignoreEndTagColgroup()
            self.endTagColgroup(impliedTagToken('colgroup'))
            if not ignoreEndTag:
                return token

    class InTableBodyPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              'tr', self.startTagTr),
             (
              ('td', 'th'), self.startTagTableCell),
             (
              ('caption', 'col', 'colgroup', 'tbody', 'tfoot', 'thead'),
              self.startTagTableOther)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              ('tbody', 'tfoot', 'thead'), self.endTagTableRowGroup),
             (
              'table', self.endTagTable),
             (
              ('body', 'caption', 'col', 'colgroup', 'html', 'td', 'th', 'tr'), self.endTagIgnore)])
            self.endTagHandler.default = self.endTagOther

        def clearStackToTableBodyContext(self):
            while self.tree.openElements[(-1)].name not in ('tbody', 'tfoot', 'thead',
                                                            'html'):
                self.tree.openElements.pop()

            if self.tree.openElements[(-1)].name == 'html':
                if not self.parser.innerHTML:
                    raise AssertionError

        def processEOF(self):
            self.parser.phases['inTable'].processEOF()

        def processSpaceCharacters(self, token):
            return self.parser.phases['inTable'].processSpaceCharacters(token)

        def processCharacters(self, token):
            return self.parser.phases['inTable'].processCharacters(token)

        def startTagTr(self, token):
            self.clearStackToTableBodyContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases['inRow']

        def startTagTableCell(self, token):
            self.parser.parseError('unexpected-cell-in-table-body', {'name': token['name']})
            self.startTagTr(impliedTagToken('tr', 'StartTag'))
            return token

        def startTagTableOther(self, token):
            if self.tree.elementInScope('tbody', variant='table') or self.tree.elementInScope('thead', variant='table') or self.tree.elementInScope('tfoot', variant='table'):
                self.clearStackToTableBodyContext()
                self.endTagTableRowGroup(impliedTagToken(self.tree.openElements[(-1)].name))
                return token
            elif not self.parser.innerHTML:
                raise AssertionError
            self.parser.parseError()

        def startTagOther(self, token):
            return self.parser.phases['inTable'].processStartTag(token)

        def endTagTableRowGroup(self, token):
            if self.tree.elementInScope((token['name']), variant='table'):
                self.clearStackToTableBodyContext()
                self.tree.openElements.pop()
                self.parser.phase = self.parser.phases['inTable']
            else:
                self.parser.parseError('unexpected-end-tag-in-table-body', {'name': token['name']})

        def endTagTable(self, token):
            if self.tree.elementInScope('tbody', variant='table') or self.tree.elementInScope('thead', variant='table') or self.tree.elementInScope('tfoot', variant='table'):
                self.clearStackToTableBodyContext()
                self.endTagTableRowGroup(impliedTagToken(self.tree.openElements[(-1)].name))
                return token
            elif not self.parser.innerHTML:
                raise AssertionError
            self.parser.parseError()

        def endTagIgnore(self, token):
            self.parser.parseError('unexpected-end-tag-in-table-body', {'name': token['name']})

        def endTagOther(self, token):
            return self.parser.phases['inTable'].processEndTag(token)

    class InRowPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              ('td', 'th'), self.startTagTableCell),
             (
              ('caption', 'col', 'colgroup', 'tbody', 'tfoot', 'thead', 'tr'), self.startTagTableOther)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'tr', self.endTagTr),
             (
              'table', self.endTagTable),
             (
              ('tbody', 'tfoot', 'thead'), self.endTagTableRowGroup),
             (
              ('body', 'caption', 'col', 'colgroup', 'html', 'td', 'th'),
              self.endTagIgnore)])
            self.endTagHandler.default = self.endTagOther

        def clearStackToTableRowContext(self):
            while self.tree.openElements[(-1)].name not in ('tr', 'html'):
                self.parser.parseError('unexpected-implied-end-tag-in-table-row', {'name': self.tree.openElements[(-1)].name})
                self.tree.openElements.pop()

        def ignoreEndTagTr(self):
            return not self.tree.elementInScope('tr', variant='table')

        def processEOF(self):
            self.parser.phases['inTable'].processEOF()

        def processSpaceCharacters(self, token):
            return self.parser.phases['inTable'].processSpaceCharacters(token)

        def processCharacters(self, token):
            return self.parser.phases['inTable'].processCharacters(token)

        def startTagTableCell(self, token):
            self.clearStackToTableRowContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases['inCell']
            self.tree.activeFormattingElements.append(Marker)

        def startTagTableOther(self, token):
            ignoreEndTag = self.ignoreEndTagTr()
            self.endTagTr(impliedTagToken('tr'))
            if not ignoreEndTag:
                return token

        def startTagOther(self, token):
            return self.parser.phases['inTable'].processStartTag(token)

        def endTagTr(self, token):
            if not self.ignoreEndTagTr():
                self.clearStackToTableRowContext()
                self.tree.openElements.pop()
                self.parser.phase = self.parser.phases['inTableBody']
            else:
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagTable(self, token):
            ignoreEndTag = self.ignoreEndTagTr()
            self.endTagTr(impliedTagToken('tr'))
            if not ignoreEndTag:
                return token

        def endTagTableRowGroup(self, token):
            if self.tree.elementInScope((token['name']), variant='table'):
                self.endTagTr(impliedTagToken('tr'))
                return token
            self.parser.parseError()

        def endTagIgnore(self, token):
            self.parser.parseError('unexpected-end-tag-in-table-row', {'name': token['name']})

        def endTagOther(self, token):
            return self.parser.phases['inTable'].processEndTag(token)

    class InCellPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              ('caption', 'col', 'colgroup', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'), self.startTagTableOther)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              ('td', 'th'), self.endTagTableCell),
             (
              ('body', 'caption', 'col', 'colgroup', 'html'), self.endTagIgnore),
             (
              ('table', 'tbody', 'tfoot', 'thead', 'tr'), self.endTagImply)])
            self.endTagHandler.default = self.endTagOther

        def closeCell(self):
            if self.tree.elementInScope('td', variant='table'):
                self.endTagTableCell(impliedTagToken('td'))
            elif self.tree.elementInScope('th', variant='table'):
                self.endTagTableCell(impliedTagToken('th'))

        def processEOF(self):
            self.parser.phases['inBody'].processEOF()

        def processCharacters(self, token):
            return self.parser.phases['inBody'].processCharacters(token)

        def startTagTableOther(self, token):
            if self.tree.elementInScope('td', variant='table') or self.tree.elementInScope('th', variant='table'):
                self.closeCell()
                return token
            elif not self.parser.innerHTML:
                raise AssertionError
            self.parser.parseError()

        def startTagOther(self, token):
            return self.parser.phases['inBody'].processStartTag(token)

        def endTagTableCell(self, token):
            if self.tree.elementInScope((token['name']), variant='table'):
                self.tree.generateImpliedEndTags(token['name'])
                if self.tree.openElements[(-1)].name != token['name']:
                    self.parser.parseError('unexpected-cell-end-tag', {'name': token['name']})
                    while True:
                        node = self.tree.openElements.pop()
                        if node.name == token['name']:
                            break

                else:
                    self.tree.openElements.pop()
                self.tree.clearActiveFormattingElements()
                self.parser.phase = self.parser.phases['inRow']
            else:
                self.parser.parseError('unexpected-end-tag', {'name': token['name']})

        def endTagIgnore(self, token):
            self.parser.parseError('unexpected-end-tag', {'name': token['name']})

        def endTagImply(self, token):
            if self.tree.elementInScope((token['name']), variant='table'):
                self.closeCell()
                return token
            self.parser.parseError()

        def endTagOther(self, token):
            return self.parser.phases['inBody'].processEndTag(token)

    class InSelectPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              'option', self.startTagOption),
             (
              'optgroup', self.startTagOptgroup),
             (
              'select', self.startTagSelect),
             (
              ('input', 'keygen', 'textarea'), self.startTagInput),
             (
              'script', self.startTagScript)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'option', self.endTagOption),
             (
              'optgroup', self.endTagOptgroup),
             (
              'select', self.endTagSelect)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            if self.tree.openElements[(-1)].name != 'html':
                self.parser.parseError('eof-in-select')
            elif not self.parser.innerHTML:
                raise AssertionError

        def processCharacters(self, token):
            if token['data'] == '\x00':
                return
            self.tree.insertText(token['data'])

        def startTagOption(self, token):
            if self.tree.openElements[(-1)].name == 'option':
                self.tree.openElements.pop()
            self.tree.insertElement(token)

        def startTagOptgroup(self, token):
            if self.tree.openElements[(-1)].name == 'option':
                self.tree.openElements.pop()
            if self.tree.openElements[(-1)].name == 'optgroup':
                self.tree.openElements.pop()
            self.tree.insertElement(token)

        def startTagSelect(self, token):
            self.parser.parseError('unexpected-select-in-select')
            self.endTagSelect(impliedTagToken('select'))

        def startTagInput(self, token):
            self.parser.parseError('unexpected-input-in-select')
            if self.tree.elementInScope('select', variant='select'):
                self.endTagSelect(impliedTagToken('select'))
                return token
            elif not self.parser.innerHTML:
                raise AssertionError

        def startTagScript(self, token):
            return self.parser.phases['inHead'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError('unexpected-start-tag-in-select', {'name': token['name']})

        def endTagOption(self, token):
            if self.tree.openElements[(-1)].name == 'option':
                self.tree.openElements.pop()
            else:
                self.parser.parseError('unexpected-end-tag-in-select', {'name': 'option'})

        def endTagOptgroup(self, token):
            if self.tree.openElements[(-1)].name == 'option':
                if self.tree.openElements[(-2)].name == 'optgroup':
                    self.tree.openElements.pop()
            else:
                if self.tree.openElements[(-1)].name == 'optgroup':
                    self.tree.openElements.pop()
                else:
                    self.parser.parseError('unexpected-end-tag-in-select', {'name': 'optgroup'})

        def endTagSelect(self, token):
            if self.tree.elementInScope('select', variant='select'):
                node = self.tree.openElements.pop()
                while node.name != 'select':
                    node = self.tree.openElements.pop()

                self.parser.resetInsertionMode()
            else:
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagOther(self, token):
            self.parser.parseError('unexpected-end-tag-in-select', {'name': token['name']})

    class InSelectInTablePhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              ('caption', 'table', 'tbody', 'tfoot', 'thead', 'tr', 'td', 'th'),
              self.startTagTable)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              ('caption', 'table', 'tbody', 'tfoot', 'thead', 'tr', 'td', 'th'),
              self.endTagTable)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.parser.phases['inSelect'].processEOF()

        def processCharacters(self, token):
            return self.parser.phases['inSelect'].processCharacters(token)

        def startTagTable(self, token):
            self.parser.parseError('unexpected-table-element-start-tag-in-select-in-table', {'name': token['name']})
            self.endTagOther(impliedTagToken('select'))
            return token

        def startTagOther(self, token):
            return self.parser.phases['inSelect'].processStartTag(token)

        def endTagTable(self, token):
            self.parser.parseError('unexpected-table-element-end-tag-in-select-in-table', {'name': token['name']})
            if self.tree.elementInScope((token['name']), variant='table'):
                self.endTagOther(impliedTagToken('select'))
                return token

        def endTagOther(self, token):
            return self.parser.phases['inSelect'].processEndTag(token)

    class InForeignContentPhase(Phase):
        breakoutElements = frozenset(['b', 'big', 'blockquote', 'body', 'br',
         'center', 'code', 'dd', 'div', 'dl', 'dt',
         'em', 'embed', 'h1', 'h2', 'h3',
         'h4', 'h5', 'h6', 'head', 'hr', 'i', 'img',
         'li', 'listing', 'menu', 'meta', 'nobr',
         'ol', 'p', 'pre', 'ruby', 's', 'small',
         'span', 'strong', 'strike', 'sub', 'sup',
         'table', 'tt', 'u', 'ul', 'var'])

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

        def adjustSVGTagNames(self, token):
            replacements = {'altglyph':'altGlyph', 
             'altglyphdef':'altGlyphDef', 
             'altglyphitem':'altGlyphItem', 
             'animatecolor':'animateColor', 
             'animatemotion':'animateMotion', 
             'animatetransform':'animateTransform', 
             'clippath':'clipPath', 
             'feblend':'feBlend', 
             'fecolormatrix':'feColorMatrix', 
             'fecomponenttransfer':'feComponentTransfer', 
             'fecomposite':'feComposite', 
             'feconvolvematrix':'feConvolveMatrix', 
             'fediffuselighting':'feDiffuseLighting', 
             'fedisplacementmap':'feDisplacementMap', 
             'fedistantlight':'feDistantLight', 
             'feflood':'feFlood', 
             'fefunca':'feFuncA', 
             'fefuncb':'feFuncB', 
             'fefuncg':'feFuncG', 
             'fefuncr':'feFuncR', 
             'fegaussianblur':'feGaussianBlur', 
             'feimage':'feImage', 
             'femerge':'feMerge', 
             'femergenode':'feMergeNode', 
             'femorphology':'feMorphology', 
             'feoffset':'feOffset', 
             'fepointlight':'fePointLight', 
             'fespecularlighting':'feSpecularLighting', 
             'fespotlight':'feSpotLight', 
             'fetile':'feTile', 
             'feturbulence':'feTurbulence', 
             'foreignobject':'foreignObject', 
             'glyphref':'glyphRef', 
             'lineargradient':'linearGradient', 
             'radialgradient':'radialGradient', 
             'textpath':'textPath'}
            if token['name'] in replacements:
                token['name'] = replacements[token['name']]

        def processCharacters(self, token):
            if token['data'] == '\x00':
                token['data'] = '�'
            else:
                if self.parser.framesetOK:
                    if any(char not in spaceCharacters for char in token['data']):
                        self.parser.framesetOK = False
            Phase.processCharacters(self, token)

        def processStartTag(self, token):
            currentNode = self.tree.openElements[(-1)]
            if token['name'] in self.breakoutElements or token['name'] == 'font' and set(token['data'].keys()) & set(['color', 'face', 'size']):
                self.parser.parseError('unexpected-html-element-in-foreign-content', {'name': token['name']})
                while self.tree.openElements[(-1)].namespace != self.tree.defaultNamespace and not self.parser.isHTMLIntegrationPoint(self.tree.openElements[(-1)]) and not self.parser.isMathMLTextIntegrationPoint(self.tree.openElements[(-1)]):
                    self.tree.openElements.pop()

                return token
            if currentNode.namespace == namespaces['mathml']:
                self.parser.adjustMathMLAttributes(token)
            else:
                if currentNode.namespace == namespaces['svg']:
                    self.adjustSVGTagNames(token)
                    self.parser.adjustSVGAttributes(token)
            self.parser.adjustForeignAttributes(token)
            token['namespace'] = currentNode.namespace
            self.tree.insertElement(token)
            if token['selfClosing']:
                self.tree.openElements.pop()
                token['selfClosingAcknowledged'] = True

        def processEndTag(self, token):
            nodeIndex = len(self.tree.openElements) - 1
            node = self.tree.openElements[(-1)]
            if node.name.translate(asciiUpper2Lower) != token['name']:
                self.parser.parseError('unexpected-end-tag', {'name': token['name']})
            while True:
                if node.name.translate(asciiUpper2Lower) == token['name']:
                    if self.parser.phase == self.parser.phases['inTableText']:
                        self.parser.phase.flushCharacters()
                        self.parser.phase = self.parser.phase.originalPhase
                    while self.tree.openElements.pop() != node:
                        assert self.tree.openElements

                    new_token = None
                    break
                nodeIndex -= 1
                node = self.tree.openElements[nodeIndex]
                if node.namespace != self.tree.defaultNamespace:
                    continue
                else:
                    new_token = self.parser.phase.processEndTag(token)
                    break

            return new_token

    class AfterBodyPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([('html', self.endTagHtml)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.openElements[0])

        def processCharacters(self, token):
            self.parser.parseError('unexpected-char-after-body')
            self.parser.phase = self.parser.phases['inBody']
            return token

        def startTagHtml(self, token):
            return self.parser.phases['inBody'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError('unexpected-start-tag-after-body', {'name': token['name']})
            self.parser.phase = self.parser.phases['inBody']
            return token

        def endTagHtml(self, name):
            if self.parser.innerHTML:
                self.parser.parseError('unexpected-end-tag-after-body-innerhtml')
            else:
                self.parser.phase = self.parser.phases['afterAfterBody']

        def endTagOther(self, token):
            self.parser.parseError('unexpected-end-tag-after-body', {'name': token['name']})
            self.parser.phase = self.parser.phases['inBody']
            return token

    class InFramesetPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              'frameset', self.startTagFrameset),
             (
              'frame', self.startTagFrame),
             (
              'noframes', self.startTagNoframes)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'frameset', self.endTagFrameset)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            if self.tree.openElements[(-1)].name != 'html':
                self.parser.parseError('eof-in-frameset')
            elif not self.parser.innerHTML:
                raise AssertionError

        def processCharacters(self, token):
            self.parser.parseError('unexpected-char-in-frameset')

        def startTagFrameset(self, token):
            self.tree.insertElement(token)

        def startTagFrame(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()

        def startTagNoframes(self, token):
            return self.parser.phases['inBody'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError('unexpected-start-tag-in-frameset', {'name': token['name']})

        def endTagFrameset(self, token):
            if self.tree.openElements[(-1)].name == 'html':
                self.parser.parseError('unexpected-frameset-in-frameset-innerhtml')
            else:
                self.tree.openElements.pop()
            if not self.parser.innerHTML:
                if self.tree.openElements[(-1)].name != 'frameset':
                    self.parser.phase = self.parser.phases['afterFrameset']

        def endTagOther(self, token):
            self.parser.parseError('unexpected-end-tag-in-frameset', {'name': token['name']})

    class AfterFramesetPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              'noframes', self.startTagNoframes)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              'html', self.endTagHtml)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            pass

        def processCharacters(self, token):
            self.parser.parseError('unexpected-char-after-frameset')

        def startTagNoframes(self, token):
            return self.parser.phases['inHead'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError('unexpected-start-tag-after-frameset', {'name': token['name']})

        def endTagHtml(self, token):
            self.parser.phase = self.parser.phases['afterAfterFrameset']

        def endTagOther(self, token):
            self.parser.parseError('unexpected-end-tag-after-frameset', {'name': token['name']})

    class AfterAfterBodyPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml)])
            self.startTagHandler.default = self.startTagOther

        def processEOF(self):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processSpaceCharacters(self, token):
            return self.parser.phases['inBody'].processSpaceCharacters(token)

        def processCharacters(self, token):
            self.parser.parseError('expected-eof-but-got-char')
            self.parser.phase = self.parser.phases['inBody']
            return token

        def startTagHtml(self, token):
            return self.parser.phases['inBody'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError('expected-eof-but-got-start-tag', {'name': token['name']})
            self.parser.phase = self.parser.phases['inBody']
            return token

        def processEndTag(self, token):
            self.parser.parseError('expected-eof-but-got-end-tag', {'name': token['name']})
            self.parser.phase = self.parser.phases['inBody']
            return token

    class AfterAfterFramesetPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              'html', self.startTagHtml),
             (
              'noframes', self.startTagNoFrames)])
            self.startTagHandler.default = self.startTagOther

        def processEOF(self):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processSpaceCharacters(self, token):
            return self.parser.phases['inBody'].processSpaceCharacters(token)

        def processCharacters(self, token):
            self.parser.parseError('expected-eof-but-got-char')

        def startTagHtml(self, token):
            return self.parser.phases['inBody'].processStartTag(token)

        def startTagNoFrames(self, token):
            return self.parser.phases['inHead'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError('expected-eof-but-got-start-tag', {'name': token['name']})

        def processEndTag(self, token):
            self.parser.parseError('expected-eof-but-got-end-tag', {'name': token['name']})

    return {'initial':InitialPhase, 
     'beforeHtml':BeforeHtmlPhase, 
     'beforeHead':BeforeHeadPhase, 
     'inHead':InHeadPhase, 
     'inHeadNoscript':InHeadNoscriptPhase, 
     'afterHead':AfterHeadPhase, 
     'inBody':InBodyPhase, 
     'text':TextPhase, 
     'inTable':InTablePhase, 
     'inTableText':InTableTextPhase, 
     'inCaption':InCaptionPhase, 
     'inColumnGroup':InColumnGroupPhase, 
     'inTableBody':InTableBodyPhase, 
     'inRow':InRowPhase, 
     'inCell':InCellPhase, 
     'inSelect':InSelectPhase, 
     'inSelectInTable':InSelectInTablePhase, 
     'inForeignContent':InForeignContentPhase, 
     'afterBody':AfterBodyPhase, 
     'inFrameset':InFramesetPhase, 
     'afterFrameset':AfterFramesetPhase, 
     'afterAfterBody':AfterAfterBodyPhase, 
     'afterAfterFrameset':AfterAfterFramesetPhase}


def adjust_attributes(token, replacements):
    needs_adjustment = viewkeys(token['data']) & viewkeys(replacements)
    if needs_adjustment:
        token['data'] = OrderedDict((replacements.get(k, k), v) for k, v in token['data'].items())


def impliedTagToken(name, type='EndTag', attributes=None, selfClosing=False):
    if attributes is None:
        attributes = {}
    return {'type':tokenTypes[type], 
     'name':name,  'data':attributes,  'selfClosing':selfClosing}


class ParseError(Exception):
    __doc__ = 'Error in parsed document'