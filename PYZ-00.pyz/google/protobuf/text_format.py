# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\google\protobuf\text_format.py
"""Contains routines for printing protocol messages in text format.

Simple usage example:

  # Create a proto object and serialize it to a text proto string.
  message = my_proto_pb2.MyMessage(foo='bar')
  text_proto = text_format.MessageToString(message)

  # Parse a text proto string.
  message = text_format.Parse(text_proto, my_proto_pb2.MyMessage())
"""
__author__ = 'kenton@google.com (Kenton Varda)'
import io, re, six
if six.PY3:
    long = int
from google.protobuf.internal import type_checkers
from google.protobuf import descriptor
from google.protobuf import text_encoding
__all__ = [
 'MessageToString', 'PrintMessage', 'PrintField', 'PrintFieldValue',
 'Merge']
_INTEGER_CHECKERS = (
 type_checkers.Uint32ValueChecker(),
 type_checkers.Int32ValueChecker(),
 type_checkers.Uint64ValueChecker(),
 type_checkers.Int64ValueChecker())
_FLOAT_INFINITY = re.compile('-?inf(?:inity)?f?', re.IGNORECASE)
_FLOAT_NAN = re.compile('nanf?', re.IGNORECASE)
_FLOAT_TYPES = frozenset([descriptor.FieldDescriptor.CPPTYPE_FLOAT,
 descriptor.FieldDescriptor.CPPTYPE_DOUBLE])
_QUOTES = frozenset(("'", '"'))
_ANY_FULL_TYPE_NAME = 'google.protobuf.Any'

class Error(Exception):
    __doc__ = 'Top-level module error for text_format.'


class ParseError(Error):
    __doc__ = 'Thrown in case of text parsing or tokenizing error.'

    def __init__(self, message=None, line=None, column=None):
        if message is not None:
            if line is not None:
                loc = str(line)
                if column is not None:
                    loc += ':{0}'.format(column)
                message = '{0} : {1}'.format(loc, message)
        else:
            if message is not None:
                super(ParseError, self).__init__(message)
            else:
                super(ParseError, self).__init__()
        self._line = line
        self._column = column

    def GetLine(self):
        return self._line

    def GetColumn(self):
        return self._column


class TextWriter(object):

    def __init__(self, as_utf8):
        if six.PY2:
            self._writer = io.BytesIO()
        else:
            self._writer = io.StringIO()

    def write(self, val):
        if six.PY2:
            if isinstance(val, six.text_type):
                val = val.encode('utf-8')
        return self._writer.write(val)

    def close(self):
        return self._writer.close()

    def getvalue(self):
        return self._writer.getvalue()


def MessageToString(message, as_utf8=False, as_one_line=False, pointy_brackets=False, use_index_order=False, float_format=None, use_field_number=False, descriptor_pool=None, indent=0, message_formatter=None):
    """Convert protobuf message to text format.

  Floating point values can be formatted compactly with 15 digits of
  precision (which is the most that IEEE 754 "double" can guarantee)
  using float_format='.15g'. To ensure that converting to text and back to a
  proto will result in an identical value, float_format='.17g' should be used.

  Args:
    message: The protocol buffers message.
    as_utf8: Produce text output in UTF8 format.
    as_one_line: Don't introduce newlines between fields.
    pointy_brackets: If True, use angle brackets instead of curly braces for
      nesting.
    use_index_order: If True, fields of a proto message will be printed using
      the order defined in source code instead of the field number, extensions
      will be printed at the end of the message and their relative order is
      determined by the extension number. By default, use the field number
      order.
    float_format: If set, use this to specify floating point number formatting
      (per the "Format Specification Mini-Language"); otherwise, str() is used.
    use_field_number: If True, print field numbers instead of names.
    descriptor_pool: A DescriptorPool used to resolve Any types.
    indent: The indent level, in terms of spaces, for pretty print.
    message_formatter: A function(message, indent, as_one_line): unicode|None
      to custom format selected sub-messages (usually based on message type).
      Use to pretty print parts of the protobuf for easier diffing.

  Returns:
    A string of the text formatted protocol buffer message.
  """
    out = TextWriter(as_utf8)
    printer = _Printer(out, indent, as_utf8, as_one_line, pointy_brackets, use_index_order, float_format, use_field_number, descriptor_pool, message_formatter)
    printer.PrintMessage(message)
    result = out.getvalue()
    out.close()
    if as_one_line:
        return result.rstrip()
    else:
        return result


def _IsMapEntry(field):
    return field.type == descriptor.FieldDescriptor.TYPE_MESSAGE and field.message_type.has_options and field.message_type.GetOptions().map_entry


def PrintMessage(message, out, indent=0, as_utf8=False, as_one_line=False, pointy_brackets=False, use_index_order=False, float_format=None, use_field_number=False, descriptor_pool=None, message_formatter=None):
    printer = _Printer(out, indent, as_utf8, as_one_line, pointy_brackets, use_index_order, float_format, use_field_number, descriptor_pool, message_formatter)
    printer.PrintMessage(message)


def PrintField(field, value, out, indent=0, as_utf8=False, as_one_line=False, pointy_brackets=False, use_index_order=False, float_format=None, message_formatter=None):
    """Print a single field name/value pair."""
    printer = _Printer(out, indent, as_utf8, as_one_line, pointy_brackets, use_index_order, float_format, message_formatter)
    printer.PrintField(field, value)


