# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\euckrprober.py
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import EUCKRDistributionAnalysis
from .mbcssm import EUCKR_SM_MODEL

class EUCKRProber(MultiByteCharSetProber):

    def __init__(self):
        super(EUCKRProber, self).__init__()
        self.coding_sm = CodingStateMachine(EUCKR_SM_MODEL)
        self.distribution_analyzer = EUCKRDistributionAnalysis()
        self.reset()

    @property
    def charset_name(self):
        return 'EUC-KR'

    @property
    def language(self):
        return 'Korean'