# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: contextlib.py
"""Utilities for with-statement contexts.  See PEP 343."""
import abc, sys, _collections_abc
from collections import deque
from functools import wraps
__all__ = [
 'contextmanager', 'closing', 'AbstractContextManager',
 'ContextDecorator', 'ExitStack', 'redirect_stdout',
 'redirect_stderr', 'suppress']

class AbstractContextManager(abc.ABC):
    __doc__ = 'An abstract base class for context managers.'

    def __enter__(self):
        """Return `self` upon entering the runtime context."""
        return self

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """Raise any exception triggered within the runtime context."""
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is AbstractContextManager:
            return _collections_abc._check_methods(C, '__enter__', '__exit__')
        else:
            return NotImplemented


class ContextDecorator(object):
    __doc__ = 'A base class or mixin that enables context managers to work as decorators.'

    def _recreate_cm(self):
        """Return a recreated instance of self.

        Allows an otherwise one-shot context manager like
        _GeneratorContextManager to support use as
        a decorator via implicit recreation.

        This is a private interface just for _GeneratorContextManager.
        See issue #11647 for details.
        """
        return self

    def __call__(self, func):

        @wraps(func)
        def inner(*args, **kwds):
            with self._recreate_cm():
                return func(*args, **kwds)

        return inner


class _GeneratorContextManager(ContextDecorator, AbstractContextManager):
    __doc__ = 'Helper for @contextmanager decorator.'

    def __init__(self, func, args, kwds):
        self.gen = func(*args, **kwds)
        self.func, self.args, self.kwds = func, args, kwds
        doc = getattr(func, '__doc__', None)
        if doc is None:
            doc = type(self).__doc__
        self.__doc__ = doc

    def _recreate_cm(self):
        return self.__class__(self.func, self.args, self.kwds)

    def __enter__(self):
        try:
            return next(self.gen)
        except StopIteration:
            raise RuntimeError("generator didn't yield") from None

    def __exit__(self, type, value, traceback):
        if type is None:
            try:
                next(self.gen)
            except StopIteration:
                return False
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                value = type()
            try:
                self.gen.throw(type, value, traceback)
            except StopIteration as exc:
                return exc is not value
            except RuntimeError as exc:
                if exc is value:
                    return False
                if type is StopIteration:
                    if exc.__cause__ is value:
                        return False
                raise
            except:
                if sys.exc_info()[1] is value:
                    return False
                raise

            raise RuntimeError("generator didn't stop after throw()")


def contextmanager(func):
    """@contextmanager decorator.

    Typical usage:

        @contextmanager
        def some_generator(<arguments>):
            <setup>
            try:
                yield <value>
            finally:
                <cleanup>

    This makes this:

        with some_generator(<arguments>) as <variable>:
            <body>

    equivalent to this:

        <setup>
        try:
            <variable> = <value>
            <body>
        finally:
            <cleanup>

    """

    @wraps(func)
    def helper(*args, **kwds):
        return _GeneratorContextManager(func, args, kwds)

    return helper


class closing(AbstractContextManager):
    __doc__ = 'Context to automatically close something at the end of a block.\n\n    Code like this:\n\n        with closing(<module>.open(<arguments>)) as f:\n            <block>\n\n    is equivalent to this:\n\n        f = <module>.open(<arguments>)\n        try:\n            <block>\n        finally:\n            f.close()\n\n    '

    def __init__(self, thing):
        self.thing = thing

    def __enter__(self):
        return self.thing

    def __exit__(self, *exc_info):
        self.thing.close()


class _RedirectStream(AbstractContextManager):
    _stream = None

    def __init__(self, new_target):
        self._new_target = new_target
        self._old_targets = []

    def __enter__(self):
        self._old_targets.append(getattr(sys, self._stream))
        setattr(sys, self._stream, self._new_target)
        return self._new_target

    def __exit__(self, exctype, excinst, exctb):
        setattr(sys, self._stream, self._old_targets.pop())


