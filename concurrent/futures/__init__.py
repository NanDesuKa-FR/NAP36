# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: concurrent\futures\__init__.py
"""Execute computations asynchronously using threads or processes."""
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
from concurrent.futures._base import FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED, CancelledError, TimeoutError, Future, Executor, wait, as_completed
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor