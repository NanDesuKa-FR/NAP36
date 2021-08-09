# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\binaries\kanji_to_romaji\models\KanjiBlock.py


class KanjiBlock(str):

    def __new__(cls, *args, **kwargs):
        obj = str.__new__(cls, '@')
        kanji = args[0]
        kanji_dict = args[1]
        obj.kanji = kanji
        if len(kanji) == 1:
            obj.romaji = ' ' + kanji_dict['romaji']
        else:
            if 'verb stem' in kanji_dict['w_type']:
                obj.romaji = ' ' + kanji_dict['romaji']
            else:
                obj.romaji = ' ' + kanji_dict['romaji'] + ' '
            if 'other_readings' in kanji_dict:
                obj.w_type = [
                 kanji_dict['w_type']]
                obj.w_type.extend([k for k in list(kanji_dict['other_readings'].keys())])
            else:
                obj.w_type = kanji_dict['w_type']
        return obj

    def __repr__(self):
        return self.kanji.encode('unicode_escape')

    def __str__(self):
        return self.romaji.encode('utf-8')