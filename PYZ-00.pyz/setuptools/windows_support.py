# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\windows_support.py
import platform, ctypes

def windows_only(func):
    if platform.system() != 'Windows':
        return lambda *args, **kwargs: None
    else:
        return func


@windows_only
def hide_file(path):
    """
    Set the hidden attribute on a file or directory.

    From http://stackoverflow.com/questions/19622133/

    `path` must be text.
    """
    __import__('ctypes.wintypes')
    SetFileAttributes = ctypes.windll.kernel32.SetFileAttributesW
    SetFileAttributes.argtypes = (ctypes.wintypes.LPWSTR, ctypes.wintypes.DWORD)
    SetFileAttributes.restype = ctypes.wintypes.BOOL
    FILE_ATTRIBUTE_HIDDEN = 2
    ret = SetFileAttributes(path, FILE_ATTRIBUTE_HIDDEN)
    if not ret:
        raise ctypes.WinError()