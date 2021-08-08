# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\google\protobuf\reflection.py
"""Contains a metaclass and helper functions used to create
protocol message classes from Descriptor objects at runtime.

Recall that a metaclass is the "type" of a class.
(A class is to a metaclass what an instance is to a class.)

In this case, we use the GeneratedProtocolMessageType metaclass
to inject all the useful functionality into the classes
output by the protocol compiler at compile-time.

The upshot of all this is that the real implementation
details for ALL pure-Python protocol buffers are *here in
this file*.
"""
__author__ = 'robinson@google.com (Will Robinson)'
from google.protobuf.internal import api_implementation
from google.protobuf import message
if api_implementation.Type() == 'cpp':
    from google.protobuf.pyext import cpp_message as message_impl
else:
    from google.protobuf.internal import python_message as message_impl
GeneratedProtocolMessageType = message_impl.GeneratedProtocolMessageType
MESSAGE_CLASS_CACHE = {}

def ParseMessage(descriptor, byte_str):
    """Generate a new Message instance from this Descriptor and a byte string.

  Args:
    descriptor: Protobuf Descriptor object
    byte_str: Serialized protocol buffer byte string

  Returns:
    Newly created protobuf Message object.
  """
    result_class = MakeClass(descriptor)
    new_msg = result_class()
    new_msg.ParseFromString(byte_str)
    return new_msg


def MakeClass(descriptor):
    """Construct a class object for a protobuf described by descriptor.

  Composite descriptors are handled by defining the new class as a member of the
  parent class, recursing as deep as necessary.
  This is the dynamic equivalent to:

  class Parent(message.Message):
    __metaclass__ = GeneratedProtocolMessageType
    DESCRIPTOR = descriptor
    class Child(message.Message):
      __metaclass__ = GeneratedProtocolMessageType
      DESCRIPTOR = descriptor.nested_types[0]

  Sample usage:
    file_descriptor = descriptor_pb2.FileDescriptorProto()
    file_descriptor.ParseFromString(proto2_string)
    msg_descriptor = descriptor.MakeDescriptor(file_descriptor.message_type[0])
    msg_class = reflection.MakeClass(msg_descriptor)
    msg = msg_class()

  Args:
    descriptor: A descriptor.Descriptor object describing the protobuf.
  Returns:
    The Message class object described by the descriptor.
  """
    if descriptor in MESSAGE_CLASS_CACHE:
        return MESSAGE_CLASS_CACHE[descriptor]
    else:
        attributes = {}
        for name, nested_type in list(descriptor.nested_types_by_name.items()):
            attributes[name] = MakeClass(nested_type)

        attributes[GeneratedProtocolMessageType._DESCRIPTOR_KEY] = descriptor
        result = GeneratedProtocolMessageType(str(descriptor.name), (message.Message,), attributes)
        MESSAGE_CLASS_CACHE[descriptor] = result
        return result