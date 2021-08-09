# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\asn1crypto\core.py
"""
ASN.1 type classes for universal types. Exports the following items:

 - load()
 - Any()
 - Asn1Value()
 - BitString()
 - BMPString()
 - Boolean()
 - CharacterString()
 - Choice()
 - EmbeddedPdv()
 - Enumerated()
 - GeneralizedTime()
 - GeneralString()
 - GraphicString()
 - IA5String()
 - InstanceOf()
 - Integer()
 - IntegerBitString()
 - IntegerOctetString()
 - Null()
 - NumericString()
 - ObjectDescriptor()
 - ObjectIdentifier()
 - OctetBitString()
 - OctetString()
 - PrintableString()
 - Real()
 - RelativeOid()
 - Sequence()
 - SequenceOf()
 - Set()
 - SetOf()
 - TeletexString()
 - UniversalString()
 - UTCTime()
 - UTF8String()
 - VideotexString()
 - VisibleString()
 - VOID
 - Void()

Other type classes are defined that help compose the types listed above.
"""
from __future__ import unicode_literals, division, absolute_import, print_function
from datetime import datetime, timedelta
import binascii, copy, math, re, sys
from . import _teletex_codec
from ._errors import unwrap
from ._ordereddict import OrderedDict
from ._types import type_name, str_cls, byte_cls, int_types, chr_cls
from .parser import _parse, _dump_header
from .util import int_to_bytes, int_from_bytes, timezone, extended_datetime
if sys.version_info <= (3, ):
    from cStringIO import StringIO as BytesIO
    range = xrange
    _PY2 = True
else:
    from io import BytesIO
    _PY2 = False
_teletex_codec.register()
CLASS_NUM_TO_NAME_MAP = {0:'universal', 
 1:'application', 
 2:'context', 
 3:'private'}
CLASS_NAME_TO_NUM_MAP = {'universal':0, 
 'application':1, 
 'context':2, 
 'private':3, 
 0:0, 
 1:1, 
 2:2, 
 3:3}
METHOD_NUM_TO_NAME_MAP = {0:'primitive', 
 1:'constructed'}
_OID_RE = re.compile('^\\d+(\\.\\d+)*$')
_SETUP_CLASSES = {}

def load(encoded_data, strict=False):
    """
    Loads a BER/DER-encoded byte string and construct a universal object based
    on the tag value:

     - 1: Boolean
     - 2: Integer
     - 3: BitString
     - 4: OctetString
     - 5: Null
     - 6: ObjectIdentifier
     - 7: ObjectDescriptor
     - 8: InstanceOf
     - 9: Real
     - 10: Enumerated
     - 11: EmbeddedPdv
     - 12: UTF8String
     - 13: RelativeOid
     - 16: Sequence,
     - 17: Set
     - 18: NumericString
     - 19: PrintableString
     - 20: TeletexString
     - 21: VideotexString
     - 22: IA5String
     - 23: UTCTime
     - 24: GeneralizedTime
     - 25: GraphicString
     - 26: VisibleString
     - 27: GeneralString
     - 28: UniversalString
     - 29: CharacterString
     - 30: BMPString

    :param encoded_data:
        A byte string of BER or DER-encoded data

    :param strict:
        A boolean indicating if trailing data should be forbidden - if so, a
        ValueError will be raised when trailing data exists

    :raises:
        ValueError - when strict is True and trailing data is present
        ValueError - when the encoded value tag a tag other than listed above
        ValueError - when the ASN.1 header length is longer than the data
        TypeError - when encoded_data is not a byte string

    :return:
        An instance of the one of the universal classes
    """
    return Asn1Value.load(encoded_data, strict=strict)


class Asn1Value(object):
    __doc__ = '\n    The basis of all ASN.1 values\n    '
    method = None
    class_ = None
    tag = None
    _bad_tag = None
    implicit = False
    explicit = None
    _header = None
    contents = None
    _trailer = b''
    _native = None

    @classmethod
    def load(cls, encoded_data, strict=False, **kwargs):
        """
        Loads a BER/DER-encoded byte string using the current class as the spec

        :param encoded_data:
            A byte string of BER or DER-encoded data

        :param strict:
            A boolean indicating if trailing data should be forbidden - if so, a
            ValueError will be raised when trailing data exists

        :return:
            An instance of the current class
        """
        if not isinstance(encoded_data, byte_cls):
            raise TypeError('encoded_data must be a byte string, not %s' % type_name(encoded_data))
        spec = None
        if cls.tag is not None:
            spec = cls
        value, _ = _parse_build(encoded_data, spec=spec, spec_params=kwargs, strict=strict)
        return value

    def __init__(self, explicit=None, implicit=None, no_explicit=False, tag_type=None, class_=None, tag=None, optional=None, default=None, contents=None):
        """
        The optional parameter is not used, but rather included so we don't
        have to delete it from the parameter dictionary when passing as keyword
        args

        :param explicit:
            An int tag number for explicit tagging, or a 2-element tuple of
            class and tag.

        :param implicit:
            An int tag number for implicit tagging, or a 2-element tuple of
            class and tag.

        :param no_explicit:
            If explicit tagging info should be removed from this instance.
            Used internally to allow contructing the underlying value that
            has been wrapped in an explicit tag.

        :param tag_type:
            None for normal values, or one of "implicit", "explicit" for tagged
            values. Deprecated in favor of explicit and implicit params.

        :param class_:
            The class for the value - defaults to "universal" if tag_type is
            None, otherwise defaults to "context". Valid values include:
             - "universal"
             - "application"
             - "context"
             - "private"
            Deprecated in favor of explicit and implicit params.

        :param tag:
            The integer tag to override - usually this is used with tag_type or
            class_. Deprecated in favor of explicit and implicit params.

        :param optional:
            Dummy parameter that allows "optional" key in spec param dicts

        :param default:
            The default value to use if the value is currently None

        :param contents:
            A byte string of the encoded contents of the value

        :raises:
            ValueError - when implicit, explicit, tag_type, class_ or tag are invalid values
        """
        try:
            if self.__class__ not in _SETUP_CLASSES:
                cls = self.__class__
                if cls.explicit is not None:
                    if isinstance(cls.explicit[0], int_types):
                        cls.explicit = (
                         cls.explicit,)
                    if hasattr(cls, '_setup'):
                        self._setup()
                    _SETUP_CLASSES[cls] = True
                else:
                    if explicit is not None:
                        if isinstance(explicit, int_types):
                            if class_ is None:
                                class_ = 'context'
                            explicit = (
                             class_, explicit)
                        if tag_type == 'explicit':
                            tag_type = None
                            tag = None
                if implicit is not None:
                    if isinstance(implicit, int_types):
                        if class_ is None:
                            class_ = 'context'
                        implicit = (
                         class_, implicit)
                    if tag_type == 'implicit':
                        tag_type = None
                        tag = None
                if tag_type is not None:
                    if class_ is None:
                        class_ = 'context'
                    else:
                        if tag_type == 'explicit':
                            explicit = (
                             class_, tag)
                        else:
                            if tag_type == 'implicit':
                                implicit = (
                                 class_, tag)
                            else:
                                raise ValueError(unwrap('\n                        tag_type must be one of "implicit", "explicit", not %s\n                        ', repr(tag_type)))
                if explicit is not None:
                    if len(explicit) == 2:
                        if isinstance(explicit[1], int_types):
                            explicit = (
                             explicit,)
                    for class_, tag in explicit:
                        invalid_class = None
                        if isinstance(class_, int_types):
                            if class_ not in CLASS_NUM_TO_NAME_MAP:
                                invalid_class = class_
                        else:
                            if class_ not in CLASS_NAME_TO_NUM_MAP:
                                invalid_class = class_
                            class_ = CLASS_NAME_TO_NUM_MAP[class_]
                        if invalid_class is not None:
                            raise ValueError(unwrap('\n                            explicit class must be one of "universal", "application",\n                            "context", "private", not %s\n                            ', repr(invalid_class)))
                        if tag is not None:
                            if not isinstance(tag, int_types):
                                raise TypeError(unwrap('\n                                explicit tag must be an integer, not %s\n                                ', type_name(tag)))
                        if self.explicit is None:
                            self.explicit = (
                             (
                              class_, tag),)
                        else:
                            self.explicit = self.explicit + ((class_, tag),)

                else:
                    if implicit is not None:
                        class_, tag = implicit
                        if class_ not in CLASS_NAME_TO_NUM_MAP:
                            raise ValueError(unwrap('\n                        implicit class must be one of "universal", "application",\n                        "context", "private", not %s\n                        ', repr(class_)))
                        if tag is not None:
                            if not isinstance(tag, int_types):
                                raise TypeError(unwrap('\n                            implicit tag must be an integer, not %s\n                            ', type_name(tag)))
                        self.class_ = CLASS_NAME_TO_NUM_MAP[class_]
                        self.tag = tag
                        self.implicit = True
                    else:
                        if class_ is not None:
                            if class_ not in CLASS_NUM_TO_NAME_MAP:
                                raise ValueError(unwrap('\n                            class_ must be one of "universal", "application",\n                            "context", "private", not %s\n                            ', repr(class_)))
                            self.class_ = CLASS_NAME_TO_NUM_MAP[class_]
                if tag is not None:
                    self.tag = tag
                if no_explicit:
                    self.explicit = None
            else:
                if contents is not None:
                    self.contents = contents
                elif default is not None:
                    self.set(default)
        except (ValueError, TypeError) as e:
            args = e.args[1:]
            e.args = (e.args[0] + '\n    while constructing %s' % type_name(self),) + args
            raise e

    def __str__(self):
        """
        Since str is different in Python 2 and 3, this calls the appropriate
        method, __unicode__() or __bytes__()

        :return:
            A unicode string
        """
        if _PY2:
            return self.__bytes__()
        else:
            return self.__unicode__()

    def __repr__(self):
        """
        :return:
            A unicode string
        """
        if _PY2:
            return '<%s %s b%s>' % (type_name(self), id(self), repr(self.dump()))
        else:
            return '<%s %s %s>' % (type_name(self), id(self), repr(self.dump()))

    def __bytes__(self):
        """
        A fall-back method for print() in Python 2

        :return:
            A byte string of the output of repr()
        """
        return self.__repr__().encode('utf-8')

    def __unicode__(self):
        """
        A fall-back method for print() in Python 3

        :return:
            A unicode string of the output of repr()
        """
        return self.__repr__()

    def _new_instance(self):
        """
        Constructs a new copy of the current object, preserving any tagging

        :return:
            An Asn1Value object
        """
        new_obj = self.__class__()
        new_obj.class_ = self.class_
        new_obj.tag = self.tag
        new_obj.implicit = self.implicit
        new_obj.explicit = self.explicit
        return new_obj

    def __copy__(self):
        """
        Implements the copy.copy() interface

        :return:
            A new shallow copy of the current Asn1Value object
        """
        new_obj = self._new_instance()
        new_obj._copy(self, copy.copy)
        return new_obj

    def __deepcopy__(self, memo):
        """
        Implements the copy.deepcopy() interface

        :param memo:
            A dict for memoization

        :return:
            A new deep copy of the current Asn1Value object
        """
        new_obj = self._new_instance()
        memo[id(self)] = new_obj
        new_obj._copy(self, copy.deepcopy)
        return new_obj

    def copy(self):
        """
        Copies the object, preserving any special tagging from it

        :return:
            An Asn1Value object
        """
        return copy.deepcopy(self)

    def retag(self, tagging, tag=None):
        """
        Copies the object, applying a new tagging to it

        :param tagging:
            A dict containing the keys "explicit" and "implicit". Legacy
            API allows a unicode string of "implicit" or "explicit".

        :param tag:
            A integer tag number. Only used when tagging is a unicode string.

        :return:
            An Asn1Value object
        """
        if not isinstance(tagging, dict):
            tagging = {tagging: tag}
        new_obj = self.__class__(explicit=(tagging.get('explicit')), implicit=(tagging.get('implicit')))
        new_obj._copy(self, copy.deepcopy)
        return new_obj

    def untag(self):
        """
        Copies the object, removing any special tagging from it

        :return:
            An Asn1Value object
        """
        new_obj = self.__class__()
        new_obj._copy(self, copy.deepcopy)
        return new_obj

    def _copy(self, other, copy_func):
        """
        Copies the contents of another Asn1Value object to itself

        :param object:
            Another instance of the same class

        :param copy_func:
            An reference of copy.copy() or copy.deepcopy() to use when copying
            lists, dicts and objects
        """
        if self.__class__ != other.__class__:
            raise TypeError(unwrap('\n                Can not copy values from %s object to %s object\n                ', type_name(other), type_name(self)))
        self.contents = other.contents
        self._native = copy_func(other._native)

    def debug(self, nest_level=1):
        """
        Show the binary data and parsed data in a tree structure
        """
        prefix = '  ' * nest_level
        has_parsed = hasattr(self, 'parsed')
        _basic_debug(prefix, self)
        if has_parsed:
            self.parsed.debug(nest_level + 2)
        else:
            if hasattr(self, 'chosen'):
                self.chosen.debug(nest_level + 2)
            elif _PY2:
                if isinstance(self.native, byte_cls):
                    print('%s    Native: b%s' % (prefix, repr(self.native)))
            else:
                print('%s    Native: %s' % (prefix, self.native))

    def dump(self, force=False):
        """
        Encodes the value using DER

        :param force:
            If the encoded contents already exist, clear them and regenerate
            to ensure they are in DER format instead of BER format

        :return:
            A byte string of the DER-encoded value
        """
        contents = self.contents
        if self._header is None or force:
            if isinstance(self, Constructable):
                if self._indefinite:
                    self.method = 0
            header = _dump_header(self.class_, self.method, self.tag, self.contents)
            if self.explicit is not None:
                for class_, tag in self.explicit:
                    header = _dump_header(class_, 1, tag, header + self.contents) + header

            self._header = header
            self._trailer = b''
        return self._header + contents