def PrintFieldValue(field, value, out, indent=0, as_utf8=False, as_one_line=False, pointy_brackets=False, use_index_order=False, float_format=None, message_formatter=None):
    """Print a single field value (not including name)."""
    printer = _Printer(out, indent, as_utf8, as_one_line, pointy_brackets, use_index_order, float_format, message_formatter)
    printer.PrintFieldValue(field, value)


def _BuildMessageFromTypeName(type_name, descriptor_pool):
    """Returns a protobuf message instance.

  Args:
    type_name: Fully-qualified protobuf  message type name string.
    descriptor_pool: DescriptorPool instance.

  Returns:
    A Message instance of type matching type_name, or None if the a Descriptor
    wasn't found matching type_name.
  """
    if descriptor_pool is None:
        from google.protobuf import descriptor_pool as pool_mod
        descriptor_pool = pool_mod.Default()
    from google.protobuf import symbol_database
    database = symbol_database.Default()
    try:
        message_descriptor = descriptor_pool.FindMessageTypeByName(type_name)
    except KeyError:
        return
    else:
        message_type = database.GetPrototype(message_descriptor)
        return message_type()


class _Printer(object):
    __doc__ = 'Text format printer for protocol message.'

    def __init__(self, out, indent=0, as_utf8=False, as_one_line=False, pointy_brackets=False, use_index_order=False, float_format=None, use_field_number=False, descriptor_pool=None, message_formatter=None):
        """Initialize the Printer.

    Floating point values can be formatted compactly with 15 digits of
    precision (which is the most that IEEE 754 "double" can guarantee)
    using float_format='.15g'. To ensure that converting to text and back to a
    proto will result in an identical value, float_format='.17g' should be used.

    Args:
      out: To record the text format result.
      indent: The indent level for pretty print.
      as_utf8: Produce text output in UTF8 format.
      as_one_line: Don't introduce newlines between fields.
      pointy_brackets: If True, use angle brackets instead of curly braces for
        nesting.
      use_index_order: If True, print fields of a proto message using the order
        defined in source code instead of the field number. By default, use the
        field number order.
      float_format: If set, use this to specify floating point number formatting
        (per the "Format Specification Mini-Language"); otherwise, str() is
        used.
      use_field_number: If True, print field numbers instead of names.
      descriptor_pool: A DescriptorPool used to resolve Any types.
      message_formatter: A function(message, indent, as_one_line): unicode|None
        to custom format selected sub-messages (usually based on message type).
        Use to pretty print parts of the protobuf for easier diffing.
    """
        self.out = out
        self.indent = indent
        self.as_utf8 = as_utf8
        self.as_one_line = as_one_line
        self.pointy_brackets = pointy_brackets
        self.use_index_order = use_index_order
        self.float_format = float_format
        self.use_field_number = use_field_number
        self.descriptor_pool = descriptor_pool
        self.message_formatter = message_formatter

    def _TryPrintAsAnyMessage(self, message):
        """Serializes if message is a google.protobuf.Any field."""
        packed_message = _BuildMessageFromTypeName(message.TypeName(), self.descriptor_pool)
        if packed_message:
            packed_message.MergeFromString(message.value)
            self.out.write('%s[%s]' % (self.indent * ' ', message.type_url))
            self._PrintMessageFieldValue(packed_message)
            self.out.write(' ' if self.as_one_line else '\n')
            return True
        else:
            return False

    def _TryCustomFormatMessage(self, message):
        formatted = self.message_formatter(message, self.indent, self.as_one_line)
        if formatted is None:
            return False
        else:
            out = self.out
            out.write(' ' * self.indent)
            out.write(formatted)
            out.write(' ' if self.as_one_line else '\n')
            return True

    def PrintMessage(self, message):
        """Convert protobuf message to text format.

    Args:
      message: The protocol buffers message.
    """
        if self.message_formatter:
            if self._TryCustomFormatMessage(message):
                return
        else:
            if message.DESCRIPTOR.full_name == _ANY_FULL_TYPE_NAME:
                if self._TryPrintAsAnyMessage(message):
                    return
            fields = message.ListFields()
            if self.use_index_order:
                fields.sort(key=(lambda x: x[0].number if x[0].is_extension else x[0].index))
        for field, value in fields:
            if _IsMapEntry(field):
                for key in sorted(value):
                    entry_submsg = value.GetEntryClass()(key=key, value=(value[key]))
                    self.PrintField(field, entry_submsg)

            else:
                if field.label == descriptor.FieldDescriptor.LABEL_REPEATED:
                    for element in value:
                        self.PrintField(field, element)

                else:
                    self.PrintField(field, value)

    def PrintField(self, field, value):
        """Print a single field name/value pair."""
        out = self.out
        out.write(' ' * self.indent)
        if self.use_field_number:
            out.write(str(field.number))
        else:
            if field.is_extension:
                out.write('[')
                if field.containing_type.GetOptions().message_set_wire_format:
                    if field.type == descriptor.FieldDescriptor.TYPE_MESSAGE:
                        if field.label == descriptor.FieldDescriptor.LABEL_OPTIONAL:
                            out.write(field.message_type.full_name)
                else:
                    out.write(field.full_name)
                out.write(']')
            else:
                if field.type == descriptor.FieldDescriptor.TYPE_GROUP:
                    out.write(field.message_type.name)
                else:
                    out.write(field.name)
        if field.cpp_type != descriptor.FieldDescriptor.CPPTYPE_MESSAGE:
            out.write(': ')
        else:
            self.PrintFieldValue(field, value)
            if self.as_one_line:
                out.write(' ')
            else:
                out.write('\n')

    def _PrintMessageFieldValue(self, value):
        if self.pointy_brackets:
            openb = '<'
            closeb = '>'
        else:
            openb = '{'
            closeb = '}'
        if self.as_one_line:
            self.out.write(' %s ' % openb)
            self.PrintMessage(value)
            self.out.write(closeb)
        else:
            self.out.write(' %s\n' % openb)
            self.indent += 2
            self.PrintMessage(value)
            self.indent -= 2
            self.out.write(' ' * self.indent + closeb)

    def PrintFieldValue(self, field, value):
        """Print a single field value (not including name).

    For repeated fields, the value should be a single element.

    Args:
      field: The descriptor of the field to be printed.
      value: The value of the field.
    """
        out = self.out
        if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_MESSAGE:
            self._PrintMessageFieldValue(value)
        else:
            if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_ENUM:
                enum_value = field.enum_type.values_by_number.get(value, None)
                if enum_value is not None:
                    out.write(enum_value.name)
                else:
                    out.write(str(value))
            else:
                if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_STRING:
                    out.write('"')
                    if isinstance(value, six.text_type):
                        out_value = value.encode('utf-8')
                    else:
                        out_value = value
                    if field.type == descriptor.FieldDescriptor.TYPE_BYTES:
                        out_as_utf8 = False
                    else:
                        out_as_utf8 = self.as_utf8
                    out.write(text_encoding.CEscape(out_value, out_as_utf8))
                    out.write('"')
                else:
                    if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_BOOL:
                        if value:
                            out.write('true')
                        else:
                            out.write('false')
                    elif field.cpp_type in _FLOAT_TYPES:
                        if self.float_format is not None:
                            out.write('{1:{0}}'.format(self.float_format, value))
                    else:
                        out.write(str(value))


