# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Util\_cpu_features.py
from Cryptodome.Util._raw_api import load_pycryptodome_raw_lib
_raw_cpuid_lib = load_pycryptodome_raw_lib('Cryptodome.Util._cpuid_c', '\n                                           int have_aes_ni(void);\n                                           int have_clmul(void);\n                                           ')

def have_aes_ni():
    return _raw_cpuid_lib.have_aes_ni()


def have_clmul():
    return _raw_cpuid_lib.have_clmul()