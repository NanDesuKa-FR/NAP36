# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\big5prober.py
from .mbcharsetprober import MultiByteCharSetProber
from .codingstatemachine import CodingStateMachine
from .chardistribution import Big5DistributionAnalysis
from .mbcssm import BIG5_SM_MODEL

class Big5Prober(MultiByteCharSetProber):

    def __init__(self):
        super(Big5Prober, self).__init__()
        self.coding_sm = CodingStateMachine(BIG5_SM_MODEL)
        self.distribution_analyzer = Big5DistributionAnalysis()
        self.reset()

    @property
    def charset_name(self):
        return 'Big5'

    @property
    def language(self):
        return 'Chinese'