class ValueMap:
    __doc__ = '\n    Basic functionality that allows for mapping values from ints or OIDs to\n    python unicode strings\n    '
    _map = None
    _reverse_map = None

    def _setup(self):
        """
        Generates _reverse_map from _map
        """
        cls = self.__class__
        if cls._map is None or cls._reverse_map is not None:
            return
        cls._reverse_map = {}
        for key, value in cls._map.items():
            cls._reverse_map[value] = key


class Castable(object):
    __doc__ = '\n    A mixin to handle converting an object between different classes that\n    represent the same encoded value, but with different rules for converting\n    to and from native Python values\n    '

    def cast(self, other_class):
        """
        Converts the current object into an object of a different class. The
        new class must use the ASN.1 encoding for the value.

        :param other_class:
            The class to instantiate the new object from

        :return:
            An instance of the type other_class
        """
        if other_class.tag != self.__class__.tag:
            raise TypeError(unwrap('\n                Can not covert a value from %s object to %s object since they\n                use different tags: %d versus %d\n                ', type_name(other_class), type_name(self), other_class.tag, self.__class__.tag))
        new_obj = other_class()
        new_obj.class_ = self.class_
        new_obj.implicit = self.implicit
        new_obj.explicit = self.explicit
        new_obj._header = self._header
        new_obj.contents = self.contents
        new_obj._trailer = self._trailer
        if isinstance(self, Constructable):
            new_obj.method = self.method
            new_obj._indefinite = self._indefinite
        return new_obj


class Constructable(object):
    __doc__ = '\n    A mixin to handle string types that may be constructed from chunks\n    contained within an indefinite length BER-encoded container\n    '
    _indefinite = False
    _chunks_offset = 0

    def _merge_chunks(self):
        """
        :return:
            A concatenation of the native values of the contained chunks
        """
        if not self._indefinite:
            return self._as_chunk()
        else:
            pointer = self._chunks_offset
            contents_len = len(self.contents)
            output = None
            while pointer < contents_len:
                sub_value, pointer = _parse_build((self.contents), pointer, spec=(self.__class__))
                if output is None:
                    output = sub_value._merge_chunks()
                else:
                    output += sub_value._merge_chunks()

            if output is None:
                return self._as_chunk()
            return output

    def _as_chunk(self):
        """
        A method to return a chunk of data that can be combined for
        constructed method values

        :return:
            A native Python value that can be added together. Examples include
            byte strings, unicode strings or tuples.
        """
        if self._chunks_offset == 0:
            return self.contents
        else:
            return self.contents[self._chunks_offset:]

    def _copy(self, other, copy_func):
        super(Constructable, self)._copy(other, copy_func)
        self.method = other.method
        self._indefinite = other._indefinite


class Void(Asn1Value):
    __doc__ = '\n    A representation of an optional value that is not present. Has .native\n    property and .dump() method to be compatible with other value classes.\n    '
    contents = b''

    def __eq__(self, other):
        """
        :param other:
            The other Primitive to compare to

        :return:
            A boolean
        """
        return other.__class__ == self.__class__

    def __nonzero__(self):
        return False

    def __len__(self):
        return 0

    def __iter__(self):
        return iter(())

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            None
        """
        pass

    def dump(self, force=False):
        """
        Encodes the value using DER

        :param force:
            If the encoded contents already exist, clear them and regenerate
            to ensure they are in DER format instead of BER format

        :return:
            A byte string of the DER-encoded value
        """
        return b''


VOID = Void()

class Any(Asn1Value):
    __doc__ = '\n    A value class that can contain any value, and allows for easy parsing of\n    the underlying encoded value using a spec. This is normally contained in\n    a Structure that has an ObjectIdentifier field and _oid_pair and _oid_specs\n    defined.\n    '
    _parsed = None

    def __init__(self, value=None, **kwargs):
        """
        Sets the value of the object before passing to Asn1Value.__init__()

        :param value:
            An Asn1Value object that will be set as the parsed value
        """
        (Asn1Value.__init__)(self, **kwargs)
        try:
            if value is not None:
                if not isinstance(value, Asn1Value):
                    raise TypeError(unwrap('\n                        value must be an instance of Asn1Value, not %s\n                        ', type_name(value)))
                self._parsed = (
                 value, value.__class__, None)
                self.contents = value.dump()
        except (ValueError, TypeError) as e:
            args = e.args[1:]
            e.args = (e.args[0] + '\n    while constructing %s' % type_name(self),) + args
            raise e

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            The .native value from the parsed value object
        """
        if self._parsed is None:
            self.parse()
        return self._parsed[0].native

    @property
    def parsed(self):
        """
        Returns the parsed object from .parse()

        :return:
            The object returned by .parse()
        """
        if self._parsed is None:
            self.parse()
        return self._parsed[0]

    def parse(self, spec=None, spec_params=None):
        """
        Parses the contents generically, or using a spec with optional params

        :param spec:
            A class derived from Asn1Value that defines what class_ and tag the
            value should have, and the semantics of the encoded value. The
            return value will be of this type. If omitted, the encoded value
            will be decoded using the standard universal tag based on the
            encoded tag number.

        :param spec_params:
            A dict of params to pass to the spec object

        :return:
            An object of the type spec, or if not present, a child of Asn1Value
        """
        if self._parsed is None or self._parsed[1:3] != (spec, spec_params):
            try:
                passed_params = spec_params or {}
                _tag_type_to_explicit_implicit(passed_params)
                if self.explicit is not None:
                    if 'explicit' in passed_params:
                        passed_params['explicit'] = self.explicit + passed_params['explicit']
                    else:
                        passed_params['explicit'] = self.explicit
                contents = self._header + self.contents + self._trailer
                parsed_value, _ = _parse_build(contents,
                  spec=spec,
                  spec_params=passed_params)
                self._parsed = (
                 parsed_value, spec, spec_params)
                self.tag = None
                self.explicit = None
                self.implicit = False
                self._header = b''
                self.contents = contents
                self._trailer = b''
            except (ValueError, TypeError) as e:
                args = e.args[1:]
                e.args = (e.args[0] + '\n    while parsing %s' % type_name(self),) + args
                raise e

        return self._parsed[0]

    def _copy(self, other, copy_func):
        super(Any, self)._copy(other, copy_func)
        self._parsed = copy_func(other._parsed)

    def dump(self, force=False):
        """
        Encodes the value using DER

        :param force:
            If the encoded contents already exist, clear them and regenerate
            to ensure they are in DER format instead of BER format

        :return:
            A byte string of the DER-encoded value
        """
        if self._parsed is None:
            self.parse()
        return self._parsed[0].dump(force=force)


class Choice(Asn1Value):
    __doc__ = '\n    A class to handle when a value may be one of several options\n    '
    _choice = None
    _name = None
    _parsed = None
    _alternatives = None
    _id_map = None
    _name_map = None

    @classmethod
    def load(cls, encoded_data, strict=False, **kwargs):
        """
        Loads a BER/DER-encoded byte string using the current class as the spec

        :param encoded_data:
            A byte string of BER or DER encoded data

        :param strict:
            A boolean indicating if trailing data should be forbidden - if so, a
            ValueError will be raised when trailing data exists

        :return:
            A instance of the current class
        """
        if not isinstance(encoded_data, byte_cls):
            raise TypeError('encoded_data must be a byte string, not %s' % type_name(encoded_data))
        value, _ = _parse_build(encoded_data, spec=cls, spec_params=kwargs, strict=strict)
        return value

    def _setup(self):
        """
        Generates _id_map from _alternatives to allow validating contents
        """
        cls = self.__class__
        cls._id_map = {}
        cls._name_map = {}
        for index, info in enumerate(cls._alternatives):
            if len(info) < 3:
                info = info + ({},)
                cls._alternatives[index] = info
            id_ = _build_id_tuple(info[2], info[1])
            cls._id_map[id_] = index
            cls._name_map[info[0]] = index

    def __init__(self, name=None, value=None, **kwargs):
        """
        Checks to ensure implicit tagging is not being used since it is
        incompatible with Choice, then forwards on to Asn1Value.__init__()

        :param name:
            The name of the alternative to be set - used with value.
            Alternatively this may be a dict with a single key being the name
            and the value being the value, or a two-element tuple of the the
            name and the value.

        :param value:
            The alternative value to set - used with name

        :raises:
            ValueError - when implicit param is passed (or legacy tag_type param is "implicit")
        """
        _tag_type_to_explicit_implicit(kwargs)
        (Asn1Value.__init__)(self, **kwargs)
        try:
            if kwargs.get('implicit') is not None:
                raise ValueError(unwrap('\n                    The Choice type can not be implicitly tagged even if in an\n                    implicit module - due to its nature any tagging must be\n                    explicit\n                    '))
            if name is not None:
                if isinstance(name, dict):
                    if len(name) != 1:
                        raise ValueError(unwrap('\n                            When passing a dict as the "name" argument to %s,\n                            it must have a single key/value - however %d were\n                            present\n                            ', type_name(self), len(name)))
                    name, value = list(name.items())[0]
                else:
                    if isinstance(name, tuple):
                        if len(name) != 2:
                            raise ValueError(unwrap('\n                            When passing a tuple as the "name" argument to %s,\n                            it must have two elements, the name and value -\n                            however %d were present\n                            ', type_name(self), len(name)))
                        value = name[1]
                        name = name[0]
                    if name not in self._name_map:
                        raise ValueError(unwrap('\n                        The name specified, "%s", is not a valid alternative\n                        for %s\n                        ', name, type_name(self)))
                    self._choice = self._name_map[name]
                    _, spec, params = self._alternatives[self._choice]
                    if not isinstance(value, spec):
                        value = spec(value, **params)
                    else:
                        value = _fix_tagging(value, params)
                self._parsed = value
        except (ValueError, TypeError) as e:
            args = e.args[1:]
            e.args = (e.args[0] + '\n    while constructing %s' % type_name(self),) + args
            raise e

    @property
    def name(self):
        """
        :return:
            A unicode string of the field name of the chosen alternative
        """
        if not self._name:
            self._name = self._alternatives[self._choice][0]
        return self._name

    def parse(self):
        """
        Parses the detected alternative

        :return:
            An Asn1Value object of the chosen alternative
        """
        if self._parsed is not None:
            return self._parsed
        try:
            _, spec, params = self._alternatives[self._choice]
            self._parsed, _ = _parse_build((self.contents), spec=spec, spec_params=params)
        except (ValueError, TypeError) as e:
            args = e.args[1:]
            e.args = (e.args[0] + '\n    while parsing %s' % type_name(self),) + args
            raise e

    @property
    def chosen(self):
        """
        :return:
            An Asn1Value object of the chosen alternative
        """
        return self.parse()

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            The .native value from the contained value object
        """
        return self.chosen.native

    def validate(self, class_, tag, contents):
        """
        Ensures that the class and tag specified exist as an alternative

        :param class_:
            The integer class_ from the encoded value header

        :param tag:
            The integer tag from the encoded value header

        :param contents:
            A byte string of the contents of the value - used when the object
            is explicitly tagged

        :raises:
            ValueError - when value is not a valid alternative
        """
        id_ = (
         class_, tag)
        if self.explicit is not None:
            if self.explicit[(-1)] != id_:
                raise ValueError(unwrap('\n                    %s was explicitly tagged, but the value provided does not\n                    match the class and tag\n                    ', type_name(self)))
            (class_, _, tag, _, _, _), _ = _parse(contents, len(contents))
            id_ = (class_, tag)
        if id_ in self._id_map:
            self._choice = self._id_map[id_]
            return
        if self.class_ is not None:
            if self.tag is not None:
                if len(self._alternatives) > 1:
                    raise ValueError(unwrap('\n                    %s was implicitly tagged, but more than one alternative\n                    exists\n                    ', type_name(self)))
                if id_ == (self.class_, self.tag):
                    self._choice = 0
                    return
        asn1 = self._format_class_tag(class_, tag)
        asn1s = [self._format_class_tag(pair[0], pair[1]) for pair in self._id_map]
        raise ValueError(unwrap('\n            Value %s did not match the class and tag of any of the alternatives\n            in %s: %s\n            ', asn1, type_name(self), ', '.join(asn1s)))

    def _format_class_tag(self, class_, tag):
        """
        :return:
            A unicode string of a human-friendly representation of the class and tag
        """
        return '[%s %s]' % (CLASS_NUM_TO_NAME_MAP[class_].upper(), tag)

    def _copy(self, other, copy_func):
        super(Choice, self)._copy(other, copy_func)
        self._choice = other._choice
        self._name = other._name
        self._parsed = copy_func(other._parsed)

    def dump(self, force=False):
        """
        Encodes the value using DER

        :param force:
            If the encoded contents already exist, clear them and regenerate
            to ensure they are in DER format instead of BER format

        :return:
            A byte string of the DER-encoded value
        """
        self.contents = self.chosen.dump(force=force)
        if self._header is None or force:
            self._header = b''
            if self.explicit is not None:
                for class_, tag in self.explicit:
                    self._header = _dump_header(class_, 1, tag, self._header + self.contents) + self._header

        return self._header + self.contents


class Concat(object):
    __doc__ = '\n    A class that contains two or more encoded child values concatentated\n    together. THIS IS NOT PART OF THE ASN.1 SPECIFICATION! This exists to handle\n    the x509.TrustedCertificate() class for OpenSSL certificates containing\n    extra information.\n    '
    _child_specs = None
    _children = None

    @classmethod
    def load(cls, encoded_data, strict=False):
        """
        Loads a BER/DER-encoded byte string using the current class as the spec

        :param encoded_data:
            A byte string of BER or DER encoded data

        :param strict:
            A boolean indicating if trailing data should be forbidden - if so, a
            ValueError will be raised when trailing data exists

        :return:
            A Concat object
        """
        return cls(contents=encoded_data, strict=strict)

    def __init__(self, value=None, contents=None, strict=False):
        """
        :param value:
            A native Python datatype to initialize the object value with

        :param contents:
            A byte string of the encoded contents of the value

        :param strict:
            A boolean indicating if trailing data should be forbidden - if so, a
            ValueError will be raised when trailing data exists in contents

        :raises:
            ValueError - when an error occurs with one of the children
            TypeError - when an error occurs with one of the children
        """
        if contents is not None:
            try:
                contents_len = len(contents)
                self._children = []
                offset = 0
                for spec in self._child_specs:
                    if offset < contents_len:
                        child_value, offset = _parse_build(contents, pointer=offset, spec=spec)
                    else:
                        child_value = spec()
                    self._children.append(child_value)

                if strict:
                    if offset != contents_len:
                        extra_bytes = contents_len - offset
                        raise ValueError('Extra data - %d bytes of trailing data were provided' % extra_bytes)
            except (ValueError, TypeError) as e:
                args = e.args[1:]
                e.args = (e.args[0] + '\n    while constructing %s' % type_name(self),) + args
                raise e

        if value is not None:
            if self._children is None:
                self._children = [
                 None] * len(self._child_specs)
            for index, data in enumerate(value):
                self.__setitem__(index, data)

    def __str__(self):
        """
        Since str is different in Python 2 and 3, this calls the appropriate
        method, __unicode__() or __bytes__()

        :return:
            A unicode string
        """
        if _PY2:
            return self.__bytes__()
        else:
            return self.__unicode__()

    def __bytes__(self):
        """
        A byte string of the DER-encoded contents
        """
        return self.dump()

    def __unicode__(self):
        """
        :return:
            A unicode string
        """
        return repr(self)

    def __repr__(self):
        """
        :return:
            A unicode string
        """
        return '<%s %s %s>' % (type_name(self), id(self), repr(self.dump()))

    def __copy__(self):
        """
        Implements the copy.copy() interface

        :return:
            A new shallow copy of the Concat object
        """
        new_obj = self.__class__()
        new_obj._copy(self, copy.copy)
        return new_obj

    def __deepcopy__(self, memo):
        """
        Implements the copy.deepcopy() interface

        :param memo:
            A dict for memoization

        :return:
            A new deep copy of the Concat object and all child objects
        """
        new_obj = self.__class__()
        memo[id(self)] = new_obj
        new_obj._copy(self, copy.deepcopy)
        return new_obj

    def copy(self):
        """
        Copies the object

        :return:
            A Concat object
        """
        return copy.deepcopy(self)

    def _copy(self, other, copy_func):
        """
        Copies the contents of another Concat object to itself

        :param object:
            Another instance of the same class

        :param copy_func:
            An reference of copy.copy() or copy.deepcopy() to use when copying
            lists, dicts and objects
        """
        if self.__class__ != other.__class__:
            raise TypeError(unwrap('\n                Can not copy values from %s object to %s object\n                ', type_name(other), type_name(self)))
        self._children = copy_func(other._children)

    def debug(self, nest_level=1):
        """
        Show the binary data and parsed data in a tree structure
        """
        prefix = '  ' * nest_level
        print('%s%s Object #%s' % (prefix, type_name(self), id(self)))
        print('%s  Children:' % (prefix,))
        for child in self._children:
            child.debug(nest_level + 2)

    def dump(self, force=False):
        """
        Encodes the value using DER

        :param force:
            If the encoded contents already exist, clear them and regenerate
            to ensure they are in DER format instead of BER format

        :return:
            A byte string of the DER-encoded value
        """
        contents = b''
        for child in self._children:
            contents += child.dump(force=force)

        return contents

    @property
    def contents(self):
        """
        :return:
            A byte string of the DER-encoded contents of the children
        """
        return self.dump()

    def __len__(self):
        """
        :return:
            Integer
        """
        return len(self._children)

    def __getitem__(self, key):
        """
        Allows accessing children by index

        :param key:
            An integer of the child index

        :raises:
            KeyError - when an index is invalid

        :return:
            The Asn1Value object of the child specified
        """
        if key > len(self._child_specs) - 1 or key < 0:
            raise KeyError(unwrap('\n                No child is definition for position %d of %s\n                ', key, type_name(self)))
        return self._children[key]

    def __setitem__(self, key, value):
        """
        Allows settings children by index

        :param key:
            An integer of the child index

        :param value:
            An Asn1Value object to set the child to

        :raises:
            KeyError - when an index is invalid
            ValueError - when the value is not an instance of Asn1Value
        """
        if key > len(self._child_specs) - 1 or key < 0:
            raise KeyError(unwrap('\n                No child is defined for position %d of %s\n                ', key, type_name(self)))
        if not isinstance(value, Asn1Value):
            raise ValueError(unwrap('\n                Value for child %s of %s is not an instance of\n                asn1crypto.core.Asn1Value\n                ', key, type_name(self)))
        self._children[key] = value

    def __iter__(self):
        """
        :return:
            An iterator of child values
        """
        return iter(self._children)


class Primitive(Asn1Value):
    __doc__ = '\n    Sets the class_ and method attributes for primitive, universal values\n    '
    class_ = 0
    method = 0

    def __init__(self, value=None, default=None, contents=None, **kwargs):
        """
        Sets the value of the object before passing to Asn1Value.__init__()

        :param value:
            A native Python datatype to initialize the object value with

        :param default:
            The default value if no value is specified

        :param contents:
            A byte string of the encoded contents of the value
        """
        (Asn1Value.__init__)(self, **kwargs)
        try:
            if contents is not None:
                self.contents = contents
            else:
                if value is not None:
                    self.set(value)
                else:
                    if default is not None:
                        self.set(default)
        except (ValueError, TypeError) as e:
            args = e.args[1:]
            e.args = (e.args[0] + '\n    while constructing %s' % type_name(self),) + args
            raise e

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            A byte string
        """
        if not isinstance(value, byte_cls):
            raise TypeError(unwrap('\n                %s value must be a byte string, not %s\n                ', type_name(self), type_name(value)))
        self._native = value
        self.contents = value
        self._header = None
        if self._trailer != b'':
            self._trailer = b''

    def dump(self, force=False):
        """
        Encodes the value using DER

        :param force:
            If the encoded contents already exist, clear them and regenerate
            to ensure they are in DER format instead of BER format

        :return:
            A byte string of the DER-encoded value
        """
        if force:
            native = self.native
            self.contents = None
            self.set(native)
        return Asn1Value.dump(self)

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        """
        :param other:
            The other Primitive to compare to

        :return:
            A boolean
        """
        if not isinstance(other, Primitive):
            return False
        else:
            if self.contents != other.contents:
                return False
            else:
                if self.__class__.tag != other.__class__.tag:
                    return False
                else:
                    if self.__class__ == other.__class__:
                        if self.contents == other.contents:
                            return True
                    self_bases = (set(self.__class__.__bases__) | set([self.__class__])) - set([Asn1Value, Primitive, ValueMap])
                    other_bases = (set(other.__class__.__bases__) | set([other.__class__])) - set([Asn1Value, Primitive, ValueMap])
                    if self_bases | other_bases:
                        return self.contents == other.contents
                if self.implicit or self.explicit or other.implicit or other.explicit:
                    return self.untag().dump() == other.untag().dump()
            return self.dump() == other.dump()


