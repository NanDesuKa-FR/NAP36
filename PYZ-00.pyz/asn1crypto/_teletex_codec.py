# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\asn1crypto\_teletex_codec.py
"""
Implementation of the teletex T.61 codec. Exports the following items:

 - register()
"""
from __future__ import unicode_literals, division, absolute_import, print_function
import codecs

class TeletexCodec(codecs.Codec):

    def encode(self, input_, errors='strict'):
        return codecs.charmap_encode(input_, errors, ENCODING_TABLE)

    def decode(self, input_, errors='strict'):
        return codecs.charmap_decode(input_, errors, DECODING_TABLE)


class TeletexIncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input_, final=False):
        return codecs.charmap_encode(input_, self.errors, ENCODING_TABLE)[0]


class TeletexIncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input_, final=False):
        return codecs.charmap_decode(input_, self.errors, DECODING_TABLE)[0]


class TeletexStreamWriter(TeletexCodec, codecs.StreamWriter):
    pass


class TeletexStreamReader(TeletexCodec, codecs.StreamReader):
    pass


def teletex_search_function(name):
    """
    Search function for teletex codec that is passed to codecs.register()
    """
    if name != 'teletex':
        return
    else:
        return codecs.CodecInfo(name='teletex',
          encode=(TeletexCodec().encode),
          decode=(TeletexCodec().decode),
          incrementalencoder=TeletexIncrementalEncoder,
          incrementaldecoder=TeletexIncrementalDecoder,
          streamreader=TeletexStreamReader,
          streamwriter=TeletexStreamWriter)


def register():
    """
    Registers the teletex codec
    """
    codecs.register(teletex_search_function)


DECODING_TABLE = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"\ufffe\ufffe%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\ufffe]\ufffe_\ufffeabcdefghijklmnopqrstuvwxyz\ufffe|\ufffe\ufffe\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0¡¢£$¥#§¤\ufffe\ufffe«\ufffe\ufffe\ufffe\ufffe°±²³×µ¶·÷\ufffe\ufffe»¼½¾¿\ufffè́̂̃̄̆̇̈\ufffȩ̨̲̊̋̌\ufffe\ufffe\ufffe\ufffe\ufffe\ufffe\ufffe\ufffe\ufffe\ufffe\ufffe\ufffe\ufffe\ufffe\ufffe\ufffeΩÆÐªĦ\ufffeĲĿŁØŒºÞŦŊŉĸæđðħıĳŀłøœßþŧŋ\ufffe'
ENCODING_TABLE = codecs.charmap_build(DECODING_TABLE)