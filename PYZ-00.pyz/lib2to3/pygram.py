# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib2to3\pygram.py
"""Export the Python grammar and symbols."""
import os
from .pgen2 import token
from .pgen2 import driver
from . import pytree
_GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), 'Grammar.txt')
_PATTERN_GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), 'PatternGrammar.txt')

class Symbols(object):

    def __init__(self, grammar):
        """Initializer.

        Creates an attribute for each grammar symbol (nonterminal),
        whose value is the symbol's type (an int >= 256).
        """
        for name, symbol in grammar.symbol2number.items():
            setattr(self, name, symbol)


python_grammar = driver.load_grammar(_GRAMMAR_FILE)
python_symbols = Symbols(python_grammar)
python_grammar_no_print_statement = python_grammar.copy()
del python_grammar_no_print_statement.keywords['print']
pattern_grammar = driver.load_grammar(_PATTERN_GRAMMAR_FILE)
pattern_symbols = Symbols(pattern_grammar)