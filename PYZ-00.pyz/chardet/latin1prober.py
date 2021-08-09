# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\latin1prober.py
from .charsetprober import CharSetProber
from .enums import ProbingState
FREQ_CAT_NUM = 4
UDF = 0
OTH = 1
ASC = 2
ASS = 3
ACV = 4
ACO = 5
ASV = 6
ASO = 7
CLASS_NUM = 8
Latin1_CharToClass = (
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, ASC, ASC, ASC, ASC, ASC, ASC, ASC,
 ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC,
 ASC, ASC, ASC, ASC, ASC, ASC, ASC, ASC,
 ASC, ASC, ASC, OTH, OTH, OTH, OTH, OTH,
 OTH, ASS, ASS, ASS, ASS, ASS, ASS, ASS,
 ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS,
 ASS, ASS, ASS, ASS, ASS, ASS, ASS, ASS,
 ASS, ASS, ASS, OTH, OTH, OTH, OTH, OTH,
 OTH, UDF, OTH, ASO, OTH, OTH, OTH, OTH,
 OTH, OTH, ACO, OTH, ACO, UDF, ACO, UDF,
 UDF, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, ASO, OTH, ASO, UDF, ASO, ACO,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 OTH, OTH, OTH, OTH, OTH, OTH, OTH, OTH,
 ACV, ACV, ACV, ACV, ACV, ACV, ACO, ACO,
 ACV, ACV, ACV, ACV, ACV, ACV, ACV, ACV,
 ACO, ACO, ACV, ACV, ACV, ACV, ACV, OTH,
 ACV, ACV, ACV, ACV, ACV, ACO, ACO, ACO,
 ASV, ASV, ASV, ASV, ASV, ASV, ASO, ASO,
 ASV, ASV, ASV, ASV, ASV, ASV, ASV, ASV,
 ASO, ASO, ASV, ASV, ASV, ASV, ASV, OTH,
 ASV, ASV, ASV, ASV, ASV, ASO, ASO, ASO)
Latin1ClassModel = (0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3,
                    3, 3, 3, 0, 3, 3, 3, 1, 1, 3, 3, 0, 3, 3, 3, 1, 2, 1, 2, 0, 3,
                    3, 3, 3, 3, 3, 3, 0, 3, 1, 3, 1, 1, 1, 3, 0, 3, 1, 3, 1, 1, 3,
                    3)

class Latin1Prober(CharSetProber):

    def __init__(self):
        super(Latin1Prober, self).__init__()
        self._last_char_class = None
        self._freq_counter = None
        self.reset()

    def reset(self):
        self._last_char_class = OTH
        self._freq_counter = [0] * FREQ_CAT_NUM
        CharSetProber.reset(self)

    @property
    def charset_name(self):
        return 'ISO-8859-1'

    @property
    def language(self):
        return ''

    def feed(self, byte_str):
        byte_str = self.filter_with_english_letters(byte_str)
        for c in byte_str:
            char_class = Latin1_CharToClass[c]
            freq = Latin1ClassModel[(self._last_char_class * CLASS_NUM + char_class)]
            if freq == 0:
                self._state = ProbingState.NOT_ME
                break
            self._freq_counter[freq] += 1
            self._last_char_class = char_class

        return self.state

    def get_confidence(self):
        if self.state == ProbingState.NOT_ME:
            return 0.01
        else:
            total = sum(self._freq_counter)
            if total < 0.01:
                confidence = 0.0
            else:
                confidence = (self._freq_counter[3] - self._freq_counter[1] * 20.0) / total
            if confidence < 0.0:
                confidence = 0.0
            confidence = confidence * 0.73
            return confidence