def Parse(text, message, allow_unknown_extension=False, allow_field_number=False, descriptor_pool=None):
    """Parses a text representation of a protocol message into a message.

  NOTE: for historical reasons this function does not clear the input
  message. This is different from what the binary msg.ParseFrom(...) does.

  Example
    a = MyProto()
    a.repeated_field.append('test')
    b = MyProto()

    text_format.Parse(repr(a), b)
    text_format.Parse(repr(a), b) # repeated_field contains ["test", "test"]

    # Binary version:
    b.ParseFromString(a.SerializeToString()) # repeated_field is now "test"

  Caller is responsible for clearing the message as needed.

  Args:
    text: Message text representation.
    message: A protocol buffer message to merge into.
    allow_unknown_extension: if True, skip over missing extensions and keep
      parsing
    allow_field_number: if True, both field number and field name are allowed.
    descriptor_pool: A DescriptorPool used to resolve Any types.

  Returns:
    The same message passed as argument.

  Raises:
    ParseError: On text parsing problems.
  """
    if not isinstance(text, str):
        if six.PY3:
            text = text.decode('utf-8')
        else:
            text = text.encode('utf-8')
    return ParseLines((text.split('\n')), message,
      allow_unknown_extension,
      allow_field_number,
      descriptor_pool=descriptor_pool)


def Merge(text, message, allow_unknown_extension=False, allow_field_number=False, descriptor_pool=None):
    """Parses a text representation of a protocol message into a message.

  Like Parse(), but allows repeated values for a non-repeated field, and uses
  the last one.

  Args:
    text: Message text representation.
    message: A protocol buffer message to merge into.
    allow_unknown_extension: if True, skip over missing extensions and keep
      parsing
    allow_field_number: if True, both field number and field name are allowed.
    descriptor_pool: A DescriptorPool used to resolve Any types.

  Returns:
    The same message passed as argument.

  Raises:
    ParseError: On text parsing problems.
  """
    if not isinstance(text, str):
        if six.PY3:
            text = text.decode('utf-8')
        else:
            text = text.encode('utf-8')
    return MergeLines((text.split('\n')),
      message,
      allow_unknown_extension,
      allow_field_number,
      descriptor_pool=descriptor_pool)


def ParseLines(lines, message, allow_unknown_extension=False, allow_field_number=False, descriptor_pool=None):
    """Parses a text representation of a protocol message into a message.

  Args:
    lines: An iterable of lines of a message's text representation.
    message: A protocol buffer message to merge into.
    allow_unknown_extension: if True, skip over missing extensions and keep
      parsing
    allow_field_number: if True, both field number and field name are allowed.
    descriptor_pool: A DescriptorPool used to resolve Any types.

  Returns:
    The same message passed as argument.

  Raises:
    ParseError: On text parsing problems.
  """
    parser = _Parser(allow_unknown_extension, allow_field_number,
      descriptor_pool=descriptor_pool)
    return parser.ParseLines(lines, message)


def MergeLines(lines, message, allow_unknown_extension=False, allow_field_number=False, descriptor_pool=None):
    """Parses a text representation of a protocol message into a message.

  Args:
    lines: An iterable of lines of a message's text representation.
    message: A protocol buffer message to merge into.
    allow_unknown_extension: if True, skip over missing extensions and keep
      parsing
    allow_field_number: if True, both field number and field name are allowed.
    descriptor_pool: A DescriptorPool used to resolve Any types.

  Returns:
    The same message passed as argument.

  Raises:
    ParseError: On text parsing problems.
  """
    parser = _Parser(allow_unknown_extension, allow_field_number,
      descriptor_pool=descriptor_pool)
    return parser.MergeLines(lines, message)


