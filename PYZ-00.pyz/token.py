# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: token.py
"""Token constants (from "token.h")."""
__all__ = [
 'tok_name', 'ISTERMINAL', 'ISNONTERMINAL', 'ISEOF']
ENDMARKER = 0
NAME = 1
NUMBER = 2
STRING = 3
NEWLINE = 4
INDENT = 5
DEDENT = 6
LPAR = 7
RPAR = 8
LSQB = 9
RSQB = 10
COLON = 11
COMMA = 12
SEMI = 13
PLUS = 14
MINUS = 15
STAR = 16
SLASH = 17
VBAR = 18
AMPER = 19
LESS = 20
GREATER = 21
EQUAL = 22
DOT = 23
PERCENT = 24
LBRACE = 25
RBRACE = 26
EQEQUAL = 27
NOTEQUAL = 28
LESSEQUAL = 29
GREATEREQUAL = 30
TILDE = 31
CIRCUMFLEX = 32
LEFTSHIFT = 33
RIGHTSHIFT = 34
DOUBLESTAR = 35
PLUSEQUAL = 36
MINEQUAL = 37
STAREQUAL = 38
SLASHEQUAL = 39
PERCENTEQUAL = 40
AMPEREQUAL = 41
VBAREQUAL = 42
CIRCUMFLEXEQUAL = 43
LEFTSHIFTEQUAL = 44
RIGHTSHIFTEQUAL = 45
DOUBLESTAREQUAL = 46
DOUBLESLASH = 47
DOUBLESLASHEQUAL = 48
AT = 49
ATEQUAL = 50
RARROW = 51
ELLIPSIS = 52
OP = 53
AWAIT = 54
ASYNC = 55
ERRORTOKEN = 56
N_TOKENS = 57
NT_OFFSET = 256
tok_name = {value:name for name, value in globals().items() if isinstance(value, int) if not name.startswith('_') if not name.startswith('_')}
__all__.extend(tok_name.values())

def ISTERMINAL(x):
    return x < NT_OFFSET


def ISNONTERMINAL(x):
    return x >= NT_OFFSET


def ISEOF(x):
    return x == ENDMARKER


def _main():
    import re, sys
    args = sys.argv[1:]
    inFileName = args and args[0] or 'Include/token.h'
    outFileName = 'Lib/token.py'
    if len(args) > 1:
        outFileName = args[1]
    try:
        fp = open(inFileName)
    except OSError as err:
        sys.stdout.write('I/O error: %s\n' % str(err))
        sys.exit(1)

    with fp:
        lines = fp.read().split('\n')
    prog = re.compile('#define[ \t][ \t]*([A-Z0-9][A-Z0-9_]*)[ \t][ \t]*([0-9][0-9]*)', re.IGNORECASE)
    tokens = {}
    for line in lines:
        match = prog.match(line)
        if match:
            name, val = match.group(1, 2)
            val = int(val)
            tokens[val] = name

    keys = sorted(tokens.keys())
    try:
        fp = open(outFileName)
    except OSError as err:
        sys.stderr.write('I/O error: %s\n' % str(err))
        sys.exit(2)

    with fp:
        format = fp.read().split('\n')
    try:
        start = format.index('#--start constants--') + 1
        end = format.index('#--end constants--')
    except ValueError:
        sys.stderr.write('target does not contain format markers')
        sys.exit(3)

    lines = []
    for val in keys:
        lines.append('%s = %d' % (tokens[val], val))

    format[start:end] = lines
    try:
        fp = open(outFileName, 'w')
    except OSError as err:
        sys.stderr.write('I/O error: %s\n' % str(err))
        sys.exit(4)

    with fp:
        fp.write('\n'.join(format))


if __name__ == '__main__':
    _main()