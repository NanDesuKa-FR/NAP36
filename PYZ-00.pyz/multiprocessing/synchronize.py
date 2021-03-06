# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: multiprocessing\synchronize.py
__all__ = [
 'Lock', 'RLock', 'Semaphore', 'BoundedSemaphore', 'Condition', 'Event']
import threading, sys, tempfile, _multiprocessing
from time import time as _time
from . import context
from . import process
from . import util
try:
    from _multiprocessing import SemLock, sem_unlink
except ImportError:
    raise ImportError('This platform lacks a functioning sem_open' + ' implementation, therefore, the required' + ' synchronization primitives needed will not' + ' function, see issue 3770.')

RECURSIVE_MUTEX, SEMAPHORE = list(range(2))
SEM_VALUE_MAX = _multiprocessing.SemLock.SEM_VALUE_MAX

class SemLock(object):
    _rand = tempfile._RandomNameSequence()

    def __init__(self, kind, value, maxvalue, *, ctx):
        if ctx is None:
            ctx = context._default_context.get_context()
        else:
            name = ctx.get_start_method()
            unlink_now = sys.platform == 'win32' or name == 'fork'
            for i in range(100):
                try:
                    sl = self._semlock = _multiprocessing.SemLock(kind, value, maxvalue, self._make_name(), unlink_now)
                except FileExistsError:
                    pass
                else:
                    break
            else:
                raise FileExistsError('cannot find name for semaphore')

            util.debug('created semlock with handle %s' % sl.handle)
            self._make_methods()
            if sys.platform != 'win32':

                def _after_fork(obj):
                    obj._semlock._after_fork()

                util.register_after_fork(self, _after_fork)
            if self._semlock.name is not None:
                from .semaphore_tracker import register
                register(self._semlock.name)
                util.Finalize(self, (SemLock._cleanup), (self._semlock.name,), exitpriority=0)

    @staticmethod
    def _cleanup(name):
        from .semaphore_tracker import unregister
        sem_unlink(name)
        unregister(name)

    def _make_methods(self):
        self.acquire = self._semlock.acquire
        self.release = self._semlock.release

    def __enter__(self):
        return self._semlock.__enter__()

    def __exit__(self, *args):
        return (self._semlock.__exit__)(*args)

    def __getstate__(self):
        context.assert_spawning(self)
        sl = self._semlock
        if sys.platform == 'win32':
            h = context.get_spawning_popen().duplicate_for_child(sl.handle)
        else:
            h = sl.handle
        return (
         h, sl.kind, sl.maxvalue, sl.name)

    def __setstate__(self, state):
        self._semlock = (_multiprocessing.SemLock._rebuild)(*state)
        util.debug('recreated blocker with handle %r' % state[0])
        self._make_methods()

    @staticmethod
    def _make_name():
        return '%s-%s' % (process.current_process()._config['semprefix'],
         next(SemLock._rand))


class Semaphore(SemLock):

    def __init__(self, value=1, *, ctx):
        SemLock.__init__(self, SEMAPHORE, value, SEM_VALUE_MAX, ctx=ctx)

    def get_value(self):
        return self._semlock._get_value()

    def __repr__(self):
        try:
            value = self._semlock._get_value()
        except Exception:
            value = 'unknown'

        return '<%s(value=%s)>' % (self.__class__.__name__, value)


class BoundedSemaphore(Semaphore):

    def __init__(self, value=1, *, ctx):
        SemLock.__init__(self, SEMAPHORE, value, value, ctx=ctx)

    def __repr__(self):
        try:
            value = self._semlock._get_value()
        except Exception:
            value = 'unknown'

        return '<%s(value=%s, maxvalue=%s)>' % (
         self.__class__.__name__, value, self._semlock.maxvalue)


class Lock(SemLock):

    def __init__(self, *, ctx):
        SemLock.__init__(self, SEMAPHORE, 1, 1, ctx=ctx)

    def __repr__(self):
        try:
            if self._semlock._is_mine():
                name = process.current_process().name
                if threading.current_thread().name != 'MainThread':
                    name += '|' + threading.current_thread().name
            else:
                if self._semlock._get_value() == 1:
                    name = 'None'
                else:
                    if self._semlock._count() > 0:
                        name = 'SomeOtherThread'
                    else:
                        name = 'SomeOtherProcess'
        except Exception:
            name = 'unknown'

        return '<%s(owner=%s)>' % (self.__class__.__name__, name)


