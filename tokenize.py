# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: tokenize.py
"""Tokenization help for Python programs.

tokenize(readline) is a generator that breaks a stream of bytes into
Python tokens.  It decodes the bytes according to PEP-0263 for
determining source file encoding.

It accepts a readline-like method which is called repeatedly to get the
next line of input (or b"" for EOF).  It generates 5-tuples with these
members:

    the token type (see token.py)
    the token (a string)
    the starting (row, column) indices of the token (a 2-tuple of ints)
    the ending (row, column) indices of the token (a 2-tuple of ints)
    the original line (string)

It is designed to match the working of the Python tokenizer exactly, except
that it produces COMMENT tokens for comments and gives type OP for all
operators.  Additionally, all token lists start with an ENCODING token
which tells you which encoding was used to decode the bytes stream.
"""
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = 'GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro, Raymond Hettinger, Trent Nelson, Michael Foord'
from builtins import open as _builtin_open
from codecs import lookup, BOM_UTF8
import collections
from io import TextIOWrapper
from itertools import chain
import itertools as _itertools, re, sys
from token import *
cookie_re = re.compile('^[ \\t\\f]*#.*?coding[:=][ \\t]*([-\\w.]+)', re.ASCII)
blank_re = re.compile(b'^[ \\t\\f]*(?:[#\\r\\n]|$)', re.ASCII)
import token
__all__ = token.__all__ + ['COMMENT', 'tokenize', 'detect_encoding',
 'NL', 'untokenize', 'ENCODING', 'TokenInfo']
del token
COMMENT = N_TOKENS
tok_name[COMMENT] = 'COMMENT'
NL = N_TOKENS + 1
tok_name[NL] = 'NL'
ENCODING = N_TOKENS + 2
tok_name[ENCODING] = 'ENCODING'
N_TOKENS += 3
EXACT_TOKEN_TYPES = {'(':LPAR, 
 ')':RPAR, 
 '[':LSQB, 
 ']':RSQB, 
 ':':COLON, 
 ',':COMMA, 
 ';':SEMI, 
 '+':PLUS, 
 '-':MINUS, 
 '*':STAR, 
 '/':SLASH, 
 '|':VBAR, 
 '&':AMPER, 
 '<':LESS, 
 '>':GREATER, 
 '=':EQUAL, 
 '.':DOT, 
 '%':PERCENT, 
 '{':LBRACE, 
 '}':RBRACE, 
 '==':EQEQUAL, 
 '!=':NOTEQUAL, 
 '<=':LESSEQUAL, 
 '>=':GREATEREQUAL, 
 '~':TILDE, 
 '^':CIRCUMFLEX, 
 '<<':LEFTSHIFT, 
 '>>':RIGHTSHIFT, 
 '**':DOUBLESTAR, 
 '+=':PLUSEQUAL, 
 '-=':MINEQUAL, 
 '*=':STAREQUAL, 
 '/=':SLASHEQUAL, 
 '%=':PERCENTEQUAL, 
 '&=':AMPEREQUAL, 
 '|=':VBAREQUAL, 
 '^=':CIRCUMFLEXEQUAL, 
 '<<=':LEFTSHIFTEQUAL, 
 '>>=':RIGHTSHIFTEQUAL, 
 '**=':DOUBLESTAREQUAL, 
 '//':DOUBLESLASH, 
 '//=':DOUBLESLASHEQUAL, 
 '@':AT, 
 '@=':ATEQUAL}

class TokenInfo(collections.namedtuple('TokenInfo', 'type string start end line')):

    def __repr__(self):
        annotated_type = '%d (%s)' % (self.type, tok_name[self.type])
        return 'TokenInfo(type=%s, string=%r, start=%r, end=%r, line=%r)' % self._replace(type=annotated_type)

    @property
    def exact_type(self):
        if self.type == OP:
            if self.string in EXACT_TOKEN_TYPES:
                return EXACT_TOKEN_TYPES[self.string]
        return self.type


def group(*choices):
    return '(' + '|'.join(choices) + ')'


def any(*choices):
    return group(*choices) + '*'


def maybe(*choices):
    return group(*choices) + '?'


