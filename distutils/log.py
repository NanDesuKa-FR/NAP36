# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: distutils\log.py
"""A simple log mechanism styled after PEP 282."""
DEBUG = 1
INFO = 2
WARN = 3
ERROR = 4
FATAL = 5
import sys

class Log:

    def __init__(self, threshold=WARN):
        self.threshold = threshold

    def _log(self, level, msg, args):
        if level not in (DEBUG, INFO, WARN, ERROR, FATAL):
            raise ValueError('%s wrong log level' % str(level))
        if level >= self.threshold:
            if args:
                msg = msg % args
            else:
                if level in (WARN, ERROR, FATAL):
                    stream = sys.stderr
                else:
                    stream = sys.stdout
            if stream.errors == 'strict':
                encoding = stream.encoding
                msg = msg.encode(encoding, 'backslashreplace').decode(encoding)
            stream.write('%s\n' % msg)
            stream.flush()

    def log(self, level, msg, *args):
        self._log(level, msg, args)

    def debug(self, msg, *args):
        self._log(DEBUG, msg, args)

    def info(self, msg, *args):
        self._log(INFO, msg, args)

    def warn(self, msg, *args):
        self._log(WARN, msg, args)

    def error(self, msg, *args):
        self._log(ERROR, msg, args)

    def fatal(self, msg, *args):
        self._log(FATAL, msg, args)


_global_log = Log()
log = _global_log.log
debug = _global_log.debug
info = _global_log.info
warn = _global_log.warn
error = _global_log.error
fatal = _global_log.fatal

def set_threshold(level):
    old = _global_log.threshold
    _global_log.threshold = level
    return old


def set_verbosity(v):
    if v <= 0:
        set_threshold(WARN)
    else:
        if v == 1:
            set_threshold(INFO)
        elif v >= 2:
            set_threshold(DEBUG)