class RLock(SemLock):

    def __init__(self, *, ctx):
        SemLock.__init__(self, RECURSIVE_MUTEX, 1, 1, ctx=ctx)

    def __repr__(self):
        try:
            if self._semlock._is_mine():
                name = process.current_process().name
                if threading.current_thread().name != 'MainThread':
                    name += '|' + threading.current_thread().name
                count = self._semlock._count()
            else:
                if self._semlock._get_value() == 1:
                    name, count = ('None', 0)
                else:
                    if self._semlock._count() > 0:
                        name, count = ('SomeOtherThread', 'nonzero')
                    else:
                        name, count = ('SomeOtherProcess', 'nonzero')
        except Exception:
            name, count = ('unknown', 'unknown')

        return '<%s(%s, %s)>' % (self.__class__.__name__, name, count)


class Condition(object):

    def __init__(self, lock=None, *, ctx):
        self._lock = lock or ctx.RLock()
        self._sleeping_count = ctx.Semaphore(0)
        self._woken_count = ctx.Semaphore(0)
        self._wait_semaphore = ctx.Semaphore(0)
        self._make_methods()

    def __getstate__(self):
        context.assert_spawning(self)
        return (self._lock, self._sleeping_count,
         self._woken_count, self._wait_semaphore)

    def __setstate__(self, state):
        self._lock, self._sleeping_count, self._woken_count, self._wait_semaphore = state
        self._make_methods()

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return (self._lock.__exit__)(*args)

    def _make_methods(self):
        self.acquire = self._lock.acquire
        self.release = self._lock.release

    def __repr__(self):
        try:
            num_waiters = self._sleeping_count._semlock._get_value() - self._woken_count._semlock._get_value()
        except Exception:
            num_waiters = 'unknown'

        return '<%s(%s, %s)>' % (self.__class__.__name__, self._lock, num_waiters)

    def wait(self, timeout=None):
        assert self._lock._semlock._is_mine(), 'must acquire() condition before using wait()'
        self._sleeping_count.release()
        count = self._lock._semlock._count()
        for i in range(count):
            self._lock.release()

        try:
            return self._wait_semaphore.acquire(True, timeout)
        finally:
            self._woken_count.release()
            for i in range(count):
                self._lock.acquire()

    def notify(self):
        if not self._lock._semlock._is_mine():
            raise AssertionError('lock is not owned')
        else:
            assert not self._wait_semaphore.acquire(False)
            while self._woken_count.acquire(False):
                res = self._sleeping_count.acquire(False)
                assert res

            if self._sleeping_count.acquire(False):
                self._wait_semaphore.release()
                self._woken_count.acquire()
                self._wait_semaphore.acquire(False)

    def notify_all(self):
        if not self._lock._semlock._is_mine():
            raise AssertionError('lock is not owned')
        else:
            assert not self._wait_semaphore.acquire(False)
            while self._woken_count.acquire(False):
                res = self._sleeping_count.acquire(False)
                assert res

            sleepers = 0
            while self._sleeping_count.acquire(False):
                self._wait_semaphore.release()
                sleepers += 1

            if sleepers:
                for i in range(sleepers):
                    self._woken_count.acquire()

                while self._wait_semaphore.acquire(False):
                    pass

    def wait_for(self, predicate, timeout=None):
        result = predicate()
        if result:
            return result
        else:
            if timeout is not None:
                endtime = _time() + timeout
            else:
                endtime = None
                waittime = None
            while not result:
                if endtime is not None:
                    waittime = endtime - _time()
                    if waittime <= 0:
                        break
                self.wait(waittime)
                result = predicate()

            return result


class Event(object):

    def __init__(self, *, ctx):
        self._cond = ctx.Condition(ctx.Lock())
        self._flag = ctx.Semaphore(0)

    def is_set(self):
        with self._cond:
            if self._flag.acquire(False):
                self._flag.release()
                return True
            else:
                return False

    def set(self):
        with self._cond:
            self._flag.acquire(False)
            self._flag.release()
            self._cond.notify_all()

    def clear(self):
        with self._cond:
            self._flag.acquire(False)

    def wait(self, timeout=None):
        with self._cond:
            if self._flag.acquire(False):
                self._flag.release()
            else:
                self._cond.wait(timeout)
            if self._flag.acquire(False):
                self._flag.release()
                return True
            else:
                return False


class Barrier(threading.Barrier):

    def __init__(self, parties, action=None, timeout=None, *, ctx):
        import struct
        from .heap import BufferWrapper
        wrapper = BufferWrapper(struct.calcsize('i') * 2)
        cond = ctx.Condition()
        self.__setstate__((parties, action, timeout, cond, wrapper))
        self._state = 0
        self._count = 0

    def __setstate__(self, state):
        self._parties, self._action, self._timeout, self._cond, self._wrapper = state
        self._array = self._wrapper.create_memoryview().cast('i')

    def __getstate__(self):
        return (
         self._parties, self._action, self._timeout,
         self._cond, self._wrapper)

    @property
    def _state(self):
        return self._array[0]

    @_state.setter
    def _state(self, value):
        self._array[0] = value

    @property
    def _count(self):
        return self._array[1]

    @_count.setter
    def _count(self, value):
        self._array[1] = value