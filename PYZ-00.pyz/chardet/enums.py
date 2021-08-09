# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\enums.py
"""
All of the Enums that are used throughout the chardet package.

:author: Dan Blanchard (dan.blanchard@gmail.com)
"""

class InputState(object):
    __doc__ = '\n    This enum represents the different states a universal detector can be in.\n    '
    PURE_ASCII = 0
    ESC_ASCII = 1
    HIGH_BYTE = 2


class LanguageFilter(object):
    __doc__ = '\n    This enum represents the different language filters we can apply to a\n    ``UniversalDetector``.\n    '
    CHINESE_SIMPLIFIED = 1
    CHINESE_TRADITIONAL = 2
    JAPANESE = 4
    KOREAN = 8
    NON_CJK = 16
    ALL = 31
    CHINESE = CHINESE_SIMPLIFIED | CHINESE_TRADITIONAL
    CJK = CHINESE | JAPANESE | KOREAN


class ProbingState(object):
    __doc__ = '\n    This enum represents the different states a prober can be in.\n    '
    DETECTING = 0
    FOUND_IT = 1
    NOT_ME = 2


class MachineState(object):
    __doc__ = '\n    This enum represents the different states a state machine can be in.\n    '
    START = 0
    ERROR = 1
    ITS_ME = 2


class SequenceLikelihood(object):
    __doc__ = '\n    This enum represents the likelihood of a character following the previous one.\n    '
    NEGATIVE = 0
    UNLIKELY = 1
    LIKELY = 2
    POSITIVE = 3

    @classmethod
    def get_num_categories(cls):
        """:returns: The number of likelihood categories in the enum."""
        return 4


class CharacterCategory(object):
    __doc__ = '\n    This enum represents the different categories language models for\n    ``SingleByteCharsetProber`` put characters into.\n\n    Anything less than CONTROL is considered a letter.\n    '
    UNDEFINED = 255
    LINE_BREAK = 254
    SYMBOL = 253
    DIGIT = 252
    CONTROL = 251