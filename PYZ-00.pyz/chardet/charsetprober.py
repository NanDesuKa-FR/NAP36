# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\charsetprober.py
import logging, re
from .enums import ProbingState

class CharSetProber(object):
    SHORTCUT_THRESHOLD = 0.95

    def __init__(self, lang_filter=None):
        self._state = None
        self.lang_filter = lang_filter
        self.logger = logging.getLogger(__name__)

    def reset(self):
        self._state = ProbingState.DETECTING

    @property
    def charset_name(self):
        pass

    def feed(self, buf):
        pass

    @property
    def state(self):
        return self._state

    def get_confidence(self):
        return 0.0

    @staticmethod
    def filter_high_byte_only(buf):
        buf = re.sub(b'([\x00-\x7f])+', b' ', buf)
        return buf

    @staticmethod
    def filter_international_words(buf):
        """
        We define three types of bytes:
        alphabet: english alphabets [a-zA-Z]
        international: international characters [\x80-ÿ]
        marker: everything else [^a-zA-Z\x80-ÿ]

        The input buffer can be thought to contain a series of words delimited
        by markers. This function works to filter all words that contain at
        least one international character. All contiguous sequences of markers
        are replaced by a single space ascii character.

        This filter applies to all scripts which do not use English characters.
        """
        filtered = bytearray()
        words = re.findall(b'[a-zA-Z]*[\x80-\xff]+[a-zA-Z]*[^a-zA-Z\x80-\xff]?', buf)
        for word in words:
            filtered.extend(word[:-1])
            last_char = word[-1:]
            if not last_char.isalpha():
                if last_char < b'\x80':
                    last_char = b' '
            filtered.extend(last_char)

        return filtered

    @staticmethod
    def filter_with_english_letters(buf):
        """
        Returns a copy of ``buf`` that retains only the sequences of English
        alphabet and high byte characters that are not between <> characters.
        Also retains English alphabet and high byte characters immediately
        before occurrences of >.

        This filter can be applied to all scripts which contain both English
        characters and extended ASCII characters, but is currently only used by
        ``Latin1Prober``.
        """
        filtered = bytearray()
        in_tag = False
        prev = 0
        for curr in range(len(buf)):
            buf_char = buf[curr:curr + 1]
            if buf_char == b'>':
                in_tag = False
            else:
                if buf_char == b'<':
                    in_tag = True
            if buf_char < b'\x80':
                if not buf_char.isalpha():
                    if curr > prev:
                        if not in_tag:
                            filtered.extend(buf[prev:curr])
                            filtered.extend(b' ')
                prev = curr + 1

        if not in_tag:
            filtered.extend(buf[prev:])
        return filtered