class _Parser(object):
    __doc__ = 'Text format parser for protocol message.'

    def __init__(self, allow_unknown_extension=False, allow_field_number=False, descriptor_pool=None):
        self.allow_unknown_extension = allow_unknown_extension
        self.allow_field_number = allow_field_number
        self.descriptor_pool = descriptor_pool

    def ParseFromString(self, text, message):
        """Parses a text representation of a protocol message into a message."""
        if not isinstance(text, str):
            text = text.decode('utf-8')
        return self.ParseLines(text.split('\n'), message)

    def ParseLines(self, lines, message):
        """Parses a text representation of a protocol message into a message."""
        self._allow_multiple_scalars = False
        self._ParseOrMerge(lines, message)
        return message

    def MergeFromString(self, text, message):
        """Merges a text representation of a protocol message into a message."""
        return self._MergeLines(text.split('\n'), message)

    def MergeLines(self, lines, message):
        """Merges a text representation of a protocol message into a message."""
        self._allow_multiple_scalars = True
        self._ParseOrMerge(lines, message)
        return message

    def _ParseOrMerge(self, lines, message):
        """Converts a text representation of a protocol message into a message.

    Args:
      lines: Lines of a message's text representation.
      message: A protocol buffer message to merge into.

    Raises:
      ParseError: On text parsing problems.
    """
        tokenizer = Tokenizer(lines)
        while not tokenizer.AtEnd():
            self._MergeField(tokenizer, message)

    def _MergeField(self, tokenizer, message):
        """Merges a single protocol message field into a message.

    Args:
      tokenizer: A tokenizer to parse the field name and values.
      message: A protocol message to record the data.

    Raises:
      ParseError: In case of text parsing problems.
    """
        message_descriptor = message.DESCRIPTOR
        if message_descriptor.full_name == _ANY_FULL_TYPE_NAME:
            if tokenizer.TryConsume('['):
                type_url_prefix, packed_type_name = self._ConsumeAnyTypeUrl(tokenizer)
                tokenizer.Consume(']')
                tokenizer.TryConsume(':')
                if tokenizer.TryConsume('<'):
                    expanded_any_end_token = '>'
                else:
                    tokenizer.Consume('{')
                    expanded_any_end_token = '}'
                expanded_any_sub_message = _BuildMessageFromTypeName(packed_type_name, self.descriptor_pool)
                if not expanded_any_sub_message:
                    raise ParseError('Type %s not found in descriptor pool' % packed_type_name)
                while not tokenizer.TryConsume(expanded_any_end_token):
                    if tokenizer.AtEnd():
                        raise tokenizer.ParseErrorPreviousToken('Expected "%s".' % (
                         expanded_any_end_token,))
                    self._MergeField(tokenizer, expanded_any_sub_message)

                message.Pack(expanded_any_sub_message, type_url_prefix=type_url_prefix)
                return
            if tokenizer.TryConsume('['):
                name = [
                 tokenizer.ConsumeIdentifier()]
                while tokenizer.TryConsume('.'):
                    name.append(tokenizer.ConsumeIdentifier())

                name = '.'.join(name)
                if not message_descriptor.is_extendable:
                    raise tokenizer.ParseErrorPreviousToken('Message type "%s" does not have extensions.' % message_descriptor.full_name)
                field = message.Extensions._FindExtensionByName(name)
                if field or self.allow_unknown_extension:
                    field = None
                else:
                    raise tokenizer.ParseErrorPreviousToken('Extension "%s" not registered. Did you import the _pb2 module which defines it? If you are trying to place the extension in the MessageSet field of another message that is in an Any or MessageSet field, that message\'s _pb2 module must be imported as well' % name)
            else:
                if message_descriptor != field.containing_type:
                    raise tokenizer.ParseErrorPreviousToken('Extension "%s" does not extend message type "%s".' % (
                     name, message_descriptor.full_name))
                tokenizer.Consume(']')
        else:
            name = tokenizer.ConsumeIdentifierOrNumber()
        if self.allow_field_number and name.isdigit():
            number = ParseInteger(name, True, True)
            field = message_descriptor.fields_by_number.get(number, None)
            if not field:
                if message_descriptor.is_extendable:
                    field = message.Extensions._FindExtensionByNumber(number)
        else:
            field = message_descriptor.fields_by_name.get(name, None)
            if not field:
                field = message_descriptor.fields_by_name.get(name.lower(), None)
                if field:
                    if field.type != descriptor.FieldDescriptor.TYPE_GROUP:
                        field = None
        if field:
            if field.type == descriptor.FieldDescriptor.TYPE_GROUP:
                if field.message_type.name != name:
                    field = None
        if not field:
            raise tokenizer.ParseErrorPreviousToken('Message type "%s" has no field named "%s".' % (
             message_descriptor.full_name, name))
        else:
            if field:
                if not self._allow_multiple_scalars:
                    if field.containing_oneof:
                        which_oneof = message.WhichOneof(field.containing_oneof.name)
                        if which_oneof is not None:
                            if which_oneof != field.name:
                                raise tokenizer.ParseErrorPreviousToken('Field "%s" is specified along with field "%s", another member of oneof "%s" for message type "%s".' % (
                                 field.name, which_oneof, field.containing_oneof.name,
                                 message_descriptor.full_name))
                else:
                    if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_MESSAGE:
                        tokenizer.TryConsume(':')
                        merger = self._MergeMessageField
                    else:
                        tokenizer.Consume(':')
                        merger = self._MergeScalarField
                if field.label == descriptor.FieldDescriptor.LABEL_REPEATED and tokenizer.TryConsume('['):
                    if not tokenizer.TryConsume(']'):
                        while True:
                            merger(tokenizer, message, field)
                            if tokenizer.TryConsume(']'):
                                break
                            tokenizer.Consume(',')

                else:
                    merger(tokenizer, message, field)
            else:
                assert self.allow_unknown_extension
                _SkipFieldContents(tokenizer)
        if not tokenizer.TryConsume(','):
            tokenizer.TryConsume(';')

    def _ConsumeAnyTypeUrl(self, tokenizer):
        """Consumes a google.protobuf.Any type URL and returns the type name."""
        prefix = [
         tokenizer.ConsumeIdentifier()]
        tokenizer.Consume('.')
        prefix.append(tokenizer.ConsumeIdentifier())
        tokenizer.Consume('.')
        prefix.append(tokenizer.ConsumeIdentifier())
        tokenizer.Consume('/')
        name = [
         tokenizer.ConsumeIdentifier()]
        while tokenizer.TryConsume('.'):
            name.append(tokenizer.ConsumeIdentifier())

        return (
         '.'.join(prefix), '.'.join(name))

    def _MergeMessageField(self, tokenizer, message, field):
        """Merges a single scalar field into a message.

    Args:
      tokenizer: A tokenizer to parse the field value.
      message: The message of which field is a member.
      field: The descriptor of the field to be merged.

    Raises:
      ParseError: In case of text parsing problems.
    """
        is_map_entry = _IsMapEntry(field)
        if tokenizer.TryConsume('<'):
            end_token = '>'
        else:
            tokenizer.Consume('{')
            end_token = '}'
        if field.label == descriptor.FieldDescriptor.LABEL_REPEATED:
            if field.is_extension:
                sub_message = message.Extensions[field].add()
            else:
                if is_map_entry:
                    sub_message = getattr(message, field.name).GetEntryClass()()
                else:
                    sub_message = getattr(message, field.name).add()
        else:
            if field.is_extension:
                if not self._allow_multiple_scalars:
                    if message.HasExtension(field):
                        raise tokenizer.ParseErrorPreviousToken('Message type "%s" should not have multiple "%s" extensions.' % (
                         message.DESCRIPTOR.full_name, field.full_name))
                sub_message = message.Extensions[field]
            else:
                if not self._allow_multiple_scalars:
                    if message.HasField(field.name):
                        raise tokenizer.ParseErrorPreviousToken('Message type "%s" should not have multiple "%s" fields.' % (
                         message.DESCRIPTOR.full_name, field.name))
                sub_message = getattr(message, field.name)
            sub_message.SetInParent()
        while not tokenizer.TryConsume(end_token):
            if tokenizer.AtEnd():
                raise tokenizer.ParseErrorPreviousToken('Expected "%s".' % (end_token,))
            self._MergeField(tokenizer, sub_message)

        if is_map_entry:
            value_cpptype = field.message_type.fields_by_name['value'].cpp_type
            if value_cpptype == descriptor.FieldDescriptor.CPPTYPE_MESSAGE:
                value = getattr(message, field.name)[sub_message.key]
                value.MergeFrom(sub_message.value)
            else:
                getattr(message, field.name)[sub_message.key] = sub_message.value

    @staticmethod
    def _IsProto3Syntax(message):
        message_descriptor = message.DESCRIPTOR
        return hasattr(message_descriptor, 'syntax') and message_descriptor.syntax == 'proto3'

    def _MergeScalarField(self, tokenizer, message, field):
        """Merges a single scalar field into a message.

    Args:
      tokenizer: A tokenizer to parse the field value.
      message: A protocol message to record the data.
      field: The descriptor of the field to be merged.

    Raises:
      ParseError: In case of text parsing problems.
      RuntimeError: On runtime errors.
    """
        _ = self.allow_unknown_extension
        value = None
        if field.type in (descriptor.FieldDescriptor.TYPE_INT32,
         descriptor.FieldDescriptor.TYPE_SINT32,
         descriptor.FieldDescriptor.TYPE_SFIXED32):
            value = _ConsumeInt32(tokenizer)
        else:
            if field.type in (descriptor.FieldDescriptor.TYPE_INT64,
             descriptor.FieldDescriptor.TYPE_SINT64,
             descriptor.FieldDescriptor.TYPE_SFIXED64):
                value = _ConsumeInt64(tokenizer)
            else:
                if field.type in (descriptor.FieldDescriptor.TYPE_UINT32,
                 descriptor.FieldDescriptor.TYPE_FIXED32):
                    value = _ConsumeUint32(tokenizer)
                else:
                    if field.type in (descriptor.FieldDescriptor.TYPE_UINT64,
                     descriptor.FieldDescriptor.TYPE_FIXED64):
                        value = _ConsumeUint64(tokenizer)
                    else:
                        if field.type in (descriptor.FieldDescriptor.TYPE_FLOAT,
                         descriptor.FieldDescriptor.TYPE_DOUBLE):
                            value = tokenizer.ConsumeFloat()
                        else:
                            if field.type == descriptor.FieldDescriptor.TYPE_BOOL:
                                value = tokenizer.ConsumeBool()
                            else:
                                if field.type == descriptor.FieldDescriptor.TYPE_STRING:
                                    value = tokenizer.ConsumeString()
                                else:
                                    if field.type == descriptor.FieldDescriptor.TYPE_BYTES:
                                        value = tokenizer.ConsumeByteString()
                                    else:
                                        if field.type == descriptor.FieldDescriptor.TYPE_ENUM:
                                            value = tokenizer.ConsumeEnum(field)
                                        else:
                                            raise RuntimeError('Unknown field type %d' % field.type)
                    if field.label == descriptor.FieldDescriptor.LABEL_REPEATED:
                        if field.is_extension:
                            message.Extensions[field].append(value)
                        else:
                            getattr(message, field.name).append(value)
                    else:
                        can_check_presence = not self._IsProto3Syntax(message)
                    if field.is_extension:
                        if not self._allow_multiple_scalars:
                            if can_check_presence:
                                if message.HasExtension(field):
                                    raise tokenizer.ParseErrorPreviousToken('Message type "%s" should not have multiple "%s" extensions.' % (
                                     message.DESCRIPTOR.full_name, field.full_name))
                        else:
                            message.Extensions[field] = value
                    elif not self._allow_multiple_scalars and can_check_presence and message.HasField(field.name):
                        raise tokenizer.ParseErrorPreviousToken('Message type "%s" should not have multiple "%s" fields.' % (
                         message.DESCRIPTOR.full_name, field.name))
                    else:
                        setattr(message, field.name, value)


