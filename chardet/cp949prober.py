# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\cp949prober.py
from .chardistribution import EUCKRDistributionAnalysis
from .codingstatemachine import CodingStateMachine
from .mbcharsetprober import MultiByteCharSetProber
from .mbcssm import CP949_SM_MODEL

class CP949Prober(MultiByteCharSetProber):

    def __init__(self):
        super(CP949Prober, self).__init__()
        self.coding_sm = CodingStateMachine(CP949_SM_MODEL)
        self.distribution_analyzer = EUCKRDistributionAnalysis()
        self.reset()

    @property
    def charset_name(self):
        return 'CP949'

    @property
    def language(self):
        return 'Korean'