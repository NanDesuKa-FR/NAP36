# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\binaries\kanji_to_romaji\models\Particle.py


class Particle(str):

    def __new__(cls, *args, **kwargs):
        particle_str = args[0]
        obj = str.__new__(cls, ' ' + particle_str + ' ')
        obj.pname = particle_str
        return obj