def _SkipFieldContents(tokenizer):
    """Skips over contents (value or message) of a field.

  Args:
    tokenizer: A tokenizer to parse the field name and values.
  """
    if tokenizer.TryConsume(':'):
        if not tokenizer.LookingAt('{'):
            if not tokenizer.LookingAt('<'):
                _SkipFieldValue(tokenizer)
    else:
        _SkipFieldMessage(tokenizer)


def _SkipField(tokenizer):
    """Skips over a complete field (name and value/message).

  Args:
    tokenizer: A tokenizer to parse the field name and values.
  """
    if tokenizer.TryConsume('['):
        tokenizer.ConsumeIdentifier()
        while tokenizer.TryConsume('.'):
            tokenizer.ConsumeIdentifier()

        tokenizer.Consume(']')
    else:
        tokenizer.ConsumeIdentifierOrNumber()
    _SkipFieldContents(tokenizer)
    if not tokenizer.TryConsume(','):
        tokenizer.TryConsume(';')


def _SkipFieldMessage(tokenizer):
    """Skips over a field message.

  Args:
    tokenizer: A tokenizer to parse the field name and values.
  """
    if tokenizer.TryConsume('<'):
        delimiter = '>'
    else:
        tokenizer.Consume('{')
        delimiter = '}'
    while not tokenizer.LookingAt('>') and not tokenizer.LookingAt('}'):
        _SkipField(tokenizer)

    tokenizer.Consume(delimiter)