class AbstractString(Constructable, Primitive):
    __doc__ = '\n    A base class for all strings that have a known encoding. In general, we do\n    not worry ourselves with confirming that the decoded values match a specific\n    set of characters, only that they are decoded into a Python unicode string\n    '
    _encoding = 'latin1'
    _unicode = None

    def set(self, value):
        """
        Sets the value of the string

        :param value:
            A unicode string
        """
        if not isinstance(value, str_cls):
            raise TypeError(unwrap('\n                %s value must be a unicode string, not %s\n                ', type_name(self), type_name(value)))
        else:
            self._unicode = value
            self.contents = value.encode(self._encoding)
            self._header = None
            if self._indefinite:
                self._indefinite = False
                self.method = 0
            if self._trailer != b'':
                self._trailer = b''

    def __unicode__(self):
        """
        :return:
            A unicode string
        """
        if self.contents is None:
            return ''
        else:
            if self._unicode is None:
                self._unicode = self._merge_chunks().decode(self._encoding)
            return self._unicode

    def _copy(self, other, copy_func):
        super(AbstractString, self)._copy(other, copy_func)
        self._unicode = other._unicode

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            A unicode string or None
        """
        if self.contents is None:
            return
        else:
            return self.__unicode__()


class Boolean(Primitive):
    __doc__ = '\n    Represents a boolean in both ASN.1 and Python\n    '
    tag = 1

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            True, False or another value that works with bool()
        """
        self._native = bool(value)
        self.contents = b'\x00' if not value else b'\xff'
        self._header = None
        if self._trailer != b'':
            self._trailer = b''

    def __nonzero__(self):
        """
        :return:
            True or False
        """
        return self.__bool__()

    def __bool__(self):
        """
        :return:
            True or False
        """
        return self.contents != b'\x00'

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            True, False or None
        """
        if self.contents is None:
            return
        else:
            if self._native is None:
                self._native = self.__bool__()
            return self._native


class Integer(Primitive, ValueMap):
    __doc__ = '\n    Represents an integer in both ASN.1 and Python\n    '
    tag = 2

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            An integer, or a unicode string if _map is set

        :raises:
            ValueError - when an invalid value is passed
        """
        if isinstance(value, str_cls):
            if self._map is None:
                raise ValueError(unwrap('\n                    %s value is a unicode string, but no _map provided\n                    ', type_name(self)))
            if value not in self._reverse_map:
                raise ValueError(unwrap('\n                    %s value, %s, is not present in the _map\n                    ', type_name(self), value))
            value = self._reverse_map[value]
        else:
            if not isinstance(value, int_types):
                raise TypeError(unwrap('\n                %s value must be an integer or unicode string when a name_map\n                is provided, not %s\n                ', type_name(self), type_name(value)))
        self._native = self._map[value] if (self._map and value in self._map) else value
        self.contents = int_to_bytes(value, signed=True)
        self._header = None
        if self._trailer != b'':
            self._trailer = b''

    def __int__(self):
        """
        :return:
            An integer
        """
        return int_from_bytes((self.contents), signed=True)

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            An integer or None
        """
        if self.contents is None:
            return
        else:
            if self._native is None:
                self._native = self.__int__()
                if self._map is not None:
                    if self._native in self._map:
                        self._native = self._map[self._native]
            return self._native


class BitString(Constructable, Castable, Primitive, ValueMap, object):
    __doc__ = '\n    Represents a bit string from ASN.1 as a Python tuple of 1s and 0s\n    '
    tag = 3
    _size = None
    _chunk = None
    _chunks_offset = 1

    def _setup(self):
        """
        Generates _reverse_map from _map
        """
        ValueMap._setup(self)
        cls = self.__class__
        if cls._map is not None:
            cls._size = max(self._map.keys()) + 1

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            An integer or a tuple of integers 0 and 1

        :raises:
            ValueError - when an invalid value is passed
        """
        if isinstance(value, set):
            if self._map is None:
                raise ValueError(unwrap('\n                    %s._map has not been defined\n                    ', type_name(self)))
            bits = [
             0] * self._size
            self._native = value
            for index in range(0, self._size):
                key = self._map.get(index)
                if key is None:
                    continue
                if key in value:
                    bits[index] = 1

            value = ''.join(map(str_cls, bits))
        else:
            if value.__class__ == tuple:
                if self._map is None:
                    self._native = value
                else:
                    self._native = set()
                    for index, bit in enumerate(value):
                        if bit:
                            name = self._map.get(index, index)
                            self._native.add(name)

                value = ''.join(map(str_cls, value))
            else:
                raise TypeError(unwrap('\n                %s value must be a tuple of ones and zeros or a set of unicode\n                strings, not %s\n                ', type_name(self), type_name(value)))
            self._chunk = None
            if self._map is not None:
                if len(value) > self._size:
                    raise ValueError(unwrap('\n                    %s value must be at most %s bits long, specified was %s long\n                    ', type_name(self), self._size, len(value)))
                value = value.rstrip('0')
            size = len(value)
            size_mod = size % 8
            extra_bits = 0
            if size_mod != 0:
                extra_bits = 8 - size_mod
                value += '0' * extra_bits
            size_in_bytes = int(math.ceil(size / 8))
            if extra_bits:
                extra_bits_byte = int_to_bytes(extra_bits)
            else:
                extra_bits_byte = b'\x00'
            if value == '':
                value_bytes = b''
            else:
                value_bytes = int_to_bytes(int(value, 2))
            if len(value_bytes) != size_in_bytes:
                value_bytes = b'\x00' * (size_in_bytes - len(value_bytes)) + value_bytes
            self.contents = extra_bits_byte + value_bytes
            self._header = None
            if self._indefinite:
                self._indefinite = False
                self.method = 0
            if self._trailer != b'':
                self._trailer = b''

    def __getitem__(self, key):
        """
        Retrieves a boolean version of one of the bits based on a name from the
        _map

        :param key:
            The unicode string of one of the bit names

        :raises:
            ValueError - when _map is not set or the key name is invalid

        :return:
            A boolean if the bit is set
        """
        is_int = isinstance(key, int_types)
        if not is_int:
            if not isinstance(self._map, dict):
                raise ValueError(unwrap('\n                    %s._map has not been defined\n                    ', type_name(self)))
            if key not in self._reverse_map:
                raise ValueError(unwrap('\n                    %s._map does not contain an entry for "%s"\n                    ', type_name(self), key))
        if self._native is None:
            self.native
        if self._map is None:
            if len(self._native) >= key + 1:
                return bool(self._native[key])
            return False
        else:
            if is_int:
                key = self._map.get(key, key)
            return key in self._native

    def __setitem__(self, key, value):
        """
        Sets one of the bits based on a name from the _map

        :param key:
            The unicode string of one of the bit names

        :param value:
            A boolean value

        :raises:
            ValueError - when _map is not set or the key name is invalid
        """
        is_int = isinstance(key, int_types)
        if not is_int:
            if self._map is None:
                raise ValueError(unwrap('\n                    %s._map has not been defined\n                    ', type_name(self)))
            if key not in self._reverse_map:
                raise ValueError(unwrap('\n                    %s._map does not contain an entry for "%s"\n                    ', type_name(self), key))
        if self._native is None:
            self.native
        if self._map is None:
            new_native = list(self._native)
            max_key = len(new_native) - 1
            if key > max_key:
                new_native.extend([0] * (key - max_key))
            new_native[key] = 1 if value else 0
            self._native = tuple(new_native)
        else:
            if is_int:
                key = self._map.get(key, key)
            if value:
                if key not in self._native:
                    self._native.add(key)
            else:
                if key in self._native:
                    self._native.remove(key)
        self.set(self._native)

    def _as_chunk(self):
        """
        Allows reconstructing indefinite length values

        :return:
            A tuple of integers
        """
        extra_bits = int_from_bytes(self.contents[0:1])
        bit_string = '{0:b}'.format(int_from_bytes(self.contents[1:]))
        byte_len = len(self.contents[1:])
        bit_len = len(bit_string)
        mod_bit_len = bit_len % 8
        if mod_bit_len != 0:
            bit_string = '0' * (8 - mod_bit_len) + bit_string
            bit_len = len(bit_string)
        if bit_len // 8 < byte_len:
            missing_bytes = byte_len - bit_len // 8
            bit_string = '0' * (8 * missing_bytes) + bit_string
        if extra_bits > 0:
            bit_string = bit_string[0:0 - extra_bits]
        return tuple(map(int, tuple(bit_string)))

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            If a _map is set, a set of names, or if no _map is set, a tuple of
            integers 1 and 0. None if no value.
        """
        if self.contents is None:
            if self._map is None:
                self.set(())
            else:
                self.set(set())
        if self._native is None:
            bits = self._merge_chunks()
            if self._map:
                self._native = set()
                for index, bit in enumerate(bits):
                    if bit:
                        name = self._map.get(index, index)
                        self._native.add(name)

            else:
                self._native = bits
        return self._native


class OctetBitString(Constructable, Castable, Primitive):
    __doc__ = '\n    Represents a bit string in ASN.1 as a Python byte string\n    '
    tag = 3
    _chunks_offset = 1
    _bytes = None

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            A byte string

        :raises:
            ValueError - when an invalid value is passed
        """
        if not isinstance(value, byte_cls):
            raise TypeError(unwrap('\n                %s value must be a byte string, not %s\n                ', type_name(self), type_name(value)))
        else:
            self._bytes = value
            self.contents = b'\x00' + value
            self._header = None
            if self._indefinite:
                self._indefinite = False
                self.method = 0
            if self._trailer != b'':
                self._trailer = b''

    def __bytes__(self):
        """
        :return:
            A byte string
        """
        if self.contents is None:
            return b''
        else:
            if self._bytes is None:
                self._bytes = self._merge_chunks()
            return self._bytes

    def _copy(self, other, copy_func):
        super(OctetBitString, self)._copy(other, copy_func)
        self._bytes = other._bytes

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            A byte string or None
        """
        if self.contents is None:
            return
        else:
            return self.__bytes__()


class IntegerBitString(Constructable, Castable, Primitive):
    __doc__ = '\n    Represents a bit string in ASN.1 as a Python integer\n    '
    tag = 3
    _chunks_offset = 1

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            An integer

        :raises:
            ValueError - when an invalid value is passed
        """
        if not isinstance(value, int_types):
            raise TypeError(unwrap('\n                %s value must be an integer, not %s\n                ', type_name(self), type_name(value)))
        else:
            self._native = value
            self.contents = b'\x00' + int_to_bytes(value, signed=True)
            self._header = None
            if self._indefinite:
                self._indefinite = False
                self.method = 0
            if self._trailer != b'':
                self._trailer = b''

    def _as_chunk(self):
        """
        Allows reconstructing indefinite length values

        :return:
            A unicode string of bits - 1s and 0s
        """
        extra_bits = int_from_bytes(self.contents[0:1])
        bit_string = '{0:b}'.format(int_from_bytes(self.contents[1:]))
        mod_bit_len = len(bit_string) % 8
        if mod_bit_len != 0:
            bit_string = '0' * (8 - mod_bit_len) + bit_string
        if extra_bits > 0:
            return bit_string[0:0 - extra_bits]
        else:
            return bit_string

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            An integer or None
        """
        if self.contents is None:
            return
        else:
            if self._native is None:
                extra_bits = int_from_bytes(self.contents[0:1])
                if not self._indefinite:
                    if extra_bits == 0:
                        self._native = int_from_bytes(self.contents[1:])
                else:
                    if self._indefinite:
                        if extra_bits > 0:
                            raise ValueError('Constructed bit string has extra bits on indefinite container')
                    self._native = int(self._merge_chunks(), 2)
            return self._native


class OctetString(Constructable, Castable, Primitive):
    __doc__ = '\n    Represents a byte string in both ASN.1 and Python\n    '
    tag = 4
    _bytes = None

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            A byte string
        """
        if not isinstance(value, byte_cls):
            raise TypeError(unwrap('\n                %s value must be a byte string, not %s\n                ', type_name(self), type_name(value)))
        else:
            self._bytes = value
            self.contents = value
            self._header = None
            if self._indefinite:
                self._indefinite = False
                self.method = 0
            if self._trailer != b'':
                self._trailer = b''

    def __bytes__(self):
        """
        :return:
            A byte string
        """
        if self.contents is None:
            return b''
        else:
            if self._bytes is None:
                self._bytes = self._merge_chunks()
            return self._bytes

    def _copy(self, other, copy_func):
        super(OctetString, self)._copy(other, copy_func)
        self._bytes = other._bytes

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            A byte string or None
        """
        if self.contents is None:
            return
        else:
            return self.__bytes__()


class IntegerOctetString(Constructable, Castable, Primitive):
    __doc__ = '\n    Represents a byte string in ASN.1 as a Python integer\n    '
    tag = 4

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            An integer

        :raises:
            ValueError - when an invalid value is passed
        """
        if not isinstance(value, int_types):
            raise TypeError(unwrap('\n                %s value must be an integer, not %s\n                ', type_name(self), type_name(value)))
        else:
            self._native = value
            self.contents = int_to_bytes(value, signed=False)
            self._header = None
            if self._indefinite:
                self._indefinite = False
                self.method = 0
            if self._trailer != b'':
                self._trailer = b''

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            An integer or None
        """
        if self.contents is None:
            return
        else:
            if self._native is None:
                self._native = int_from_bytes(self._merge_chunks())
            return self._native


class ParsableOctetString(Constructable, Castable, Primitive):
    tag = 4
    _parsed = None
    _bytes = None

    def __init__(self, value=None, parsed=None, **kwargs):
        """
        Allows providing a parsed object that will be serialized to get the
        byte string value

        :param value:
            A native Python datatype to initialize the object value with

        :param parsed:
            If value is None and this is an Asn1Value object, this will be
            set as the parsed value, and the value will be obtained by calling
            .dump() on this object.
        """
        set_parsed = False
        if value is None:
            if parsed is not None:
                if isinstance(parsed, Asn1Value):
                    value = parsed.dump()
                    set_parsed = True
        (Primitive.__init__)(self, value=value, **kwargs)
        if set_parsed:
            self._parsed = (
             parsed, parsed.__class__, None)

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            A byte string
        """
        if not isinstance(value, byte_cls):
            raise TypeError(unwrap('\n                %s value must be a byte string, not %s\n                ', type_name(self), type_name(value)))
        else:
            self._bytes = value
            self.contents = value
            self._header = None
            if self._indefinite:
                self._indefinite = False
                self.method = 0
            if self._trailer != b'':
                self._trailer = b''

    def parse(self, spec=None, spec_params=None):
        """
        Parses the contents generically, or using a spec with optional params

        :param spec:
            A class derived from Asn1Value that defines what class_ and tag the
            value should have, and the semantics of the encoded value. The
            return value will be of this type. If omitted, the encoded value
            will be decoded using the standard universal tag based on the
            encoded tag number.

        :param spec_params:
            A dict of params to pass to the spec object

        :return:
            An object of the type spec, or if not present, a child of Asn1Value
        """
        if self._parsed is None or self._parsed[1:3] != (spec, spec_params):
            parsed_value, _ = _parse_build((self.__bytes__()), spec=spec, spec_params=spec_params)
            self._parsed = (parsed_value, spec, spec_params)
        return self._parsed[0]

    def __bytes__(self):
        """
        :return:
            A byte string
        """
        if self.contents is None:
            return b''
        else:
            if self._bytes is None:
                self._bytes = self._merge_chunks()
            return self._bytes

    def _copy(self, other, copy_func):
        super(ParsableOctetString, self)._copy(other, copy_func)
        self._bytes = other._bytes
        self._parsed = copy_func(other._parsed)

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            A byte string or None
        """
        if self.contents is None:
            return
        else:
            if self._parsed is not None:
                return self._parsed[0].native
            return self.__bytes__()

    @property
    def parsed(self):
        """
        Returns the parsed object from .parse()

        :return:
            The object returned by .parse()
        """
        if self._parsed is None:
            self.parse()
        return self._parsed[0]

    def dump(self, force=False):
        """
        Encodes the value using DER

        :param force:
            If the encoded contents already exist, clear them and regenerate
            to ensure they are in DER format instead of BER format

        :return:
            A byte string of the DER-encoded value
        """
        if force:
            if self._parsed is not None:
                native = self.parsed.dump(force=force)
            else:
                native = self.native
            self.contents = None
            self.set(native)
        return Asn1Value.dump(self)


class ParsableOctetBitString(ParsableOctetString):
    tag = 3
    _chunks_offset = 1

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            A byte string

        :raises:
            ValueError - when an invalid value is passed
        """
        if not isinstance(value, byte_cls):
            raise TypeError(unwrap('\n                %s value must be a byte string, not %s\n                ', type_name(self), type_name(value)))
        else:
            self._bytes = value
            self.contents = b'\x00' + value
            self._header = None
            if self._indefinite:
                self._indefinite = False
                self.method = 0
            if self._trailer != b'':
                self._trailer = b''