Whitespace = '[ \\f\\t]*'
Comment = '#[^\\r\\n]*'
Ignore = Whitespace + any('\\\\\\r?\\n' + Whitespace) + maybe(Comment)
Name = '\\w+'
Hexnumber = '0[xX](?:_?[0-9a-fA-F])+'
Binnumber = '0[bB](?:_?[01])+'
Octnumber = '0[oO](?:_?[0-7])+'
Decnumber = '(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
Exponent = '[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = group('[0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?', '\\.[0-9](?:_?[0-9])*') + maybe(Exponent)
Expfloat = '[0-9](?:_?[0-9])*' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group('[0-9](?:_?[0-9])*[jJ]', Floatnumber + '[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)

def _all_string_prefixes():
    _valid_string_prefixes = [
     'b', 'r', 'u', 'f', 'br', 'fr']
    result = set([''])
    for prefix in _valid_string_prefixes:
        for t in _itertools.permutations(prefix):
            for u in (_itertools.product)(*[(c, c.upper()) for c in t]):
                result.add(''.join(u))

    return result


def _compile(expr):
    return re.compile(expr, re.UNICODE)


StringPrefix = group(*_all_string_prefixes())
Single = "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
Double = '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
Single3 = "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
Double3 = '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
Triple = group(StringPrefix + "'''", StringPrefix + '"""')
String = group(StringPrefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'", StringPrefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
Operator = group('\\*\\*=?', '>>=?', '<<=?', '!=', '//=?', '->', '[+\\-*/%&@|^=<>]=?', '~')
Bracket = '[][(){}]'
Special = group('\\r?\\n', '\\.\\.\\.', '[:;.,@]')
Funny = group(Operator, Bracket, Special)
PlainToken = group(Number, Funny, String, Name)
Token = Ignore + PlainToken
ContStr = group(StringPrefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*" + group("'", '\\\\\\r?\\n'), StringPrefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*' + group('"', '\\\\\\r?\\n'))
PseudoExtras = group('\\\\\\r?\\n|\\Z', Comment, Triple)
PseudoToken = Whitespace + group(PseudoExtras, Number, Funny, ContStr, Name)
endpats = {}
for _prefix in _all_string_prefixes():
    endpats[_prefix + "'"] = Single
    endpats[_prefix + '"'] = Double
    endpats[_prefix + "'''"] = Single3
    endpats[_prefix + '"""'] = Double3

single_quoted = set()
triple_quoted = set()
for t in _all_string_prefixes():
    for u in (t + '"', t + "'"):
        single_quoted.add(u)

    for u in (t + '"""', t + "'''"):
        triple_quoted.add(u)

tabsize = 8

class TokenError(Exception):
    pass


class StopTokenizing(Exception):
    pass


class Untokenizer:

    def __init__(self):
        self.tokens = []
        self.prev_row = 1
        self.prev_col = 0
        self.encoding = None

    def add_whitespace(self, start):
        row, col = start
        if row < self.prev_row or row == self.prev_row and col < self.prev_col:
            raise ValueError('start ({},{}) precedes previous end ({},{})'.format(row, col, self.prev_row, self.prev_col))
        row_offset = row - self.prev_row
        if row_offset:
            self.tokens.append('\\\n' * row_offset)
            self.prev_col = 0
        col_offset = col - self.prev_col
        if col_offset:
            self.tokens.append(' ' * col_offset)

    def untokenize(self, iterable):
        it = iter(iterable)
        indents = []
        startline = False
        for t in it:
            if len(t) == 2:
                self.compat(t, it)
                break
            tok_type, token, start, end, line = t
            if tok_type == ENCODING:
                self.encoding = token
            else:
                if tok_type == ENDMARKER:
                    break
                else:
                    if tok_type == INDENT:
                        indents.append(token)
                        continue
                    else:
                        if tok_type == DEDENT:
                            indents.pop()
                            self.prev_row, self.prev_col = end
                            continue
                        else:
                            if tok_type in (NEWLINE, NL):
                                startline = True
                            elif startline:
                                if indents:
                                    indent = indents[(-1)]
                                    if start[1] >= len(indent):
                                        self.tokens.append(indent)
                                        self.prev_col = len(indent)
                                    startline = False
                self.add_whitespace(start)
                self.tokens.append(token)
                self.prev_row, self.prev_col = end
                if tok_type in (NEWLINE, NL):
                    self.prev_row += 1
                    self.prev_col = 0

        return ''.join(self.tokens)

    def compat(self, token, iterable):
        indents = []
        toks_append = self.tokens.append
        startline = token[0] in (NEWLINE, NL)
        prevstring = False
        for tok in chain([token], iterable):
            toknum, tokval = tok[:2]
            if toknum == ENCODING:
                self.encoding = tokval
            else:
                if toknum in (NAME, NUMBER, ASYNC, AWAIT):
                    tokval += ' '
                else:
                    if toknum == STRING:
                        if prevstring:
                            tokval = ' ' + tokval
                        prevstring = True
                    else:
                        prevstring = False
                if toknum == INDENT:
                    indents.append(tokval)
                    continue
                else:
                    if toknum == DEDENT:
                        indents.pop()
                        continue
                    else:
                        if toknum in (NEWLINE, NL):
                            startline = True
                        else:
                            if startline:
                                if indents:
                                    toks_append(indents[(-1)])
                                    startline = False
                toks_append(tokval)


def untokenize(iterable):
    """Transform tokens back into Python source code.
    It returns a bytes object, encoded using the ENCODING
    token, which is the first token sequence output by tokenize.

    Each element returned by the iterable must be a token sequence
    with at least two elements, a token number and token value.  If
    only two tokens are passed, the resulting output is poor.

    Round-trip invariant for full input:
        Untokenized source will match input source exactly

    Round-trip invariant for limited input:
        # Output bytes will tokenize back to the input
        t1 = [tok[:2] for tok in tokenize(f.readline)]
        newcode = untokenize(t1)
        readline = BytesIO(newcode).readline
        t2 = [tok[:2] for tok in tokenize(readline)]
        assert t1 == t2
    """
    ut = Untokenizer()
    out = ut.untokenize(iterable)
    if ut.encoding is not None:
        out = out.encode(ut.encoding)
    return out


def _get_normal_name(orig_enc):
    """Imitates get_normal_name in tokenizer.c."""
    enc = orig_enc[:12].lower().replace('_', '-')
    if enc == 'utf-8' or enc.startswith('utf-8-'):
        return 'utf-8'
    else:
        if enc in ('latin-1', 'iso-8859-1', 'iso-latin-1') or enc.startswith(('latin-1-',
                                                                              'iso-8859-1-',
                                                                              'iso-latin-1-')):
            return 'iso-8859-1'
        return orig_enc


def detect_encoding(readline):
    """
    The detect_encoding() function is used to detect the encoding that should
    be used to decode a Python source file.  It requires one argument, readline,
    in the same way as the tokenize() generator.

    It will call readline a maximum of twice, and return the encoding used
    (as a string) and a list of any lines (left as bytes) it has read in.

    It detects the encoding from the presence of a utf-8 bom or an encoding
    cookie as specified in pep-0263.  If both a bom and a cookie are present,
    but disagree, a SyntaxError will be raised.  If the encoding cookie is an
    invalid charset, raise a SyntaxError.  Note that if a utf-8 bom is found,
    'utf-8-sig' is returned.

    If no encoding is specified, then the default of 'utf-8' will be returned.
    """
    try:
        filename = readline.__self__.name
    except AttributeError:
        filename = None

    bom_found = False
    encoding = None
    default = 'utf-8'

    def read_or_stop():
        try:
            return readline()
        except StopIteration:
            return b''

    def find_cookie(line):
        try:
            line_string = line.decode('utf-8')
        except UnicodeDecodeError:
            msg = 'invalid or missing encoding declaration'
            if filename is not None:
                msg = '{} for {!r}'.format(msg, filename)
            raise SyntaxError(msg)

        match = cookie_re.match(line_string)
        if not match:
            return
        else:
            encoding = _get_normal_name(match.group(1))
            try:
                codec = lookup(encoding)
            except LookupError:
                if filename is None:
                    msg = 'unknown encoding: ' + encoding
                else:
                    msg = 'unknown encoding for {!r}: {}'.format(filename, encoding)
                raise SyntaxError(msg)

            if bom_found:
                if encoding != 'utf-8':
                    if filename is None:
                        msg = 'encoding problem: utf-8'
                    else:
                        msg = 'encoding problem for {!r}: utf-8'.format(filename)
                    raise SyntaxError(msg)
                encoding += '-sig'
            return encoding

    first = read_or_stop()
    if first.startswith(BOM_UTF8):
        bom_found = True
        first = first[3:]
        default = 'utf-8-sig'
    if not first:
        return (
         default, [])
    encoding = find_cookie(first)
    if encoding:
        return (
         encoding, [first])
    if not blank_re.match(first):
        return (
         default, [first])
    second = read_or_stop()
    if not second:
        return (default, [first])
    else:
        encoding = find_cookie(second)
        if encoding:
            return (
             encoding, [first, second])
        return (default, [first, second])


def open(filename):
    """Open a file in read only mode using the encoding detected by
    detect_encoding().
    """
    buffer = _builtin_open(filename, 'rb')
    try:
        encoding, lines = detect_encoding(buffer.readline)
        buffer.seek(0)
        text = TextIOWrapper(buffer, encoding, line_buffering=True)
        text.mode = 'r'
        return text
    except:
        buffer.close()
        raise


def tokenize(readline):
    """
    The tokenize() generator requires one argument, readline, which
    must be a callable object which provides the same interface as the
    readline() method of built-in file objects.  Each call to the function
    should return one line of input as bytes.  Alternatively, readline
    can be a callable function terminating with StopIteration:
        readline = open(myfile, 'rb').__next__  # Example of alternate readline

    The generator produces 5-tuples with these members: the token type; the
    token string; a 2-tuple (srow, scol) of ints specifying the row and
    column where the token begins in the source; a 2-tuple (erow, ecol) of
    ints specifying the row and column where the token ends in the source;
    and the line on which the token was found.  The line passed is the
    logical line; continuation lines are included.

    The first token sequence will always be an ENCODING token
    which tells you which encoding was used to decode the bytes stream.
    """
    from itertools import chain, repeat
    encoding, consumed = detect_encoding(readline)
    rl_gen = iter(readline, b'')
    empty = repeat(b'')
    return _tokenize(chain(consumed, rl_gen, empty).__next__, encoding)


def _tokenize--- This code section failed: ---

 L. 493         0  LOAD_CONST               0
                2  DUP_TOP          
                4  STORE_FAST               'lnum'
                6  DUP_TOP          
                8  STORE_FAST               'parenlev'
               10  STORE_FAST               'continued'

 L. 494        12  LOAD_STR                 '0123456789'
               14  STORE_FAST               'numchars'

 L. 495        16  LOAD_CONST               ('', 0)
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'contstr'
               22  STORE_FAST               'needcont'

 L. 496        24  LOAD_CONST               None
               26  STORE_FAST               'contline'

 L. 497        28  LOAD_CONST               0
               30  BUILD_LIST_1          1 
               32  STORE_FAST               'indents'

 L. 500        34  LOAD_CONST               None
               36  STORE_FAST               'stashed'

 L. 501        38  LOAD_CONST               False
               40  STORE_FAST               'async_def'

 L. 502        42  LOAD_CONST               0
               44  STORE_FAST               'async_def_indent'

 L. 503        46  LOAD_CONST               False
               48  STORE_FAST               'async_def_nl'

 L. 505        50  LOAD_FAST                'encoding'
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
               56  POP_JUMP_IF_FALSE    88  'to 88'

 L. 506        58  LOAD_FAST                'encoding'
               60  LOAD_STR                 'utf-8-sig'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    70  'to 70'

 L. 508        66  LOAD_STR                 'utf-8'
               68  STORE_FAST               'encoding'
             70_0  COME_FROM            64  '64'

 L. 509        70  LOAD_GLOBAL              TokenInfo
               72  LOAD_GLOBAL              ENCODING
               74  LOAD_FAST                'encoding'
               76  LOAD_CONST               (0, 0)
               78  LOAD_CONST               (0, 0)
               80  LOAD_STR                 ''
               82  CALL_FUNCTION_5       5  '5 positional arguments'
               84  YIELD_VALUE      
               86  POP_TOP          
             88_0  COME_FROM            56  '56'

 L. 510        88  SETUP_LOOP         1908  'to 1908'

 L. 511        92  SETUP_EXCEPT        104  'to 104'

 L. 512        94  LOAD_FAST                'readline'
               96  CALL_FUNCTION_0       0  '0 positional arguments'
               98  STORE_FAST               'line'
              100  POP_BLOCK        
              102  JUMP_FORWARD        128  'to 128'
            104_0  COME_FROM_EXCEPT     92  '92'

 L. 513       104  DUP_TOP          
              106  LOAD_GLOBAL              StopIteration
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   126  'to 126'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 514       118  LOAD_CONST               b''
              120  STORE_FAST               'line'
              122  POP_EXCEPT       
              124  JUMP_FORWARD        128  'to 128'
              126  END_FINALLY      
            128_0  COME_FROM           124  '124'
            128_1  COME_FROM           102  '102'

 L. 516       128  LOAD_FAST                'encoding'
              130  LOAD_CONST               None
              132  COMPARE_OP               is-not
              134  POP_JUMP_IF_FALSE   146  'to 146'

 L. 517       136  LOAD_FAST                'line'
              138  LOAD_ATTR                decode
              140  LOAD_FAST                'encoding'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  STORE_FAST               'line'
            146_0  COME_FROM           134  '134'

 L. 518       146  LOAD_FAST                'lnum'
              148  LOAD_CONST               1
              150  INPLACE_ADD      
              152  STORE_FAST               'lnum'

 L. 519       154  LOAD_CONST               0
              156  LOAD_GLOBAL              len
              158  LOAD_FAST                'line'
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  ROT_TWO          
              164  STORE_FAST               'pos'
              166  STORE_FAST               'max'

 L. 521       168  LOAD_FAST                'contstr'
              170  POP_JUMP_IF_FALSE   376  'to 376'

 L. 522       174  LOAD_FAST                'line'
              176  POP_JUMP_IF_TRUE    188  'to 188'

 L. 523       178  LOAD_GLOBAL              TokenError
              180  LOAD_STR                 'EOF in multi-line string'
              182  LOAD_FAST                'strstart'
              184  CALL_FUNCTION_2       2  '2 positional arguments'
              186  RAISE_VARARGS_1       1  'exception'
            188_0  COME_FROM           176  '176'

 L. 524       188  LOAD_FAST                'endprog'
              190  LOAD_ATTR                match
              192  LOAD_FAST                'line'
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  STORE_FAST               'endmatch'

 L. 525       198  LOAD_FAST                'endmatch'
              200  POP_JUMP_IF_FALSE   270  'to 270'

 L. 526       204  LOAD_FAST                'endmatch'
              206  LOAD_ATTR                end
              208  LOAD_CONST               0
              210  CALL_FUNCTION_1       1  '1 positional argument'
              212  DUP_TOP          
              214  STORE_FAST               'pos'
              216  STORE_FAST               'end'

 L. 527       218  LOAD_GLOBAL              TokenInfo
              220  LOAD_GLOBAL              STRING
              222  LOAD_FAST                'contstr'
              224  LOAD_FAST                'line'
              226  LOAD_CONST               None
              228  LOAD_FAST                'end'
              230  BUILD_SLICE_2         2 
              232  BINARY_SUBSCR    
              234  BINARY_ADD       

 L. 528       236  LOAD_FAST                'strstart'
              238  LOAD_FAST                'lnum'
              240  LOAD_FAST                'end'
              242  BUILD_TUPLE_2         2 
              244  LOAD_FAST                'contline'
              246  LOAD_FAST                'line'
              248  BINARY_ADD       
              250  CALL_FUNCTION_5       5  '5 positional arguments'
              252  YIELD_VALUE      
              254  POP_TOP          

 L. 529       256  LOAD_CONST               ('', 0)
              258  UNPACK_SEQUENCE_2     2 
              260  STORE_FAST               'contstr'
              262  STORE_FAST               'needcont'

 L. 530       264  LOAD_CONST               None
              266  STORE_FAST               'contline'
              268  JUMP_FORWARD        372  'to 372'
              270  ELSE                     '372'

 L. 531       270  LOAD_FAST                'needcont'
              272  POP_JUMP_IF_FALSE   354  'to 354'
              276  LOAD_FAST                'line'
              278  LOAD_CONST               -2
              280  LOAD_CONST               None
              282  BUILD_SLICE_2         2 
              284  BINARY_SUBSCR    
              286  LOAD_STR                 '\\\n'
              288  COMPARE_OP               !=
              290  POP_JUMP_IF_FALSE   354  'to 354'
              294  LOAD_FAST                'line'
              296  LOAD_CONST               -3
              298  LOAD_CONST               None
              300  BUILD_SLICE_2         2 
              302  BINARY_SUBSCR    
              304  LOAD_STR                 '\\\r\n'
              306  COMPARE_OP               !=
              308  POP_JUMP_IF_FALSE   354  'to 354'

 L. 532       312  LOAD_GLOBAL              TokenInfo
              314  LOAD_GLOBAL              ERRORTOKEN
              316  LOAD_FAST                'contstr'
              318  LOAD_FAST                'line'
              320  BINARY_ADD       

 L. 533       322  LOAD_FAST                'strstart'
              324  LOAD_FAST                'lnum'
              326  LOAD_GLOBAL              len
              328  LOAD_FAST                'line'
              330  CALL_FUNCTION_1       1  '1 positional argument'
              332  BUILD_TUPLE_2         2 
              334  LOAD_FAST                'contline'
              336  CALL_FUNCTION_5       5  '5 positional arguments'
              338  YIELD_VALUE      
              340  POP_TOP          

 L. 534       342  LOAD_STR                 ''
              344  STORE_FAST               'contstr'

 L. 535       346  LOAD_CONST               None
              348  STORE_FAST               'contline'

 L. 536       350  CONTINUE             92  'to 92'
              352  JUMP_FORWARD        372  'to 372'
            354_0  COME_FROM           290  '290'
            354_1  COME_FROM           272  '272'

 L. 538       354  LOAD_FAST                'contstr'
              356  LOAD_FAST                'line'
              358  BINARY_ADD       
              360  STORE_FAST               'contstr'

 L. 539       362  LOAD_FAST                'contline'
              364  LOAD_FAST                'line'
              366  BINARY_ADD       
              368  STORE_FAST               'contline'

 L. 540       370  CONTINUE             92  'to 92'
            372_0  COME_FROM           352  '352'
            372_1  COME_FROM           268  '268'
              372  JUMP_FORWARD        952  'to 952'
              376  ELSE                     '952'

 L. 542       376  LOAD_FAST                'parenlev'
              378  LOAD_CONST               0
              380  COMPARE_OP               ==
              382  POP_JUMP_IF_FALSE   928  'to 928'
              386  LOAD_FAST                'continued'
              388  UNARY_NOT        
              390  POP_JUMP_IF_FALSE   928  'to 928'

 L. 543       394  LOAD_FAST                'line'
              396  POP_JUMP_IF_TRUE    402  'to 402'

 L. 543       400  BREAK_LOOP       
            402_0  COME_FROM           396  '396'

 L. 544       402  LOAD_CONST               0
              404  STORE_FAST               'column'

 L. 545       406  SETUP_LOOP          510  'to 510'
              408  LOAD_FAST                'pos'
              410  LOAD_FAST                'max'
              412  COMPARE_OP               <
              414  POP_JUMP_IF_FALSE   508  'to 508'

 L. 546       418  LOAD_FAST                'line'
              420  LOAD_FAST                'pos'
              422  BINARY_SUBSCR    
              424  LOAD_STR                 ' '
              426  COMPARE_OP               ==
              428  POP_JUMP_IF_FALSE   442  'to 442'

 L. 547       432  LOAD_FAST                'column'
              434  LOAD_CONST               1
              436  INPLACE_ADD      
              438  STORE_FAST               'column'
              440  JUMP_FORWARD        496  'to 496'
              442  ELSE                     '496'

 L. 548       442  LOAD_FAST                'line'
              444  LOAD_FAST                'pos'
              446  BINARY_SUBSCR    
              448  LOAD_STR                 '\t'
              450  COMPARE_OP               ==
              452  POP_JUMP_IF_FALSE   474  'to 474'

 L. 549       456  LOAD_FAST                'column'
              458  LOAD_GLOBAL              tabsize
              460  BINARY_FLOOR_DIVIDE
              462  LOAD_CONST               1
              464  BINARY_ADD       
              466  LOAD_GLOBAL              tabsize
              468  BINARY_MULTIPLY  
              470  STORE_FAST               'column'
              472  JUMP_FORWARD        496  'to 496'
              474  ELSE                     '496'

 L. 550       474  LOAD_FAST                'line'
              476  LOAD_FAST                'pos'
              478  BINARY_SUBSCR    
              480  LOAD_STR                 '\x0c'
              482  COMPARE_OP               ==
              484  POP_JUMP_IF_FALSE   494  'to 494'

 L. 551       488  LOAD_CONST               0
              490  STORE_FAST               'column'
              492  JUMP_FORWARD        496  'to 496'
              494  ELSE                     '496'

 L. 553       494  BREAK_LOOP       
            496_0  COME_FROM           492  '492'
            496_1  COME_FROM           472  '472'
            496_2  COME_FROM           440  '440'

 L. 554       496  LOAD_FAST                'pos'
              498  LOAD_CONST               1
              500  INPLACE_ADD      
              502  STORE_FAST               'pos'
              504  JUMP_BACK           408  'to 408'
            508_0  COME_FROM           414  '414'
              508  POP_BLOCK        
            510_0  COME_FROM_LOOP      406  '406'

 L. 555       510  LOAD_FAST                'pos'
              512  LOAD_FAST                'max'
              514  COMPARE_OP               ==
              516  POP_JUMP_IF_FALSE   522  'to 522'

 L. 556       520  BREAK_LOOP       
            522_0  COME_FROM           516  '516'

 L. 558       522  LOAD_FAST                'line'
              524  LOAD_FAST                'pos'
              526  BINARY_SUBSCR    
              528  LOAD_STR                 '#\r\n'
              530  COMPARE_OP               in
              532  POP_JUMP_IF_FALSE   710  'to 710'

 L. 559       536  LOAD_FAST                'line'
              538  LOAD_FAST                'pos'
              540  BINARY_SUBSCR    
              542  LOAD_STR                 '#'
              544  COMPARE_OP               ==
              546  POP_JUMP_IF_FALSE   654  'to 654'

 L. 560       550  LOAD_FAST                'line'
              552  LOAD_FAST                'pos'
              554  LOAD_CONST               None
              556  BUILD_SLICE_2         2 
              558  BINARY_SUBSCR    
              560  LOAD_ATTR                rstrip
              562  LOAD_STR                 '\r\n'
              564  CALL_FUNCTION_1       1  '1 positional argument'
              566  STORE_FAST               'comment_token'

 L. 561       568  LOAD_FAST                'pos'
              570  LOAD_GLOBAL              len
              572  LOAD_FAST                'comment_token'
              574  CALL_FUNCTION_1       1  '1 positional argument'
              576  BINARY_ADD       
              578  STORE_FAST               'nl_pos'

 L. 562       580  LOAD_GLOBAL              TokenInfo
              582  LOAD_GLOBAL              COMMENT
              584  LOAD_FAST                'comment_token'

 L. 563       586  LOAD_FAST                'lnum'
              588  LOAD_FAST                'pos'
              590  BUILD_TUPLE_2         2 
              592  LOAD_FAST                'lnum'
              594  LOAD_FAST                'pos'
              596  LOAD_GLOBAL              len
              598  LOAD_FAST                'comment_token'
              600  CALL_FUNCTION_1       1  '1 positional argument'
              602  BINARY_ADD       
              604  BUILD_TUPLE_2         2 
              606  LOAD_FAST                'line'
              608  CALL_FUNCTION_5       5  '5 positional arguments'
              610  YIELD_VALUE      
              612  POP_TOP          

 L. 564       614  LOAD_GLOBAL              TokenInfo
              616  LOAD_GLOBAL              NL
              618  LOAD_FAST                'line'
              620  LOAD_FAST                'nl_pos'
              622  LOAD_CONST               None
              624  BUILD_SLICE_2         2 
              626  BINARY_SUBSCR    

 L. 565       628  LOAD_FAST                'lnum'
              630  LOAD_FAST                'nl_pos'
              632  BUILD_TUPLE_2         2 
              634  LOAD_FAST                'lnum'
              636  LOAD_GLOBAL              len
              638  LOAD_FAST                'line'
              640  CALL_FUNCTION_1       1  '1 positional argument'
              642  BUILD_TUPLE_2         2 
              644  LOAD_FAST                'line'
              646  CALL_FUNCTION_5       5  '5 positional arguments'
              648  YIELD_VALUE      
              650  POP_TOP          
              652  JUMP_BACK            92  'to 92'
              654  ELSE                     '708'

 L. 567       654  LOAD_GLOBAL              TokenInfo
              656  LOAD_GLOBAL              NL
              658  LOAD_GLOBAL              COMMENT
              660  BUILD_TUPLE_2         2 
              662  LOAD_FAST                'line'
              664  LOAD_FAST                'pos'
              666  BINARY_SUBSCR    
              668  LOAD_STR                 '#'
              670  COMPARE_OP               ==
              672  BINARY_SUBSCR    
              674  LOAD_FAST                'line'
              676  LOAD_FAST                'pos'
              678  LOAD_CONST               None
              680  BUILD_SLICE_2         2 
              682  BINARY_SUBSCR    

 L. 568       684  LOAD_FAST                'lnum'
              686  LOAD_FAST                'pos'
              688  BUILD_TUPLE_2         2 
              690  LOAD_FAST                'lnum'
              692  LOAD_GLOBAL              len
              694  LOAD_FAST                'line'
              696  CALL_FUNCTION_1       1  '1 positional argument'
              698  BUILD_TUPLE_2         2 
              700  LOAD_FAST                'line'
              702  CALL_FUNCTION_5       5  '5 positional arguments'
              704  YIELD_VALUE      
              706  POP_TOP          

 L. 569       708  CONTINUE             92  'to 92'

 L. 571       710  LOAD_FAST                'column'
              712  LOAD_FAST                'indents'
              714  LOAD_CONST               -1
              716  BINARY_SUBSCR    
              718  COMPARE_OP               >
              720  POP_JUMP_IF_FALSE   768  'to 768'

 L. 572       724  LOAD_FAST                'indents'
              726  LOAD_ATTR                append
              728  LOAD_FAST                'column'
              730  CALL_FUNCTION_1       1  '1 positional argument'
              732  POP_TOP          

 L. 573       734  LOAD_GLOBAL              TokenInfo
              736  LOAD_GLOBAL              INDENT
              738  LOAD_FAST                'line'
              740  LOAD_CONST               None
              742  LOAD_FAST                'pos'
              744  BUILD_SLICE_2         2 
              746  BINARY_SUBSCR    
              748  LOAD_FAST                'lnum'
              750  LOAD_CONST               0
              752  BUILD_TUPLE_2         2 
              754  LOAD_FAST                'lnum'
              756  LOAD_FAST                'pos'
              758  BUILD_TUPLE_2         2 
              760  LOAD_FAST                'line'
              762  CALL_FUNCTION_5       5  '5 positional arguments'
              764  YIELD_VALUE      
              766  POP_TOP          
            768_0  COME_FROM           720  '720'

 L. 574       768  SETUP_LOOP          888  'to 888'
              770  LOAD_FAST                'column'
              772  LOAD_FAST                'indents'
              774  LOAD_CONST               -1
              776  BINARY_SUBSCR    
              778  COMPARE_OP               <
              780  POP_JUMP_IF_FALSE   886  'to 886'

 L. 575       784  LOAD_FAST                'column'
              786  LOAD_FAST                'indents'
              788  COMPARE_OP               not-in
              790  POP_JUMP_IF_FALSE   812  'to 812'

 L. 576       794  LOAD_GLOBAL              IndentationError

 L. 577       796  LOAD_STR                 'unindent does not match any outer indentation level'

 L. 578       798  LOAD_STR                 '<tokenize>'
              800  LOAD_FAST                'lnum'
              802  LOAD_FAST                'pos'
              804  LOAD_FAST                'line'
              806  BUILD_TUPLE_4         4 
              808  CALL_FUNCTION_2       2  '2 positional arguments'
              810  RAISE_VARARGS_1       1  'exception'
            812_0  COME_FROM           790  '790'

 L. 579       812  LOAD_FAST                'indents'
              814  LOAD_CONST               None
              816  LOAD_CONST               -1
              818  BUILD_SLICE_2         2 
              820  BINARY_SUBSCR    
              822  STORE_FAST               'indents'

 L. 581       824  LOAD_FAST                'async_def'
              826  POP_JUMP_IF_FALSE   856  'to 856'
              830  LOAD_FAST                'async_def_indent'
              832  LOAD_FAST                'indents'
              834  LOAD_CONST               -1
              836  BINARY_SUBSCR    
              838  COMPARE_OP               >=
              840  POP_JUMP_IF_FALSE   856  'to 856'

 L. 582       844  LOAD_CONST               False
              846  STORE_FAST               'async_def'

 L. 583       848  LOAD_CONST               False
              850  STORE_FAST               'async_def_nl'

 L. 584       852  LOAD_CONST               0
              854  STORE_FAST               'async_def_indent'
            856_0  COME_FROM           840  '840'
            856_1  COME_FROM           826  '826'

 L. 586       856  LOAD_GLOBAL              TokenInfo
              858  LOAD_GLOBAL              DEDENT
              860  LOAD_STR                 ''
              862  LOAD_FAST                'lnum'
              864  LOAD_FAST                'pos'
              866  BUILD_TUPLE_2         2 
              868  LOAD_FAST                'lnum'
              870  LOAD_FAST                'pos'
              872  BUILD_TUPLE_2         2 
              874  LOAD_FAST                'line'
              876  CALL_FUNCTION_5       5  '5 positional arguments'
              878  YIELD_VALUE      
              880  POP_TOP          
              882  JUMP_BACK           770  'to 770'
            886_0  COME_FROM           780  '780'
              886  POP_BLOCK        
            888_0  COME_FROM_LOOP      768  '768'

 L. 588       888  LOAD_FAST                'async_def'
              890  POP_JUMP_IF_FALSE   952  'to 952'
              894  LOAD_FAST                'async_def_nl'
              896  POP_JUMP_IF_FALSE   952  'to 952'
              900  LOAD_FAST                'async_def_indent'
              902  LOAD_FAST                'indents'
              904  LOAD_CONST               -1
              906  BINARY_SUBSCR    
              908  COMPARE_OP               >=
              910  POP_JUMP_IF_FALSE   952  'to 952'

 L. 589       914  LOAD_CONST               False
              916  STORE_FAST               'async_def'

 L. 590       918  LOAD_CONST               False
              920  STORE_FAST               'async_def_nl'

 L. 591       922  LOAD_CONST               0
              924  STORE_FAST               'async_def_indent'
              926  JUMP_FORWARD        952  'to 952'
            928_0  COME_FROM           382  '382'

 L. 594       928  LOAD_FAST                'line'
              930  POP_JUMP_IF_TRUE    948  'to 948'

 L. 595       934  LOAD_GLOBAL              TokenError
              936  LOAD_STR                 'EOF in multi-line statement'
              938  LOAD_FAST                'lnum'
              940  LOAD_CONST               0
              942  BUILD_TUPLE_2         2 
              944  CALL_FUNCTION_2       2  '2 positional arguments'
              946  RAISE_VARARGS_1       1  'exception'
            948_0  COME_FROM           930  '930'

 L. 596       948  LOAD_CONST               0
              950  STORE_FAST               'continued'
            952_0  COME_FROM           926  '926'
            952_1  COME_FROM           910  '910'
            952_2  COME_FROM           896  '896'
            952_3  COME_FROM           890  '890'
            952_4  COME_FROM           372  '372'

 L. 598       952  SETUP_LOOP         1904  'to 1904'
              956  LOAD_FAST                'pos'
              958  LOAD_FAST                'max'
              960  COMPARE_OP               <
              962  POP_JUMP_IF_FALSE  1902  'to 1902'

 L. 599       966  LOAD_GLOBAL              _compile
              968  LOAD_GLOBAL              PseudoToken
              970  CALL_FUNCTION_1       1  '1 positional argument'
              972  LOAD_ATTR                match
              974  LOAD_FAST                'line'
              976  LOAD_FAST                'pos'
              978  CALL_FUNCTION_2       2  '2 positional arguments'
              980  STORE_FAST               'pseudomatch'

 L. 600       982  LOAD_FAST                'pseudomatch'
              984  POP_JUMP_IF_FALSE  1856  'to 1856'

 L. 601       988  LOAD_FAST                'pseudomatch'
              990  LOAD_ATTR                span
              992  LOAD_CONST               1
              994  CALL_FUNCTION_1       1  '1 positional argument'
              996  UNPACK_SEQUENCE_2     2 
              998  STORE_FAST               'start'
             1000  STORE_FAST               'end'

 L. 602      1002  LOAD_FAST                'lnum'
             1004  LOAD_FAST                'start'
             1006  BUILD_TUPLE_2         2 
             1008  LOAD_FAST                'lnum'
             1010  LOAD_FAST                'end'
             1012  BUILD_TUPLE_2         2 
             1014  LOAD_FAST                'end'
             1016  ROT_THREE        
             1018  ROT_TWO          
             1020  STORE_FAST               'spos'
             1022  STORE_FAST               'epos'
             1024  STORE_FAST               'pos'

 L. 603      1026  LOAD_FAST                'start'
             1028  LOAD_FAST                'end'
             1030  COMPARE_OP               ==
             1032  POP_JUMP_IF_FALSE  1040  'to 1040'

 L. 604      1036  CONTINUE            956  'to 956'
             1040  ELSE                     '1854'

 L. 605      1040  LOAD_FAST                'line'
             1042  LOAD_FAST                'start'
             1044  LOAD_FAST                'end'
             1046  BUILD_SLICE_2         2 
             1048  BINARY_SUBSCR    
             1050  LOAD_FAST                'line'
             1052  LOAD_FAST                'start'
             1054  BINARY_SUBSCR    
             1056  ROT_TWO          
             1058  STORE_FAST               'token'
             1060  STORE_FAST               'initial'

 L. 607      1062  LOAD_FAST                'initial'
             1064  LOAD_FAST                'numchars'
             1066  COMPARE_OP               in
             1068  POP_JUMP_IF_TRUE   1102  'to 1102'

 L. 608      1072  LOAD_FAST                'initial'
             1074  LOAD_STR                 '.'
             1076  COMPARE_OP               ==
             1078  POP_JUMP_IF_FALSE  1124  'to 1124'
             1082  LOAD_FAST                'token'
             1084  LOAD_STR                 '.'
             1086  COMPARE_OP               !=
             1088  POP_JUMP_IF_FALSE  1124  'to 1124'
             1092  LOAD_FAST                'token'
             1094  LOAD_STR                 '...'
             1096  COMPARE_OP               !=
           1098_0  COME_FROM          1088  '1088'
           1098_1  COME_FROM          1078  '1078'
           1098_2  COME_FROM          1068  '1068'
             1098  POP_JUMP_IF_FALSE  1124  'to 1124'

 L. 609      1102  LOAD_GLOBAL              TokenInfo
             1104  LOAD_GLOBAL              NUMBER
             1106  LOAD_FAST                'token'
             1108  LOAD_FAST                'spos'
             1110  LOAD_FAST                'epos'
             1112  LOAD_FAST                'line'
             1114  CALL_FUNCTION_5       5  '5 positional arguments'
             1116  YIELD_VALUE      
             1118  POP_TOP          
             1120  JUMP_ABSOLUTE      1898  'to 1898'
             1124  ELSE                     '1854'

 L. 610      1124  LOAD_FAST                'initial'
             1126  LOAD_STR                 '\r\n'
             1128  COMPARE_OP               in
             1130  POP_JUMP_IF_FALSE  1212  'to 1212'

 L. 611      1134  LOAD_FAST                'stashed'
             1136  POP_JUMP_IF_FALSE  1150  'to 1150'

 L. 612      1140  LOAD_FAST                'stashed'
             1142  YIELD_VALUE      
             1144  POP_TOP          

 L. 613      1146  LOAD_CONST               None
             1148  STORE_FAST               'stashed'
           1150_0  COME_FROM          1136  '1136'

 L. 614      1150  LOAD_FAST                'parenlev'
             1152  LOAD_CONST               0
             1154  COMPARE_OP               >
             1156  POP_JUMP_IF_FALSE  1180  'to 1180'

 L. 615      1160  LOAD_GLOBAL              TokenInfo
             1162  LOAD_GLOBAL              NL
             1164  LOAD_FAST                'token'
             1166  LOAD_FAST                'spos'
             1168  LOAD_FAST                'epos'
             1170  LOAD_FAST                'line'
             1172  CALL_FUNCTION_5       5  '5 positional arguments'
             1174  YIELD_VALUE      
             1176  POP_TOP          
             1178  JUMP_FORWARD       1208  'to 1208'
             1180  ELSE                     '1208'

 L. 617      1180  LOAD_GLOBAL              TokenInfo
             1182  LOAD_GLOBAL              NEWLINE
             1184  LOAD_FAST                'token'
             1186  LOAD_FAST                'spos'
             1188  LOAD_FAST                'epos'
             1190  LOAD_FAST                'line'
             1192  CALL_FUNCTION_5       5  '5 positional arguments'
             1194  YIELD_VALUE      
             1196  POP_TOP          

 L. 618      1198  LOAD_FAST                'async_def'
             1200  POP_JUMP_IF_FALSE  1854  'to 1854'

 L. 619      1204  LOAD_CONST               True
             1206  STORE_FAST               'async_def_nl'
           1208_0  COME_FROM          1178  '1178'
             1208  JUMP_ABSOLUTE      1898  'to 1898'
             1212  ELSE                     '1854'

 L. 621      1212  LOAD_FAST                'initial'
             1214  LOAD_STR                 '#'
             1216  COMPARE_OP               ==
             1218  POP_JUMP_IF_FALSE  1278  'to 1278'

 L. 622      1222  LOAD_FAST                'token'
             1224  LOAD_ATTR                endswith
             1226  LOAD_STR                 '\n'
             1228  CALL_FUNCTION_1       1  '1 positional argument'
             1230  UNARY_NOT        
             1232  POP_JUMP_IF_TRUE   1240  'to 1240'
             1236  LOAD_ASSERT              AssertionError
             1238  RAISE_VARARGS_1       1  'exception'
           1240_0  COME_FROM          1232  '1232'

 L. 623      1240  LOAD_FAST                'stashed'
             1242  POP_JUMP_IF_FALSE  1256  'to 1256'

 L. 624      1246  LOAD_FAST                'stashed'
             1248  YIELD_VALUE      
             1250  POP_TOP          

 L. 625      1252  LOAD_CONST               None
             1254  STORE_FAST               'stashed'
           1256_0  COME_FROM          1242  '1242'

 L. 626      1256  LOAD_GLOBAL              TokenInfo
             1258  LOAD_GLOBAL              COMMENT
             1260  LOAD_FAST                'token'
             1262  LOAD_FAST                'spos'
             1264  LOAD_FAST                'epos'
             1266  LOAD_FAST                'line'
             1268  CALL_FUNCTION_5       5  '5 positional arguments'
             1270  YIELD_VALUE      
             1272  POP_TOP          
             1274  JUMP_ABSOLUTE      1898  'to 1898'
             1278  ELSE                     '1854'

 L. 628      1278  LOAD_FAST                'token'
             1280  LOAD_GLOBAL              triple_quoted
             1282  COMPARE_OP               in
             1284  POP_JUMP_IF_FALSE  1394  'to 1394'

 L. 629      1288  LOAD_GLOBAL              _compile
             1290  LOAD_GLOBAL              endpats
             1292  LOAD_FAST                'token'
             1294  BINARY_SUBSCR    
             1296  CALL_FUNCTION_1       1  '1 positional argument'
             1298  STORE_FAST               'endprog'

 L. 630      1300  LOAD_FAST                'endprog'
             1302  LOAD_ATTR                match
             1304  LOAD_FAST                'line'
             1306  LOAD_FAST                'pos'
             1308  CALL_FUNCTION_2       2  '2 positional arguments'
             1310  STORE_FAST               'endmatch'

 L. 631      1312  LOAD_FAST                'endmatch'
             1314  POP_JUMP_IF_FALSE  1364  'to 1364'

 L. 632      1318  LOAD_FAST                'endmatch'
             1320  LOAD_ATTR                end
             1322  LOAD_CONST               0
             1324  CALL_FUNCTION_1       1  '1 positional argument'
             1326  STORE_FAST               'pos'

 L. 633      1328  LOAD_FAST                'line'
             1330  LOAD_FAST                'start'
             1332  LOAD_FAST                'pos'
             1334  BUILD_SLICE_2         2 
             1336  BINARY_SUBSCR    
             1338  STORE_FAST               'token'

 L. 634      1340  LOAD_GLOBAL              TokenInfo
             1342  LOAD_GLOBAL              STRING
             1344  LOAD_FAST                'token'
             1346  LOAD_FAST                'spos'
             1348  LOAD_FAST                'lnum'
             1350  LOAD_FAST                'pos'
             1352  BUILD_TUPLE_2         2 
             1354  LOAD_FAST                'line'
             1356  CALL_FUNCTION_5       5  '5 positional arguments'
             1358  YIELD_VALUE      
             1360  POP_TOP          
             1362  JUMP_FORWARD       1390  'to 1390'
             1364  ELSE                     '1390'

 L. 636      1364  LOAD_FAST                'lnum'
             1366  LOAD_FAST                'start'
             1368  BUILD_TUPLE_2         2 
             1370  STORE_FAST               'strstart'

 L. 637      1372  LOAD_FAST                'line'
             1374  LOAD_FAST                'start'
             1376  LOAD_CONST               None
             1378  BUILD_SLICE_2         2 
             1380  BINARY_SUBSCR    
             1382  STORE_FAST               'contstr'

 L. 638      1384  LOAD_FAST                'line'
             1386  STORE_FAST               'contline'

 L. 639      1388  BREAK_LOOP       
           1390_0  COME_FROM          1362  '1362'
             1390  JUMP_ABSOLUTE      1898  'to 1898'
             1394  ELSE                     '1854'

 L. 651      1394  LOAD_FAST                'initial'
             1396  LOAD_GLOBAL              single_quoted
             1398  COMPARE_OP               in
             1400  POP_JUMP_IF_TRUE   1440  'to 1440'

 L. 652      1404  LOAD_FAST                'token'
             1406  LOAD_CONST               None
             1408  LOAD_CONST               2
             1410  BUILD_SLICE_2         2 
             1412  BINARY_SUBSCR    
             1414  LOAD_GLOBAL              single_quoted
             1416  COMPARE_OP               in
             1418  POP_JUMP_IF_TRUE   1440  'to 1440'

 L. 653      1422  LOAD_FAST                'token'
             1424  LOAD_CONST               None
             1426  LOAD_CONST               3
             1428  BUILD_SLICE_2         2 
             1430  BINARY_SUBSCR    
             1432  LOAD_GLOBAL              single_quoted
             1434  COMPARE_OP               in
           1436_0  COME_FROM          1418  '1418'
           1436_1  COME_FROM          1400  '1400'
             1436  POP_JUMP_IF_FALSE  1556  'to 1556'

 L. 654      1440  LOAD_FAST                'token'
             1442  LOAD_CONST               -1
             1444  BINARY_SUBSCR    
             1446  LOAD_STR                 '\n'
             1448  COMPARE_OP               ==
             1450  POP_JUMP_IF_FALSE  1534  'to 1534'

 L. 655      1454  LOAD_FAST                'lnum'
             1456  LOAD_FAST                'start'
             1458  BUILD_TUPLE_2         2 
             1460  STORE_FAST               'strstart'

 L. 662      1462  LOAD_GLOBAL              _compile
             1464  LOAD_GLOBAL              endpats
             1466  LOAD_ATTR                get
             1468  LOAD_FAST                'initial'
             1470  CALL_FUNCTION_1       1  '1 positional argument'
             1472  JUMP_IF_TRUE_OR_POP  1504  'to 1504'

 L. 663      1476  LOAD_GLOBAL              endpats
             1478  LOAD_ATTR                get
             1480  LOAD_FAST                'token'
             1482  LOAD_CONST               1
             1484  BINARY_SUBSCR    
             1486  CALL_FUNCTION_1       1  '1 positional argument'
             1488  JUMP_IF_TRUE_OR_POP  1504  'to 1504'

 L. 664      1492  LOAD_GLOBAL              endpats
             1494  LOAD_ATTR                get
             1496  LOAD_FAST                'token'
             1498  LOAD_CONST               2
             1500  BINARY_SUBSCR    
             1502  CALL_FUNCTION_1       1  '1 positional argument'
           1504_0  COME_FROM          1488  '1488'
           1504_1  COME_FROM          1472  '1472'
             1504  CALL_FUNCTION_1       1  '1 positional argument'
             1506  STORE_FAST               'endprog'

 L. 665      1508  LOAD_FAST                'line'
             1510  LOAD_FAST                'start'
             1512  LOAD_CONST               None
             1514  BUILD_SLICE_2         2 
             1516  BINARY_SUBSCR    
             1518  LOAD_CONST               1
             1520  ROT_TWO          
             1522  STORE_FAST               'contstr'
             1524  STORE_FAST               'needcont'

 L. 666      1526  LOAD_FAST                'line'
             1528  STORE_FAST               'contline'

 L. 667      1530  BREAK_LOOP       
             1532  JUMP_FORWARD       1552  'to 1552'
             1534  ELSE                     '1552'

 L. 669      1534  LOAD_GLOBAL              TokenInfo
             1536  LOAD_GLOBAL              STRING
             1538  LOAD_FAST                'token'
             1540  LOAD_FAST                'spos'
             1542  LOAD_FAST                'epos'
             1544  LOAD_FAST                'line'
             1546  CALL_FUNCTION_5       5  '5 positional arguments'
             1548  YIELD_VALUE      
             1550  POP_TOP          
           1552_0  COME_FROM          1532  '1532'
             1552  JUMP_ABSOLUTE      1898  'to 1898'
             1556  ELSE                     '1854'

 L. 671      1556  LOAD_FAST                'initial'
             1558  LOAD_ATTR                isidentifier
             1560  CALL_FUNCTION_0       0  '0 positional arguments'
             1562  POP_JUMP_IF_FALSE  1766  'to 1766'

 L. 672      1566  LOAD_FAST                'token'
             1568  LOAD_CONST               ('async', 'await')
             1570  COMPARE_OP               in
             1572  POP_JUMP_IF_FALSE  1618  'to 1618'

 L. 673      1576  LOAD_FAST                'async_def'
             1578  POP_JUMP_IF_FALSE  1618  'to 1618'

 L. 674      1582  LOAD_GLOBAL              TokenInfo

 L. 675      1584  LOAD_FAST                'token'
             1586  LOAD_STR                 'async'
             1588  COMPARE_OP               ==
             1590  POP_JUMP_IF_FALSE  1598  'to 1598'
             1594  LOAD_GLOBAL              ASYNC
             1596  JUMP_FORWARD       1600  'to 1600'
             1598  ELSE                     '1600'
             1598  LOAD_GLOBAL              AWAIT
           1600_0  COME_FROM          1596  '1596'

 L. 676      1600  LOAD_FAST                'token'
             1602  LOAD_FAST                'spos'
             1604  LOAD_FAST                'epos'
             1606  LOAD_FAST                'line'
             1608  CALL_FUNCTION_5       5  '5 positional arguments'
             1610  YIELD_VALUE      
             1612  POP_TOP          

 L. 677      1614  CONTINUE            956  'to 956'
           1618_0  COME_FROM          1572  '1572'

 L. 679      1618  LOAD_GLOBAL              TokenInfo
             1620  LOAD_GLOBAL              NAME
             1622  LOAD_FAST                'token'
             1624  LOAD_FAST                'spos'
             1626  LOAD_FAST                'epos'
             1628  LOAD_FAST                'line'
             1630  CALL_FUNCTION_5       5  '5 positional arguments'
             1632  STORE_FAST               'tok'

 L. 680      1634  LOAD_FAST                'token'
             1636  LOAD_STR                 'async'
             1638  COMPARE_OP               ==
             1640  POP_JUMP_IF_FALSE  1660  'to 1660'
             1644  LOAD_FAST                'stashed'
             1646  UNARY_NOT        
             1648  POP_JUMP_IF_FALSE  1660  'to 1660'

 L. 681      1652  LOAD_FAST                'tok'
             1654  STORE_FAST               'stashed'

 L. 682      1656  CONTINUE            956  'to 956'
           1660_0  COME_FROM          1640  '1640'

 L. 684      1660  LOAD_FAST                'token'
             1662  LOAD_STR                 'def'
             1664  COMPARE_OP               ==
             1666  POP_JUMP_IF_FALSE  1742  'to 1742'

 L. 685      1670  LOAD_FAST                'stashed'
             1672  POP_JUMP_IF_FALSE  1742  'to 1742'

 L. 686      1676  LOAD_FAST                'stashed'
             1678  LOAD_ATTR                type
             1680  LOAD_GLOBAL              NAME
             1682  COMPARE_OP               ==
             1684  POP_JUMP_IF_FALSE  1742  'to 1742'

 L. 687      1688  LOAD_FAST                'stashed'
             1690  LOAD_ATTR                string
             1692  LOAD_STR                 'async'
             1694  COMPARE_OP               ==
             1696  POP_JUMP_IF_FALSE  1742  'to 1742'

 L. 689      1700  LOAD_CONST               True
             1702  STORE_FAST               'async_def'

 L. 690      1704  LOAD_FAST                'indents'
             1706  LOAD_CONST               -1
             1708  BINARY_SUBSCR    
             1710  STORE_FAST               'async_def_indent'

 L. 692      1712  LOAD_GLOBAL              TokenInfo
             1714  LOAD_GLOBAL              ASYNC
             1716  LOAD_FAST                'stashed'
             1718  LOAD_ATTR                string

 L. 693      1720  LOAD_FAST                'stashed'
             1722  LOAD_ATTR                start
             1724  LOAD_FAST                'stashed'
             1726  LOAD_ATTR                end

 L. 694      1728  LOAD_FAST                'stashed'
             1730  LOAD_ATTR                line
             1732  CALL_FUNCTION_5       5  '5 positional arguments'
             1734  YIELD_VALUE      
             1736  POP_TOP          

 L. 695      1738  LOAD_CONST               None
             1740  STORE_FAST               'stashed'
           1742_0  COME_FROM          1696  '1696'
           1742_1  COME_FROM          1684  '1684'
           1742_2  COME_FROM          1672  '1672'
           1742_3  COME_FROM          1666  '1666'

 L. 697      1742  LOAD_FAST                'stashed'
             1744  POP_JUMP_IF_FALSE  1758  'to 1758'

 L. 698      1748  LOAD_FAST                'stashed'
             1750  YIELD_VALUE      
             1752  POP_TOP          

 L. 699      1754  LOAD_CONST               None
             1756  STORE_FAST               'stashed'
           1758_0  COME_FROM          1744  '1744'

 L. 701      1758  LOAD_FAST                'tok'
             1760  YIELD_VALUE      
             1762  POP_TOP          
             1764  JUMP_FORWARD       1854  'to 1854'
             1766  ELSE                     '1854'

 L. 702      1766  LOAD_FAST                'initial'
             1768  LOAD_STR                 '\\'
             1770  COMPARE_OP               ==
             1772  POP_JUMP_IF_FALSE  1782  'to 1782'

 L. 703      1776  LOAD_CONST               1
             1778  STORE_FAST               'continued'
             1780  JUMP_FORWARD       1854  'to 1854'
             1782  ELSE                     '1854'

 L. 705      1782  LOAD_FAST                'initial'
             1784  LOAD_STR                 '([{'
             1786  COMPARE_OP               in
             1788  POP_JUMP_IF_FALSE  1802  'to 1802'

 L. 706      1792  LOAD_FAST                'parenlev'
             1794  LOAD_CONST               1
             1796  INPLACE_ADD      
             1798  STORE_FAST               'parenlev'
             1800  JUMP_FORWARD       1820  'to 1820'
             1802  ELSE                     '1820'

 L. 707      1802  LOAD_FAST                'initial'
             1804  LOAD_STR                 ')]}'
             1806  COMPARE_OP               in
             1808  POP_JUMP_IF_FALSE  1820  'to 1820'

 L. 708      1812  LOAD_FAST                'parenlev'
             1814  LOAD_CONST               1
             1816  INPLACE_SUBTRACT 
             1818  STORE_FAST               'parenlev'
           1820_0  COME_FROM          1808  '1808'
           1820_1  COME_FROM          1800  '1800'

 L. 709      1820  LOAD_FAST                'stashed'
             1822  POP_JUMP_IF_FALSE  1836  'to 1836'

 L. 710      1826  LOAD_FAST                'stashed'
             1828  YIELD_VALUE      
             1830  POP_TOP          

 L. 711      1832  LOAD_CONST               None
             1834  STORE_FAST               'stashed'
           1836_0  COME_FROM          1822  '1822'

 L. 712      1836  LOAD_GLOBAL              TokenInfo
             1838  LOAD_GLOBAL              OP
             1840  LOAD_FAST                'token'
             1842  LOAD_FAST                'spos'
             1844  LOAD_FAST                'epos'
             1846  LOAD_FAST                'line'
             1848  CALL_FUNCTION_5       5  '5 positional arguments'
             1850  YIELD_VALUE      
             1852  POP_TOP          
           1854_0  COME_FROM          1780  '1780'
           1854_1  COME_FROM          1764  '1764'
           1854_2  COME_FROM          1200  '1200'
             1854  JUMP_FORWARD       1898  'to 1898'
             1856  ELSE                     '1898'

 L. 714      1856  LOAD_GLOBAL              TokenInfo
             1858  LOAD_GLOBAL              ERRORTOKEN
             1860  LOAD_FAST                'line'
             1862  LOAD_FAST                'pos'
             1864  BINARY_SUBSCR    

 L. 715      1866  LOAD_FAST                'lnum'
             1868  LOAD_FAST                'pos'
             1870  BUILD_TUPLE_2         2 
             1872  LOAD_FAST                'lnum'
             1874  LOAD_FAST                'pos'
             1876  LOAD_CONST               1
             1878  BINARY_ADD       
             1880  BUILD_TUPLE_2         2 
             1882  LOAD_FAST                'line'
             1884  CALL_FUNCTION_5       5  '5 positional arguments'
             1886  YIELD_VALUE      
             1888  POP_TOP          

 L. 716      1890  LOAD_FAST                'pos'
             1892  LOAD_CONST               1
             1894  INPLACE_ADD      
             1896  STORE_FAST               'pos'
           1898_0  COME_FROM          1854  '1854'
             1898  JUMP_BACK           956  'to 956'
           1902_0  COME_FROM           962  '962'
             1902  POP_BLOCK        
           1904_0  COME_FROM_LOOP      952  '952'
             1904  JUMP_BACK            92  'to 92'
             1906  POP_BLOCK        
           1908_0  COME_FROM_LOOP       88  '88'

 L. 718      1908  LOAD_FAST                'stashed'
             1910  POP_JUMP_IF_FALSE  1924  'to 1924'

 L. 719      1914  LOAD_FAST                'stashed'
             1916  YIELD_VALUE      
             1918  POP_TOP          

 L. 720      1920  LOAD_CONST               None
             1922  STORE_FAST               'stashed'
           1924_0  COME_FROM          1910  '1910'

 L. 722      1924  SETUP_LOOP         1974  'to 1974'
             1926  LOAD_FAST                'indents'
             1928  LOAD_CONST               1
             1930  LOAD_CONST               None
             1932  BUILD_SLICE_2         2 
             1934  BINARY_SUBSCR    
             1936  GET_ITER         
             1938  FOR_ITER           1972  'to 1972'
             1940  STORE_FAST               'indent'

 L. 723      1942  LOAD_GLOBAL              TokenInfo
             1944  LOAD_GLOBAL              DEDENT
             1946  LOAD_STR                 ''
             1948  LOAD_FAST                'lnum'
             1950  LOAD_CONST               0
             1952  BUILD_TUPLE_2         2 
             1954  LOAD_FAST                'lnum'
             1956  LOAD_CONST               0
             1958  BUILD_TUPLE_2         2 
             1960  LOAD_STR                 ''
             1962  CALL_FUNCTION_5       5  '5 positional arguments'
             1964  YIELD_VALUE      
             1966  POP_TOP          
             1968  JUMP_BACK          1938  'to 1938'
             1972  POP_BLOCK        
           1974_0  COME_FROM_LOOP     1924  '1924'

 L. 724      1974  LOAD_GLOBAL              TokenInfo
             1976  LOAD_GLOBAL              ENDMARKER
             1978  LOAD_STR                 ''
             1980  LOAD_FAST                'lnum'
             1982  LOAD_CONST               0
             1984  BUILD_TUPLE_2         2 
             1986  LOAD_FAST                'lnum'
             1988  LOAD_CONST               0
             1990  BUILD_TUPLE_2         2 
             1992  LOAD_STR                 ''
             1994  CALL_FUNCTION_5       5  '5 positional arguments'
             1996  YIELD_VALUE      
             1998  POP_TOP          

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 1208


def generate_tokens(readline):
    return _tokenize(readline, None)


def main():
    import argparse

    def perror(message):
        print(message, file=(sys.stderr))

    def error(message, filename=None, location=None):
        if location:
            args = (
             filename,) + location + (message,)
            perror('%s:%d:%d: error: %s' % args)
        else:
            if filename:
                perror('%s: error: %s' % (filename, message))
            else:
                perror('error: %s' % message)
        sys.exit(1)

    parser = argparse.ArgumentParser(prog='python -m tokenize')
    parser.add_argument(dest='filename', nargs='?', metavar='filename.py',
      help='the file to tokenize; defaults to stdin')
    parser.add_argument('-e', '--exact', dest='exact', action='store_true', help='display token names using the exact type')
    args = parser.parse_args()
    try:
        if args.filename:
            filename = args.filename
            with _builtin_open(filename, 'rb') as (f):
                tokens = list(tokenize(f.readline))
        else:
            filename = '<stdin>'
            tokens = _tokenize(sys.stdin.readline, None)
        for token in tokens:
            token_type = token.type
            if args.exact:
                token_type = token.exact_type
            token_range = '%d,%d-%d,%d:' % (token.start + token.end)
            print('%-20s%-15s%-15r' % (
             token_range, tok_name[token_type], token.string))

    except IndentationError as err:
        line, column = err.args[1][1:3]
        error(err.args[0], filename, (line, column))
    except TokenError as err:
        line, column = err.args[1]
        error(err.args[0], filename, (line, column))
    except SyntaxError as err:
        error(err, filename)
    except OSError as err:
        error(err)
    except KeyboardInterrupt:
        print('interrupted\n')
    except Exception as err:
        perror('unexpected error: %s' % err)
        raise


if __name__ == '__main__':
    main()