def _SkipFieldValue(tokenizer):
    """Skips over a field value.

  Args:
    tokenizer: A tokenizer to parse the field name and values.

  Raises:
    ParseError: In case an invalid field value is found.
  """
    if tokenizer.TryConsumeByteString():
        while tokenizer.TryConsumeByteString():
            pass

        return
    if not tokenizer.TryConsumeIdentifier():
        if not _TryConsumeInt64(tokenizer):
            if not _TryConsumeUint64(tokenizer):
                if not tokenizer.TryConsumeFloat():
                    raise ParseError('Invalid field value: ' + tokenizer.token)


class Tokenizer(object):
    __doc__ = 'Protocol buffer text representation tokenizer.\n\n  This class handles the lower level string parsing by splitting it into\n  meaningful tokens.\n\n  It was directly ported from the Java protocol buffer API.\n  '
    _WHITESPACE = re.compile('\\s+')
    _COMMENT = re.compile('(\\s*#.*$)', re.MULTILINE)
    _WHITESPACE_OR_COMMENT = re.compile('(\\s|(#.*$))+', re.MULTILINE)
    _TOKEN = re.compile('|'.join([
     '[a-zA-Z_][0-9a-zA-Z_+-]*',
     '([0-9+-]|(\\.[0-9]))[0-9a-zA-Z_.+-]*'] + ['{qt}([^{qt}\\n\\\\]|\\\\.)*({qt}|\\\\?$)'.format(qt=mark) for mark in _QUOTES]))
    _IDENTIFIER = re.compile('[^\\d\\W]\\w*')
    _IDENTIFIER_OR_NUMBER = re.compile('\\w+')

    def __init__(self, lines, skip_comments=True):
        self._position = 0
        self._line = -1
        self._column = 0
        self._token_start = None
        self.token = ''
        self._lines = iter(lines)
        self._current_line = ''
        self._previous_line = 0
        self._previous_column = 0
        self._more_lines = True
        self._skip_comments = skip_comments
        self._whitespace_pattern = skip_comments and self._WHITESPACE_OR_COMMENT or self._WHITESPACE
        self._SkipWhitespace()
        self.NextToken()

    def LookingAt(self, token):
        return self.token == token

    def AtEnd(self):
        """Checks the end of the text was reached.

    Returns:
      True iff the end was reached.
    """
        return not self.token

    def _PopLine(self):
        while len(self._current_line) <= self._column:
            try:
                self._current_line = next(self._lines)
            except StopIteration:
                self._current_line = ''
                self._more_lines = False
                return
            else:
                self._line += 1
                self._column = 0

    def _SkipWhitespace(self):
        while True:
            self._PopLine()
            match = self._whitespace_pattern.match(self._current_line, self._column)
            if not match:
                break
            length = len(match.group(0))
            self._column += length

    def TryConsume(self, token):
        """Tries to consume a given piece of text.

    Args:
      token: Text to consume.

    Returns:
      True iff the text was consumed.
    """
        if self.token == token:
            self.NextToken()
            return True
        else:
            return False

    def Consume(self, token):
        """Consumes a piece of text.

    Args:
      token: Text to consume.

    Raises:
      ParseError: If the text couldn't be consumed.
    """
        if not self.TryConsume(token):
            raise self.ParseError('Expected "%s".' % token)

    def ConsumeComment(self):
        result = self.token
        if not self._COMMENT.match(result):
            raise self.ParseError('Expected comment.')
        self.NextToken()
        return result

    def ConsumeCommentOrTrailingComment(self):
        """Consumes a comment, returns a 2-tuple (trailing bool, comment str)."""
        just_started = self._line == 0 and self._column == 0
        before_parsing = self._previous_line
        comment = self.ConsumeComment()
        trailing = self._previous_line == before_parsing and not just_started
        return (
         trailing, comment)

    def TryConsumeIdentifier(self):
        try:
            self.ConsumeIdentifier()
            return True
        except ParseError:
            return False

    def ConsumeIdentifier(self):
        """Consumes protocol message field identifier.

    Returns:
      Identifier string.

    Raises:
      ParseError: If an identifier couldn't be consumed.
    """
        result = self.token
        if not self._IDENTIFIER.match(result):
            raise self.ParseError('Expected identifier.')
        self.NextToken()
        return result

    def TryConsumeIdentifierOrNumber(self):
        try:
            self.ConsumeIdentifierOrNumber()
            return True
        except ParseError:
            return False

    def ConsumeIdentifierOrNumber(self):
        """Consumes protocol message field identifier.

    Returns:
      Identifier string.

    Raises:
      ParseError: If an identifier couldn't be consumed.
    """
        result = self.token
        if not self._IDENTIFIER_OR_NUMBER.match(result):
            raise self.ParseError('Expected identifier or number, got %s.' % result)
        self.NextToken()
        return result

    def TryConsumeInteger(self):
        try:
            self.ConsumeInteger()
            return True
        except ParseError:
            return False

    def ConsumeInteger(self, is_long=False):
        """Consumes an integer number.

    Args:
      is_long: True if the value should be returned as a long integer.
    Returns:
      The integer parsed.

    Raises:
      ParseError: If an integer couldn't be consumed.
    """
        try:
            result = _ParseAbstractInteger((self.token), is_long=is_long)
        except ValueError as e:
            raise self.ParseError(str(e))

        self.NextToken()
        return result

    def TryConsumeFloat(self):
        try:
            self.ConsumeFloat()
            return True
        except ParseError:
            return False

    def ConsumeFloat(self):
        """Consumes an floating point number.

    Returns:
      The number parsed.

    Raises:
      ParseError: If a floating point number couldn't be consumed.
    """
        try:
            result = ParseFloat(self.token)
        except ValueError as e:
            raise self.ParseError(str(e))

        self.NextToken()
        return result

    def ConsumeBool(self):
        """Consumes a boolean value.

    Returns:
      The bool parsed.

    Raises:
      ParseError: If a boolean value couldn't be consumed.
    """
        try:
            result = ParseBool(self.token)
        except ValueError as e:
            raise self.ParseError(str(e))

        self.NextToken()
        return result

    def TryConsumeByteString(self):
        try:
            self.ConsumeByteString()
            return True
        except ParseError:
            return False

    def ConsumeString(self):
        """Consumes a string value.

    Returns:
      The string parsed.

    Raises:
      ParseError: If a string value couldn't be consumed.
    """
        the_bytes = self.ConsumeByteString()
        try:
            return six.text_type(the_bytes, 'utf-8')
        except UnicodeDecodeError as e:
            raise self._StringParseError(e)

    def ConsumeByteString(self):
        """Consumes a byte array value.

    Returns:
      The array parsed (as a string).

    Raises:
      ParseError: If a byte array value couldn't be consumed.
    """
        the_list = [
         self._ConsumeSingleByteString()]
        while self.token and self.token[0] in _QUOTES:
            the_list.append(self._ConsumeSingleByteString())

        return (b'').join(the_list)

    def _ConsumeSingleByteString(self):
        """Consume one token of a string literal.

    String literals (whether bytes or text) can come in multiple adjacent
    tokens which are automatically concatenated, like in C or Python.  This
    method only consumes one token.

    Returns:
      The token parsed.
    Raises:
      ParseError: When the wrong format data is found.
    """
        text = self.token
        if len(text) < 1 or text[0] not in _QUOTES:
            raise self.ParseError('Expected string but found: %r' % (text,))
        if len(text) < 2 or text[(-1)] != text[0]:
            raise self.ParseError('String missing ending quote: %r' % (text,))
        try:
            result = text_encoding.CUnescape(text[1:-1])
        except ValueError as e:
            raise self.ParseError(str(e))

        self.NextToken()
        return result

    def ConsumeEnum(self, field):
        try:
            result = ParseEnum(field, self.token)
        except ValueError as e:
            raise self.ParseError(str(e))

        self.NextToken()
        return result

    def ParseErrorPreviousToken(self, message):
        """Creates and *returns* a ParseError for the previously read token.

    Args:
      message: A message to set for the exception.

    Returns:
      A ParseError instance.
    """
        return ParseError(message, self._previous_line + 1, self._previous_column + 1)

    def ParseError(self, message):
        """Creates and *returns* a ParseError for the current token."""
        return ParseError(message, self._line + 1, self._column + 1)

    def _StringParseError(self, e):
        return self.ParseError("Couldn't parse string: " + str(e))

    def NextToken(self):
        """Reads the next meaningful token."""
        self._previous_line = self._line
        self._previous_column = self._column
        self._column += len(self.token)
        self._SkipWhitespace()
        if not self._more_lines:
            self.token = ''
            return
        else:
            match = self._TOKEN.match(self._current_line, self._column)
            if not match:
                if not self._skip_comments:
                    match = self._COMMENT.match(self._current_line, self._column)
            if match:
                token = match.group(0)
                self.token = token
            else:
                self.token = self._current_line[self._column]


