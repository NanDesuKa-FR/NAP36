# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib2to3\patcomp.py
"""Pattern compiler.

The grammar is taken from PatternGrammar.txt.

The compiler compiles a pattern to a pytree.*Pattern instance.
"""
__author__ = 'Guido van Rossum <guido@python.org>'
import io, os
from .pgen2 import driver, literals, token, tokenize, parse, grammar
from . import pytree
from . import pygram
_PATTERN_GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), 'PatternGrammar.txt')

class PatternSyntaxError(Exception):
    pass


def tokenize_wrapper(input):
    """Tokenizes a string suppressing significant whitespace."""
    skip = {
     token.NEWLINE, token.INDENT, token.DEDENT}
    tokens = tokenize.generate_tokens(io.StringIO(input).readline)
    for quintuple in tokens:
        type, value, start, end, line_text = quintuple
        if type not in skip:
            yield quintuple


class PatternCompiler(object):

    def __init__(self, grammar_file=_PATTERN_GRAMMAR_FILE):
        """Initializer.

        Takes an optional alternative filename for the pattern grammar.
        """
        self.grammar = driver.load_grammar(grammar_file)
        self.syms = pygram.Symbols(self.grammar)
        self.pygrammar = pygram.python_grammar
        self.pysyms = pygram.python_symbols
        self.driver = driver.Driver((self.grammar), convert=pattern_convert)

    def compile_pattern(self, input, debug=False, with_tree=False):
        """Compiles a pattern string to a nested pytree.*Pattern object."""
        tokens = tokenize_wrapper(input)
        try:
            root = self.driver.parse_tokens(tokens, debug=debug)
        except parse.ParseError as e:
            raise PatternSyntaxError(str(e))

        if with_tree:
            return (self.compile_node(root), root)
        else:
            return self.compile_node(root)

    def compile_node(self, node):
        """Compiles a node, recursively.

        This is one big switch on the node type.
        """
        if node.type == self.syms.Matcher:
            node = node.children[0]
        if node.type == self.syms.Alternatives:
            alts = [self.compile_node(ch) for ch in node.children[::2]]
            if len(alts) == 1:
                return alts[0]
            else:
                p = pytree.WildcardPattern([[a] for a in alts], min=1, max=1)
                return p.optimize()
        if node.type == self.syms.Alternative:
            units = [self.compile_node(ch) for ch in node.children]
            if len(units) == 1:
                return units[0]
            p = pytree.WildcardPattern([units], min=1, max=1)
            return p.optimize()
        else:
            if node.type == self.syms.NegatedUnit:
                pattern = self.compile_basic(node.children[1:])
                p = pytree.NegatedPattern(pattern)
                return p.optimize()
            else:
                if not node.type == self.syms.Unit:
                    raise AssertionError
                else:
                    name = None
                    nodes = node.children
                    if len(nodes) >= 3:
                        if nodes[1].type == token.EQUAL:
                            name = nodes[0].value
                            nodes = nodes[2:]
                    repeat = None
                    if len(nodes) >= 2:
                        if nodes[(-1)].type == self.syms.Repeater:
                            repeat = nodes[(-1)]
                            nodes = nodes[:-1]
                    pattern = self.compile_basic(nodes, repeat)
                    if repeat is not None:
                        assert repeat.type == self.syms.Repeater
                        children = repeat.children
                        child = children[0]
                        if child.type == token.STAR:
                            min = 0
                            max = pytree.HUGE
                        else:
                            if child.type == token.PLUS:
                                min = 1
                                max = pytree.HUGE
                            else:
                                if child.type == token.LBRACE:
                                    if not children[(-1)].type == token.RBRACE:
                                        raise AssertionError
                                    elif not len(children) in (3, 5):
                                        raise AssertionError
                                    min = max = self.get_int(children[1])
                                    if len(children) == 5:
                                        max = self.get_int(children[3])
                                else:
                                    assert False
                        if min != 1 or max != 1:
                            pattern = pattern.optimize()
                            pattern = pytree.WildcardPattern([[pattern]], min=min, max=max)
                if name is not None:
                    pattern.name = name
            return pattern.optimize()

    def compile_basic(self, nodes, repeat=None):
        if not len(nodes) >= 1:
            raise AssertionError
        else:
            node = nodes[0]
            if node.type == token.STRING:
                value = str(literals.evalString(node.value))
                return pytree.LeafPattern(_type_of_literal(value), value)
            if node.type == token.NAME:
                value = node.value
                if value.isupper():
                    if value not in TOKEN_MAP:
                        raise PatternSyntaxError('Invalid token: %r' % value)
                    if nodes[1:]:
                        raise PatternSyntaxError("Can't have details for token")
                    return pytree.LeafPattern(TOKEN_MAP[value])
                else:
                    if value == 'any':
                        type = None
                    else:
                        if not value.startswith('_'):
                            type = getattr(self.pysyms, value, None)
                            if type is None:
                                raise PatternSyntaxError('Invalid symbol: %r' % value)
                        if nodes[1:]:
                            content = [
                             self.compile_node(nodes[1].children[1])]
                        else:
                            content = None
                    return pytree.NodePattern(type, content)
            else:
                if node.value == '(':
                    return self.compile_node(nodes[1])
            if node.value == '[':
                assert repeat is None
                subpattern = self.compile_node(nodes[1])
                return pytree.WildcardPattern([[subpattern]], min=0, max=1)
            assert False, node

    def get_int(self, node):
        assert node.type == token.NUMBER
        return int(node.value)


TOKEN_MAP = {'NAME':token.NAME, 
 'STRING':token.STRING, 
 'NUMBER':token.NUMBER, 
 'TOKEN':None}

def _type_of_literal(value):
    if value[0].isalpha():
        return token.NAME
    else:
        if value in grammar.opmap:
            return grammar.opmap[value]
        return


def pattern_convert(grammar, raw_node_info):
    """Converts raw node information to a Node or Leaf instance."""
    type, value, context, children = raw_node_info
    if children or type in grammar.number2symbol:
        return pytree.Node(type, children, context=context)
    else:
        return pytree.Leaf(type, value, context=context)


def compile_pattern(pattern):
    return PatternCompiler().compile_pattern(pattern)