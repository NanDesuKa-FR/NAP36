# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\chardistribution.py
from .euctwfreq import EUCTW_CHAR_TO_FREQ_ORDER, EUCTW_TABLE_SIZE, EUCTW_TYPICAL_DISTRIBUTION_RATIO
from .euckrfreq import EUCKR_CHAR_TO_FREQ_ORDER, EUCKR_TABLE_SIZE, EUCKR_TYPICAL_DISTRIBUTION_RATIO
from .gb2312freq import GB2312_CHAR_TO_FREQ_ORDER, GB2312_TABLE_SIZE, GB2312_TYPICAL_DISTRIBUTION_RATIO
from .big5freq import BIG5_CHAR_TO_FREQ_ORDER, BIG5_TABLE_SIZE, BIG5_TYPICAL_DISTRIBUTION_RATIO
from .jisfreq import JIS_CHAR_TO_FREQ_ORDER, JIS_TABLE_SIZE, JIS_TYPICAL_DISTRIBUTION_RATIO

class CharDistributionAnalysis(object):
    ENOUGH_DATA_THRESHOLD = 1024
    SURE_YES = 0.99
    SURE_NO = 0.01
    MINIMUM_DATA_THRESHOLD = 3

    def __init__(self):
        self._char_to_freq_order = None
        self._table_size = None
        self.typical_distribution_ratio = None
        self._done = None
        self._total_chars = None
        self._freq_chars = None
        self.reset()

    def reset(self):
        """reset analyser, clear any state"""
        self._done = False
        self._total_chars = 0
        self._freq_chars = 0

    def feed(self, char, char_len):
        """feed a character with known length"""
        if char_len == 2:
            order = self.get_order(char)
        else:
            order = -1
        if order >= 0:
            self._total_chars += 1
            if order < self._table_size:
                if 512 > self._char_to_freq_order[order]:
                    self._freq_chars += 1

    def get_confidence(self):
        """return confidence based on existing data"""
        if self._total_chars <= 0 or self._freq_chars <= self.MINIMUM_DATA_THRESHOLD:
            return self.SURE_NO
        else:
            if self._total_chars != self._freq_chars:
                r = self._freq_chars / ((self._total_chars - self._freq_chars) * self.typical_distribution_ratio)
                if r < self.SURE_YES:
                    return r
            return self.SURE_YES

    def got_enough_data(self):
        return self._total_chars > self.ENOUGH_DATA_THRESHOLD

    def get_order(self, byte_str):
        return -1


class EUCTWDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super(EUCTWDistributionAnalysis, self).__init__()
        self._char_to_freq_order = EUCTW_CHAR_TO_FREQ_ORDER
        self._table_size = EUCTW_TABLE_SIZE
        self.typical_distribution_ratio = EUCTW_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, byte_str):
        first_char = byte_str[0]
        if first_char >= 196:
            return 94 * (first_char - 196) + byte_str[1] - 161
        else:
            return -1


class EUCKRDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super(EUCKRDistributionAnalysis, self).__init__()
        self._char_to_freq_order = EUCKR_CHAR_TO_FREQ_ORDER
        self._table_size = EUCKR_TABLE_SIZE
        self.typical_distribution_ratio = EUCKR_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, byte_str):
        first_char = byte_str[0]
        if first_char >= 176:
            return 94 * (first_char - 176) + byte_str[1] - 161
        else:
            return -1


class GB2312DistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super(GB2312DistributionAnalysis, self).__init__()
        self._char_to_freq_order = GB2312_CHAR_TO_FREQ_ORDER
        self._table_size = GB2312_TABLE_SIZE
        self.typical_distribution_ratio = GB2312_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, byte_str):
        first_char, second_char = byte_str[0], byte_str[1]
        if first_char >= 176:
            if second_char >= 161:
                return 94 * (first_char - 176) + second_char - 161
        return -1


class Big5DistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super(Big5DistributionAnalysis, self).__init__()
        self._char_to_freq_order = BIG5_CHAR_TO_FREQ_ORDER
        self._table_size = BIG5_TABLE_SIZE
        self.typical_distribution_ratio = BIG5_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, byte_str):
        first_char, second_char = byte_str[0], byte_str[1]
        if first_char >= 164:
            if second_char >= 161:
                return 157 * (first_char - 164) + second_char - 161 + 63
            else:
                return 157 * (first_char - 164) + second_char - 64
        else:
            return -1


class SJISDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super(SJISDistributionAnalysis, self).__init__()
        self._char_to_freq_order = JIS_CHAR_TO_FREQ_ORDER
        self._table_size = JIS_TABLE_SIZE
        self.typical_distribution_ratio = JIS_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, byte_str):
        first_char, second_char = byte_str[0], byte_str[1]
        if first_char >= 129:
            if first_char <= 159:
                order = 188 * (first_char - 129)
        elif first_char >= 224:
            if first_char <= 239:
                order = 188 * (first_char - 224 + 31)
        else:
            return -1
        order = order + second_char - 64
        if second_char > 127:
            order = -1
        return order


class EUCJPDistributionAnalysis(CharDistributionAnalysis):

    def __init__(self):
        super(EUCJPDistributionAnalysis, self).__init__()
        self._char_to_freq_order = JIS_CHAR_TO_FREQ_ORDER
        self._table_size = JIS_TABLE_SIZE
        self.typical_distribution_ratio = JIS_TYPICAL_DISTRIBUTION_RATIO

    def get_order(self, byte_str):
        char = byte_str[0]
        if char >= 160:
            return 94 * (char - 161) + byte_str[1] - 161
        else:
            return -1