class Null(Primitive):
    __doc__ = '\n    Represents a null value in ASN.1 as None in Python\n    '
    tag = 5
    contents = b''

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            None
        """
        self.contents = b''

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            None
        """
        pass


class ObjectIdentifier(Primitive, ValueMap):
    __doc__ = '\n    Represents an object identifier in ASN.1 as a Python unicode dotted\n    integer string\n    '
    tag = 6
    _dotted = None

    @classmethod
    def map(cls, value):
        """
        Converts a dotted unicode string OID into a mapped unicode string

        :param value:
            A dotted unicode string OID

        :raises:
            ValueError - when no _map dict has been defined on the class
            TypeError - when value is not a unicode string

        :return:
            A mapped unicode string
        """
        if cls._map is None:
            raise ValueError(unwrap('\n                %s._map has not been defined\n                ', type_name(cls)))
        if not isinstance(value, str_cls):
            raise TypeError(unwrap('\n                value must be a unicode string, not %s\n                ', type_name(value)))
        return cls._map.get(value, value)

    @classmethod
    def unmap(cls, value):
        """
        Converts a mapped unicode string value into a dotted unicode string OID

        :param value:
            A mapped unicode string OR dotted unicode string OID

        :raises:
            ValueError - when no _map dict has been defined on the class or the value can't be unmapped
            TypeError - when value is not a unicode string

        :return:
            A dotted unicode string OID
        """
        if cls not in _SETUP_CLASSES:
            cls()._setup()
            _SETUP_CLASSES[cls] = True
        else:
            if cls._map is None:
                raise ValueError(unwrap('\n                %s._map has not been defined\n                ', type_name(cls)))
            raise isinstance(value, str_cls) or TypeError(unwrap('\n                value must be a unicode string, not %s\n                ', type_name(value)))
        if value in cls._reverse_map:
            return cls._reverse_map[value]
        else:
            if not _OID_RE.match(value):
                raise ValueError(unwrap('\n                %s._map does not contain an entry for "%s"\n                ', type_name(cls), value))
            return value

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            A unicode string. May be a dotted integer string, or if _map is
            provided, one of the mapped values.

        :raises:
            ValueError - when an invalid value is passed
        """
        if not isinstance(value, str_cls):
            raise TypeError(unwrap('\n                %s value must be a unicode string, not %s\n                ', type_name(self), type_name(value)))
        else:
            self._native = value
            if self._map is not None:
                if value in self._reverse_map:
                    value = self._reverse_map[value]
            self.contents = b''
            first = None
            for index, part in enumerate(value.split('.')):
                part = int(part)
                if index == 0:
                    first = part
                    continue
                else:
                    if index == 1:
                        part = first * 40 + part
                encoded_part = chr_cls(127 & part)
                part = part >> 7
                while part > 0:
                    encoded_part = chr_cls(128 | 127 & part) + encoded_part
                    part = part >> 7

                self.contents += encoded_part

            self._header = None
            if self._trailer != b'':
                self._trailer = b''

    def __unicode__(self):
        """
        :return:
            A unicode string
        """
        return self.dotted

    @property
    def dotted(self):
        """
        :return:
            A unicode string of the object identifier in dotted notation, thus
            ignoring any mapped value
        """
        if self._dotted is None:
            output = []
            part = 0
            for byte in self.contents:
                if _PY2:
                    byte = ord(byte)
                part = part * 128
                part += byte & 127
                if byte & 128 == 0:
                    if len(output) == 0:
                        output.append(str_cls(part // 40))
                        output.append(str_cls(part % 40))
                    else:
                        output.append(str_cls(part))
                    part = 0

            self._dotted = '.'.join(output)
        return self._dotted

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            A unicode string or None. If _map is not defined, the unicode string
            is a string of dotted integers. If _map is defined and the dotted
            string is present in the _map, the mapped value is returned.
        """
        if self.contents is None:
            return
        else:
            if self._native is None:
                self._native = self.dotted
                if self._map is not None:
                    if self._native in self._map:
                        self._native = self._map[self._native]
            return self._native


