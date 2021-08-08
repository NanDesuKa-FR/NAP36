# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\universaldetector.py
"""
Module containing the UniversalDetector detector class, which is the primary
class a user of ``chardet`` should use.

:author: Mark Pilgrim (initial port to Python)
:author: Shy Shalom (original C code)
:author: Dan Blanchard (major refactoring for 3.0)
:author: Ian Cordasco
"""
import codecs, logging, re
from .charsetgroupprober import CharSetGroupProber
from .enums import InputState, LanguageFilter, ProbingState
from .escprober import EscCharSetProber
from .latin1prober import Latin1Prober
from .mbcsgroupprober import MBCSGroupProber
from .sbcsgroupprober import SBCSGroupProber

class UniversalDetector(object):
    __doc__ = '\n    The ``UniversalDetector`` class underlies the ``chardet.detect`` function\n    and coordinates all of the different charset probers.\n\n    To get a ``dict`` containing an encoding and its confidence, you can simply\n    run:\n\n    .. code::\n\n            u = UniversalDetector()\n            u.feed(some_bytes)\n            u.close()\n            detected = u.result\n\n    '
    MINIMUM_THRESHOLD = 0.2
    HIGH_BYTE_DETECTOR = re.compile(b'[\x80-\xff]')
    ESC_DETECTOR = re.compile(b'(\x1b|~{)')
    WIN_BYTE_DETECTOR = re.compile(b'[\x80-\x9f]')
    ISO_WIN_MAP = {'iso-8859-1':'Windows-1252',  'iso-8859-2':'Windows-1250', 
     'iso-8859-5':'Windows-1251', 
     'iso-8859-6':'Windows-1256', 
     'iso-8859-7':'Windows-1253', 
     'iso-8859-8':'Windows-1255', 
     'iso-8859-9':'Windows-1254', 
     'iso-8859-13':'Windows-1257'}

    def __init__(self, lang_filter=LanguageFilter.ALL):
        self._esc_charset_prober = None
        self._charset_probers = []
        self.result = None
        self.done = None
        self._got_data = None
        self._input_state = None
        self._last_char = None
        self.lang_filter = lang_filter
        self.logger = logging.getLogger(__name__)
        self._has_win_bytes = None
        self.reset()

    def reset(self):
        """
        Reset the UniversalDetector and all of its probers back to their
        initial states.  This is called by ``__init__``, so you only need to
        call this directly in between analyses of different documents.
        """
        self.result = {'encoding':None, 
         'confidence':0.0,  'language':None}
        self.done = False
        self._got_data = False
        self._has_win_bytes = False
        self._input_state = InputState.PURE_ASCII
        self._last_char = b''
        if self._esc_charset_prober:
            self._esc_charset_prober.reset()
        for prober in self._charset_probers:
            prober.reset()

    def feed(self, byte_str):
        """
        Takes a chunk of a document and feeds it through all of the relevant
        charset probers.

        After calling ``feed``, you can check the value of the ``done``
        attribute to see if you need to continue feeding the
        ``UniversalDetector`` more data, or if it has made a prediction
        (in the ``result`` attribute).

        .. note::
           You should always call ``close`` when you're done feeding in your
           document if ``done`` is not already ``True``.
        """
        if self.done:
            return
        elif not len(byte_str):
            return
        elif not isinstance(byte_str, bytearray):
            byte_str = bytearray(byte_str)
        else:
            if self._got_data or byte_str.startswith(codecs.BOM_UTF8):
                self.result = {'encoding':'UTF-8-SIG',  'confidence':1.0, 
                 'language':''}
            else:
                if byte_str.startswith((codecs.BOM_UTF32_LE,
                 codecs.BOM_UTF32_BE)):
                    self.result = {'encoding':'UTF-32', 
                     'confidence':1.0, 
                     'language':''}
                else:
                    if byte_str.startswith(b'\xfe\xff\x00\x00'):
                        self.result = {'encoding':'X-ISO-10646-UCS-4-3412',  'confidence':1.0, 
                         'language':''}
                    else:
                        if byte_str.startswith(b'\x00\x00\xff\xfe'):
                            self.result = {'encoding':'X-ISO-10646-UCS-4-2143',  'confidence':1.0, 
                             'language':''}
                        elif byte_str.startswith((codecs.BOM_LE, codecs.BOM_BE)):
                            self.result = {'encoding':'UTF-16', 
                             'confidence':1.0, 
                             'language':''}
                        else:
                            self._got_data = True
                            if self.result['encoding'] is not None:
                                self.done = True
                                return
                            if self._input_state == InputState.PURE_ASCII:
                                if self.HIGH_BYTE_DETECTOR.search(byte_str):
                                    self._input_state = InputState.HIGH_BYTE
                                elif self._input_state == InputState.PURE_ASCII:
                                    if self.ESC_DETECTOR.search(self._last_char + byte_str):
                                        self._input_state = InputState.ESC_ASCII
                self._last_char = byte_str[-1:]
                if self._input_state == InputState.ESC_ASCII:
                    if not self._esc_charset_prober:
                        self._esc_charset_prober = EscCharSetProber(self.lang_filter)
                    if self._esc_charset_prober.feed(byte_str) == ProbingState.FOUND_IT:
                        self.result = {'encoding':self._esc_charset_prober.charset_name,  'confidence':self._esc_charset_prober.get_confidence(), 
                         'language':self._esc_charset_prober.language}
                        self.done = True
                elif self._input_state == InputState.HIGH_BYTE:
                    if not self._charset_probers:
                        self._charset_probers = [
                         MBCSGroupProber(self.lang_filter)]
                        if self.lang_filter & LanguageFilter.NON_CJK:
                            self._charset_probers.append(SBCSGroupProber())
                        self._charset_probers.append(Latin1Prober())
                    for prober in self._charset_probers:
                        if prober.feed(byte_str) == ProbingState.FOUND_IT:
                            self.result = {'encoding':prober.charset_name, 
                             'confidence':prober.get_confidence(), 
                             'language':prober.language}
                            self.done = True
                            break

                    if self.WIN_BYTE_DETECTOR.search(byte_str):
                        self._has_win_bytes = True

    def close(self):
        """
        Stop analyzing the current document and come up with a final
        prediction.

        :returns:  The ``result`` attribute, a ``dict`` with the keys
                   `encoding`, `confidence`, and `language`.
        """
        if self.done:
            return self.result
        else:
            self.done = True
            if not self._got_data:
                self.logger.debug('no data received!')
            else:
                if self._input_state == InputState.PURE_ASCII:
                    self.result = {'encoding':'ascii', 
                     'confidence':1.0, 
                     'language':''}
                else:
                    if self._input_state == InputState.HIGH_BYTE:
                        prober_confidence = None
                        max_prober_confidence = 0.0
                        max_prober = None
                        for prober in self._charset_probers:
                            if not prober:
                                pass
                            else:
                                prober_confidence = prober.get_confidence()
                                if prober_confidence > max_prober_confidence:
                                    max_prober_confidence = prober_confidence
                                    max_prober = prober

                        if max_prober:
                            if max_prober_confidence > self.MINIMUM_THRESHOLD:
                                charset_name = max_prober.charset_name
                                lower_charset_name = max_prober.charset_name.lower()
                                confidence = max_prober.get_confidence()
                                if lower_charset_name.startswith('iso-8859'):
                                    if self._has_win_bytes:
                                        charset_name = self.ISO_WIN_MAP.get(lower_charset_name, charset_name)
                                self.result = {'encoding':charset_name, 
                                 'confidence':confidence, 
                                 'language':max_prober.language}
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                if self.result['encoding'] is None:
                    self.logger.debug('no probers hit minimum threshold')
                    for group_prober in self._charset_probers:
                        if not group_prober:
                            pass
                        else:
                            if isinstance(group_prober, CharSetGroupProber):
                                for prober in group_prober.probers:
                                    self.logger.debug('%s %s confidence = %s', prober.charset_name, prober.language, prober.get_confidence())

                            else:
                                self.logger.debug('%s %s confidence = %s', prober.charset_name, prober.language, prober.get_confidence())

            return self.result