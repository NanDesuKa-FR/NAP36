# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib2to3\pgen2\literals.py
"""Safely evaluate Python string literals without using eval()."""
import re
simple_escapes = {'a':'\x07', 
 'b':'\x08', 
 'f':'\x0c', 
 'n':'\n', 
 'r':'\r', 
 't':'\t', 
 'v':'\x0b', 
 "'":"'", 
 '"':'"', 
 '\\':'\\'}

def escape(m):
    all, tail = m.group(0, 1)
    assert all.startswith('\\')
    esc = simple_escapes.get(tail)
    if esc is not None:
        return esc
    if tail.startswith('x'):
        hexes = tail[1:]
        if len(hexes) < 2:
            raise ValueError("invalid hex string escape ('\\%s')" % tail)
        try:
            i = int(hexes, 16)
        except ValueError:
            raise ValueError("invalid hex string escape ('\\%s')" % tail)

    else:
        try:
            i = int(tail, 8)
        except ValueError:
            raise ValueError("invalid octal string escape ('\\%s')" % tail)

        return chr(i)


def evalString(s):
    if not s.startswith("'"):
        if not s.startswith('"'):
            raise AssertionError(repr(s[:1]))
    else:
        q = s[0]
        if s[:3] == q * 3:
            q = q * 3
        assert s.endswith(q), repr(s[-len(q):])
        assert len(s) >= 2 * len(q)
    s = s[len(q):-len(q)]
    return re.sub('\\\\(\\\'|\\"|\\\\|[abfnrtv]|x.{0,2}|[0-7]{1,3})', escape, s)


def test():
    for i in range(256):
        c = chr(i)
        s = repr(c)
        e = evalString(s)
        if e != c:
            print(i, c, s, e)


if __name__ == '__main__':
    test()