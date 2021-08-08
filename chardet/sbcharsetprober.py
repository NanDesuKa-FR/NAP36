# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\sbcharsetprober.py
from .charsetprober import CharSetProber
from .enums import CharacterCategory, ProbingState, SequenceLikelihood

class SingleByteCharSetProber(CharSetProber):
    SAMPLE_SIZE = 64
    SB_ENOUGH_REL_THRESHOLD = 1024
    POSITIVE_SHORTCUT_THRESHOLD = 0.95
    NEGATIVE_SHORTCUT_THRESHOLD = 0.05

    def __init__(self, model, reversed=False, name_prober=None):
        super(SingleByteCharSetProber, self).__init__()
        self._model = model
        self._reversed = reversed
        self._name_prober = name_prober
        self._last_order = None
        self._seq_counters = None
        self._total_seqs = None
        self._total_char = None
        self._freq_char = None
        self.reset()

    def reset(self):
        super(SingleByteCharSetProber, self).reset()
        self._last_order = 255
        self._seq_counters = [0] * SequenceLikelihood.get_num_categories()
        self._total_seqs = 0
        self._total_char = 0
        self._freq_char = 0

    @property
    def charset_name(self):
        if self._name_prober:
            return self._name_prober.charset_name
        else:
            return self._model['charset_name']

    @property
    def language(self):
        if self._name_prober:
            return self._name_prober.language
        else:
            return self._model.get('language')

    def feed(self, byte_str):
        if not self._model['keep_english_letter']:
            byte_str = self.filter_international_words(byte_str)
        if not byte_str:
            return self.state
        else:
            char_to_order_map = self._model['char_to_order_map']
            for i, c in enumerate(byte_str):
                order = char_to_order_map[c]
                if order < CharacterCategory.CONTROL:
                    self._total_char += 1
                if order < self.SAMPLE_SIZE:
                    self._freq_char += 1
                    if self._last_order < self.SAMPLE_SIZE:
                        self._total_seqs += 1
                        if not self._reversed:
                            i = self._last_order * self.SAMPLE_SIZE + order
                            model = self._model['precedence_matrix'][i]
                        else:
                            i = order * self.SAMPLE_SIZE + self._last_order
                            model = self._model['precedence_matrix'][i]
                        self._seq_counters[model] += 1
                self._last_order = order

            charset_name = self._model['charset_name']
            if self.state == ProbingState.DETECTING:
                if self._total_seqs > self.SB_ENOUGH_REL_THRESHOLD:
                    confidence = self.get_confidence()
                    if confidence > self.POSITIVE_SHORTCUT_THRESHOLD:
                        self.logger.debug('%s confidence = %s, we have a winner', charset_name, confidence)
                        self._state = ProbingState.FOUND_IT
                    elif confidence < self.NEGATIVE_SHORTCUT_THRESHOLD:
                        self.logger.debug('%s confidence = %s, below negative shortcut threshhold %s', charset_name, confidence, self.NEGATIVE_SHORTCUT_THRESHOLD)
                        self._state = ProbingState.NOT_ME
            return self.state

    def get_confidence(self):
        r = 0.01
        if self._total_seqs > 0:
            r = 1.0 * self._seq_counters[SequenceLikelihood.POSITIVE] / self._total_seqs / self._model['typical_positive_ratio']
            r = r * self._freq_char / self._total_char
            if r >= 1.0:
                r = 0.99
        return r