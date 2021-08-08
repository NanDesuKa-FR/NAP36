# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: multiprocessing\popen_fork.py
import os, sys, signal
from . import util
__all__ = [
 'Popen']

class Popen(object):
    method = 'fork'

    def __init__(self, process_obj):
        sys.stdout.flush()
        sys.stderr.flush()
        self.returncode = None
        self._launch(process_obj)

    def duplicate_for_child(self, fd):
        return fd

    def poll(self, flag=os.WNOHANG):
        if self.returncode is None:
            while True:
                try:
                    pid, sts = os.waitpid(self.pid, flag)
                except OSError as e:
                    return
                else:
                    break

            if pid == self.pid:
                if os.WIFSIGNALED(sts):
                    self.returncode = -os.WTERMSIG(sts)
                else:
                    assert os.WIFEXITED(sts)
                    self.returncode = os.WEXITSTATUS(sts)
        return self.returncode

    def wait(self, timeout=None):
        if self.returncode is None:
            if timeout is not None:
                from multiprocessing.connection import wait
                if not wait([self.sentinel], timeout):
                    return
            return self.poll(os.WNOHANG if timeout == 0.0 else 0)
        else:
            return self.returncode

    def terminate(self):
        if self.returncode is None:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            except OSError:
                if self.wait(timeout=0.1) is None:
                    raise

    def _launch(self, process_obj):
        code = 1
        parent_r, child_w = os.pipe()
        self.pid = os.fork()
        if self.pid == 0:
            try:
                os.close(parent_r)
                if 'random' in sys.modules:
                    import random
                    random.seed()
                code = process_obj._bootstrap()
            finally:
                os._exit(code)

        else:
            os.close(child_w)
            util.Finalize(self, os.close, (parent_r,))
            self.sentinel = parent_r