# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Util\_file_system.py
import os

def pycryptodome_filename(dir_comps, filename):
    """Return the complete file name for the module

    dir_comps : list of string
        The list of directory names in the PyCryptodome package.
        The first element must be "Cryptodome".

    filename : string
        The filename (inclusing extension) in the target directory.
    """
    if dir_comps[0] != 'Cryptodome':
        raise ValueError("Only available for modules under 'Cryptodome'")
    dir_comps = list(dir_comps[1:]) + [filename]
    util_lib, _ = os.path.split(os.path.abspath(__file__))
    root_lib = os.path.join(util_lib, '..')
    return (os.path.join)(root_lib, *dir_comps)