class ObjectDescriptor(Primitive):
    __doc__ = '\n    Represents an object descriptor from ASN.1 - no Python implementation\n    '
    tag = 7


class InstanceOf(Primitive):
    __doc__ = '\n    Represents an instance from ASN.1 - no Python implementation\n    '
    tag = 8


class Real(Primitive):
    __doc__ = '\n    Represents a real number from ASN.1 - no Python implementation\n    '
    tag = 9


class Enumerated(Integer):
    __doc__ = '\n    Represents a enumerated list of integers from ASN.1 as a Python\n    unicode string\n    '
    tag = 10

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            An integer or a unicode string from _map

        :raises:
            ValueError - when an invalid value is passed
        """
        if not isinstance(value, int_types):
            if not isinstance(value, str_cls):
                raise TypeError(unwrap('\n                %s value must be an integer or a unicode string, not %s\n                ', type_name(self), type_name(value)))
        if isinstance(value, str_cls):
            if value not in self._reverse_map:
                raise ValueError(unwrap('\n                    %s value "%s" is not a valid value\n                    ', type_name(self), value))
            value = self._reverse_map[value]
        else:
            if value not in self._map:
                raise ValueError(unwrap('\n                %s value %s is not a valid value\n                ', type_name(self), value))
        Integer.set(self, value)

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            A unicode string or None
        """
        if self.contents is None:
            return
        else:
            if self._native is None:
                self._native = self._map[self.__int__()]
            return self._native


class UTF8String(AbstractString):
    __doc__ = '\n    Represents a UTF-8 string from ASN.1 as a Python unicode string\n    '
    tag = 12
    _encoding = 'utf-8'


class RelativeOid(ObjectIdentifier):
    __doc__ = '\n    Represents an object identifier in ASN.1 as a Python unicode dotted\n    integer string\n    '
    tag = 13


