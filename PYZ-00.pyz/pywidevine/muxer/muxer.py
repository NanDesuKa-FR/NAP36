# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\pywidevine\muxer\muxer.py
import os, subprocess

class Muxer(object):

    def __init__(self, CurrentName, SeasonFolder, CurrentHeigh, Type, mkvmergeexe):
        self.CurrentName = CurrentName
        self.SeasonFolder = SeasonFolder
        self.CurrentHeigh = CurrentHeigh
        self.Type = Type
        self.mkvmergeexe = mkvmergeexe

    def NetflixMuxer(self, lang):
        VideoInputNoExist = False
        if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].h264'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].h264'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mkv'
        elif os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mp4'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mp4'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mkv'
        elif os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].h265'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].h265'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mkv'
        elif os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mp4'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mp4'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mkv'
        elif os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].vp9'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].vp9'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mkv'
        elif os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mp4'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mp4'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mkv'
        elif os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].h265'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].h265'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mkv'
        elif os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].h265'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].h265'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mkv'
        elif os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mp4'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mp4'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mkv'
        elif os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].h264'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].h264'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mkv'
        else:
            if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mp4'):
                VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mp4'
                if self.Type == 'show':
                    VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mkv'
                else:
                    VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mkv'
            else:
                VideoInputNoExist = True
            if VideoInputNoExist == False:
                AudioExtensionsList = [
                 '.ac3',
                 '.eac3',
                 '.m4a',
                 '.dts',
                 '.mp3',
                 '.aac']
                SubsExtensionsList = [
                 '.srt',
                 '.ass']
                if lang == 'English':
                    language_tag = 'English'
                else:
                    if lang == 'Spanish':
                        language_tag = 'Spanish'
                    else:
                        if lang == 'German':
                            language_tag = 'German'
                        else:
                            language_tag = 'English'
            if language_tag == 'English':
                subs_forced = '[Forced]'
                subs_full = '[Full]'
                subs_sdh = '[SDH]'
                LanguageList = [
                 [
                  'English', 'eng', 'eng', 'English', 'yes', 'yes'],
                 [
                  'British English', 'enGB', 'eng', 'British English', 'no', 'no'],
                 [
                  'European Spanish', 'euSpa', 'spa', 'Castilian', 'no', 'no'],
                 [
                  'Spanish', 'spa', 'spa', 'Spanish', 'no', 'no'],
                 [
                  'Catalan', 'cat', 'cat', 'Catalan', 'no', 'no'],
                 [
                  'Basque', 'eus', 'baq', 'Basque', 'no', 'no'],
                 [
                  'French', 'fra', 'fre', 'French', 'no', 'no'],
                 [
                  'German', 'deu', 'ger', 'German', 'no', 'no'],
                 [
                  'Italian', 'ita', 'ita', 'Italian', 'no', 'no'],
                 [
                  'Portuguese', 'por', 'por', 'Portuguese', 'no', 'no'],
                 [
                  'Brazilian Portuguese', 'brPor', 'por', 'Brazilian Portuguese', 'no', 'no'],
                 [
                  'Polish', 'pol', 'pol', 'Polish', 'no', 'no'],
                 [
                  'Turkish', 'tur', 'tur', 'Turkish', 'no', 'no'],
                 [
                  'Armenian', 'hye', 'arm', 'Armenian', 'no', 'no'],
                 [
                  'Swedish', 'swe', 'swe', 'Swedish', 'no', 'no'],
                 [
                  'Danish', 'dan', 'dan', 'Danish', 'no', 'no'],
                 [
                  'Finnish', 'fin', 'fin', 'Finnish', 'no', 'no'],
                 [
                  'Dutch', 'nld', 'dut', 'Dutch', 'no', 'no'],
                 [
                  'Flemish', 'nlBE', 'dut', 'Flemish', 'no', 'no'],
                 [
                  'Norwegian', 'nob', 'nor', 'Norwegian', 'no', 'no'],
                 [
                  'Icelandic', 'isl', 'ice', 'Icelandic', 'no', 'no'],
                 [
                  'Russian', 'rus', 'rus', 'Russian', 'no', 'no'],
                 [
                  'Ukrainian', 'ukr', 'ukr', 'Ukrainian', 'no', 'no'],
                 [
                  'Hungarian', 'hun', 'hun', 'Hungarian', 'no', 'no'],
                 [
                  'Bulgarian', 'bul', 'bul', 'Bulgarian', 'no', 'no'],
                 [
                  'Croatian', 'hrv', 'hrv', 'Croatian', 'no', 'no'],
                 [
                  'Lithuanian', 'lit', 'lit', 'Lithuanian', 'no', 'no'],
                 [
                  'Estonian', 'est', 'est', 'Estonian', 'no', 'no'],
                 [
                  'Greek', 'ell', 'gre', 'Greek', 'no', 'no'],
                 [
                  'Hebrew', 'heb', 'heb', 'Hebrew', 'no', 'no'],
                 [
                  'Arabic', 'ara', 'ara', 'Arabic', 'no', 'no'],
                 [
                  'Persian', 'fas', 'per', 'Persian', 'no', 'no'],
                 [
                  'Romanian', 'ron', 'rum', 'Romanian', 'no', 'no'],
                 [
                  'Serbian', 'srp', 'srp', 'Serbian', 'no', 'no'],
                 [
                  'Czech', 'ces', 'cze', 'Czech', 'no', 'no'],
                 [
                  'Slovak', 'slk', 'slo', 'Slovak', 'no', 'no'],
                 [
                  'Afrikaans', 'af', 'afr', 'Afrikaans', 'no', 'no'],
                 [
                  'Hindi', 'hin', 'hin', 'Hindi', 'no', 'no'],
                 [
                  'Bangla', 'ben', 'ben', 'Bengali', 'no', 'no'],
                 [
                  'Urdu', 'urd', 'urd', 'Urdu', 'no', 'no'],
                 [
                  'Punjabi', 'pan', 'pan', 'Punjabi', 'no', 'no'],
                 [
                  'Tamil', 'tam', 'tam', 'Tamil', 'no', 'no'],
                 [
                  'Telugu', 'tel', 'tel', 'Telugu', 'no', 'no'],
                 [
                  'Marathi', 'mar', 'mar', 'Marathi', 'no', 'no'],
                 [
                  'Kannada (India)', 'kan', 'kan', 'Kannada (India)', 'no', 'no'],
                 [
                  'Gujarati', 'guj', 'guj', 'Gujarati', 'no', 'no'],
                 [
                  'Malayalam', 'mal', 'mal', 'Malayalam', 'no', 'no'],
                 [
                  'Sinhala', 'sin', 'sin', 'Sinhala', 'no', 'no'],
                 [
                  'Assamese', 'asm', 'asm', 'Assamese', 'no', 'no'],
                 [
                  'Manipuri', 'mni', 'mni', 'Manipuri', 'no', 'no'],
                 [
                  'Tagalog', 'tgl', 'tgl', 'Tagalog', 'no', 'no'],
                 [
                  'Indonesian', 'ind', 'ind', 'Indonesian', 'no', 'no'],
                 [
                  'Malay', 'msa', 'may', 'Malay', 'no', 'no'],
                 [
                  'Filipino', 'fil', 'fil', 'Filipino', 'no', 'no'],
                 [
                  'Vietnamese', 'vie', 'vie', 'Vietnamese', 'no', 'no'],
                 [
                  'Thai', 'tha', 'tha', 'Thai', 'no', 'no'],
                 [
                  'Khmer', 'khm', 'khm', 'Khmer', 'no', 'no'],
                 [
                  'Korean', 'kor', 'kor', 'Korean', 'no', 'no'],
                 [
                  'Mandarin', 'None', 'chi', 'Mandarin', 'no', 'no'],
                 [
                  'Cantonese', 'None', 'chi', 'Cantonese', 'no', 'no'],
                 [
                  'Simplified Chinese', 'zhoS', 'chi', 'Chinese (Simplified)', 'no', 'no'],
                 [
                  'Traditional Chinese', 'zhoT', 'chi', 'Chinese (Traditional)', 'no', 'no'],
                 [
                  'Japanese', 'jpn', 'jpn', 'Japanese', 'no', 'no'],
                 [
                  'Klingon', 'tlh', 'tlh', 'Klingon', 'no', 'no'],
                 [
                  'No Dialogue', 'zxx', 'zxx', 'No Dialogue', 'no', 'no']]
            else:
                if language_tag == 'Spanish':
                    subs_forced = '[Forzados]'
                    subs_full = '[Completos]'
                    subs_sdh = '[Para sordos]'
                    LanguageList = [
                     [
                      'European Spanish', 'euSpa', 'spa', 'Castellano', 'yes', 'yes'],
                     [
                      'Spanish', 'spa', 'spa', 'Español latino', 'no', 'no'],
                     [
                      'Catalan', 'cat', 'cat', 'Catalán', 'no', 'no'],
                     [
                      'Basque', 'eus', 'baq', 'Euskera', 'no', 'no'],
                     [
                      'English', 'eng', 'eng', 'Inglés', 'no', 'no'],
                     [
                      'British English', 'enGB', 'eng', 'Inglés británico', 'no', 'no'],
                     [
                      'French', 'fra', 'fre', 'Francés', 'no', 'no'],
                     [
                      'German', 'deu', 'ger', 'Alemán', 'no', 'no'],
                     [
                      'Italian', 'ita', 'ita', 'Italiano', 'no', 'no'],
                     [
                      'Portuguese', 'por', 'por', 'Portugués', 'no', 'no'],
                     [
                      'Brazilian Portuguese', 'brPor', 'por', 'Portugués brasileño', 'no', 'no'],
                     [
                      'Polish', 'pol', 'pol', 'Polaco', 'no', 'no'],
                     [
                      'Turkish', 'tur', 'tur', 'Turco', 'no', 'no'],
                     [
                      'Armenian', 'hye', 'arm', 'Armenio', 'no', 'no'],
                     [
                      'Swedish', 'swe', 'swe', 'Sueco', 'no', 'no'],
                     [
                      'Danish', 'dan', 'dan', 'Danés', 'no', 'no'],
                     [
                      'Finnish', 'fin', 'fin', 'Finés', 'no', 'no'],
                     [
                      'Dutch', 'nld', 'dut', 'Holandés', 'no', 'no'],
                     [
                      'Flemish', 'nlBE', 'dut', 'Flamenco', 'no', 'no'],
                     [
                      'Norwegian', 'nob', 'nor', 'Noruego', 'no', 'no'],
                     [
                      'Icelandic', 'isl', 'ice', 'Islandés', 'no', 'no'],
                     [
                      'Russian', 'rus', 'rus', 'Ruso', 'no', 'no'],
                     [
                      'Ukrainian', 'ukr', 'ukr', 'Ucrainés', 'no', 'no'],
                     [
                      'Hungarian', 'hun', 'hun', 'Húngaro', 'no', 'no'],
                     [
                      'Bulgarian', 'bul', 'bul', 'Búlgaro', 'no', 'no'],
                     [
                      'Croatian', 'hrv', 'hrv', 'Croata', 'no', 'no'],
                     [
                      'Lithuanian', 'lit', 'lit', 'Lituano', 'no', 'no'],
                     [
                      'Estonian', 'est', 'est', 'Estonio', 'no', 'no'],
                     [
                      'Greek', 'ell', 'gre', 'Griego', 'no', 'no'],
                     [
                      'Hebrew', 'heb', 'heb', 'Hebreo', 'no', 'no'],
                     [
                      'Arabic', 'ara', 'ara', 'Árabe', 'no', 'no'],
                     [
                      'Persian', 'fas', 'per', 'Persa', 'no', 'no'],
                     [
                      'Romanian', 'ron', 'rum', 'Rumano', 'no', 'no'],
                     [
                      'Serbian', 'srp', 'srp', 'Serbio', 'no', 'no'],
                     [
                      'Czech', 'ces', 'cze', 'Checo', 'no', 'no'],
                     [
                      'Slovak', 'slk', 'slo', 'Eslovaco', 'no', 'no'],
                     [
                      'Afrikaans', 'af', 'afr', 'Afrikáans', 'no', 'no'],
                     [
                      'Hindi', 'hin', 'hin', 'Hindi', 'no', 'no'],
                     [
                      'Bangla', 'ben', 'ben', 'Bengalí', 'no', 'no'],
                     [
                      'Urdu', 'urd', 'urd', 'Urdú', 'no', 'no'],
                     [
                      'Punjabi', 'pan', 'pan', 'Panyabí', 'no', 'no'],
                     [
                      'Tamil', 'tam', 'tam', 'Tamil', 'no', 'no'],
                     [
                      'Telugu', 'tel', 'tel', 'Télugu', 'no', 'no'],
                     [
                      'Marathi', 'mar', 'mar', 'Maratí', 'no', 'no'],
                     [
                      'Kannada (India)', 'kan', 'kan', 'Canarés', 'no', 'no'],
                     [
                      'Gujarati', 'guj', 'guj', 'Guyaratí', 'no', 'no'],
                     [
                      'Malayalam', 'mal', 'mal', 'Malabar', 'no', 'no'],
                     [
                      'Sinhala', 'sin', 'sin', 'Cingalés', 'no', 'no'],
                     [
                      'Assamese', 'asm', 'asm', 'Asamés', 'no', 'no'],
                     [
                      'Manipuri', 'mni', 'mni', 'Meitei', 'no', 'no'],
                     [
                      'Tagalog', 'tgl', 'tgl', 'Tagalo', 'no', 'no'],
                     [
                      'Indonesian', 'ind', 'ind', 'Indonesio', 'no', 'no'],
                     [
                      'Malay', 'msa', 'may', 'Malayo', 'no', 'no'],
                     [
                      'Filipino', 'fil', 'fil', 'Filipino', 'no', 'no'],
                     [
                      'Vietnamese', 'vie', 'vie', 'Vietnamita', 'no', 'no'],
                     [
                      'Thai', 'tha', 'tha', 'Tailandés', 'no', 'no'],
                     [
                      'Khmer', 'khm', 'khm', 'Camboyano', 'no', 'no'],
                     [
                      'Korean', 'kor', 'kor', 'Coreano', 'no', 'no'],
                     [
                      'Mandarin', 'None', 'chi', 'Mandarín', 'no', 'no'],
                     [
                      'Cantonese', 'None', 'chi', 'Cantonés', 'no', 'no'],
                     [
                      'Simplified Chinese', 'zhoS', 'chi', 'Chino (Simplificado)', 'no', 'no'],
                     [
                      'Traditional Chinese', 'zhoT', 'chi', 'Chino (Tradicional)', 'no', 'no'],
                     [
                      'Japanese', 'jpn', 'jpn', 'Japonés', 'no', 'no'],
                     [
                      'Klingon', 'tlh', 'tlh', 'Klingon', 'no', 'no'],
                     [
                      'No Dialogue', 'zxx', 'zxx', 'Sin diálogo', 'no', 'no']]
                else:
                    if language_tag == 'German':
                        subs_forced = '[Forced]'
                        subs_full = '[Full]'
                        subs_sdh = '[SDH]'
                        LanguageList = [
                         [
                          'German', 'deu', 'ger', 'Deutsch', 'yes', 'yes'],
                         [
                          'English', 'eng', 'eng', 'Englisch', 'no', 'no'],
                         [
                          'British English', 'enGB', 'eng', 'Britisches Englisch', 'no', 'no'],
                         [
                          'European Spanish', 'euSpa', 'spa', 'Kastilisch', 'no', 'no'],
                         [
                          'Spanish', 'spa', 'spa', 'Spanisch', 'no', 'no'],
                         [
                          'Catalan', 'cat', 'cat', 'Katalanisch', 'no', 'no'],
                         [
                          'Basque', 'eus', 'baq', 'Baskisch', 'no', 'no'],
                         [
                          'French', 'fra', 'fre', 'Französisch', 'no', 'no'],
                         [
                          'Italian', 'ita', 'ita', 'Italienisch', 'no', 'no'],
                         [
                          'Portuguese', 'por', 'por', 'Portugiesisch', 'no', 'no'],
                         [
                          'Brazilian Portuguese', 'brPor', 'por', 'Brasilianisches Portugiesisch', 'no', 'no'],
                         [
                          'Polish', 'pol', 'pol', 'Polnisch', 'no', 'no'],
                         [
                          'Turkish', 'tur', 'tur', 'Türkisch', 'no', 'no'],
                         [
                          'Armenian', 'hye', 'arm', 'Armenisch', 'no', 'no'],
                         [
                          'Swedish', 'swe', 'swe', 'Schwedisch', 'no', 'no'],
                         [
                          'Danish', 'dan', 'dan', 'Dänisch', 'no', 'no'],
                         [
                          'Finnish', 'fin', 'fin', 'Finnisch', 'no', 'no'],
                         [
                          'Dutch', 'nld', 'dut', 'Holländisch', 'no', 'no'],
                         [
                          'Flemish', 'nlBE', 'dut', 'Flämisch', 'no', 'no'],
                         [
                          'Norwegian', 'nob', 'nor', 'Norwegisch', 'no', 'no'],
                         [
                          'Icelandic', 'isl', 'ice', 'Isländisch', 'no', 'no'],
                         [
                          'Russian', 'rus', 'rus', 'Russisch', 'no', 'no'],
                         [
                          'Ukrainian', 'ukr', 'ukr', 'Ukrainisch', 'no', 'no'],
                         [
                          'Hungarian', 'hun', 'hun', 'Ungarisch', 'no', 'no'],
                         [
                          'Bulgarian', 'bul', 'bul', 'Bulgarisch', 'no', 'no'],
                         [
                          'Croatian', 'hrv', 'hrv', 'Kroatisch', 'no', 'no'],
                         [
                          'Lithuanian', 'lit', 'lit', 'Litauisch', 'no', 'no'],
                         [
                          'Estonian', 'est', 'est', 'Estnisch', 'no', 'no'],
                         [
                          'Greek', 'ell', 'gre', 'Griechisch', 'no', 'no'],
                         [
                          'Hebrew', 'heb', 'heb', 'Hebräisch', 'no', 'no'],
                         [
                          'Arabic', 'ara', 'ara', 'Arabisch', 'no', 'no'],
                         [
                          'Persian', 'fas', 'per', 'Persisch', 'no', 'no'],
                         [
                          'Romanian', 'ron', 'rum', 'Romänisch', 'no', 'no'],
                         [
                          'Serbian', 'srp', 'srp', 'Serbisch', 'no', 'no'],
                         [
                          'Czech', 'ces', 'cze', 'Tschechisch', 'no', 'no'],
                         [
                          'Slovak', 'slk', 'slo', 'Slowakisch', 'no', 'no'],
                         [
                          'Afrikaans', 'af', 'afr', 'Afrikaans', 'no', 'no'],
                         [
                          'Hindi', 'hin', 'hin', 'Hindi', 'no', 'no'],
                         [
                          'Bangla', 'ben', 'ben', 'Bengalisch', 'no', 'no'],
                         [
                          'Urdu', 'urd', 'urd', 'Urdu', 'no', 'no'],
                         [
                          'Punjabi', 'pan', 'pan', 'Panjabi', 'no', 'no'],
                         [
                          'Tamil', 'tam', 'tam', 'Tamil', 'no', 'no'],
                         [
                          'Telugu', 'tel', 'tel', 'Telugu', 'no', 'no'],
                         [
                          'Marathi', 'mar', 'mar', 'Marathi', 'no', 'no'],
                         [
                          'Kannada (India)', 'kan', 'kan', 'Kanaresisch (Indien)', 'no', 'no'],
                         [
                          'Gujarati', 'guj', 'guj', 'Gujarati', 'no', 'no'],
                         [
                          'Malayalam', 'mal', 'mal', 'Malayalam', 'no', 'no'],
                         [
                          'Sinhala', 'sin', 'sin', 'Singhalesisch', 'no', 'no'],
                         [
                          'Assamese', 'asm', 'asm', 'Assamesisch', 'no', 'no'],
                         [
                          'Manipuri', 'mni', 'mni', 'Manipuri', 'no', 'no'],
                         [
                          'Tagalog', 'tgl', 'tgl', 'Tagalog', 'no', 'no'],
                         [
                          'Indonesian', 'ind', 'ind', 'Indonesisch', 'no', 'no'],
                         [
                          'Malay', 'msa', 'may', 'Malaiisch', 'no', 'no'],
                         [
                          'Filipino', 'fil', 'fil', 'Filipino', 'no', 'no'],
                         [
                          'Vietnamese', 'vie', 'vie', 'Vietnamesisch', 'no', 'no'],
                         [
                          'Thai', 'tha', 'tha', 'Thailändisch', 'no', 'no'],
                         [
                          'Khmer', 'khm', 'khm', 'Khmer', 'no', 'no'],
                         [
                          'Korean', 'kor', 'kor', 'Koreanisch', 'no', 'no'],
                         [
                          'Mandarin', 'None', 'chi', 'Mandarin', 'no', 'no'],
                         [
                          'Cantonese', 'None', 'chi', 'Kantonesisch', 'no', 'no'],
                         [
                          'Simplified Chinese', 'zhoS', 'chi', 'Chinesisch (Vereinfacht)', 'no', 'no'],
                         [
                          'Traditional Chinese', 'zhoT', 'chi', 'Chinesisch (Traditionell)', 'no', 'no'],
                         [
                          'Japanese', 'jpn', 'jpn', 'Japanisch', 'no', 'no'],
                         [
                          'Klingon', 'tlh', 'tlh', 'Klingonisch', 'no', 'no'],
                         [
                          'No Dialogue', 'zxx', 'zxx', 'Kein Dialog', 'no', 'no']]
            ALLAUDIOS = []
            for audio_language, subs_language, language_id, language_name, audio_default, subs_default in LanguageList:
                for AudioExtension in AudioExtensionsList:
                    if os.path.isfile('.\\' + self.CurrentName + ' ' + audio_language + AudioExtension):
                        ALLAUDIOS = ALLAUDIOS + ['--language', '0:' + language_id, '--track-name',
                         '0:' + language_name, '--default-track', '0:' + audio_default, '(',
                         '.\\' + self.CurrentName + ' ' + audio_language + AudioExtension, ')']
                        audio_default = False

            for audio_language, subs_language, language_id, language_name, audio_default, subs_default in LanguageList:
                for AudioExtension in AudioExtensionsList:
                    if os.path.isfile('.\\' + self.CurrentName + ' ' + audio_language + ' - Audio Description' + AudioExtension):
                        ALLAUDIOS = ALLAUDIOS + ['--language', '0:' + language_id, '--track-name',
                         '0:' + language_name + ' (Audio Description)',
                         '--default-track', '0:no', '(',
                         '.\\' + self.CurrentName + ' ' + audio_language + ' - Audio Description' + AudioExtension, ')']
                        audio_default = False

            OnlyOneLanguage = False
            if len(ALLAUDIOS) == 9:
                OnlyOneLanguage = True
            if len(ALLAUDIOS) == 18:
                if ALLAUDIOS[1] == ALLAUDIOS[10]:
                    if ' - Audio Description' in ALLAUDIOS[7] or ' - Audio Description' in ALLAUDIOS[16]:
                        OnlyOneLanguage = True
                    else:
                        OnlyOneLanguage = False
            ALLSUBS = []
            default_active_subs = False
            for audio_language, subs_language, language_id, language_name, audio_default, subs_default in LanguageList:
                for SubsExtension in SubsExtensionsList:
                    if os.path.isfile('.\\' + self.CurrentName + ' ' + 'forced-' + subs_language + SubsExtension):
                        default_active_subs = True
                        ALLSUBS = ALLSUBS + ['--language', '0:' + language_id, '--track-name', '0:' + language_name + ' ' + subs_forced, '--forced-track', '0:yes', '--default-track', '0:' + subs_default, '--compression', '0:none', '(', '.\\' + self.CurrentName + ' ' + 'forced-' + subs_language + SubsExtension, ')']
                    if OnlyOneLanguage == True:
                        if default_active_subs == True:
                            subs_default = 'no'
                        if os.path.isfile('.\\' + self.CurrentName + ' ' + subs_language + SubsExtension):
                            ALLSUBS = ALLSUBS + ['--language', '0:' + language_id, '--track-name', '0:' + language_name + ' ' + subs_full, '--forced-track', '0:no', '--default-track', '0:' + subs_default, '--compression', '0:none', '(', '.\\' + self.CurrentName + ' ' + subs_language + SubsExtension, ')']
                        else:
                            if os.path.isfile('.\\' + self.CurrentName + ' ' + subs_language + SubsExtension):
                                ALLSUBS = ALLSUBS + ['--language', '0:' + language_id, '--track-name', '0:' + language_name + ' ' + subs_full, '--forced-track', '0:no', '--default-track', '0:no', '--compression', '0:none', '(', '.\\' + self.CurrentName + ' ' + subs_language + SubsExtension, ')']
                        if os.path.isfile('.\\' + self.CurrentName + ' ' + 'sdh-' + subs_language + SubsExtension):
                            ALLSUBS = ALLSUBS + ['--language', '0:' + language_id, '--track-name',
                             '0:' + language_name + ' ' + subs_sdh, '--forced-track', '0:no',
                             '--default-track', '0:no', '--compression', '0:none', '(',
                             '.\\' + self.CurrentName + ' ' + 'sdh-' + subs_language + SubsExtension, ')']

            mkvmerge_command_video = [
             self.mkvmergeexe,
             '-q',
             '--output',
             VideoOutputName,
             '--language',
             '0:und',
             '--default-track',
             '0:yes',
             '(',
             VideoInputName,
             ')']
            mkvmerge_command = mkvmerge_command_video + ALLAUDIOS + ALLSUBS
            mkvmerge_process = subprocess.Popen(mkvmerge_command)
            stdoutdata, stderrdata = mkvmerge_process.communicate()
            mkvmerge_process.wait()

    def AmazonAndPrimeVideoMuxer(self, lang):
        VideoInputNoExist = False
        if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].h264'):
            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].h264'
            if self.Type == 'show':
                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mkv'
            else:
                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mkv'
        else:
            if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mp4'):
                VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mp4'
                if self.Type == 'show':
                    VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mkv'
                else:
                    VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mkv'
            else:
                if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].h265'):
                    VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].h265'
                    if self.Type == 'show':
                        VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mkv'
                    else:
                        VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HEVC].mkv'
                else:
                    if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mp4'):
                        VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mp4'
                        if self.Type == 'show':
                            VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mkv'
                        else:
                            VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mkv'
                    else:
                        if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].vp9'):
                            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].vp9'
                            if self.Type == 'show':
                                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mkv'
                            else:
                                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [VP9].mkv'
                        else:
                            if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mp4'):
                                VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mp4'
                                if self.Type == 'show':
                                    VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mkv'
                                else:
                                    VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mkv'
                            else:
                                if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].h265'):
                                    VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].h265'
                                    if self.Type == 'show':
                                        VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mkv'
                                    else:
                                        VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [HDR].mkv'
                                else:
                                    if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mp4'):
                                        VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mp4'
                                        if self.Type == 'show':
                                            VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mkv'
                                        else:
                                            VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mkv'
                                    else:
                                        if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].h264'):
                                            VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].h264'
                                            if self.Type == 'show':
                                                VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mkv'
                                            else:
                                                VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p] [AVC HIGH].mkv'
                                        else:
                                            if os.path.isfile('.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mp4'):
                                                VideoInputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mp4'
                                                if self.Type == 'show':
                                                    VideoOutputName = '.\\' + self.SeasonFolder + '\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mkv'
                                                else:
                                                    VideoOutputName = '.\\' + self.CurrentName + ' [' + self.CurrentHeigh + 'p].mkv'
                                            else:
                                                VideoInputNoExist = True
        if VideoInputNoExist == False:
            AudioExtensionsList = ['.ac3', '.eac3', '.m4a', '.dts', '.mp3', '.aac']
            SubsExtensionsList = [
             '.srt', '.ass']
            if lang == 'English':
                language_tag = 'English'
            else:
                if lang == 'Spanish':
                    language_tag = 'Spanish'
                else:
                    if lang == 'German':
                        language_tag = 'German'
                    else:
                        language_tag = 'English'
                    if language_tag == 'English':
                        subs_forced = '[Forced]'
                        subs_full = '[Full]'
                        subs_sdh = '[SDH]'
                        LanguageList = [
                         [
                          'en', 'en', 'eng', 'English', 'yes', 'yes'],
                         [
                          'es', 'es', 'spa', 'Castilian', 'no', 'no'],
                         [
                          'es-la', 'es-la', 'spa', 'Spanish', 'no', 'no'],
                         [
                          'cat', 'cat', 'cat', 'Catalan', 'no', 'no'],
                         [
                          'eu', 'eu', 'baq', 'Basque', 'no', 'no'],
                         [
                          'fr', 'fr', 'fre', 'French', 'no', 'no'],
                         [
                          'fr-bg', 'fr-bg', 'fre', 'French (Belgium)', 'no', 'no'],
                         [
                          'fr-lu', 'fr-lu', 'fre', 'French (Luxembourg)', 'no', 'no'],
                         [
                          'fr-ca', 'fr-ca', 'fre', 'French (Canada)', 'no', 'no'],
                         [
                          'de', 'de', 'ger', 'German', 'no', 'no'],
                         [
                          'it', 'it', 'ita', 'Italian', 'no', 'no'],
                         [
                          'pt', 'pt', 'por', 'Portuguese', 'no', 'no'],
                         [
                          'pt-br', 'pt-br', 'por', 'Brazilian Portuguese', 'no', 'no'],
                         [
                          'pl', 'pl', 'pol', 'Polish', 'no', 'no'],
                         [
                          'tr', 'tr', 'tur', 'Turkish', 'no', 'no'],
                         [
                          'hy', 'hy', 'arm', 'Armenian', 'no', 'no'],
                         [
                          'sv', 'sv', 'swe', 'Swedish', 'no', 'no'],
                         [
                          'da', 'da', 'dan', 'Danish', 'no', 'no'],
                         [
                          'fi', 'fi', 'fin', 'Finnish', 'no', 'no'],
                         [
                          'nl', 'nl', 'dut', 'Dutch', 'no', 'no'],
                         [
                          'nl-be', 'nl-be', 'dut', 'Flemish', 'no', 'no'],
                         [
                          'no', 'no', 'nor', 'Norwegian', 'no', 'no'],
                         [
                          'lv', 'lv', 'lav', 'Latvian', 'no', 'no'],
                         [
                          'is', 'is', 'ice', 'Icelandic', 'no', 'no'],
                         [
                          'ru', 'ru', 'rus', 'Russian', 'no', 'no'],
                         [
                          'ru-by', 'ru-by', 'rus', 'Belarusian', 'no', 'no'],
                         [
                          'uk', 'uk', 'ukr', 'Ukrainian', 'no', 'no'],
                         [
                          'hu', 'hu', 'hun', 'Hungarian', 'no', 'no'],
                         [
                          'bg', 'bg', 'bul', 'Bulgarian', 'no', 'no'],
                         [
                          'hr', 'hr', 'hrv', 'Croatian', 'no', 'no'],
                         [
                          'lt', 'lt', 'lit', 'Lithuanian', 'no', 'no'],
                         [
                          'et', 'et', 'est', 'Estonian', 'no', 'no'],
                         [
                          'el', 'el', 'gre', 'Greek', 'no', 'no'],
                         [
                          'he', 'he', 'heb', 'Hebrew', 'no', 'no'],
                         [
                          'ar', 'ar', 'ara', 'Arabic', 'no', 'no'],
                         [
                          'fa', 'fa', 'per', 'Persian', 'no', 'no'],
                         [
                          'ro', 'ro', 'rum', 'Romanian', 'no', 'no'],
                         [
                          'sr', 'sr', 'srp', 'Serbian', 'no', 'no'],
                         [
                          'cs', 'cs', 'cze', 'Czech', 'no', 'no'],
                         [
                          'sk', 'sk', 'slo', 'Slovak', 'no', 'no'],
                         [
                          'sl', 'sl', 'slv', 'Slovenian', 'no', 'no'],
                         [
                          'sq', 'sq', 'alb', 'Albanian', 'no', 'no'],
                         [
                          'bs', 'bs', 'bos', 'Bosnian', 'no', 'no'],
                         [
                          'mk', 'mk', 'mac', 'Macedonian', 'no', 'no'],
                         [
                          'hi', 'hi', 'hin', 'Hindi', 'no', 'no'],
                         [
                          'bn', 'bn', 'ben', 'Bengali', 'no', 'no'],
                         [
                          'ur', 'ur', 'urd', 'Urdu', 'no', 'no'],
                         [
                          'pa', 'pa', 'pan', 'Punjabi', 'no', 'no'],
                         [
                          'ta', 'ta', 'tam', 'Tamil', 'no', 'no'],
                         [
                          'te', 'te', 'tel', 'Telugu', 'no', 'no'],
                         [
                          'mr', 'mr', 'mar', 'Marathi', 'no', 'no'],
                         [
                          'kn', 'kn', 'kan', 'Kannada (India)', 'no', 'no'],
                         [
                          'gu', 'gu', 'guj', 'Gujarati', 'no', 'no'],
                         [
                          'ml', 'ml', 'mal', 'Malayalam', 'no', 'no'],
                         [
                          'si', 'si', 'sin', 'Sinhala', 'no', 'no'],
                         [
                          'as', 'as', 'asm', 'Assamese', 'no', 'no'],
                         [
                          'mni', 'mni', 'mni', 'Manipuri', 'no', 'no'],
                         [
                          'tl', 'tl', 'tgl', 'Tagalog', 'no', 'no'],
                         [
                          'id', 'id', 'ind', 'Indonesian', 'no', 'no'],
                         [
                          'ms', 'ms', 'may', 'Malay', 'no', 'no'],
                         [
                          'vi', 'vi', 'vie', 'Vietnamese', 'no', 'no'],
                         [
                          'th', 'th', 'tha', 'Thai', 'no', 'no'],
                         [
                          'km', 'km', 'khm', 'Khmer', 'no', 'no'],
                         [
                          'ko', 'ko', 'kor', 'Korean', 'no', 'no'],
                         [
                          'zh', 'zh', 'chi', 'Mandarin', 'no', 'no'],
                         [
                          'yue', 'yue', 'chi', 'Cantonese', 'no', 'no'],
                         [
                          'zh-hans', 'zh-hans', 'chi', 'Chinese (Simplified)', 'no', 'no'],
                         [
                          'zh-hant', 'zh-hant', 'chi', 'Chinese (Traditional)', 'no', 'no'],
                         [
                          'zh-hk', 'zh-hk', 'chi', 'Chinese (Simplified)', 'no', 'no'],
                         [
                          'zh-tw', 'zh-tw', 'chi', 'Chinese (Traditional)', 'no', 'no'],
                         [
                          'ja', 'ja', 'jpn', 'Japanese', 'no', 'no'],
                         [
                          'tlh', 'tlh', 'tlh', 'Klingon', 'no', 'no'],
                         [
                          'zxx', 'zxx', 'zxx', 'No Dialogue', 'no', 'no']]
                    else:
                        if language_tag == 'Spanish':
                            subs_forced = '[Forzados]'
                            subs_full = '[Completos]'
                            subs_sdh = '[Para sordos]'
                            LanguageList = [
                             [
                              'es', 'es', 'spa', 'Castellano', 'yes', 'yes'],
                             [
                              'es-la', 'es-la', 'spa', 'Español latino', 'no', 'no'],
                             [
                              'cat', 'cat', 'cat', 'Catalán', 'no', 'no'],
                             [
                              'eu', 'eu', 'baq', 'Euskera', 'no', 'no'],
                             [
                              'en', 'en', 'eng', 'Inglés', 'no', 'no'],
                             [
                              'fr', 'fr', 'fre', 'Francés', 'no', 'no'],
                             [
                              'fr-bg', 'fr-bg', 'fre', 'Francés (Bélgica)', 'no', 'no'],
                             [
                              'fr-lu', 'fr-lu', 'fre', 'Francés (Luxemburgo)', 'no', 'no'],
                             [
                              'fr-ca', 'fr-ca', 'fre', 'Francés (Canadá)', 'no', 'no'],
                             [
                              'de', 'de', 'ger', 'Alemán', 'no', 'no'],
                             [
                              'it', 'it', 'ita', 'Italiano', 'no', 'no'],
                             [
                              'pt', 'pt', 'por', 'Portugués', 'no', 'no'],
                             [
                              'pt-br', 'pt-br', 'por', 'Portugués brasileño', 'no', 'no'],
                             [
                              'pl', 'pl', 'pol', 'Polaco', 'no', 'no'],
                             [
                              'tr', 'tr', 'tur', 'Turco', 'no', 'no'],
                             [
                              'hy', 'hy', 'arm', 'Armenio', 'no', 'no'],
                             [
                              'sv', 'sv', 'swe', 'Sueco', 'no', 'no'],
                             [
                              'da', 'da', 'dan', 'Danés', 'no', 'no'],
                             [
                              'fi', 'fi', 'fin', 'Finés', 'no', 'no'],
                             [
                              'nl', 'nl', 'dut', 'Holandés', 'no', 'no'],
                             [
                              'nl-be', 'nl-be', 'dut', 'Flamenco', 'no', 'no'],
                             [
                              'no', 'no', 'nor', 'Noruego', 'no', 'no'],
                             [
                              'lv', 'lv', 'lav', 'Letón', 'no', 'no'],
                             [
                              'is', 'is', 'ice', 'Islandés', 'no', 'no'],
                             [
                              'ru', 'ru', 'rus', 'Ruso', 'no', 'no'],
                             [
                              'ru-by', 'ru-by', 'rus', 'Bielorruso', 'no', 'no'],
                             [
                              'uk', 'uk', 'ukr', 'Ucrainés', 'no', 'no'],
                             [
                              'hu', 'hu', 'hun', 'Húngaro', 'no', 'no'],
                             [
                              'bg', 'bg', 'bul', 'Búlgaro', 'no', 'no'],
                             [
                              'hr', 'hr', 'hrv', 'Croata', 'no', 'no'],
                             [
                              'lt', 'lt', 'lit', 'Lituano', 'no', 'no'],
                             [
                              'et', 'et', 'est', 'Estonio', 'no', 'no'],
                             [
                              'el', 'el', 'gre', 'Griego', 'no', 'no'],
                             [
                              'he', 'he', 'heb', 'Hebreo', 'no', 'no'],
                             [
                              'ar', 'ar', 'ara', 'Árabe', 'no', 'no'],
                             [
                              'fa', 'fa', 'per', 'Persa', 'no', 'no'],
                             [
                              'ro', 'ro', 'rum', 'Rumano', 'no', 'no'],
                             [
                              'sr', 'sr', 'srp', 'Serbio', 'no', 'no'],
                             [
                              'cs', 'cs', 'cze', 'Checo', 'no', 'no'],
                             [
                              'sk', 'sk', 'slo', 'Eslovaco', 'no', 'no'],
                             [
                              'sl', 'sl', 'slv', 'Esloveno', 'no', 'no'],
                             [
                              'sq', 'sq', 'alb', 'Albanés', 'no', 'no'],
                             [
                              'bs', 'bs', 'bos', 'Bosnio', 'no', 'no'],
                             [
                              'mk', 'mk', 'mac', 'Macedonio', 'no', 'no'],
                             [
                              'hi', 'hi', 'hin', 'Hindi', 'no', 'no'],
                             [
                              'bn', 'bn', 'ben', 'Bengalí', 'no', 'no'],
                             [
                              'ur', 'ur', 'urd', 'Urdú', 'no', 'no'],
                             [
                              'pa', 'pa', 'pan', 'Panyabí', 'no', 'no'],
                             [
                              'ta', 'ta', 'tam', 'Tamil', 'no', 'no'],
                             [
                              'te', 'te', 'tel', 'Télugu', 'no', 'no'],
                             [
                              'mr', 'mr', 'mar', 'Maratí', 'no', 'no'],
                             [
                              'kn', 'kn', 'kan', 'Canarés', 'no', 'no'],
                             [
                              'gu', 'gu', 'guj', 'Guyaratí', 'no', 'no'],
                             [
                              'ml', 'ml', 'mal', 'Malabar', 'no', 'no'],
                             [
                              'si', 'si', 'sin', 'Cingalés', 'no', 'no'],
                             [
                              'as', 'as', 'asm', 'Asamés', 'no', 'no'],
                             [
                              'mni', 'mni', 'mni', 'Meitei', 'no', 'no'],
                             [
                              'tl', 'tl', 'tgl', 'Tagalo', 'no', 'no'],
                             [
                              'id', 'id', 'ind', 'Indonesio', 'no', 'no'],
                             [
                              'ms', 'ms', 'may', 'Malayo', 'no', 'no'],
                             [
                              'vi', 'vi', 'vie', 'Vietnamita', 'no', 'no'],
                             [
                              'th', 'th', 'tha', 'Tailandés', 'no', 'no'],
                             [
                              'km', 'km', 'khm', 'Camboyano', 'no', 'no'],
                             [
                              'ko', 'ko', 'kor', 'Coreano', 'no', 'no'],
                             [
                              'zh', 'zh', 'chi', 'Mandarín', 'no', 'no'],
                             [
                              'yue', 'yue', 'chi', 'Cantonés', 'no', 'no'],
                             [
                              'zh-hans', 'zh-hans', 'chi', 'Chino (Simplificado)', 'no', 'no'],
                             [
                              'zh-hant', 'zh-hant', 'chi', 'Chino (Tradicional)', 'no', 'no'],
                             [
                              'zh-hk', 'zh-hk', 'chi', 'Chino (Simplificado)', 'no', 'no'],
                             [
                              'zh-tw', 'zh-tw', 'chi', 'Chino (Tradicional)', 'no', 'no'],
                             [
                              'ja', 'ja', 'jpn', 'Japonés', 'no', 'no'],
                             [
                              'tlh', 'tlh', 'tlh', 'Klingon', 'no', 'no'],
                             [
                              'zxx', 'zxx', 'zxx', 'Sin diálogo', 'no', 'no']]
                        else:
                            if language_tag == 'German':
                                subs_forced = '[Forced]'
                                subs_full = '[Full]'
                                subs_sdh = '[SDH]'
                                LanguageList = [
                                 [
                                  'German', 'deu', 'ger', 'Deutsch', 'yes', 'yes'],
                                 [
                                  'English', 'eng', 'eng', 'Englisch', 'no', 'no'],
                                 [
                                  'British English', 'enGB', 'eng', 'Britisches Englisch', 'no', 'no'],
                                 [
                                  'European Spanish', 'euSpa', 'spa', 'Kastilisch', 'no', 'no'],
                                 [
                                  'Spanish', 'spa', 'spa', 'Spanisch', 'no', 'no'],
                                 [
                                  'Catalan', 'cat', 'cat', 'Katalanisch', 'no', 'no'],
                                 [
                                  'Basque', 'eus', 'baq', 'Baskisch', 'no', 'no'],
                                 [
                                  'French', 'fra', 'fre', 'Französisch', 'no', 'no'],
                                 [
                                  'Italian', 'ita', 'ita', 'Italienisch', 'no', 'no'],
                                 [
                                  'Portuguese', 'por', 'por', 'Portugiesisch', 'no', 'no'],
                                 [
                                  'Brazilian Portuguese', 'brPor', 'por', 'Brasilianisches Portugiesisch', 'no', 'no'],
                                 [
                                  'Polish', 'pol', 'pol', 'Polnisch', 'no', 'no'],
                                 [
                                  'Turkish', 'tur', 'tur', 'Türkisch', 'no', 'no'],
                                 [
                                  'Armenian', 'hye', 'arm', 'Armenisch', 'no', 'no'],
                                 [
                                  'Swedish', 'swe', 'swe', 'Schwedisch', 'no', 'no'],
                                 [
                                  'Danish', 'dan', 'dan', 'Dänisch', 'no', 'no'],
                                 [
                                  'Finnish', 'fin', 'fin', 'Finnisch', 'no', 'no'],
                                 [
                                  'Dutch', 'nld', 'dut', 'Holländisch', 'no', 'no'],
                                 [
                                  'Flemish', 'nlBE', 'dut', 'Flämisch', 'no', 'no'],
                                 [
                                  'Norwegian', 'nob', 'nor', 'Norwegisch', 'no', 'no'],
                                 [
                                  'Icelandic', 'isl', 'ice', 'Isländisch', 'no', 'no'],
                                 [
                                  'Russian', 'rus', 'rus', 'Russisch', 'no', 'no'],
                                 [
                                  'Ukrainian', 'ukr', 'ukr', 'Ukrainisch', 'no', 'no'],
                                 [
                                  'Hungarian', 'hun', 'hun', 'Ungarisch', 'no', 'no'],
                                 [
                                  'Bulgarian', 'bul', 'bul', 'Bulgarisch', 'no', 'no'],
                                 [
                                  'Croatian', 'hrv', 'hrv', 'Kroatisch', 'no', 'no'],
                                 [
                                  'Lithuanian', 'lit', 'lit', 'Litauisch', 'no', 'no'],
                                 [
                                  'Estonian', 'est', 'est', 'Estnisch', 'no', 'no'],
                                 [
                                  'Greek', 'ell', 'gre', 'Griechisch', 'no', 'no'],
                                 [
                                  'Hebrew', 'heb', 'heb', 'Hebräisch', 'no', 'no'],
                                 [
                                  'Arabic', 'ara', 'ara', 'Arabisch', 'no', 'no'],
                                 [
                                  'Persian', 'fas', 'per', 'Persisch', 'no', 'no'],
                                 [
                                  'Romanian', 'ron', 'rum', 'Romänisch', 'no', 'no'],
                                 [
                                  'Serbian', 'srp', 'srp', 'Serbisch', 'no', 'no'],
                                 [
                                  'Czech', 'ces', 'cze', 'Tschechisch', 'no', 'no'],
                                 [
                                  'Slovak', 'slk', 'slo', 'Slowakisch', 'no', 'no'],
                                 [
                                  'Afrikaans', 'af', 'afr', 'Afrikaans', 'no', 'no'],
                                 [
                                  'Hindi', 'hin', 'hin', 'Hindi', 'no', 'no'],
                                 [
                                  'Bangla', 'ben', 'ben', 'Bengalisch', 'no', 'no'],
                                 [
                                  'Urdu', 'urd', 'urd', 'Urdu', 'no', 'no'],
                                 [
                                  'Punjabi', 'pan', 'pan', 'Panjabi', 'no', 'no'],
                                 [
                                  'Tamil', 'tam', 'tam', 'Tamil', 'no', 'no'],
                                 [
                                  'Telugu', 'tel', 'tel', 'Telugu', 'no', 'no'],
                                 [
                                  'Marathi', 'mar', 'mar', 'Marathi', 'no', 'no'],
                                 [
                                  'Kannada (India)', 'kan', 'kan', 'Kanaresisch (Indien)', 'no', 'no'],
                                 [
                                  'Gujarati', 'guj', 'guj', 'Gujarati', 'no', 'no'],
                                 [
                                  'Malayalam', 'mal', 'mal', 'Malayalam', 'no', 'no'],
                                 [
                                  'Sinhala', 'sin', 'sin', 'Singhalesisch', 'no', 'no'],
                                 [
                                  'Assamese', 'asm', 'asm', 'Assamesisch', 'no', 'no'],
                                 [
                                  'Manipuri', 'mni', 'mni', 'Manipuri', 'no', 'no'],
                                 [
                                  'Tagalog', 'tgl', 'tgl', 'Tagalog', 'no', 'no'],
                                 [
                                  'Indonesian', 'ind', 'ind', 'Indonesisch', 'no', 'no'],
                                 [
                                  'Malay', 'msa', 'may', 'Malaiisch', 'no', 'no'],
                                 [
                                  'Filipino', 'fil', 'fil', 'Filipino', 'no', 'no'],
                                 [
                                  'Vietnamese', 'vie', 'vie', 'Vietnamesisch', 'no', 'no'],
                                 [
                                  'Thai', 'tha', 'tha', 'Thailändisch', 'no', 'no'],
                                 [
                                  'Khmer', 'khm', 'khm', 'Khmer', 'no', 'no'],
                                 [
                                  'Korean', 'kor', 'kor', 'Koreanisch', 'no', 'no'],
                                 [
                                  'Mandarin', 'None', 'chi', 'Mandarin', 'no', 'no'],
                                 [
                                  'Cantonese', 'None', 'chi', 'Kantonesisch', 'no', 'no'],
                                 [
                                  'Simplified Chinese', 'zhoS', 'chi', 'Chinesisch (Vereinfacht)', 'no', 'no'],
                                 [
                                  'Traditional Chinese', 'zhoT', 'chi', 'Chinesisch (Traditionell)', 'no', 'no'],
                                 [
                                  'Japanese', 'jpn', 'jpn', 'Japanisch', 'no', 'no'],
                                 [
                                  'Klingon', 'tlh', 'tlh', 'Klingonisch', 'no', 'no'],
                                 [
                                  'No Dialogue', 'zxx', 'zxx', 'Kein Dialog', 'no', 'no']]
                    ALLAUDIOS = []
                    for audio_language, subs_language, language_id, language_name, audio_default, subs_default in LanguageList:
                        for AudioExtension in AudioExtensionsList:
                            if os.path.isfile('.\\' + self.CurrentName + ' (' + audio_language + ')' + AudioExtension):
                                ALLAUDIOS = ALLAUDIOS + ['--language', '0:' + language_id,
                                 '--track-name', '0:' + language_name,
                                 '--default-track', '0:' + audio_default,
                                 '(',
                                 '.\\' + self.CurrentName + ' (' + audio_language + ')' + AudioExtension, ')']
                                audio_default = False

                    for audio_language, subs_language, language_id, language_name, audio_default, subs_default in LanguageList:
                        for AudioExtension in AudioExtensionsList:
                            if os.path.isfile('.\\' + self.CurrentName + ' (' + audio_language + '_descriptive)' + AudioExtension):
                                ALLAUDIOS = ALLAUDIOS + ['--language', '0:' + language_id,
                                 '--track-name',
                                 '0:' + language_name + ' (Audio Description)', '--default-track',
                                 '0:no', '(',
                                 '.\\' + self.CurrentName + ' (' + audio_language + '_descriptive)' + AudioExtension, ')']
                                audio_default = False

                    OnlyOneLanguage = False
                    if len(ALLAUDIOS) == 9:
                        OnlyOneLanguage = True
                if len(ALLAUDIOS) == 18:
                    if ALLAUDIOS[1] == ALLAUDIOS[10]:
                        if '_descriptive' in ALLAUDIOS[7] or '_descriptive' in ALLAUDIOS[16]:
                            OnlyOneLanguage = True
                        else:
                            OnlyOneLanguage = False
                ALLSUBS = []
                for audio_language, subs_language, language_id, language_name, audio_default, subs_default in LanguageList:
                    for SubsExtension in SubsExtensionsList:
                        if os.path.isfile('.\\' + self.CurrentName + ' (' + subs_language + ') Forced' + SubsExtension):
                            ALLSUBS = ALLSUBS + ['--language', '0:' + language_id,
                             '--track-name',
                             '0:' + language_name + ' ' + subs_forced, '--forced-track', '0:yes',
                             '--default-track', '0:' + subs_default,
                             '--compression', '0:none', '(',
                             '.\\' + self.CurrentName + ' (' + subs_language + ') Forced' + SubsExtension, ')']
                            subs_default = 'no'
                            if OnlyOneLanguage == True:
                                subs_default = 'no'
                            if os.path.isfile('.\\' + self.CurrentName + ' (' + subs_language + ')' + SubsExtension):
                                ALLSUBS = ALLSUBS + ['--language', '0:' + language_id,
                                 '--track-name',
                                 '0:' + language_name + ' ' + subs_full, '--forced-track', '0:no',
                                 '--default-track', '0:' + subs_default,
                                 '--compression', '0:none', '(',
                                 '.\\' + self.CurrentName + ' (' + subs_language + ')' + SubsExtension, ')']
                            else:
                                if os.path.isfile('.\\' + self.CurrentName + ' (' + subs_language + ')' + SubsExtension):
                                    ALLSUBS = ALLSUBS + ['--language', '0:' + language_id,
                                     '--track-name', '0:' + language_name + ' ' + subs_full,
                                     '--forced-track', '0:no',
                                     '--default-track', '0:no',
                                     '--compression', '0:none',
                                     '(',
                                     '.\\' + self.CurrentName + ' (' + subs_language + ')' + SubsExtension, ')']
                            if os.path.isfile('.\\' + self.CurrentName + ' (' + subs_language + '-sdh)' + SubsExtension):
                                ALLSUBS = ALLSUBS + ['--language', '0:' + language_id, '--track-name',
                                 '0:' + language_name + ' ' + subs_sdh, '--forced-track', '0:no',
                                 '--default-track', '0:no', '--compression', '0:none',
                                 '(',
                                 '.\\' + self.CurrentName + ' (' + subs_language + '-sdh)' + SubsExtension, ')']

                if os.path.isfile('.\\' + self.CurrentName + ' Chapters.txt'):
                    CHAPTERS = ['--chapter-charset', 'UTF-8', '--chapters', '.\\' + self.CurrentName + ' Chapters.txt']
                else:
                    CHAPTERS = []
            mkvmerge_command_video = [
             self.mkvmergeexe,
             '-q',
             '--output',
             VideoOutputName,
             '--language',
             '0:und',
             '--default-track',
             '0:yes',
             '(',
             VideoInputName,
             ')']
            mkvmerge_command = mkvmerge_command_video + ALLAUDIOS + ALLSUBS + CHAPTERS
            mkvmerge_process = subprocess.Popen(mkvmerge_command)
            stdoutdata, stderrdata = mkvmerge_process.communicate()
            mkvmerge_process.wait()