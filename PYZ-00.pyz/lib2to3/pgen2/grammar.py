# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib2to3\pgen2\grammar.py
"""This module defines the data structures used to represent a grammar.

These are a bit arcane because they are derived from the data
structures used by Python's 'pgen' parser generator.

There's also a table here mapping operators to their names in the
token module; the Python tokenize module reports all operators as the
fallback token code OP, but the parser needs the actual token code.

"""
import collections, pickle
from . import token, tokenize

class Grammar(object):
    __doc__ = "Pgen parsing tables conversion class.\n\n    Once initialized, this class supplies the grammar tables for the\n    parsing engine implemented by parse.py.  The parsing engine\n    accesses the instance variables directly.  The class here does not\n    provide initialization of the tables; several subclasses exist to\n    do this (see the conv and pgen modules).\n\n    The load() method reads the tables from a pickle file, which is\n    much faster than the other ways offered by subclasses.  The pickle\n    file is written by calling dump() (after loading the grammar\n    tables using a subclass).  The report() method prints a readable\n    representation of the tables to stdout, for debugging.\n\n    The instance variables are as follows:\n\n    symbol2number -- a dict mapping symbol names to numbers.  Symbol\n                     numbers are always 256 or higher, to distinguish\n                     them from token numbers, which are between 0 and\n                     255 (inclusive).\n\n    number2symbol -- a dict mapping numbers to symbol names;\n                     these two are each other's inverse.\n\n    states        -- a list of DFAs, where each DFA is a list of\n                     states, each state is a list of arcs, and each\n                     arc is a (i, j) pair where i is a label and j is\n                     a state number.  The DFA number is the index into\n                     this list.  (This name is slightly confusing.)\n                     Final states are represented by a special arc of\n                     the form (0, j) where j is its own state number.\n\n    dfas          -- a dict mapping symbol numbers to (DFA, first)\n                     pairs, where DFA is an item from the states list\n                     above, and first is a set of tokens that can\n                     begin this grammar rule (represented by a dict\n                     whose values are always 1).\n\n    labels        -- a list of (x, y) pairs where x is either a token\n                     number or a symbol number, and y is either None\n                     or a string; the strings are keywords.  The label\n                     number is the index in this list; label numbers\n                     are used to mark state transitions (arcs) in the\n                     DFAs.\n\n    start         -- the number of the grammar's start symbol.\n\n    keywords      -- a dict mapping keyword strings to arc labels.\n\n    tokens        -- a dict mapping token numbers to arc labels.\n\n    "

    def __init__(self):
        self.symbol2number = {}
        self.number2symbol = {}
        self.states = []
        self.dfas = {}
        self.labels = [
         (0, 'EMPTY')]
        self.keywords = {}
        self.tokens = {}
        self.symbol2label = {}
        self.start = 256

    def dump(self, filename):
        """Dump the grammar tables to a pickle file.

        dump() recursively changes all dict to OrderedDict, so the pickled file
        is not exactly the same as what was passed in to dump(). load() uses the
        pickled file to create the tables, but  only changes OrderedDict to dict
        at the top level; it does not recursively change OrderedDict to dict.
        So, the loaded tables are different from the original tables that were
        passed to load() in that some of the OrderedDict (from the pickled file)
        are not changed back to dict. For parsing, this has no effect on
        performance because OrderedDict uses dict's __getitem__ with nothing in
        between.
        """
        with open(filename, 'wb') as (f):
            d = _make_deterministic(self.__dict__)
            pickle.dump(d, f, 2)

    def load(self, filename):
        """Load the grammar tables from a pickle file."""
        with open(filename, 'rb') as (f):
            d = pickle.load(f)
        self.__dict__.update(d)

    def copy(self):
        """
        Copy the grammar.
        """
        new = self.__class__()
        for dict_attr in ('symbol2number', 'number2symbol', 'dfas', 'keywords', 'tokens',
                          'symbol2label'):
            setattr(new, dict_attr, getattr(self, dict_attr).copy())

        new.labels = self.labels[:]
        new.states = self.states[:]
        new.start = self.start
        return new

    def report(self):
        """Dump the grammar tables to standard output, for debugging."""
        from pprint import pprint
        print('s2n')
        pprint(self.symbol2number)
        print('n2s')
        pprint(self.number2symbol)
        print('states')
        pprint(self.states)
        print('dfas')
        pprint(self.dfas)
        print('labels')
        pprint(self.labels)
        print('start', self.start)


def _make_deterministic(top):
    if isinstance(top, dict):
        return collections.OrderedDict(sorted((k, _make_deterministic(v)) for k, v in top.items()))
    else:
        if isinstance(top, list):
            return [_make_deterministic(e) for e in top]
        if isinstance(top, tuple):
            return tuple(_make_deterministic(e) for e in top)
        return top


opmap_raw = '\n( LPAR\n) RPAR\n[ LSQB\n] RSQB\n: COLON\n, COMMA\n; SEMI\n+ PLUS\n- MINUS\n* STAR\n/ SLASH\n| VBAR\n& AMPER\n< LESS\n> GREATER\n= EQUAL\n. DOT\n% PERCENT\n` BACKQUOTE\n{ LBRACE\n} RBRACE\n@ AT\n@= ATEQUAL\n== EQEQUAL\n!= NOTEQUAL\n<> NOTEQUAL\n<= LESSEQUAL\n>= GREATEREQUAL\n~ TILDE\n^ CIRCUMFLEX\n<< LEFTSHIFT\n>> RIGHTSHIFT\n** DOUBLESTAR\n+= PLUSEQUAL\n-= MINEQUAL\n*= STAREQUAL\n/= SLASHEQUAL\n%= PERCENTEQUAL\n&= AMPEREQUAL\n|= VBAREQUAL\n^= CIRCUMFLEXEQUAL\n<<= LEFTSHIFTEQUAL\n>>= RIGHTSHIFTEQUAL\n**= DOUBLESTAREQUAL\n// DOUBLESLASH\n//= DOUBLESLASHEQUAL\n-> RARROW\n'
opmap = {}
for line in opmap_raw.splitlines():
    if line:
        op, name = line.split()
        opmap[op] = getattr(token, name)