class Sequence(Asn1Value):
    __doc__ = '\n    Represents a sequence of fields from ASN.1 as a Python object with a\n    dict-like interface\n    '
    tag = 16
    class_ = 0
    method = 1
    children = None
    _contents = None
    _mutated = False
    _fields = []
    _spec_callbacks = None
    _field_map = None
    _field_ids = None
    _oid_pair = None
    _oid_specs = None
    _oid_nums = None
    _precomputed_specs = None

    def __init__(self, value=None, default=None, **kwargs):
        """
        Allows setting field values before passing everything else along to
        Asn1Value.__init__()

        :param value:
            A native Python datatype to initialize the object value with

        :param default:
            The default value if no value is specified
        """
        (Asn1Value.__init__)(self, **kwargs)
        check_existing = False
        if value is None:
            if default is not None:
                check_existing = True
                if self.children is None:
                    if self.contents is None:
                        check_existing = False
                    else:
                        self._parse_children()
                value = default
        if value is not None:
            try:
                if self._fields:
                    keys = [info[0] for info in self._fields]
                    unused_keys = set(value.keys())
                else:
                    keys = value.keys()
                    unused_keys = set(keys)
                for key in keys:
                    if check_existing:
                        index = self._field_map[key]
                        if index < len(self.children):
                            if self.children[index] is not VOID:
                                if key in unused_keys:
                                    unused_keys.remove(key)
                                    continue
                        if key in value:
                            self.__setitem__(key, value[key])
                            unused_keys.remove(key)

                if len(unused_keys):
                    raise ValueError(unwrap('\n                        One or more unknown fields was passed to the constructor\n                        of %s: %s\n                        ', type_name(self), ', '.join(sorted(list(unused_keys)))))
            except (ValueError, TypeError) as e:
                args = e.args[1:]
                e.args = (e.args[0] + '\n    while constructing %s' % type_name(self),) + args
                raise e

    @property
    def contents(self):
        """
        :return:
            A byte string of the DER-encoded contents of the sequence
        """
        if self.children is None:
            return self._contents
        else:
            if self._is_mutated():
                self._set_contents()
            return self._contents

    @contents.setter
    def contents(self, value):
        """
        :param value:
            A byte string of the DER-encoded contents of the sequence
        """
        self._contents = value

    def _is_mutated(self):
        """
        :return:
            A boolean - if the sequence or any children (recursively) have been
            mutated
        """
        mutated = self._mutated
        if self.children is not None:
            for child in self.children:
                if isinstance(child, Sequence) or isinstance(child, SequenceOf):
                    mutated = mutated or child._is_mutated()

        return mutated

    def _lazy_child(self, index):
        """
        Builds a child object if the child has only been parsed into a tuple so far
        """
        child = self.children[index]
        if child.__class__ == tuple:
            child = self.children[index] = _build(*child)
        return child

    def __len__(self):
        """
        :return:
            Integer
        """
        if self.children is None:
            self._parse_children()
        return len(self.children)

    def __getitem__(self, key):
        """
        Allows accessing fields by name or index

        :param key:
            A unicode string of the field name, or an integer of the field index

        :raises:
            KeyError - when a field name or index is invalid

        :return:
            The Asn1Value object of the field specified
        """
        if self.children is None:
            self._parse_children()
        else:
            if not isinstance(key, int_types):
                if key not in self._field_map:
                    raise KeyError(unwrap('\n                    No field named "%s" defined for %s\n                    ', key, type_name(self)))
                key = self._field_map[key]
            if key >= len(self.children):
                raise KeyError(unwrap('\n                No field numbered %s is present in this %s\n                ', key, type_name(self)))
            try:
                return self._lazy_child(key)
            except (ValueError, TypeError) as e:
                args = e.args[1:]
                e.args = (e.args[0] + '\n    while parsing %s' % type_name(self),) + args
                raise e

    def __setitem__(self, key, value):
        """
        Allows settings fields by name or index

        :param key:
            A unicode string of the field name, or an integer of the field index

        :param value:
            A native Python datatype to set the field value to. This method will
            construct the appropriate Asn1Value object from _fields.

        :raises:
            ValueError - when a field name or index is invalid
        """
        if self.children is None:
            self._parse_children()
        else:
            if not isinstance(key, int_types):
                if key not in self._field_map:
                    raise KeyError(unwrap('\n                    No field named "%s" defined for %s\n                    ', key, type_name(self)))
                key = self._field_map[key]
            else:
                field_name, field_spec, value_spec, field_params, _ = self._determine_spec(key)
                new_value = self._make_value(field_name, field_spec, value_spec, field_params, value)
                invalid_value = False
                if isinstance(new_value, Any):
                    invalid_value = new_value.parsed is None
                else:
                    if isinstance(new_value, Choice):
                        invalid_value = new_value.chosen.contents is None
                    else:
                        invalid_value = new_value.contents is None
            if invalid_value:
                raise ValueError(unwrap('\n                Value for field "%s" of %s is not set\n                ', field_name, type_name(self)))
            self.children[key] = new_value
            if self._native is not None:
                self._native[self._fields[key][0]] = self.children[key].native
        self._mutated = True

    def __delitem__(self, key):
        """
        Allows deleting optional or default fields by name or index

        :param key:
            A unicode string of the field name, or an integer of the field index

        :raises:
            ValueError - when a field name or index is invalid, or the field is not optional or defaulted
        """
        if self.children is None:
            self._parse_children()
        elif not isinstance(key, int_types):
            if key not in self._field_map:
                raise KeyError(unwrap('\n                    No field named "%s" defined for %s\n                    ', key, type_name(self)))
            key = self._field_map[key]
        else:
            name, _, params = self._fields[key]
            if not params or 'default' not in params and 'optional' not in params:
                raise ValueError(unwrap('\n                Can not delete the value for the field "%s" of %s since it is\n                not optional or defaulted\n                ', name, type_name(self)))
            if 'optional' in params:
                self.children[key] = VOID
                if self._native is not None:
                    self._native[name] = None
            else:
                self.__setitem__(key, None)
        self._mutated = True

    def __iter__(self):
        """
        :return:
            An iterator of field key names
        """
        for info in self._fields:
            yield info[0]

    def _set_contents(self, force=False):
        """
        Updates the .contents attribute of the value with the encoded value of
        all of the child objects

        :param force:
            Ensure all contents are in DER format instead of possibly using
            cached BER-encoded data
        """
        if self.children is None:
            self._parse_children()
        contents = BytesIO()
        for index, info in enumerate(self._fields):
            child = self.children[index]
            if child is None:
                child_dump = b''
            else:
                if child.__class__ == tuple:
                    if force:
                        child_dump = self._lazy_child(index).dump(force=force)
                    else:
                        child_dump = child[3] + child[4] + child[5]
                else:
                    child_dump = child.dump(force=force)
            if info[2]:
                if 'default' in info[2]:
                    default_value = (info[1])(**info[2])
                    if default_value.dump() == child_dump:
                        continue
            contents.write(child_dump)

        self._contents = contents.getvalue()
        self._header = None
        if self._trailer != b'':
            self._trailer = b''

    def _setup(self):
        """
        Generates _field_map, _field_ids and _oid_nums for use in parsing
        """
        cls = self.__class__
        cls._field_map = {}
        cls._field_ids = []
        cls._precomputed_specs = []
        for index, field in enumerate(cls._fields):
            if len(field) < 3:
                field = field + ({},)
                cls._fields[index] = field
            cls._field_map[field[0]] = index
            cls._field_ids.append(_build_id_tuple(field[2], field[1]))

        if cls._oid_pair is not None:
            cls._oid_nums = (
             cls._field_map[cls._oid_pair[0]], cls._field_map[cls._oid_pair[1]])
        for index, field in enumerate(cls._fields):
            has_callback = cls._spec_callbacks is not None and field[0] in cls._spec_callbacks
            is_mapped_oid = cls._oid_nums is not None and cls._oid_nums[1] == index
            if has_callback or is_mapped_oid:
                cls._precomputed_specs.append(None)
            else:
                cls._precomputed_specs.append((field[0], field[1], field[1], field[2], None))

    def _determine_spec--- This code section failed: ---

 L.3469         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _fields
                4  LOAD_FAST                'index'
                6  BINARY_SUBSCR    
                8  UNPACK_SEQUENCE_3     3 
               10  STORE_FAST               'name'
               12  STORE_FAST               'field_spec'
               14  STORE_FAST               'field_params'

 L.3470        16  LOAD_FAST                'field_spec'
               18  STORE_FAST               'value_spec'

 L.3471        20  LOAD_CONST               None
               22  STORE_FAST               'spec_override'

 L.3473        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _spec_callbacks
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE   142  'to 142'
               34  LOAD_FAST                'name'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _spec_callbacks
               40  COMPARE_OP               in
               42  POP_JUMP_IF_FALSE   142  'to 142'

 L.3474        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _spec_callbacks
               48  LOAD_FAST                'name'
               50  BINARY_SUBSCR    
               52  STORE_FAST               'callback'

 L.3475        54  LOAD_FAST                'callback'
               56  LOAD_FAST                'self'
               58  CALL_FUNCTION_1       1  '1 positional argument'
               60  STORE_FAST               'spec_override'

 L.3476        62  LOAD_FAST                'spec_override'
               64  POP_JUMP_IF_FALSE   208  'to 208'

 L.3479        66  LOAD_FAST                'spec_override'
               68  LOAD_ATTR                __class__
               70  LOAD_GLOBAL              tuple
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE   114  'to 114'
               76  LOAD_GLOBAL              len
               78  LOAD_FAST                'spec_override'
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  LOAD_CONST               2
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   114  'to 114'

 L.3480        88  LOAD_FAST                'spec_override'
               90  UNPACK_SEQUENCE_2     2 
               92  STORE_FAST               'field_spec'
               94  STORE_FAST               'value_spec'

 L.3481        96  LOAD_FAST                'value_spec'
               98  LOAD_CONST               None
              100  COMPARE_OP               is
              102  POP_JUMP_IF_FALSE   140  'to 140'

 L.3482       104  LOAD_FAST                'field_spec'
              106  STORE_FAST               'value_spec'

 L.3483       108  LOAD_CONST               None
              110  STORE_FAST               'spec_override'
              112  JUMP_ABSOLUTE       208  'to 208'
            114_0  COME_FROM            74  '74'

 L.3485       114  LOAD_FAST                'field_spec'
              116  LOAD_CONST               None
              118  COMPARE_OP               is
              120  POP_JUMP_IF_FALSE   136  'to 136'

 L.3486       122  LOAD_FAST                'spec_override'
              124  STORE_FAST               'field_spec'

 L.3487       126  LOAD_FAST                'field_spec'
              128  STORE_FAST               'value_spec'

 L.3488       130  LOAD_CONST               None
              132  STORE_FAST               'spec_override'
              134  JUMP_ABSOLUTE       208  'to 208'
              136  ELSE                     '140'

 L.3490       136  LOAD_FAST                'spec_override'
              138  STORE_FAST               'value_spec'
            140_0  COME_FROM           102  '102'
              140  JUMP_FORWARD        208  'to 208'
            142_0  COME_FROM            32  '32'

 L.3492       142  LOAD_FAST                'self'
              144  LOAD_ATTR                _oid_nums
              146  LOAD_CONST               None
              148  COMPARE_OP               is-not
              150  POP_JUMP_IF_FALSE   208  'to 208'
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                _oid_nums
              156  LOAD_CONST               1
              158  BINARY_SUBSCR    
              160  LOAD_FAST                'index'
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_FALSE   208  'to 208'

 L.3493       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _lazy_child
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                _oid_nums
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  LOAD_ATTR                native
              182  STORE_FAST               'oid'

 L.3494       184  LOAD_FAST                'oid'
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                _oid_specs
              190  COMPARE_OP               in
              192  POP_JUMP_IF_FALSE   208  'to 208'

 L.3495       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _oid_specs
              198  LOAD_FAST                'oid'
              200  BINARY_SUBSCR    
              202  STORE_FAST               'spec_override'

 L.3496       204  LOAD_FAST                'spec_override'
              206  STORE_FAST               'value_spec'
            208_0  COME_FROM           192  '192'
            208_1  COME_FROM           164  '164'
            208_2  COME_FROM           150  '150'
            208_3  COME_FROM           140  '140'
            208_4  COME_FROM            64  '64'

 L.3498       208  LOAD_FAST                'name'
              210  LOAD_FAST                'field_spec'
              212  LOAD_FAST                'value_spec'
              214  LOAD_FAST                'field_params'
              216  LOAD_FAST                'spec_override'
              218  BUILD_TUPLE_5         5 
              220  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 114_0

    def _make_value(self, field_name, field_spec, value_spec, field_params, value):
        """
        Contructs an appropriate Asn1Value object for a field

        :param field_name:
            A unicode string of the field name

        :param field_spec:
            An Asn1Value class that is the field spec

        :param value_spec:
            An Asn1Value class that is the vaue spec

        :param field_params:
            None or a dict of params for the field spec

        :param value:
            The value to construct an Asn1Value object from

        :return:
            An instance of a child class of Asn1Value
        """
        if value is None:
            if 'optional' in field_params:
                return VOID
            specs_different = field_spec != value_spec
            is_any = issubclass(field_spec, Any)
            if issubclass(value_spec, Choice):
                if not isinstance(value, Asn1Value):
                    raise ValueError(unwrap('\n                    Can not set a native python value to %s, which has the\n                    choice type of %s - value must be an instance of Asn1Value\n                    ', field_name, type_name(value_spec)))
                wrapper = isinstance(value, value_spec) or value_spec()
                wrapper.validate(value.class_, value.tag, value.contents)
                wrapper._parsed = value
                new_value = wrapper
            else:
                new_value = value
        elif isinstance(value, field_spec):
            new_value = value
            if specs_different:
                new_value.parse(value_spec)
        else:
            if (not specs_different or is_any) and not isinstance(value, value_spec):
                new_value = value_spec(value, **field_params)
            else:
                if isinstance(value, value_spec):
                    new_value = value
                else:
                    new_value = value_spec(value)
                if specs_different and not is_any:
                    wrapper = field_spec(value=new_value.dump(), **field_params)
                    wrapper._parsed = (new_value, new_value.__class__, None)
                    new_value = wrapper
            new_value = _fix_tagging(new_value, field_params)
            return new_value

    def _parse_children(self, recurse=False):
        """
        Parses the contents and generates Asn1Value objects based on the
        definitions from _fields.

        :param recurse:
            If child objects that are Sequence or SequenceOf objects should
            be recursively parsed

        :raises:
            ValueError - when an error occurs parsing child objects
        """
        cls = self.__class__
        if self._contents is None:
            if self._fields:
                self.children = [
                 VOID] * len(self._fields)
                for index, (_, _, params) in enumerate(self._fields):
                    if 'default' in params:
                        if cls._precomputed_specs[index]:
                            field_name, field_spec, value_spec, field_params, _ = cls._precomputed_specs[index]
                        else:
                            field_name, field_spec, value_spec, field_params, _ = self._determine_spec(index)
                        self.children[index] = self._make_value(field_name, field_spec, value_spec, field_params, None)

            return
        try:
            self.children = []
            contents_length = len(self._contents)
            child_pointer = 0
            field = 0
            field_len = len(self._fields)
            parts = None
            again = child_pointer < contents_length
            while again:
                if parts is None:
                    parts, child_pointer = _parse((self._contents), contents_length, pointer=child_pointer)
                again = child_pointer < contents_length
                if field < field_len:
                    _, field_spec, value_spec, field_params, spec_override = cls._precomputed_specs[field] or self._determine_spec(field)
                    if field_params:
                        if 'optional' in field_params or 'default' in field_params:
                            if self._field_ids[field] != (parts[0], parts[2]):
                                if field_spec != Any:
                                    choice_match = False
                                    if issubclass(field_spec, Choice):
                                        try:
                                            tester = field_spec(**field_params)
                                            tester.validate(parts[0], parts[2], parts[4])
                                            choice_match = True
                                        except ValueError:
                                            pass

                                    if not choice_match:
                                        if 'optional' in field_params:
                                            self.children.append(VOID)
                                        else:
                                            self.children.append(field_spec(**field_params))
                                        field += 1
                                        again = True
                                        continue
                    if field_spec is None or spec_override and issubclass(field_spec, Any):
                        field_spec = value_spec
                        spec_override = None
                    if spec_override:
                        child = parts + (field_spec, field_params, value_spec)
                    else:
                        child = parts + (field_spec, field_params)
                else:
                    if field_len > 0:
                        if field + 1 <= field_len:
                            missed_fields = []
                            prev_field = field - 1
                            while prev_field >= 0:
                                prev_field_info = self._fields[prev_field]
                                if len(prev_field_info) < 3:
                                    break
                                if 'optional' in prev_field_info[2] or 'default' in prev_field_info[2]:
                                    missed_fields.append(prev_field_info[0])
                                prev_field -= 1

                            plural = 's' if len(missed_fields) > 1 else ''
                            missed_field_names = ', '.join(missed_fields)
                            raise ValueError(unwrap('\n                        Data for field %s (%s class, %s method, tag %s) does\n                        not match the field definition%s of %s\n                        ', field + 1, CLASS_NUM_TO_NAME_MAP.get(parts[0]), METHOD_NUM_TO_NAME_MAP.get(parts[1]), parts[2], plural, missed_field_names))
                        else:
                            child = parts
                    else:
                        if recurse:
                            child = _build(*child)
                            if isinstance(child, (Sequence, SequenceOf)):
                                child._parse_children(recurse=True)
                    self.children.append(child)
                    field += 1
                    parts = None

            index = len(self.children)
            while index < field_len:
                name, field_spec, field_params = self._fields[index]
                if 'default' in field_params:
                    self.children.append(field_spec(**field_params))
                else:
                    if 'optional' in field_params:
                        self.children.append(VOID)
                    else:
                        raise ValueError(unwrap('\n                        Field "%s" is missing from structure\n                        ', name))
                index += 1

        except (ValueError, TypeError) as e:
            args = e.args[1:]
            e.args = (e.args[0] + '\n    while parsing %s' % type_name(self),) + args
            raise e

    def spec(self, field_name):
        """
        Determines the spec to use for the field specified. Depending on how
        the spec is determined (_oid_pair or _spec_callbacks), it may be
        necessary to set preceding field values before calling this. Usually
        specs, if dynamic, are controlled by a preceding ObjectIdentifier
        field.

        :param field_name:
            A unicode string of the field name to get the spec for

        :return:
            A child class of asn1crypto.core.Asn1Value that the field must be
            encoded using
        """
        if not isinstance(field_name, str_cls):
            raise TypeError(unwrap('\n                field_name must be a unicode string, not %s\n                ', type_name(field_name)))
        if self._fields is None:
            raise ValueError(unwrap('\n                Unable to retrieve spec for field %s in the class %s because\n                _fields has not been set\n                ', repr(field_name), type_name(self)))
        index = self._field_map[field_name]
        info = self._determine_spec(index)
        return info[2]

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            An OrderedDict or None. If an OrderedDict, all child values are
            recursively converted to native representation also.
        """
        if self.contents is None:
            return
        else:
            if self._native is None:
                if self.children is None:
                    self._parse_children(recurse=True)
                try:
                    self._native = OrderedDict()
                    for index, child in enumerate(self.children):
                        if child.__class__ == tuple:
                            child = _build(*child)
                            self.children[index] = child
                        try:
                            name = self._fields[index][0]
                        except IndexError:
                            name = str_cls(index)

                        self._native[name] = child.native

                except (ValueError, TypeError) as e:
                    args = e.args[1:]
                    e.args = (e.args[0] + '\n    while parsing %s' % type_name(self),) + args
                    raise e

            return self._native

    def _copy(self, other, copy_func):
        super(Sequence, self)._copy(other, copy_func)
        if self.children is not None:
            self.children = []
            for child in other.children:
                if child.__class__ == tuple:
                    self.children.append(child)
                else:
                    self.children.append(child.copy())

    def debug(self, nest_level=1):
        """
        Show the binary data and parsed data in a tree structure
        """
        if self.children is None:
            self._parse_children()
        prefix = '  ' * nest_level
        _basic_debug(prefix, self)
        for field_name in self:
            child = self._lazy_child(self._field_map[field_name])
            if child is not VOID:
                print('%s    Field "%s"' % (prefix, field_name))
                child.debug(nest_level + 3)

    def dump(self, force=False):
        """
        Encodes the value using DER

        :param force:
            If the encoded contents already exist, clear them and regenerate
            to ensure they are in DER format instead of BER format

        :return:
            A byte string of the DER-encoded value
        """
        if force:
            self._set_contents(force=force)
        if self._fields:
            if self.children is not None:
                for index, (field_name, _, params) in enumerate(self._fields):
                    if self.children[index] is not VOID:
                        pass
                    else:
                        if not 'default' in params:
                            if 'optional' in params:
                                pass
                            else:
                                raise ValueError(unwrap('\n                    Field "%s" is missing from structure\n                    ', field_name))

        return Asn1Value.dump(self)


class SequenceOf(Asn1Value):
    __doc__ = '\n    Represents a sequence (ordered) of a single type of values from ASN.1 as a\n    Python object with a list-like interface\n    '
    tag = 16
    class_ = 0
    method = 1
    children = None
    _contents = None
    _mutated = False
    _child_spec = None

    def __init__(self, value=None, default=None, contents=None, spec=None, **kwargs):
        """
        Allows setting child objects and the _child_spec via the spec parameter
        before passing everything else along to Asn1Value.__init__()

        :param value:
            A native Python datatype to initialize the object value with

        :param default:
            The default value if no value is specified

        :param contents:
            A byte string of the encoded contents of the value

        :param spec:
            A class derived from Asn1Value to use to parse children
        """
        if spec:
            self._child_spec = spec
        (Asn1Value.__init__)(self, **kwargs)
        try:
            if contents is not None:
                self.contents = contents
            else:
                if value is None:
                    if default is not None:
                        value = default
            if value is not None:
                for index, child in enumerate(value):
                    self.__setitem__(index, child)

                if self.contents is None:
                    self._set_contents()
        except (ValueError, TypeError) as e:
            args = e.args[1:]
            e.args = (e.args[0] + '\n    while constructing %s' % type_name(self),) + args
            raise e

    @property
    def contents(self):
        """
        :return:
            A byte string of the DER-encoded contents of the sequence
        """
        if self.children is None:
            return self._contents
        else:
            if self._is_mutated():
                self._set_contents()
            return self._contents

    @contents.setter
    def contents(self, value):
        """
        :param value:
            A byte string of the DER-encoded contents of the sequence
        """
        self._contents = value

    def _is_mutated(self):
        """
        :return:
            A boolean - if the sequence or any children (recursively) have been
            mutated
        """
        mutated = self._mutated
        if self.children is not None:
            for child in self.children:
                if isinstance(child, Sequence) or isinstance(child, SequenceOf):
                    mutated = mutated or child._is_mutated()

        return mutated

    def _lazy_child(self, index):
        """
        Builds a child object if the child has only been parsed into a tuple so far
        """
        child = self.children[index]
        if child.__class__ == tuple:
            child = _build(*child)
            self.children[index] = child
        return child

    def _make_value(self, value):
        """
        Constructs a _child_spec value from a native Python data type, or
        an appropriate Asn1Value object

        :param value:
            A native Python value, or some child of Asn1Value

        :return:
            An object of type _child_spec
        """
        if isinstance(value, self._child_spec):
            new_value = value
        else:
            if issubclass(self._child_spec, Any):
                if isinstance(value, Asn1Value):
                    new_value = value
                else:
                    raise ValueError(unwrap('\n                    Can not set a native python value to %s where the\n                    _child_spec is Any - value must be an instance of Asn1Value\n                    ', type_name(self)))
            else:
                if issubclass(self._child_spec, Choice):
                    if not isinstance(value, Asn1Value):
                        raise ValueError(unwrap('\n                    Can not set a native python value to %s where the\n                    _child_spec is the choice type %s - value must be an\n                    instance of Asn1Value\n                    ', type_name(self), self._child_spec.__name__))
                    if not isinstance(value, self._child_spec):
                        wrapper = self._child_spec()
                        wrapper.validate(value.class_, value.tag, value.contents)
                        wrapper._parsed = value
                        value = wrapper
                    new_value = value
                else:
                    return self._child_spec(value=value)
            params = {}
            if self._child_spec.explicit:
                params['explicit'] = self._child_spec.explicit
            if self._child_spec.implicit:
                params['implicit'] = (
                 self._child_spec.class_, self._child_spec.tag)
        return _fix_tagging(new_value, params)

    def __len__(self):
        """
        :return:
            An integer
        """
        if self.children is None:
            self._parse_children()
        return len(self.children)

    def __getitem__(self, key):
        """
        Allows accessing children via index

        :param key:
            Integer index of child
        """
        if self.children is None:
            self._parse_children()
        return self._lazy_child(key)

    def __setitem__(self, key, value):
        """
        Allows overriding a child via index

        :param key:
            Integer index of child

        :param value:
            Native python datatype that will be passed to _child_spec to create
            new child object
        """
        if self.children is None:
            self._parse_children()
        else:
            new_value = self._make_value(value)
            if key == len(self.children):
                self.children.append(None)
                if self._native is not None:
                    self._native.append(None)
            self.children[key] = new_value
            if self._native is not None:
                self._native[key] = self.children[key].native
        self._mutated = True

    def __delitem__(self, key):
        """
        Allows removing a child via index

        :param key:
            Integer index of child
        """
        if self.children is None:
            self._parse_children()
        self.children.pop(key)
        if self._native is not None:
            self._native.pop(key)
        self._mutated = True

    def __iter__(self):
        """
        :return:
            An iter() of child objects
        """
        if self.children is None:
            self._parse_children()
        for index in range(0, len(self.children)):
            yield self._lazy_child(index)

    def __contains__(self, item):
        """
        :param item:
            An object of the type cls._child_spec

        :return:
            A boolean if the item is contained in this SequenceOf
        """
        if item is None or item is VOID:
            return False
        else:
            if not isinstance(item, self._child_spec):
                raise TypeError(unwrap('\n                Checking membership in %s is only available for instances of\n                %s, not %s\n                ', type_name(self), type_name(self._child_spec), type_name(item)))
            for child in self:
                if child == item:
                    return True

            return False

    def append(self, value):
        """
        Allows adding a child to the end of the sequence

        :param value:
            Native python datatype that will be passed to _child_spec to create
            new child object
        """
        if self.children is None:
            self._parse_children()
        self.children.append(self._make_value(value))
        if self._native is not None:
            self._native.append(self.children[(-1)].native)
        self._mutated = True

    def _set_contents(self, force=False):
        """
        Encodes all child objects into the contents for this object

        :param force:
            Ensure all contents are in DER format instead of possibly using
            cached BER-encoded data
        """
        if self.children is None:
            self._parse_children()
        contents = BytesIO()
        for child in self:
            contents.write(child.dump(force=force))

        self._contents = contents.getvalue()
        self._header = None
        if self._trailer != b'':
            self._trailer = b''

    def _parse_children(self, recurse=False):
        """
        Parses the contents and generates Asn1Value objects based on the
        definitions from _child_spec.

        :param recurse:
            If child objects that are Sequence or SequenceOf objects should
            be recursively parsed

        :raises:
            ValueError - when an error occurs parsing child objects
        """
        try:
            self.children = []
            if self._contents is None:
                return
            contents_length = len(self._contents)
            child_pointer = 0
            while child_pointer < contents_length:
                parts, child_pointer = _parse((self._contents), contents_length, pointer=child_pointer)
                if self._child_spec:
                    child = parts + (self._child_spec,)
                else:
                    child = parts
                if recurse:
                    child = _build(*child)
                    if isinstance(child, (Sequence, SequenceOf)):
                        child._parse_children(recurse=True)
                self.children.append(child)

        except (ValueError, TypeError) as e:
            args = e.args[1:]
            e.args = (e.args[0] + '\n    while parsing %s' % type_name(self),) + args
            raise e

    def spec(self):
        """
        Determines the spec to use for child values.

        :return:
            A child class of asn1crypto.core.Asn1Value that child values must be
            encoded using
        """
        return self._child_spec

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            A list or None. If a list, all child values are recursively
            converted to native representation also.
        """
        if self.contents is None:
            return
        else:
            if self._native is None:
                if self.children is None:
                    self._parse_children(recurse=True)
                try:
                    self._native = [child.native for child in self]
                except (ValueError, TypeError) as e:
                    args = e.args[1:]
                    e.args = (e.args[0] + '\n    while parsing %s' % type_name(self),) + args
                    raise e

            return self._native

    def _copy(self, other, copy_func):
        super(SequenceOf, self)._copy(other, copy_func)
        if self.children is not None:
            self.children = []
            for child in other.children:
                if child.__class__ == tuple:
                    self.children.append(child)
                else:
                    self.children.append(child.copy())

    def debug(self, nest_level=1):
        """
        Show the binary data and parsed data in a tree structure
        """
        if self.children is None:
            self._parse_children()
        prefix = '  ' * nest_level
        _basic_debug(prefix, self)
        for child in self:
            child.debug(nest_level + 1)

    def dump(self, force=False):
        """
        Encodes the value using DER

        :param force:
            If the encoded contents already exist, clear them and regenerate
            to ensure they are in DER format instead of BER format

        :return:
            A byte string of the DER-encoded value
        """
        if force:
            self._set_contents(force=force)
        return Asn1Value.dump(self)