_Tokenizer = Tokenizer

def _ConsumeInt32(tokenizer):
    """Consumes a signed 32bit integer number from tokenizer.

  Args:
    tokenizer: A tokenizer used to parse the number.

  Returns:
    The integer parsed.

  Raises:
    ParseError: If a signed 32bit integer couldn't be consumed.
  """
    return _ConsumeInteger(tokenizer, is_signed=True, is_long=False)


def _ConsumeUint32(tokenizer):
    """Consumes an unsigned 32bit integer number from tokenizer.

  Args:
    tokenizer: A tokenizer used to parse the number.

  Returns:
    The integer parsed.

  Raises:
    ParseError: If an unsigned 32bit integer couldn't be consumed.
  """
    return _ConsumeInteger(tokenizer, is_signed=False, is_long=False)


def _TryConsumeInt64(tokenizer):
    try:
        _ConsumeInt64(tokenizer)
        return True
    except ParseError:
        return False


def _ConsumeInt64(tokenizer):
    """Consumes a signed 32bit integer number from tokenizer.

  Args:
    tokenizer: A tokenizer used to parse the number.

  Returns:
    The integer parsed.

  Raises:
    ParseError: If a signed 32bit integer couldn't be consumed.
  """
    return _ConsumeInteger(tokenizer, is_signed=True, is_long=True)


