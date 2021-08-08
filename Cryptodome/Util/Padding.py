# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\Cryptodome\Util\Padding.py
__all__ = [
 'pad', 'unpad']
from Cryptodome.Util.py3compat import *

def pad(data_to_pad, block_size, style='pkcs7'):
    """Apply standard padding.

    Args:
      data_to_pad (byte string):
        The data that needs to be padded.
      block_size (integer):
        The block boundary to use for padding. The output length is guaranteed
        to be a multiple of :data:`block_size`.
      style (string):
        Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.

    Return:
      byte string : the original data with the appropriate padding added at the end.
    """
    padding_len = block_size - len(data_to_pad) % block_size
    if style == 'pkcs7':
        padding = bchr(padding_len) * padding_len
    else:
        if style == 'x923':
            padding = bchr(0) * (padding_len - 1) + bchr(padding_len)
        else:
            if style == 'iso7816':
                padding = bchr(128) + bchr(0) * (padding_len - 1)
            else:
                raise ValueError('Unknown padding style')
    return data_to_pad + padding


def unpad(padded_data, block_size, style='pkcs7'):
    """Remove standard padding.

    Args:
      padded_data (byte string):
        A piece of data with padding that needs to be stripped.
      block_size (integer):
        The block boundary to use for padding. The input length
        must be a multiple of :data:`block_size`.
      style (string):
        Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.
    Return:
        byte string : data without padding.
    Raises:
      ValueError: if the padding is incorrect.
    """
    pdata_len = len(padded_data)
    if pdata_len % block_size:
        raise ValueError('Input data is not padded')
    if style in ('pkcs7', 'x923'):
        padding_len = bord(padded_data[(-1)])
        if padding_len < 1 or padding_len > min(block_size, pdata_len):
            raise ValueError('Padding is incorrect.')
        if style == 'pkcs7':
            if padded_data[-padding_len:] != bchr(padding_len) * padding_len:
                raise ValueError('PKCS#7 padding is incorrect.')
        elif padded_data[-padding_len:-1] != bchr(0) * (padding_len - 1):
            raise ValueError('ANSI X.923 padding is incorrect.')
    else:
        if style == 'iso7816':
            padding_len = pdata_len - padded_data.rfind(bchr(128))
            if padding_len < 1 or padding_len > min(block_size, pdata_len):
                raise ValueError('Padding is incorrect.')
            if padding_len > 1:
                if padded_data[1 - padding_len:] != bchr(0) * (padding_len - 1):
                    raise ValueError('ISO 7816-4 padding is incorrect.')
        else:
            raise ValueError('Unknown padding style')
        return padded_data[:-padding_len]