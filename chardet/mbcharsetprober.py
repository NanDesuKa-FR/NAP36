# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\mbcharsetprober.py
from .charsetprober import CharSetProber
from .enums import ProbingState, MachineState

class MultiByteCharSetProber(CharSetProber):
    __doc__ = '\n    MultiByteCharSetProber\n    '

    def __init__(self, lang_filter=None):
        super(MultiByteCharSetProber, self).__init__(lang_filter=lang_filter)
        self.distribution_analyzer = None
        self.coding_sm = None
        self._last_char = [0, 0]

    def reset(self):
        super(MultiByteCharSetProber, self).reset()
        if self.coding_sm:
            self.coding_sm.reset()
        if self.distribution_analyzer:
            self.distribution_analyzer.reset()
        self._last_char = [
         0, 0]

    @property
    def charset_name(self):
        raise NotImplementedError

    @property
    def language(self):
        raise NotImplementedError

    def feed(self, byte_str):
        for i in range(len(byte_str)):
            coding_state = self.coding_sm.next_state(byte_str[i])
            if coding_state == MachineState.ERROR:
                self.logger.debug('%s %s prober hit error at byte %s', self.charset_name, self.language, i)
                self._state = ProbingState.NOT_ME
                break
            else:
                if coding_state == MachineState.ITS_ME:
                    self._state = ProbingState.FOUND_IT
                    break
                else:
                    if coding_state == MachineState.START:
                        char_len = self.coding_sm.get_current_charlen()
                        if i == 0:
                            self._last_char[1] = byte_str[0]
                            self.distribution_analyzer.feed(self._last_char, char_len)
                        else:
                            self.distribution_analyzer.feed(byte_str[i - 1:i + 1], char_len)

        self._last_char[0] = byte_str[(-1)]
        if self.state == ProbingState.DETECTING:
            if self.distribution_analyzer.got_enough_data():
                if self.get_confidence() > self.SHORTCUT_THRESHOLD:
                    self._state = ProbingState.FOUND_IT
        return self.state

    def get_confidence(self):
        return self.distribution_analyzer.get_confidence()