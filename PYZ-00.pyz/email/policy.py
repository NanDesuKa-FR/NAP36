# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: email\policy.py
"""This will be the home for the policy that hooks in the new
code that adds all the email6 features.
"""
import re
from email._policybase import Policy, Compat32, compat32, _extend_docstrings
from email.utils import _has_surrogates
from email.headerregistry import HeaderRegistry
from email.contentmanager import raw_data_manager
from email.message import EmailMessage
__all__ = [
 'Compat32',
 'compat32',
 'Policy',
 'EmailPolicy',
 'default',
 'strict',
 'SMTP',
 'HTTP']
linesep_splitter = re.compile('\\n|\\r')

@_extend_docstrings
class EmailPolicy(Policy):
    __doc__ = "+\n    PROVISIONAL\n\n    The API extensions enabled by this policy are currently provisional.\n    Refer to the documentation for details.\n\n    This policy adds new header parsing and folding algorithms.  Instead of\n    simple strings, headers are custom objects with custom attributes\n    depending on the type of the field.  The folding algorithm fully\n    implements RFCs 2047 and 5322.\n\n    In addition to the settable attributes listed above that apply to\n    all Policies, this policy adds the following additional attributes:\n\n    utf8                -- if False (the default) message headers will be\n                           serialized as ASCII, using encoded words to encode\n                           any non-ASCII characters in the source strings.  If\n                           True, the message headers will be serialized using\n                           utf8 and will not contain encoded words (see RFC\n                           6532 for more on this serialization format).\n\n    refold_source       -- if the value for a header in the Message object\n                           came from the parsing of some source, this attribute\n                           indicates whether or not a generator should refold\n                           that value when transforming the message back into\n                           stream form.  The possible values are:\n\n                           none  -- all source values use original folding\n                           long  -- source values that have any line that is\n                                    longer than max_line_length will be\n                                    refolded\n                           all  -- all values are refolded.\n\n                           The default is 'long'.\n\n    header_factory      -- a callable that takes two arguments, 'name' and\n                           'value', where 'name' is a header field name and\n                           'value' is an unfolded header field value, and\n                           returns a string-like object that represents that\n                           header.  A default header_factory is provided that\n                           understands some of the RFC5322 header field types.\n                           (Currently address fields and date fields have\n                           special treatment, while all other fields are\n                           treated as unstructured.  This list will be\n                           completed before the extension is marked stable.)\n\n    content_manager     -- an object with at least two methods: get_content\n                           and set_content.  When the get_content or\n                           set_content method of a Message object is called,\n                           it calls the corresponding method of this object,\n                           passing it the message object as its first argument,\n                           and any arguments or keywords that were passed to\n                           it as additional arguments.  The default\n                           content_manager is\n                           :data:`~email.contentmanager.raw_data_manager`.\n\n    "
    message_factory = EmailMessage
    utf8 = False
    refold_source = 'long'
    header_factory = HeaderRegistry()
    content_manager = raw_data_manager

    def __init__(self, **kw):
        if 'header_factory' not in kw:
            object.__setattr__(self, 'header_factory', HeaderRegistry())
        (super().__init__)(**kw)

    def header_max_count(self, name):
        """+
        The implementation for this class returns the max_count attribute from
        the specialized header class that would be used to construct a header
        of type 'name'.
        """
        return self.header_factory[name].max_count

    def header_source_parse(self, sourcelines):
        """+
        The name is parsed as everything up to the ':' and returned unmodified.
        The value is determined by stripping leading whitespace off the
        remainder of the first line, joining all subsequent lines together, and
        stripping any trailing carriage return or linefeed characters.  (This
        is the same as Compat32).

        """
        name, value = sourcelines[0].split(':', 1)
        value = value.lstrip(' \t') + ''.join(sourcelines[1:])
        return (name, value.rstrip('\r\n'))

    def header_store_parse(self, name, value):
        """+
        The name is returned unchanged.  If the input value has a 'name'
        attribute and it matches the name ignoring case, the value is returned
        unchanged.  Otherwise the name and value are passed to header_factory
        method, and the resulting custom header object is returned as the
        value.  In this case a ValueError is raised if the input value contains
        CR or LF characters.

        """
        if hasattr(value, 'name'):
            if value.name.lower() == name.lower():
                return (
                 name, value)
        if isinstance(value, str):
            if len(value.splitlines()) > 1:
                raise ValueError('Header values may not contain linefeed or carriage return characters')
        return (
         name, self.header_factory(name, value))

    def header_fetch_parse(self, name, value):
        """+
        If the value has a 'name' attribute, it is returned to unmodified.
        Otherwise the name and the value with any linesep characters removed
        are passed to the header_factory method, and the resulting custom
        header object is returned.  Any surrogateescaped bytes get turned
        into the unicode unknown-character glyph.

        """
        if hasattr(value, 'name'):
            return value
        else:
            value = ''.join(linesep_splitter.split(value))
            return self.header_factory(name, value)

    def fold(self, name, value):
        """+
        Header folding is controlled by the refold_source policy setting.  A
        value is considered to be a 'source value' if and only if it does not
        have a 'name' attribute (having a 'name' attribute means it is a header
        object of some sort).  If a source value needs to be refolded according
        to the policy, it is converted into a custom header object by passing
        the name and the value with any linesep characters removed to the
        header_factory method.  Folding of a custom header object is done by
        calling its fold method with the current policy.

        Source values are split into lines using splitlines.  If the value is
        not to be refolded, the lines are rejoined using the linesep from the
        policy and returned.  The exception is lines containing non-ascii
        binary data.  In that case the value is refolded regardless of the
        refold_source setting, which causes the binary data to be CTE encoded
        using the unknown-8bit charset.

        """
        return self._fold(name, value, refold_binary=True)

    def fold_binary(self, name, value):
        """+
        The same as fold if cte_type is 7bit, except that the returned value is
        bytes.

        If cte_type is 8bit, non-ASCII binary data is converted back into
        bytes.  Headers with binary data are not refolded, regardless of the
        refold_header setting, since there is no way to know whether the binary
        data consists of single byte characters or multibyte characters.

        If utf8 is true, headers are encoded to utf8, otherwise to ascii with
        non-ASCII unicode rendered as encoded words.

        """
        folded = self._fold(name, value, refold_binary=(self.cte_type == '7bit'))
        charset = 'utf8' if self.utf8 else 'ascii'
        return folded.encode(charset, 'surrogateescape')

    def _fold(self, name, value, refold_binary=False):
        if hasattr(value, 'name'):
            return value.fold(policy=self)
        else:
            maxlen = self.max_line_length if self.max_line_length else float('inf')
            lines = value.splitlines()
            refold = self.refold_source == 'all' or self.refold_source == 'long' and (lines and len(lines[0]) + len(name) + 2 > maxlen or any(len(x) > maxlen for x in lines[1:]))
            if refold or refold_binary and _has_surrogates(value):
                return self.header_factory(name, ''.join(lines)).fold(policy=self)
            return name + ': ' + self.linesep.join(lines) + self.linesep


default = EmailPolicy()
del default.header_factory
strict = default.clone(raise_on_defect=True)
SMTP = default.clone(linesep='\r\n')
HTTP = default.clone(linesep='\r\n', max_line_length=None)
SMTPUTF8 = SMTP.clone(utf8=True)