class Set(Sequence):
    __doc__ = '\n    Represents a set of fields (unordered) from ASN.1 as a Python object with a\n    dict-like interface\n    '
    method = 1
    class_ = 0
    tag = 17
    _field_ids = None

    def _setup(self):
        """
        Generates _field_map, _field_ids and _oid_nums for use in parsing
        """
        cls = self.__class__
        cls._field_map = {}
        cls._field_ids = {}
        cls._precomputed_specs = []
        for index, field in enumerate(cls._fields):
            if len(field) < 3:
                field = field + ({},)
                cls._fields[index] = field
            cls._field_map[field[0]] = index
            cls._field_ids[_build_id_tuple(field[2], field[1])] = index

        if cls._oid_pair is not None:
            cls._oid_nums = (
             cls._field_map[cls._oid_pair[0]], cls._field_map[cls._oid_pair[1]])
        for index, field in enumerate(cls._fields):
            has_callback = cls._spec_callbacks is not None and field[0] in cls._spec_callbacks
            is_mapped_oid = cls._oid_nums is not None and cls._oid_nums[1] == index
            if has_callback or is_mapped_oid:
                cls._precomputed_specs.append(None)
            else:
                cls._precomputed_specs.append((field[0], field[1], field[1], field[2], None))

    def _parse_children(self, recurse=False):
        """
        Parses the contents and generates Asn1Value objects based on the
        definitions from _fields.

        :param recurse:
            If child objects that are Sequence or SequenceOf objects should
            be recursively parsed

        :raises:
            ValueError - when an error occurs parsing child objects
        """
        cls = self.__class__
        if self._contents is None:
            if self._fields:
                self.children = [
                 VOID] * len(self._fields)
                for index, (_, _, params) in enumerate(self._fields):
                    if 'default' in params:
                        if cls._precomputed_specs[index]:
                            field_name, field_spec, value_spec, field_params, _ = cls._precomputed_specs[index]
                        else:
                            field_name, field_spec, value_spec, field_params, _ = self._determine_spec(index)
                        self.children[index] = self._make_value(field_name, field_spec, value_spec, field_params, None)

            return
        try:
            child_map = {}
            contents_length = len(self.contents)
            child_pointer = 0
            seen_field = 0
            while child_pointer < contents_length:
                parts, child_pointer = _parse((self.contents), contents_length, pointer=child_pointer)
                id_ = (
                 parts[0], parts[2])
                field = self._field_ids.get(id_)
                if field is None:
                    raise ValueError(unwrap('\n                        Data for field %s (%s class, %s method, tag %s) does\n                        not match any of the field definitions\n                        ', seen_field, CLASS_NUM_TO_NAME_MAP.get(parts[0]), METHOD_NUM_TO_NAME_MAP.get(parts[1]), parts[2]))
                _, field_spec, value_spec, field_params, spec_override = cls._precomputed_specs[field] or self._determine_spec(field)
                if field_spec is None or spec_override and issubclass(field_spec, Any):
                    field_spec = value_spec
                    spec_override = None
                if spec_override:
                    child = parts + (field_spec, field_params, value_spec)
                else:
                    child = parts + (field_spec, field_params)
                if recurse:
                    child = _build(*child)
                    if isinstance(child, (Sequence, SequenceOf)):
                        child._parse_children(recurse=True)
                child_map[field] = child
                seen_field += 1

            total_fields = len(self._fields)
            for index in range(0, total_fields):
                if index in child_map:
                    pass
                else:
                    name, field_spec, value_spec, field_params, spec_override = cls._precomputed_specs[index] or self._determine_spec(index)
                    if field_spec is None or spec_override and issubclass(field_spec, Any):
                        field_spec = value_spec
                        spec_override = None
                    missing = False
                    if not field_params:
                        missing = True
                    elif 'optional' not in field_params and 'default' not in field_params:
                        missing = True
                    else:
                        if 'optional' in field_params:
                            child_map[index] = VOID
                        else:
                            if 'default' in field_params:
                                child_map[index] = field_spec(**field_params)
                    if missing:
                        raise ValueError(unwrap('\n                        Missing required field "%s" from %s\n                        ', name, type_name(self)))

            self.children = []
            for index in range(0, total_fields):
                self.children.append(child_map[index])

        except (ValueError, TypeError) as e:
            args = e.args[1:]
            e.args = (e.args[0] + '\n    while parsing %s' % type_name(self),) + args
            raise e

    def _set_contents(self, force=False):
        """
        Encodes all child objects into the contents for this object.

        This method is overridden because a Set needs to be encoded by
        removing defaulted fields and then sorting the fields by tag.

        :param force:
            Ensure all contents are in DER format instead of possibly using
            cached BER-encoded data
        """
        if self.children is None:
            self._parse_children()
        child_tag_encodings = []
        for index, child in enumerate(self.children):
            child_encoding = child.dump(force=force)
            name, spec, field_params = self._fields[index]
            if 'default' in field_params:
                if spec(**field_params).dump() == child_encoding:
                    continue
            child_tag_encodings.append((child.tag, child_encoding))

        child_tag_encodings.sort(key=(lambda ct: ct[0]))
        self._contents = (b'').join([ct[1] for ct in child_tag_encodings])
        self._header = None
        if self._trailer != b'':
            self._trailer = b''


class SetOf(SequenceOf):
    __doc__ = '\n    Represents a set (unordered) of a single type of values from ASN.1 as a\n    Python object with a list-like interface\n    '
    tag = 17

    def _set_contents(self, force=False):
        """
        Encodes all child objects into the contents for this object.

        This method is overridden because a SetOf needs to be encoded by
        sorting the child encodings.

        :param force:
            Ensure all contents are in DER format instead of possibly using
            cached BER-encoded data
        """
        if self.children is None:
            self._parse_children()
        child_encodings = []
        for child in self:
            child_encodings.append(child.dump(force=force))

        self._contents = (b'').join(sorted(child_encodings))
        self._header = None
        if self._trailer != b'':
            self._trailer = b''


class EmbeddedPdv(Sequence):
    __doc__ = '\n    A sequence structure\n    '
    tag = 11


class NumericString(AbstractString):
    __doc__ = '\n    Represents a numeric string from ASN.1 as a Python unicode string\n    '
    tag = 18
    _encoding = 'latin1'


class PrintableString(AbstractString):
    __doc__ = '\n    Represents a printable string from ASN.1 as a Python unicode string\n    '
    tag = 19
    _encoding = 'latin1'


class TeletexString(AbstractString):
    __doc__ = '\n    Represents a teletex string from ASN.1 as a Python unicode string\n    '
    tag = 20
    _encoding = 'teletex'


class VideotexString(OctetString):
    __doc__ = '\n    Represents a videotex string from ASN.1 as a Python byte string\n    '
    tag = 21


class IA5String(AbstractString):
    __doc__ = '\n    Represents an IA5 string from ASN.1 as a Python unicode string\n    '
    tag = 22
    _encoding = 'ascii'


class AbstractTime(AbstractString):
    __doc__ = '\n    Represents a time from ASN.1 as a Python datetime.datetime object\n    '

    @property
    def native(self):
        """
        The a native Python datatype representation of this value

        :return:
            A datetime.datetime object in the UTC timezone or None
        """
        if self.contents is None:
            return
        else:
            if self._native is None:
                string = str_cls(self)
                has_timezone = re.search('[-\\+]', string)
                if not has_timezone:
                    string = string.rstrip('Z')
                    date = self._date_by_len(string)
                    self._native = date.replace(tzinfo=(timezone.utc))
                else:
                    date = self._date_by_len(string[0:-5])
                    hours = int(string[-4:-2])
                    minutes = int(string[-2:])
                    delta = timedelta(hours=(abs(hours)), minutes=minutes)
                    if hours < 0:
                        date -= delta
                    else:
                        date += delta
                    self._native = date.replace(tzinfo=(timezone.utc))
            return self._native