class redirect_stdout(_RedirectStream):
    __doc__ = "Context manager for temporarily redirecting stdout to another file.\n\n        # How to send help() to stderr\n        with redirect_stdout(sys.stderr):\n            help(dir)\n\n        # How to write help() to a file\n        with open('help.txt', 'w') as f:\n            with redirect_stdout(f):\n                help(pow)\n    "
    _stream = 'stdout'


class redirect_stderr(_RedirectStream):
    __doc__ = 'Context manager for temporarily redirecting stderr to another file.'
    _stream = 'stderr'


class suppress(AbstractContextManager):
    __doc__ = 'Context manager to suppress specified exceptions\n\n    After the exception is suppressed, execution proceeds with the next\n    statement following the with statement.\n\n         with suppress(FileNotFoundError):\n             os.remove(somefile)\n         # Execution still resumes here if the file was already removed\n    '

    def __init__(self, *exceptions):
        self._exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exctype, excinst, exctb):
        return exctype is not None and issubclass(exctype, self._exceptions)


class ExitStack(AbstractContextManager):
    __doc__ = 'Context manager for dynamic management of a stack of exit callbacks\n\n    For example:\n\n        with ExitStack() as stack:\n            files = [stack.enter_context(open(fname)) for fname in filenames]\n            # All opened files will automatically be closed at the end of\n            # the with statement, even if attempts to open files later\n            # in the list raise an exception\n\n    '

    def __init__(self):
        self._exit_callbacks = deque()

    def pop_all(self):
        """Preserve the context stack by transferring it to a new instance"""
        new_stack = type(self)()
        new_stack._exit_callbacks = self._exit_callbacks
        self._exit_callbacks = deque()
        return new_stack

    def _push_cm_exit(self, cm, cm_exit):
        """Helper to correctly register callbacks to __exit__ methods"""

        def _exit_wrapper(*exc_details):
            return cm_exit(cm, *exc_details)

        _exit_wrapper.__self__ = cm
        self.push(_exit_wrapper)

    def push(self, exit):
        """Registers a callback with the standard __exit__ method signature

        Can suppress exceptions the same way __exit__ methods can.

        Also accepts any object with an __exit__ method (registering a call
        to the method instead of the object itself)
        """
        _cb_type = type(exit)
        try:
            exit_method = _cb_type.__exit__
        except AttributeError:
            self._exit_callbacks.append(exit)
        else:
            self._push_cm_exit(exit, exit_method)
        return exit

    def callback(self, callback, *args, **kwds):
        """Registers an arbitrary callback and arguments.

        Cannot suppress exceptions.
        """

        def _exit_wrapper(exc_type, exc, tb):
            callback(*args, **kwds)

        _exit_wrapper.__wrapped__ = callback
        self.push(_exit_wrapper)
        return callback

    def enter_context(self, cm):
        """Enters the supplied context manager

        If successful, also pushes its __exit__ method as a callback and
        returns the result of the __enter__ method.
        """
        _cm_type = type(cm)
        _exit = _cm_type.__exit__
        result = _cm_type.__enter__(cm)
        self._push_cm_exit(cm, _exit)
        return result

    def close(self):
        """Immediately unwind the context stack"""
        self.__exit__(None, None, None)

    def __exit__(self, *exc_details):
        received_exc = exc_details[0] is not None
        frame_exc = sys.exc_info()[1]

        def _fix_exception_context(new_exc, old_exc):
            while True:
                exc_context = new_exc.__context__
                if exc_context is old_exc:
                    return
                if exc_context is None or exc_context is frame_exc:
                    break
                new_exc = exc_context

            new_exc.__context__ = old_exc

        suppressed_exc = False
        pending_raise = False
        while self._exit_callbacks:
            cb = self._exit_callbacks.pop()
            try:
                if cb(*exc_details):
                    suppressed_exc = True
                    pending_raise = False
                    exc_details = (None, None, None)
            except:
                new_exc_details = sys.exc_info()
                _fix_exception_context(new_exc_details[1], exc_details[1])
                pending_raise = True
                exc_details = new_exc_details

        if pending_raise:
            try:
                fixed_ctx = exc_details[1].__context__
                raise exc_details[1]
            except BaseException:
                exc_details[1].__context__ = fixed_ctx
                raise

        return received_exc and suppressed_exc