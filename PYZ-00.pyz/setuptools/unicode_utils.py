# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\unicode_utils.py
import unicodedata, sys
from setuptools.extern import six

def decompose(path):
    if isinstance(path, six.text_type):
        return unicodedata.normalize('NFD', path)
    else:
        try:
            path = path.decode('utf-8')
            path = unicodedata.normalize('NFD', path)
            path = path.encode('utf-8')
        except UnicodeError:
            pass

        return path


def filesys_decode(path):
    """
    Ensure that the given path is decoded,
    NONE when no expected encoding works
    """
    if isinstance(path, six.text_type):
        return path
    fs_enc = sys.getfilesystemencoding() or 'utf-8'
    candidates = (fs_enc, 'utf-8')
    for enc in candidates:
        try:
            return path.decode(enc)
        except UnicodeDecodeError:
            continue


def try_encode(string, enc):
    """turn unicode encoding into a functional routine"""
    try:
        return string.encode(enc)
    except UnicodeEncodeError:
        return