class UTCTime(AbstractTime):
    __doc__ = '\n    Represents a UTC time from ASN.1 as a Python datetime.datetime object in UTC\n    '
    tag = 23

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            A unicode string or a datetime.datetime object

        :raises:
            ValueError - when an invalid value is passed
        """
        if isinstance(value, datetime):
            value = value.strftime('%y%m%d%H%M%SZ')
            if _PY2:
                value = value.decode('ascii')
        AbstractString.set(self, value)
        self._native = None

    def _date_by_len(self, string):
        """
        Parses a date from a string based on its length

        :param string:
            A unicode string to parse

        :return:
            A datetime.datetime object or a unicode string
        """
        strlen = len(string)
        year_num = int(string[0:2])
        if year_num < 50:
            prefix = '20'
        else:
            prefix = '19'
        if strlen == 10:
            return datetime.strptime(prefix + string, '%Y%m%d%H%M')
        else:
            if strlen == 12:
                return datetime.strptime(prefix + string, '%Y%m%d%H%M%S')
            return string


class GeneralizedTime(AbstractTime):
    __doc__ = '\n    Represents a generalized time from ASN.1 as a Python datetime.datetime\n    object or asn1crypto.util.extended_datetime object in UTC\n    '
    tag = 24

    def set(self, value):
        """
        Sets the value of the object

        :param value:
            A unicode string, a datetime.datetime object or an
            asn1crypto.util.extended_datetime object

        :raises:
            ValueError - when an invalid value is passed
        """
        if isinstance(value, (datetime, extended_datetime)):
            value = value.strftime('%Y%m%d%H%M%SZ')
            if _PY2:
                value = value.decode('ascii')
        AbstractString.set(self, value)
        self._native = None

    def _date_by_len(self, string):
        """
        Parses a date from a string based on its length

        :param string:
            A unicode string to parse

        :return:
            A datetime.datetime object, asn1crypto.util.extended_datetime object or
            a unicode string
        """
        strlen = len(string)
        date_format = None
        if strlen == 10:
            date_format = '%Y%m%d%H'
        else:
            if strlen == 12:
                date_format = '%Y%m%d%H%M'
            else:
                if strlen == 14:
                    date_format = '%Y%m%d%H%M%S'
                else:
                    if strlen == 18:
                        date_format = '%Y%m%d%H%M%S.%f'
        if date_format:
            if len(string) >= 4:
                if string[0:4] == '0000':
                    t = datetime.strptime('2000' + string[4:], date_format)
                    return extended_datetime(0, t.month, t.day, t.hour, t.minute, t.second, t.microsecond, t.tzinfo)
            return datetime.strptime(string, date_format)
        else:
            return string


class GraphicString(AbstractString):
    __doc__ = '\n    Represents a graphic string from ASN.1 as a Python unicode string\n    '
    tag = 25
    _encoding = 'latin1'


class VisibleString(AbstractString):
    __doc__ = '\n    Represents a visible string from ASN.1 as a Python unicode string\n    '
    tag = 26
    _encoding = 'latin1'


class GeneralString(AbstractString):
    __doc__ = '\n    Represents a general string from ASN.1 as a Python unicode string\n    '
    tag = 27
    _encoding = 'latin1'


class UniversalString(AbstractString):
    __doc__ = '\n    Represents a universal string from ASN.1 as a Python unicode string\n    '
    tag = 28
    _encoding = 'utf-32-be'


class CharacterString(AbstractString):
    __doc__ = '\n    Represents a character string from ASN.1 as a Python unicode string\n    '
    tag = 29
    _encoding = 'latin1'


class BMPString(AbstractString):
    __doc__ = '\n    Represents a BMP string from ASN.1 as a Python unicode string\n    '
    tag = 30
    _encoding = 'utf-16-be'


def _basic_debug(prefix, self):
    """
    Prints out basic information about an Asn1Value object. Extracted for reuse
    among different classes that customize the debug information.

    :param prefix:
        A unicode string of spaces to prefix output line with

    :param self:
        The object to print the debugging information about
    """
    print('%s%s Object #%s' % (prefix, type_name(self), id(self)))
    if self._header:
        print('%s  Header: 0x%s' % (prefix, binascii.hexlify(self._header or b'').decode('utf-8')))
    has_header = self.method is not None and self.class_ is not None and self.tag is not None
    if has_header:
        method_name = METHOD_NUM_TO_NAME_MAP.get(self.method)
        class_name = CLASS_NUM_TO_NAME_MAP.get(self.class_)
    if self.explicit is not None:
        for class_, tag in self.explicit:
            print('%s    %s tag %s (explicitly tagged)' % (
             prefix,
             CLASS_NUM_TO_NAME_MAP.get(class_),
             tag))

        if has_header:
            print('%s      %s %s %s' % (prefix, method_name, class_name, self.tag))
    elif self.implicit:
        if has_header:
            print('%s    %s %s tag %s (implicitly tagged)' % (prefix, method_name, class_name, self.tag))
    else:
        if has_header:
            print('%s    %s %s tag %s' % (prefix, method_name, class_name, self.tag))
        print('%s  Data: 0x%s' % (prefix, binascii.hexlify(self.contents or b'').decode('utf-8')))


def _tag_type_to_explicit_implicit(params):
    """
    Converts old-style "tag_type" and "tag" params to "explicit" and "implicit"

    :param params:
        A dict of parameters to convert from tag_type/tag to explicit/implicit
    """
    if 'tag_type' in params:
        if params['tag_type'] == 'explicit':
            params['explicit'] = (
             params.get('class', 2), params['tag'])
        else:
            if params['tag_type'] == 'implicit':
                params['implicit'] = (
                 params.get('class', 2), params['tag'])
            del params['tag_type']
            del params['tag']
            if 'class' in params:
                del params['class']


def _fix_tagging(value, params):
    """
    Checks if a value is properly tagged based on the spec, and re/untags as
    necessary

    :param value:
        An Asn1Value object

    :param params:
        A dict of spec params

    :return:
        An Asn1Value that is properly tagged
    """
    _tag_type_to_explicit_implicit(params)
    retag = False
    if 'implicit' not in params:
        if value.implicit is not False:
            retag = True
    else:
        if isinstance(params['implicit'], tuple):
            class_, tag = params['implicit']
        else:
            tag = params['implicit']
            class_ = 'context'
    if value.implicit is False:
        retag = True
    else:
        if value.class_ != CLASS_NAME_TO_NUM_MAP[class_] or value.tag != tag:
            retag = True
    if params.get('explicit') != value.explicit:
        retag = True
    if retag:
        return value.retag(params)
    else:
        return value


def _build_id_tuple(params, spec):
    """
    Builds a 2-element tuple used to identify fields by grabbing the class_
    and tag from an Asn1Value class and the params dict being passed to it

    :param params:
        A dict of params to pass to spec

    :param spec:
        An Asn1Value class

    :return:
        A 2-element integer tuple in the form (class_, tag)
    """
    if spec is None:
        return (None, None)
    else:
        required_class = spec.class_
        required_tag = spec.tag
        _tag_type_to_explicit_implicit(params)
        if 'explicit' in params:
            if isinstance(params['explicit'], tuple):
                required_class, required_tag = params['explicit']
            else:
                required_class = 2
                required_tag = params['explicit']
        else:
            if 'implicit' in params:
                if isinstance(params['implicit'], tuple):
                    required_class, required_tag = params['implicit']
                else:
                    required_class = 2
                    required_tag = params['implicit']
        if required_class is not None:
            if not isinstance(required_class, int_types):
                required_class = CLASS_NAME_TO_NUM_MAP[required_class]
        required_class = params.get('class_', required_class)
        required_tag = params.get('tag', required_tag)
        return (
         required_class, required_tag)


_UNIVERSAL_SPECS = {1:Boolean, 
 2:Integer, 
 3:BitString, 
 4:OctetString, 
 5:Null, 
 6:ObjectIdentifier, 
 7:ObjectDescriptor, 
 8:InstanceOf, 
 9:Real, 
 10:Enumerated, 
 11:EmbeddedPdv, 
 12:UTF8String, 
 13:RelativeOid, 
 16:Sequence, 
 17:Set, 
 18:NumericString, 
 19:PrintableString, 
 20:TeletexString, 
 21:VideotexString, 
 22:IA5String, 
 23:UTCTime, 
 24:GeneralizedTime, 
 25:GraphicString, 
 26:VisibleString, 
 27:GeneralString, 
 28:UniversalString, 
 29:CharacterString, 
 30:BMPString}

def _build(class_, method, tag, header, contents, trailer, spec=None, spec_params=None, nested_spec=None):
    """
    Builds an Asn1Value object generically, or using a spec with optional params

    :param class_:
        An integer representing the ASN.1 class

    :param method:
        An integer representing the ASN.1 method

    :param tag:
        An integer representing the ASN.1 tag

    :param header:
        A byte string of the ASN.1 header (class, method, tag, length)

    :param contents:
        A byte string of the ASN.1 value

    :param trailer:
        A byte string of any ASN.1 trailer (only used by indefinite length encodings)

    :param spec:
        A class derived from Asn1Value that defines what class_ and tag the
        value should have, and the semantics of the encoded value. The
        return value will be of this type. If omitted, the encoded value
        will be decoded using the standard universal tag based on the
        encoded tag number.

    :param spec_params:
        A dict of params to pass to the spec object

    :param nested_spec:
        For certain Asn1Value classes (such as OctetString and BitString), the
        contents can be further parsed and interpreted as another Asn1Value.
        This parameter controls the spec for that sub-parsing.

    :return:
        An object of the type spec, or if not specified, a child of Asn1Value
    """
    if spec_params is not None:
        _tag_type_to_explicit_implicit(spec_params)
    if header is None:
        return VOID
    else:
        header_set = False
        if spec is not None:
            no_explicit = spec_params and 'no_explicit' in spec_params
            if not no_explicit and (spec.explicit or spec_params and 'explicit' in spec_params):
                if spec_params:
                    value = spec(**spec_params)
                else:
                    value = spec()
                original_explicit = value.explicit
                explicit_info = reversed(original_explicit)
                parsed_class = class_
                parsed_method = method
                parsed_tag = tag
                to_parse = contents
                explicit_header = header
                explicit_trailer = trailer or b''
                for expected_class, expected_tag in explicit_info:
                    if parsed_class != expected_class:
                        raise ValueError(unwrap('\n                        Error parsing %s - explicitly-tagged class should have been\n                        %s, but %s was found\n                        ', type_name(value), CLASS_NUM_TO_NAME_MAP.get(expected_class), CLASS_NUM_TO_NAME_MAP.get(parsed_class, parsed_class)))
                    else:
                        if parsed_method != 1:
                            raise ValueError(unwrap('\n                        Error parsing %s - explicitly-tagged method should have\n                        been %s, but %s was found\n                        ', type_name(value), METHOD_NUM_TO_NAME_MAP.get(1), METHOD_NUM_TO_NAME_MAP.get(parsed_method, parsed_method)))
                        if parsed_tag != expected_tag:
                            raise ValueError(unwrap('\n                        Error parsing %s - explicitly-tagged tag should have been\n                        %s, but %s was found\n                        ', type_name(value), expected_tag, parsed_tag))
                    info, _ = _parse(to_parse, len(to_parse))
                    parsed_class, parsed_method, parsed_tag, parsed_header, to_parse, parsed_trailer = info
                    explicit_header += parsed_header
                    explicit_trailer = parsed_trailer + explicit_trailer

                value = _build(*info, spec=spec, spec_params={'no_explicit': True})
                value._header = explicit_header
                value._trailer = explicit_trailer
                value.explicit = original_explicit
                header_set = True
            else:
                if spec_params:
                    value = spec(contents=contents, **spec_params)
                else:
                    value = spec(contents=contents)
                if spec is Any:
                    pass
                else:
                    if isinstance(value, Choice):
                        value.validate(class_, tag, contents)
                        try:
                            value.contents = header + value.contents
                            header = b''
                            value.parse()
                        except (ValueError, TypeError) as e:
                            args = e.args[1:]
                            e.args = (e.args[0] + '\n    while parsing %s' % type_name(value),) + args
                            raise e

            if class_ != value.class_:
                raise ValueError(unwrap('\n                        Error parsing %s - class should have been %s, but %s was\n                        found\n                        ', type_name(value), CLASS_NUM_TO_NAME_MAP.get(value.class_), CLASS_NUM_TO_NAME_MAP.get(class_, class_)))
            if method != value.method:
                ber_indef = method == 1 and value.method == 0 and trailer == b'\x00\x00'
                if not ber_indef or not isinstance(value, Constructable):
                    raise ValueError(unwrap('\n                            Error parsing %s - method should have been %s, but %s was found\n                            ', type_name(value), METHOD_NUM_TO_NAME_MAP.get(value.method), METHOD_NUM_TO_NAME_MAP.get(method, method)))
                else:
                    value.method = method
                    value._indefinite = True
            if tag != value.tag and tag != value._bad_tag:
                raise ValueError(unwrap('\n                        Error parsing %s - tag should have been %s, but %s was found\n                        ', type_name(value), value.tag, tag))
        elif spec_params:
            if 'explicit' in spec_params:
                original_value = Asn1Value(contents=contents, **spec_params)
                original_explicit = original_value.explicit
                to_parse = contents
                explicit_header = header
                explicit_trailer = trailer or b''
                for expected_class, expected_tag in reversed(original_explicit):
                    info, _ = _parse(to_parse, len(to_parse))
                    _, _, _, parsed_header, to_parse, parsed_trailer = info
                    explicit_header += parsed_header
                    explicit_trailer = parsed_trailer + explicit_trailer

                value = _build(*info, spec=spec, spec_params={'no_explicit': True})
                value._header = header + value._header
                value._trailer += trailer or b''
                value.explicit = original_explicit
                header_set = True
            elif tag not in _UNIVERSAL_SPECS:
                raise ValueError(unwrap('\n                Unknown element - %s class, %s method, tag %s\n                ', CLASS_NUM_TO_NAME_MAP.get(class_), METHOD_NUM_TO_NAME_MAP.get(method), tag))
        else:
            spec = _UNIVERSAL_SPECS[tag]
            value = spec(contents=contents, class_=class_)
            ber_indef = method == 1 and value.method == 0 and trailer == b'\x00\x00'
            if ber_indef:
                if isinstance(value, Constructable):
                    value._indefinite = True
            value.method = method
        if not header_set:
            value._header = header
            value._trailer = trailer or b''
        value._native = None
        if nested_spec:
            try:
                value.parse(nested_spec)
            except (ValueError, TypeError) as e:
                args = e.args[1:]
                e.args = (e.args[0] + '\n    while parsing %s' % type_name(value),) + args
                raise e

        return value


def _parse_build(encoded_data, pointer=0, spec=None, spec_params=None, strict=False):
    """
    Parses a byte string generically, or using a spec with optional params

    :param encoded_data:
        A byte string that contains BER-encoded data

    :param pointer:
        The index in the byte string to parse from

    :param spec:
        A class derived from Asn1Value that defines what class_ and tag the
        value should have, and the semantics of the encoded value. The
        return value will be of this type. If omitted, the encoded value
        will be decoded using the standard universal tag based on the
        encoded tag number.

    :param spec_params:
        A dict of params to pass to the spec object

    :param strict:
        A boolean indicating if trailing data should be forbidden - if so, a
        ValueError will be raised when trailing data exists

    :return:
        A 2-element tuple:
         - 0: An object of the type spec, or if not specified, a child of Asn1Value
         - 1: An integer indicating how many bytes were consumed
    """
    encoded_len = len(encoded_data)
    info, new_pointer = _parse(encoded_data, encoded_len, pointer)
    if strict:
        if new_pointer != pointer + encoded_len:
            extra_bytes = pointer + encoded_len - new_pointer
            raise ValueError('Extra data - %d bytes of trailing data were provided' % extra_bytes)
    return (
     _build(*info, spec=spec, spec_params=spec_params), new_pointer)