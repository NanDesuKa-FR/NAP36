# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\asn1crypto\_errors.py
"""
Helper for formatting exception messages. Exports the following items:

 - unwrap()
"""
from __future__ import unicode_literals, division, absolute_import, print_function
import re, textwrap

def unwrap(string, *params):
    """
    Takes a multi-line string and does the following:

     - dedents
     - converts newlines with text before and after into a single line
     - strips leading and trailing whitespace

    :param string:
        The string to format

    :param *params:
        Params to interpolate into the string

    :return:
        The formatted string
    """
    output = textwrap.dedent(string)
    if output.find('\n') != -1:
        output = re.sub('(?<=\\S)\n(?=[^ \n\t\\d\\*\\-=])', ' ', output)
    if params:
        output = output % params
    output = output.strip()
    return output