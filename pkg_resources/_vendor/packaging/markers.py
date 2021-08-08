# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\pkg_resources\_vendor\packaging\markers.py
from __future__ import absolute_import, division, print_function
import operator, os, platform, sys
from pkg_resources.extern.pyparsing import ParseException, ParseResults, stringStart, stringEnd
from pkg_resources.extern.pyparsing import ZeroOrMore, Group, Forward, QuotedString
from pkg_resources.extern.pyparsing import Literal as L
from ._compat import string_types
from .specifiers import Specifier, InvalidSpecifier
__all__ = [
 'InvalidMarker', 'UndefinedComparison', 'UndefinedEnvironmentName',
 'Marker', 'default_environment']

class InvalidMarker(ValueError):
    __doc__ = '\n    An invalid marker was found, users should refer to PEP 508.\n    '


class UndefinedComparison(ValueError):
    __doc__ = "\n    An invalid operation was attempted on a value that doesn't support it.\n    "


class UndefinedEnvironmentName(ValueError):
    __doc__ = '\n    A name was attempted to be used that does not exist inside of the\n    environment.\n    '


class Node(object):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '<{0}({1!r})>'.format(self.__class__.__name__, str(self))

    def serialize(self):
        raise NotImplementedError


class Variable(Node):

    def serialize(self):
        return str(self)


class Value(Node):

    def serialize(self):
        return '"{0}"'.format(self)


class Op(Node):

    def serialize(self):
        return str(self)


VARIABLE = L('implementation_version') | L('platform_python_implementation') | L('implementation_name') | L('python_full_version') | L('platform_release') | L('platform_version') | L('platform_machine') | L('platform_system') | L('python_version') | L('sys_platform') | L('os_name') | L('os.name') | L('sys.platform') | L('platform.version') | L('platform.machine') | L('platform.python_implementation') | L('python_implementation') | L('extra')
ALIASES = {'os.name':'os_name', 
 'sys.platform':'sys_platform', 
 'platform.version':'platform_version', 
 'platform.machine':'platform_machine', 
 'platform.python_implementation':'platform_python_implementation', 
 'python_implementation':'platform_python_implementation'}
VARIABLE.setParseAction(lambda s, l, t: Variable(ALIASES.get(t[0], t[0])))
VERSION_CMP = L('===') | L('==') | L('>=') | L('<=') | L('!=') | L('~=') | L('>') | L('<')
MARKER_OP = VERSION_CMP | L('not in') | L('in')
MARKER_OP.setParseAction(lambda s, l, t: Op(t[0]))
MARKER_VALUE = QuotedString("'") | QuotedString('"')
MARKER_VALUE.setParseAction(lambda s, l, t: Value(t[0]))
BOOLOP = L('and') | L('or')
MARKER_VAR = VARIABLE | MARKER_VALUE
MARKER_ITEM = Group(MARKER_VAR + MARKER_OP + MARKER_VAR)
MARKER_ITEM.setParseAction(lambda s, l, t: tuple(t[0]))
LPAREN = L('(').suppress()
RPAREN = L(')').suppress()
MARKER_EXPR = Forward()
MARKER_ATOM = MARKER_ITEM | Group(LPAREN + MARKER_EXPR + RPAREN)
MARKER_EXPR << MARKER_ATOM + ZeroOrMore(BOOLOP + MARKER_EXPR)
MARKER = stringStart + MARKER_EXPR + stringEnd

def _coerce_parse_result(results):
    if isinstance(results, ParseResults):
        return [_coerce_parse_result(i) for i in results]
    else:
        return results


def _format_marker(marker, first=True):
    if not isinstance(marker, (list, tuple, string_types)):
        raise AssertionError
    else:
        if isinstance(marker, list):
            if len(marker) == 1:
                if isinstance(marker[0], (list, tuple)):
                    return _format_marker(marker[0])
        if isinstance(marker, list):
            inner = (_format_marker(m, first=False) for m in marker)
            if first:
                return ' '.join(inner)
            else:
                return '(' + ' '.join(inner) + ')'
        else:
            if isinstance(marker, tuple):
                return ' '.join([m.serialize() for m in marker])
            else:
                return marker


_operators = {'in':lambda lhs, rhs: lhs in rhs,  'not in':lambda lhs, rhs: lhs not in rhs, 
 '<':operator.lt, 
 '<=':operator.le, 
 '==':operator.eq, 
 '!=':operator.ne, 
 '>=':operator.ge, 
 '>':operator.gt}

def _eval_op(lhs, op, rhs):
    try:
        spec = Specifier(''.join([op.serialize(), rhs]))
    except InvalidSpecifier:
        pass
    else:
        return spec.contains(lhs)
        oper = _operators.get(op.serialize())
        if oper is None:
            raise UndefinedComparison('Undefined {0!r} on {1!r} and {2!r}.'.format(op, lhs, rhs))
        return oper(lhs, rhs)


_undefined = object()

def _get_env(environment, name):
    value = environment.get(name, _undefined)
    if value is _undefined:
        raise UndefinedEnvironmentName('{0!r} does not exist in evaluation environment.'.format(name))
    return value


def _evaluate_markers(markers, environment):
    groups = [[]]
    for marker in markers:
        assert isinstance(marker, (list, tuple, string_types))
        if isinstance(marker, list):
            groups[(-1)].append(_evaluate_markers(marker, environment))
        elif isinstance(marker, tuple):
            lhs, op, rhs = marker
            if isinstance(lhs, Variable):
                lhs_value = _get_env(environment, lhs.value)
                rhs_value = rhs.value
            else:
                lhs_value = lhs.value
                rhs_value = _get_env(environment, rhs.value)
            groups[(-1)].append(_eval_op(lhs_value, op, rhs_value))
        else:
            assert marker in ('and', 'or')
            if marker == 'or':
                groups.append([])

    return any(all(item) for item in groups)


def format_full_version(info):
    version = '{0.major}.{0.minor}.{0.micro}'.format(info)
    kind = info.releaselevel
    if kind != 'final':
        version += kind[0] + str(info.serial)
    return version


def default_environment():
    if hasattr(sys, 'implementation'):
        iver = format_full_version(sys.implementation.version)
        implementation_name = sys.implementation.name
    else:
        iver = '0'
        implementation_name = ''
    return {'implementation_name':implementation_name, 
     'implementation_version':iver, 
     'os_name':os.name, 
     'platform_machine':platform.machine(), 
     'platform_release':platform.release(), 
     'platform_system':platform.system(), 
     'platform_version':platform.version(), 
     'python_full_version':platform.python_version(), 
     'platform_python_implementation':platform.python_implementation(), 
     'python_version':platform.python_version()[:3], 
     'sys_platform':sys.platform}


class Marker(object):

    def __init__(self, marker):
        try:
            self._markers = _coerce_parse_result(MARKER.parseString(marker))
        except ParseException as e:
            err_str = 'Invalid marker: {0!r}, parse error at {1!r}'.format(marker, marker[e.loc:e.loc + 8])
            raise InvalidMarker(err_str)

    def __str__(self):
        return _format_marker(self._markers)

    def __repr__(self):
        return '<Marker({0!r})>'.format(str(self))

    def evaluate(self, environment=None):
        """Evaluate a marker.

        Return the boolean from evaluating the given marker against the
        environment. environment is an optional argument to override all or
        part of the determined environment.

        The environment is determined from the current Python process.
        """
        current_environment = default_environment()
        if environment is not None:
            current_environment.update(environment)
        return _evaluate_markers(self._markers, current_environment)