def _TryConsumeUint64(tokenizer):
    try:
        _ConsumeUint64(tokenizer)
        return True
    except ParseError:
        return False


def _ConsumeUint64(tokenizer):
    """Consumes an unsigned 64bit integer number from tokenizer.

  Args:
    tokenizer: A tokenizer used to parse the number.

  Returns:
    The integer parsed.

  Raises:
    ParseError: If an unsigned 64bit integer couldn't be consumed.
  """
    return _ConsumeInteger(tokenizer, is_signed=False, is_long=True)


def _TryConsumeInteger(tokenizer, is_signed=False, is_long=False):
    try:
        _ConsumeInteger(tokenizer, is_signed=is_signed, is_long=is_long)
        return True
    except ParseError:
        return False


def _ConsumeInteger(tokenizer, is_signed=False, is_long=False):
    """Consumes an integer number from tokenizer.

  Args:
    tokenizer: A tokenizer used to parse the number.
    is_signed: True if a signed integer must be parsed.
    is_long: True if a long integer must be parsed.

  Returns:
    The integer parsed.

  Raises:
    ParseError: If an integer with given characteristics couldn't be consumed.
  """
    try:
        result = ParseInteger((tokenizer.token), is_signed=is_signed, is_long=is_long)
    except ValueError as e:
        raise tokenizer.ParseError(str(e))

    tokenizer.NextToken()
    return result


def ParseInteger(text, is_signed=False, is_long=False):
    """Parses an integer.

  Args:
    text: The text to parse.
    is_signed: True if a signed integer must be parsed.
    is_long: True if a long integer must be parsed.

  Returns:
    The integer value.

  Raises:
    ValueError: Thrown Iff the text is not a valid integer.
  """
    result = _ParseAbstractInteger(text, is_long=is_long)
    checker = _INTEGER_CHECKERS[(2 * int(is_long) + int(is_signed))]
    checker.CheckValue(result)
    return result


def _ParseAbstractInteger(text, is_long=False):
    """Parses an integer without checking size/signedness.

  Args:
    text: The text to parse.
    is_long: True if the value should be returned as a long integer.

  Returns:
    The integer value.

  Raises:
    ValueError: Thrown Iff the text is not a valid integer.
  """
    try:
        if is_long:
            return int(text, 0)
        else:
            return int(text, 0)
    except ValueError:
        raise ValueError("Couldn't parse integer: %s" % text)


def ParseFloat(text):
    """Parse a floating point number.

  Args:
    text: Text to parse.

  Returns:
    The number parsed.

  Raises:
    ValueError: If a floating point number couldn't be parsed.
  """
    try:
        return float(text)
    except ValueError:
        if _FLOAT_INFINITY.match(text):
            if text[0] == '-':
                return float('-inf')
            else:
                return float('inf')
        else:
            if _FLOAT_NAN.match(text):
                return float('nan')
            try:
                return float(text.rstrip('f'))
            except ValueError:
                raise ValueError("Couldn't parse float: %s" % text)


def ParseBool(text):
    """Parse a boolean value.

  Args:
    text: Text to parse.

  Returns:
    Boolean values parsed

  Raises:
    ValueError: If text is not a valid boolean.
  """
    if text in ('true', 't', '1', 'True'):
        return True
    if text in ('false', 'f', '0', 'False'):
        return False
    raise ValueError('Expected "true" or "false".')


def ParseEnum(field, value):
    """Parse an enum value.

  The value can be specified by a number (the enum value), or by
  a string literal (the enum name).

  Args:
    field: Enum field descriptor.
    value: String value.

  Returns:
    Enum value number.

  Raises:
    ValueError: If the enum value could not be parsed.
  """
    enum_descriptor = field.enum_type
    try:
        number = int(value, 0)
    except ValueError:
        enum_value = enum_descriptor.values_by_name.get(value, None)
        if enum_value is None:
            raise ValueError('Enum type "%s" has no value named %s.' % (
             enum_descriptor.full_name, value))
    else:
        if hasattr(field.file, 'syntax'):
            if field.file.syntax == 'proto3':
                return number
        enum_value = enum_descriptor.values_by_number.get(number, None)
        if enum_value is None:
            raise ValueError('Enum type "%s" has no value with number %d.' % (
             enum_descriptor.full_name, number))
        return enum_value.number