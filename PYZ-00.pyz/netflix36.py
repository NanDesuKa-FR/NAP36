# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\netflix36.py
import hashlib
from titlecase import titlecase
import html, http.cookiejar, binascii, configparser, inspect, urllib.request, urllib.parse, urllib.error, argparse, base64, glob, gzip, json, os, pprint, pycountry, random, string, re, requests, sys, time, xml.etree.ElementTree as ET, zlib
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import HMAC, SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util import Padding
from io import StringIO
from datetime import datetime
from subprocess import call
import subprocess, ffmpy
from io import BytesIO
import subprocess as sp
from collections import defaultdict
from binaries.kanji_to_romaji.kanji_to_romaji_module import convert_hiragana_to_katakana, translate_to_romaji, translate_soukon, translate_long_vowel, translate_soukon_ch, kanji_to_romaji
from pywidevine.clientsconfig.netflix import NetflixConfig
from pywidevine.decrypt.wvdecryptcustom import WvDecrypt
from pywidevine.muxer.muxer import Muxer
from nap36 import args
currentFile = 'netflix36'
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
msl_data_path = dirPath + '/cookies/'
TimeStretch_dll = dirPath + '/binaries/BeHappy/plugins32/TimeStretch.dll'
lsmashsource_dll = dirPath + '/binaries/BeHappy/plugins32/LSMASHSource.dll'
netflix_nuevo = dirPath + '/netflix_nuevo.py'
SubtitleEditexe = dirPath + '/binaries/SubtitleEdit.exe'
mp4decryptexe = dirPath + '/binaries/mp4decrypt.exe'
mp4dumptexe = dirPath + '/binaries/mp4dump.exe'
ffmpegpath = dirPath + '/binaries/ffmpeg.exe'
ffprobepath = dirPath + '/binaries/ffprobe.exe'
python36 = dirPath + '/binaries/python36.exe'
mkvmergeexe = dirPath + '/binaries/mkvmerge.exe'
aria2cexe = dirPath + '/binaries/aria2c.exe'
wvDecrypterexe = dirPath + '/binaries/wvDecrypter/wvDecrypter.exe'
challengeBIN = dirPath + '/binaries/wvDecrypter/challenge.bin'
licenceBIN = dirPath + '/binaries/wvDecrypter/licence.bin'
cookies_nf = dirPath + '/cookies/cookies_nf.txt'
cert_nf = dirPath + '/binaries'

def Ay_Clean_Videolist(vlist, ipv):
    todel = []
    res = None
    for i, dic in enumerate(vlist):
        le_str = dic['Url']
        if ipv == 6:
            res = re.search('https:\\/\\/ipv4', le_str)
        else:
            if ipv == 4:
                res = re.search('https:\\/\\/ipv6', le_str)
        if res:
            todel.append(i)

    todel.sort(reverse=True)
    for j in todel:
        del vlist[j]

    return vlist


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as (f):
        for chunk in iter(lambda : f.read(65536), b''):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


hash_dec_exe = md5(wvDecrypterexe)
if __name__ == 'netflix36':
    from pywidevine.decrypt.netflix36_MSL_medium import MSL as netflix36_MSL_medium
    from pywidevine.decrypt.netflix36_MSL_high import MSL as netflix36_MSL_high
    from pywidevine.decrypt import netflix36_keys
    from pywidevine.decrypt import netflix36_nokeys
    from pywidevine.decrypt import netflix36_keys_high
    from pywidevine.decrypt import netflix36_keys_vp9
    from pywidevine.decrypt import netflix36_keys_hevc
    from pywidevine.decrypt import netflix36_keys_hdr

    def generate_esn(prefix):
        """
        generate_esn()
        @param prefix: Prefix of ESN to append generated device ID onto
        @return: ESN to use with MSL API
        """
        return prefix + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))


    username, password, esn_keys, esn_manifest, MANIFEST_ENDPOINT, LICENSE_ENDPOINT = NetflixConfig.configNetflix()
    account_info = {'email':username,  'password':password}
    if not os.path.exists(dirPath + '/KEYS'):
        os.makedirs(dirPath + '/KEYS')
    keys_file = dirPath + '/KEYS/KEYS_NETFLIX.txt'
    try:
        keys_file_netflix = open(keys_file, 'r')
    except Exception:
        with open(keys_file, 'a', encoding='utf8') as (file):
            file.write('##### Una KEY por linea. (One KEY for line.) #####\n')

    languageCodes = {'zh-Hans':'zhoS', 
     'zh-Hant':'zhoT', 
     'pt-BR':'brPor', 
     'es-ES':'euSpa', 
     'en-GB':'enGB', 
     'nl-BE':'nlBE'}
    if not os.path.exists(msl_data_path):
        os.makedirs(msl_data_path)
    if args.output:
        if not os.path.exists(args.output):
            os.makedirs(args.output)
    else:
        os.chdir(args.output)
        if ':' in str(args.output):
            folderdownloader = str(args.output).replace('/', '\\').replace('.\\', '\\')
        else:
            folderdownloader = dirPath + str(args.output).replace('/', '\\').replace('.\\', '\\')
else:
    folderdownloader = dirPath.replace('/', '\\').replace('.\\', '\\')

def ReplaceSubs1(X):
    pattern1 = re.compile('(?!<i>|<b>|<u>|<\\/i>|<\\/b>|<\\/u>)(<)(?:[A-Za-z0-9_ -=]*)(>)')
    pattern2 = re.compile('(?!<\\/i>|<\\/b>|<\\/u>)(<\\/)(?:[A-Za-z0-9_ -=]*)(>)')
    X = X.replace('&rlm;', '').replace('{\\an1}', '').replace('{\\an2}', '').replace('{\\an3}', '').replace('{\\an4}', '').replace('{\\an5}', '').replace('{\\an6}', '').replace('{\\an7}', '').replace('{\\an8}', '').replace('{\\an9}', '')
    X = pattern1.sub('', X)
    X = pattern2.sub('', X)
    return X


def ReplaceSubs2(X):
    pattern1 = re.compile('(?!<i>|<b>|<u>|<\\/i>|<\\/b>|<\\/u>)(<)(?:[A-Za-z0-9_ -=]*)(>)')
    pattern2 = re.compile('(?!<\\/i>|<\\/b>|<\\/u>)(<\\/)(?:[A-Za-z0-9_ -=]*)(>)')
    X = X.replace('&rlm;', '').replace('{\\an1}', '').replace('{\\an2}', '').replace('{\\an3}', '').replace('{\\an4}', '').replace('{\\an6}', '').replace('{\\an7}', '').replace('{\\an9}', '')
    X = pattern1.sub('', X)
    X = pattern2.sub('', X)
    return X


def ReplaceDontLikeWord(X):
    try:
        X = X.replace(' : ', ' - ').replace(': ', ' - ').replace(':', ' - ').replace('&', 'and').replace('+', '').replace(';', '').replace('ÃƒÂ³', 'o').replace('[', '').replace("'", '').replace(']', '').replace('/', '').replace('//', '').replace('’', "'").replace('*', 'x').replace('<', '').replace('>', '').replace('|', '').replace('~', '').replace('#', '').replace('%', '').replace('{', '').replace('}', '').replace(',', '').replace('?', '').encode('latin-1').decode('latin-1')
    except Exception:
        X = X.decode('utf-8').replace(' : ', ' - ').replace(': ', ' - ').replace(':', ' - ').replace('&', 'and').replace('+', '').replace(';', '').replace('ÃƒÂ³', 'o').replace('[', '').replace("'", '').replace(']', '').replace('/', '').replace('//', '').replace('’', "'").replace('*', 'x').replace('<', '').replace('>', '').replace(',', '').replace('|', '').replace('~', '').replace('#', '').replace('%', '').replace('{', '').replace('}', '').replace('?', '').encode('latin-1').decode('latin-1')

    return titlecase(X)


def find_str(s, char):
    return s.find(char)


def getKeyId(name):
    mp4dump = subprocess.Popen([mp4dumptexe, name], stdout=(subprocess.PIPE))
    mp4dump = str(mp4dump.stdout.read())
    A = find_str(mp4dump, 'default_KID')
    KID = mp4dump[A:A + 63].replace('default_KID = ', '').replace('[', '').replace(']', '').replace(' ', '')
    KID = KID.upper()
    KID = KID[0:8] + '-' + KID[8:12] + '-' + KID[12:16] + '-' + KID[16:20] + '-' + KID[20:32]
    if KID == '':
        KID = 'nothing'
    return KID


def getKeyId2(name):
    mp4dump = subprocess.Popen([mp4dumptexe, name], stdout=(subprocess.PIPE))
    mp4dump = str(mp4dump.stdout.read())
    A = find_str(mp4dump, 'default_KID')
    KID = mp4dump[A:A + 63].replace('default_KID = ', '').replace('[', '').replace(']', '').replace(' ', '')
    if KID == '':
        KID = 'nothing'
    return KID


def base64key_decode(payload):
    l = len(payload) % 4
    if l == 2:
        payload += '=='
    else:
        if l == 3:
            payload += '='
        else:
            if l != 0:
                raise ValueError('Invalid base64 string')
            return base64.urlsafe_b64decode(payload.encode('utf-8'))


def DecryptAudio(inputAudio, outputAudioTemp, outputAudio, IDNet, Name):
    key_id_original = getKeyId2(inputAudio)
    keys_audio = []
    if key_id_original != 'nothing':
        try:
            keys_audio = netflix36_keys.GettingKEYS_Netflix(IDNet)
        except Exception:
            keys_audio = []

        if keys_audio != []:
            keys_audio = list(set(keys_audio))
            print('Done!')
        else:
            print('Error!')
        keys_audio = keys_audio
        for key in keys_audio:
            key_id = key[0:32]
            key_key = key[33:]
            if key_id == key_id_original:
                print('\nDecrypting audio...')
                print('Using KEY: ' + key)
                with open(keys_file, 'a', encoding='utf8') as (file):
                    file.write(Name + '\n' + key + '\n')
                wvdecrypt_process = subprocess.Popen([
                 mp4decryptexe, '--show-progress', '--key', key, inputAudio, outputAudioTemp])
                stdoutdata, stderrdata = wvdecrypt_process.communicate()
                wvdecrypt_process.wait()
                print('\nDemuxing audio...')
                time.sleep(0.05)
                print('Done!')
                return True

    elif key_id_original == 'nothing':
        if netflixType == 'supplemental':
            print('\nDemuxing audio...')
            os.rename(inputAudio, outputAudioTemp)
            ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={outputAudioTemp: None}, outputs={outputAudio: '-c copy'},
              global_options='-y -hide_banner -loglevel warning')
            ff.run()
            time.sleep(0.05)
            os.remove(outputAudioTemp)
            print('Done!')
            return True
        if key_id_original == 'nothing':
            if netflixType != 'supplemental':
                return True
            if key_id_original not in keys_audio:
                print('KEY for ' + inputAudio + ' is not in txt.')
                return False


def DecryptAlternative(inputVideo, outputVideo, outputVideoTemp, IDNet, Type, Profile):
    key_id_original = getKeyId(inputVideo)
    Correct = False
    if key_id_original != 'nothing':
        Correct = netflix36_nokeys.DecryptAlternative_Netflix(nfID=IDNet, KID=key_id_original, FInput=inputVideo, FOutput=outputVideo,
          Type=Type,
          Profile=Profile)
        if Correct == True:
            if os.path.isfile(outputVideo):
                os.remove(inputVideo)
        return Correct
    if key_id_original == 'nothing':
        if netflixType == 'supplemental':
            print('\nRemuxing video...')
            os.rename(inputVideo, outputVideoTemp)
            ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={outputVideoTemp: None}, outputs={inputVideo: '-c copy'},
              global_options='-y -hide_banner -loglevel warning')
            ff.run()
            time.sleep(0.05)
            os.remove(outputVideoTemp)
            print('Done!')
            return True
        if key_id_original == 'nothing':
            if netflixType != 'supplemental':
                return True


def DecryptVideo(inputVideo, outputVideoTemp, outputVideo, IDNet, Name):
    key_id_original = getKeyId(inputVideo)
    keys_video = []
    if key_id_original != 'nothing':
        try:
            try:
                keys_video_main = netflix36_keys.GettingKEYS_Netflix(nfID_current)
            except Exception:
                keys_video_main = []

            if keys_video_main != []:
                keys_video_main = list(set(keys_video_main))
                keys_video_main = ['Main KEYS'] + keys_video_main
                print('Done!')
            else:
                print('Error!')
            try:
                keys_video_vp9 = netflix36_keys_vp9.GettingKEYS_Netflix(nfID_current)
            except Exception:
                keys_video_vp9 = []

            if keys_video_vp9 == []:
                print('Error!')
            else:
                keys_video_vp9 = list(set(keys_video_vp9))
                keys_video_vp9 = ['VP9 KEYS'] + keys_video_vp9
                print('Done!')
            try:
                keys_video_high = netflix36_keys_high.GettingKEYS_Netflix(nfID_current)
            except Exception:
                keys_video_high = []

            if keys_video_high == []:
                print('Error!')
            else:
                keys_video_high = list(set(keys_video_high))
                keys_video_high = ['High KEYS'] + keys_video_high
                print('Done!')
            try:
                keys_video_hevc = netflix36_keys_hevc.GettingKEYS_Netflix(nfID_current)
            except Exception:
                keys_video_hevc = []

            if keys_video_hevc == []:
                print('Error!')
            else:
                keys_video_hevc = list(set(keys_video_hevc))
                keys_video_hevc = ['HEVC and HDR-10 KEYS'] + keys_video_hevc
                print('Done!')
            try:
                keys_video_hdr = netflix36_keys_hdr.GettingKEYS_Netflix(nfID_current)
            except Exception:
                keys_video_hdr = []

            if keys_video_hdr == []:
                print('Error!')
            else:
                keys_video_hdr = list(set(keys_video_hdr))
                keys_video_hdr = ['HDR-DV KEYS'] + keys_video_hdr
                print('Done!')
            keys_video = keys_video_main + keys_video_vp9 + keys_video_high + keys_video_hevc + keys_video_hdr
        except Exception:
            keys_file_netflix = open(keys_file, 'r')
            keys_file_txt = keys_file_netflix.readlines()
            keys_video = keys_file_txt
            print('Done!')

        if keys_video == []:
            keys_file_netflix = open(keys_file, 'r')
            keys_file_txt = keys_file_netflix.readlines()
            keys_video = keys_file_txt
            print('Done!')
        for key in keys_video:
            key_id = key[0:32]
            key_key = key[33:]
            if key_id == key_id_original:
                print('\nDecrypting video...')
                print('Using KEY: ' + key)
                with open(keys_file, 'a', encoding='utf8') as (file):
                    file.write(Name + '\n' + key + '\n')
                wvdecrypt_process = subprocess.Popen([
                 mp4decryptexe, '--show-progress', '--key', key, inputVideo, outputVideoTemp])
                stdoutdata, stderrdata = wvdecrypt_process.communicate()
                wvdecrypt_process.wait()
                print('\nRemuxing video...')
                ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={outputVideoTemp: None}, outputs={outputVideo: '-c copy'},
                  global_options='-y -hide_banner -loglevel warning')
                ff.run()
                time.sleep(0.05)
                os.remove(outputVideoTemp)
                print('Done!')
                return True

    elif key_id_original == 'nothing':
        if netflixType == 'supplemental':
            print('\nRemuxing video...')
            os.rename(inputVideo, outputVideoTemp)
            ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={outputVideoTemp: None}, outputs={outputVideo: '-c copy'},
              global_options='-y -hide_banner -loglevel warning')
            ff.run()
            time.sleep(0.05)
            os.remove(outputVideoTemp)
            print('Done!')
            return True
        if key_id_original == 'nothing':
            if netflixType != 'supplemental':
                return True
            if key_id_original not in keys_video:
                print('KEY for ' + inputVideo + ' is not in txt.')
                return False


def downloadFile(link, file_name):
    print('\n' + file_name)
    aria_command = [aria2cexe, link,
     '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"',
     '--async-dns=false',
     '--enable-color=false',
     '--allow-overwrite=true',
     '--auto-file-renaming=false',
     '--file-allocation=none',
     '--summary-interval=0',
     '--retry-wait=5',
     '--uri-selector=inorder',
     '--console-log-level=warn',
     '-x16', '-j16', '-s16',
     '-o', file_name]
    if sys.version_info >= (3, 5):
        aria_out = subprocess.run(aria_command)
        aria_out.check_returncode
    else:
        aria_out = subprocess.call(aria_command)
    if aria_out != 0:
        raise ValueError('aria failed with exit code {}'.format(aria_out))


def downloadFile2(link, file_name):
    with open(file_name, 'wb') as (f):
        print('Downloading %s' % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write('\r[%s%s]' % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()


def downloadNetflix(nfID_current, seriesName):
    global CurrentName
    global SeasonFolder
    if not args.novideo:
        print('\nDownloading video...')
        if args.hevc:
            inputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HEVC].mp4'
            inputVideo_demuxed = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HEVC].h265'
        else:
            if args.hdr:
                inputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HDR].mp4'
                inputVideo_demuxed = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HDR].h265'
            else:
                if args.video_vp9:
                    inputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [VP9].mp4'
                    inputVideo_demuxed = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [VP9].vp9'
                else:
                    if 'playready-h264hpl' in str(dict(videoList[(-1)])['Profile']) or 'playready-h264shpl' in str(dict(videoList[(-1)])['Profile']):
                        inputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [AVC HIGH].mp4'
                        inputVideo_demuxed = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [AVC HIGH].h264'
                    else:
                        inputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p].mp4'
                        inputVideo_demuxed = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p].h264'
                if os.path.isfile(inputVideo) and not os.path.isfile(inputVideo + '.aria2') or os.path.isfile(inputVideo_demuxed):
                    print('\n' + inputVideo + '\nFile has already been successfully downloaded previously.')
                    CorrectDecryptVideo = True
                else:
                    downloadFile(str(dict(videoList[(-1)])['Url']), inputVideo)
        if not args.noaudio:
            print('\nDownloading audios...')
            for a in audioList:
                lang = dict(a)['Language']
                try:
                    langAbbrev = str(dict(a)['langAbbrev'])
                except KeyError:
                    langAbbrev = lang

                inputAudio = seriesName + ' ' + langAbbrev + '-audio.mp4'
                inputAudio2 = seriesName + ' ' + langAbbrev + '.ac3'
                inputAudio3 = seriesName + ' ' + langAbbrev + '.eac3'
                inputAudio4 = seriesName + ' ' + langAbbrev + '.m4a'
                inputAudio5 = seriesName + ' ' + langAbbrev + '.oga'
                if os.path.isfile(inputAudio) and not os.path.isfile(inputAudio + '.aria2') or os.path.isfile(inputAudio2) or os.path.isfile(inputAudio3) or os.path.isfile(inputAudio4) or os.path.isfile(inputAudio5):
                    print('\n' + inputAudio + '\nFile has already been successfully downloaded previously.')
                else:
                    downloadFile(str(dict(a)['Url']), inputAudio)

        if not args.nosubs:
            downloadingsubs = False
            print('\nDownloading subtitles...')
            for z in subtitleList:
                lang = dict(z)['Language']
                try:
                    langAbbrev = str(dict(z)['langAbbrev'])
                except KeyError:
                    langAbbrev = lang

                if z['Language'] == 'Off':
                    langAbbrev = 'forced-' + langAbbrev
                if z['Type'] == 'CLOSEDCAPTIONS':
                    langAbbrev = 'sdh-' + langAbbrev
                if os.path.isfile(seriesName + ' ' + langAbbrev + '.srt') or os.path.isfile(seriesName + ' ' + langAbbrev + '.dfxp'):
                    downloadingsubs = False
                    continue
                else:
                    downloadFile2(str(dict(z)['Url']), seriesName + ' ' + langAbbrev + '.dfxp')
                    downloadingsubs = True
                    print('Downloaded!')

            if downloadingsubs == False:
                print('File has already been successfully downloaded previously.')
        if not args.novideo:
            if args.hevc:
                inputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HEVC].mp4'
                outputVideoTemp = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HEVC]_DecryptTemp.mp4'
                outputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HEVC].mp4'
                outputVideo2 = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HEVC].h265'
            else:
                if args.hdr:
                    inputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HDR].mp4'
                    outputVideoTemp = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HDR]_DecryptTemp.mp4'
                    outputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HDR].mp4'
                    outputVideo2 = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [HDR].h265'
                else:
                    if args.video_vp9:
                        inputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [VP9].mp4'
                        outputVideoTemp = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [VP9]_DecryptTemp.mp4'
                        outputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [VP9].mp4'
                        outputVideo2 = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [VP9].vp9'
                    else:
                        if 'playready-h264hpl' in str(dict(videoList[(-1)])['Profile']) or 'playready-h264shpl' in str(dict(videoList[(-1)])['Profile']):
                            inputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [AVC HIGH].mp4'
                            outputVideoTemp = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [AVC HIGH]_DecryptTemp.mp4'
                            outputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [AVC HIGH].mp4'
                            outputVideo2 = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p] [AVC HIGH].h264'
                        else:
                            inputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p].mp4'
                            outputVideoTemp = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p]_DecryptTemp.mp4'
                            outputVideo = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p].mp4'
                            outputVideo2 = seriesName + ' [' + str(dict(videoList[(-1)])['Height']) + 'p].h264'
                        IDNet = nfID_current
                        CorrectDecryptVideo = False
                    if os.path.isfile(inputVideo):
                        CorrectDecryptVideo = DecryptAlternative(inputVideo, outputVideo2, outputVideoTemp, IDNet=IDNet,
                          Type='video',
                          Profile=(str(dict(videoList[(-1)])['Profile'])))
                    else:
                        if not os.path.isfile(inputVideo):
                            if os.path.isfile(outputVideo2):
                                CorrectDecryptVideo = True
        if not args.noaudio:
            for a in audioList:
                lang = dict(a)['Language']
                try:
                    langAbbrev = str(dict(a)['langAbbrev'])
                except KeyError:
                    langAbbrev = lang

                inputAudio = seriesName + ' ' + langAbbrev + '-audio.mp4'
                if os.path.isfile(inputAudio):
                    print('\nDemuxing audio...')
                    if dict(a)['Profile'] == 'ddplus-2.0-dash' or dict(a)['Profile'] == 'ddplus-atmos-dash' or dict(a)['Profile'] == 'ddplus-5.1hq-dash':
                        print(seriesName + ' ' + langAbbrev + '-audio.mp4 -> ' + seriesName + ' ' + langAbbrev + '.eac3')
                        ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={seriesName + ' ' + langAbbrev + '-audio.mp4': None},
                          outputs={seriesName + ' ' + langAbbrev + '.eac3': '-c copy'},
                          global_options='-y -hide_banner -loglevel warning')
                        ff.run()
                        time.sleep(0.05)
                        os.remove(seriesName + ' ' + langAbbrev + '-audio.mp4')
                    else:
                        if dict(a)['Profile'] == 'dd-5.1-dash':
                            print(seriesName + ' ' + langAbbrev + '-audio.mp4 -> ' + seriesName + ' ' + langAbbrev + '.ac3')
                            ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={seriesName + ' ' + langAbbrev + '-audio.mp4': None},
                              outputs={seriesName + ' ' + langAbbrev + '.ac3': '-c copy'},
                              global_options='-y -hide_banner -loglevel warning')
                            ff.run()
                            time.sleep(0.05)
                            os.remove(seriesName + ' ' + langAbbrev + '-audio.mp4')
                        else:
                            if dict(a)['Profile'] == 'heaac-2-dash':
                                print(seriesName + ' ' + langAbbrev + '-audio.mp4 -> ' + seriesName + ' ' + langAbbrev + '.m4a')
                                ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={seriesName + ' ' + langAbbrev + '-audio.mp4': None},
                                  outputs={seriesName + ' ' + langAbbrev + '.m4a': '-c copy'},
                                  global_options='-y -hide_banner -loglevel warning')
                                ff.run()
                                time.sleep(0.05)
                                os.remove(seriesName + ' ' + langAbbrev + '-audio.mp4')
                            else:
                                if dict(a)['Profile'] == 'playready-oggvorbis-2-dash':
                                    inputAudio = seriesName + ' ' + langAbbrev + '-audio.mp4'
                                    outputAudioTemp = seriesName + ' ' + langAbbrev + '-audio_DecryptTemp.mp4'
                                    outputAudio = seriesName + ' ' + langAbbrev + '.oga'
                                    IDNet = nfID_current
                                    CorrectDecryptAudio = False
                                    CorrectDecryptAudio = DecryptAudio(inputAudio=inputAudio, outputAudioTemp=outputAudioTemp,
                                      outputAudio=outputAudio,
                                      IDNet=IDNet,
                                      Name=seriesName)
                    print('Done!')

    elif not args.nosubs:
        subsinfolder = False
        for z in subtitleList:
            lang = dict(z)['Language']
            try:
                langAbbrev = str(dict(z)['langAbbrev'])
            except KeyError:
                langAbbrev = lang

            if z['Language'] == 'Off':
                langAbbrev = 'forced-' + langAbbrev
            if z['Type'] == 'CLOSEDCAPTIONS':
                langAbbrev = 'sdh-' + langAbbrev
            if os.path.isfile(seriesName + ' ' + langAbbrev + '.dfxp'):
                subsinfolder = True

        if subsinfolder == True:
            print('\nConverting subtitles...')
            SubtitleEdit_process = subprocess.Popen([
             SubtitleEditexe, '/convert', seriesName + '*.dfxp', 'srt'])
            stdoutdata, stderrdata = SubtitleEdit_process.communicate()
            SubtitleEdit_process.wait()
            for f in glob.glob(seriesName + '*.srt'):
                with open(f, 'r+', encoding='utf-8') as (x):
                    old = x.read()
                with open(f, 'w+', encoding='utf-8') as (x):
                    if not args.nocleansubs:
                        x.write(ReplaceSubs1(old))
                    else:
                        x.write(ReplaceSubs2(old))

            for f in glob.glob(seriesName + '*.dfxp'):
                os.remove(f)

            print('Done!')
    elif not args.noaudio:
        if args.fpitch:
            CurrentName = seriesName
            if args.sourcefps:
                sourcefps = float(args.sourcefps[0])
            else:
                sourcefps = float(23.976)
            if args.targetfps:
                targetfps = float(args.targetfps[0])
            else:
                targetfps = float(25)
            pitch = float(targetfps * 100 / sourcefps)
            pitch = round(pitch, 4)
            for a in audioList:
                lang = dict(a)['Language']
                try:
                    langAbbrev = str(dict(a)['langAbbrev'])
                except KeyError:
                    langAbbrev = lang

                if str(langAbbrev) in list(args.fpitch):
                    inputAudio1 = CurrentName + ' ' + langAbbrev + '.eac3'
                    outputAudio1 = CurrentName + ' ' + langAbbrev + '.eac3'
                    originalAudio1 = CurrentName + ' ' + langAbbrev + '_original.eac3'
                    originalAudio_index1 = CurrentName + ' ' + langAbbrev + '_original.eac3.lwi'
                    avsfile1 = originalAudio1 + '.avs'
                    inputAudio2 = CurrentName + ' ' + langAbbrev + '.ac3'
                    outputAudio2 = CurrentName + ' ' + langAbbrev + '.ac3'
                    originalAudio2 = CurrentName + ' ' + langAbbrev + '_original.ac3'
                    originalAudio_index2 = CurrentName + ' ' + langAbbrev + '_original.ac3.lwi'
                    avsfile2 = originalAudio2 + '.avs'
                    inputAudio3 = CurrentName + ' ' + langAbbrev + '.m4a'
                    outputAudio3 = CurrentName + ' ' + langAbbrev + '.m4a'
                    originalAudio3 = CurrentName + ' ' + langAbbrev + '_original.m4a'
                    originalAudio_index3 = CurrentName + ' ' + langAbbrev + '_original.m4a.lwi'
                    avsfile3 = originalAudio3 + '.avs'
                    if dict(a)['Profile'] == 'ddplus-2.0-dash' or dict(a)['Profile'] == 'ddplus-atmos-dash' or dict(a)['Profile'] == 'ddplus-5.1hq-dash':
                        if os.path.isfile(inputAudio1):
                            if not os.path.isfile(originalAudio1):
                                os.rename(inputAudio1, originalAudio1)
                                if not os.path.isfile(avsfile1):
                                    with open(avsfile1, 'w+', encoding='utf-8') as (f):
                                        f.write('LoadPlugin("' + TimeStretch_dll + '")' + '\n')
                                        f.write('LoadPlugin("' + lsmashsource_dll + '")' + '\n')
                                        f.write('TimeStretchPlugin(LWLibavAudioSource("' + originalAudio1 + '"), pitch=' + str(pitch) + ')')
                            os.path.isfile(originalAudio1) and os.path.isfile(outputAudio1) or print('\nFixing pitch of ' + langAbbrev + '...')
                            print(str(sourcefps) + ' -> ' + str(targetfps))
                            mediainfo = subprocess.Popen([
                             ffprobepath, '-v', 'quiet', '-print_format', 'json', '-show_format',
                             '-show_streams', originalAudio1],
                              stdout=(subprocess.PIPE))
                            mediainfo = json.load(mediainfo.stdout)
                            audio_bitrate = int(float(mediainfo['streams'][0]['bit_rate']) / 1000)
                            ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={avsfile1: None}, outputs={outputAudio1: '-c:a eac3 -b:a ' + str(audio_bitrate) + 'k -room_type -1 -copyright 1 -original 1 -mixing_level -1 -dialnorm -31'},
                              global_options='-y -hide_banner -loglevel warning')
                            ff.run()
                            print('Done!')
                        elif dict(a)['Profile'] == 'dd-5.1-dash':
                            if os.path.isfile(inputAudio2):
                                if not os.path.isfile(originalAudio2):
                                    os.rename(inputAudio2, originalAudio2)
                                    if not os.path.isfile(avsfile2):
                                        with open(avsfile2, 'w+', encoding='utf-8') as (f):
                                            f.write('LoadPlugin("' + TimeStretch_dll + '")' + '\n')
                                            f.write('LoadPlugin("' + lsmashsource_dll + '")' + '\n')
                                            f.write('TimeStretchPlugin(LWLibavAudioSource("' + originalAudio2 + '"), pitch=' + str(pitch) + ')')
                    os.path.isfile(originalAudio2) and os.path.isfile(outputAudio2) or print('\nFixing pitch of ' + langAbbrev + '...')
                    print(str(sourcefps) + ' -> ' + str(targetfps))
                    mediainfo = subprocess.Popen([
                     ffprobepath, '-v', 'quiet', '-print_format', 'json', '-show_format',
                     '-show_streams', originalAudio2],
                      stdout=(subprocess.PIPE))
                    mediainfo = json.load(mediainfo.stdout)
                    audio_bitrate = int(float(mediainfo['streams'][0]['bit_rate']) / 1000)
                    ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={avsfile2: None}, outputs={outputAudio2: '-c:a ac3 -b:a ' + str(audio_bitrate) + 'k -room_type -1 -copyright 1 -original 1 -mixing_level -1 -dialnorm -31'},
                      global_options='-y -hide_banner -loglevel warning')
                    ff.run()
                    print('Done!')
                else:
                    if dict(a)['Profile'] == 'heaac-2-dash':
                        if os.path.isfile(inputAudio3):
                            if not os.path.isfile(originalAudio3):
                                os.rename(inputAudio3, originalAudio3)
                                if not os.path.isfile(avsfile3):
                                    with open(avsfile3, 'w+', encoding='utf-8') as (f):
                                        f.write('LoadPlugin("' + TimeStretch_dll + '")' + '\n')
                                        f.write('LoadPlugin("' + lsmashsource_dll + '")' + '\n')
                                        f.write('TimeStretchPlugin(LWLibavAudioSource("' + originalAudio3 + '"), pitch=' + str(pitch) + ')')
                        if not (os.path.isfile(originalAudio3) and os.path.isfile(outputAudio3)):
                            print('\nFixing pitch of ' + langAbbrev + '...')
                            print(str(sourcefps) + ' -> ' + str(targetfps))
                            mediainfo = subprocess.Popen([
                             ffprobepath, '-v', 'quiet', '-print_format', 'json', '-show_format',
                             '-show_streams', originalAudio2],
                              stdout=(subprocess.PIPE))
                            mediainfo = json.load(mediainfo.stdout)
                            audio_bitrate = int(float(mediainfo['streams'][0]['bit_rate']) / 1000)
                            ff = ffmpy.FFmpeg(executable=ffmpegpath, inputs={avsfile3: None}, outputs={outputAudio3: '-c:a aac -f mp4 -b:a ' + str(audio_bitrate) + 'k'},
                              global_options='-y -hide_banner -loglevel warning')
                            ff.run()
                            print('Done!')

    else:
        if not args.novideo:
            if not args.noaudio:
                if not args.nomux:
                    if CorrectDecryptVideo == True:
                        print('\nMuxing...')
                        CurrentHeigh = str(dict(videoList[(-1)])['Height'])
                        CurrentName = seriesName
                        if netflixType == 'show':
                            MKV_Muxer = Muxer(CurrentName=CurrentName, SeasonFolder=SeasonFolder, CurrentHeigh=CurrentHeigh,
                              Type=netflixType,
                              mkvmergeexe=mkvmergeexe)
                        else:
                            MKV_Muxer = Muxer(CurrentName=CurrentName, SeasonFolder=None, CurrentHeigh=CurrentHeigh,
                              Type=netflixType,
                              mkvmergeexe=mkvmergeexe)
                        if args.langtag:
                            MKV_Muxer.NetflixMuxer(lang=(str(args.langtag[0])))
                        else:
                            MKV_Muxer.NetflixMuxer(lang='English')
                        if args.keep:
                            pass
                        else:
                            os.system('if exist "' + CurrentName + '*.mp4" (del /q /f "' + CurrentName + '*.mp4")')
                            os.system('if exist "' + CurrentName + '*.h265" (del /q /f "' + CurrentName + '*.h265")')
                            os.system('if exist "' + CurrentName + '*.h264" (del /q /f "' + CurrentName + '*.h264")')
                            os.system('if exist "' + CurrentName + '*.eac3" (del /q /f "' + CurrentName + '*.eac3")')
                            os.system('if exist "' + CurrentName + '*.m4a" (del /q /f "' + CurrentName + '*.m4a")')
                            os.system('if exist "' + CurrentName + '*.oga" (del /q /f "' + CurrentName + '*.oga")')
                            os.system('if exist "' + CurrentName + '*.ac3" (del /q /f "' + CurrentName + '*.ac3")')
                            os.system('if exist "' + CurrentName + '*.srt" (del /q /f "' + CurrentName + '*.srt")')
                            os.system('if exist "' + CurrentName + '*.txt" (del /q /f "' + CurrentName + '*.txt")')
                            os.system('if exist "' + CurrentName + '*.avs" (del /q /f "' + CurrentName + '*.avs")')
                            os.system('if exist "' + CurrentName + '*.lwi" (del /q /f "' + CurrentName + '*.lwi")')
                        print('Done!')


BUILD = ''
SESSION = requests.Session()

def alphanumericSort(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def login(username, password):
    """Logs into netflix"""
    r = SESSION.get('https://www.netflix.com/login', stream=True, allow_redirects=False, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'})
    loc = None
    while 'Location' in r.headers:
        loc = r.headers['Location']
        r = SESSION.get(loc, stream=True, allow_redirects=False, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'})

    x = re.search('name="authURL" value="([^"]+)"', r.text)
    if not x:
        return
    else:
        authURL = x.group(1)
        post_data = {'userLoginId':username,  'password':password, 
         'rememberMe':'true', 
         'mode':'login', 
         'flow':'websiteSignUp', 
         'action':'loginAction', 
         'authURL':authURL, 
         'withFields':'userLoginId,password,rememberMe,nextPage,showPassword', 
         'nextPage':'', 
         'showPassword':''}
        req = SESSION.post(loc, post_data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'})
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            logger.error(e)
            sys.exit(1)

        match = re.search('"BUILD_IDENTIFIER":"([a-z0-9]+)"', req.text)
        if match is not None:
            return match.group(1)
        return


def fetch_metadata(movieid, cookies):
    global BUILD
    if BUILD == '':
        BUILD = login(username, password)
    else:
        if cookies == 'off':
            req = SESSION.get('https://www.netflix.com/api/shakti/' + BUILD + '/metadata?movieid=' + movieid + '&drmSystem=widevine&isWatchlistEnabled=false&isShortformEnabled=false&isVolatileBillboardsEnabled=false&languages=en')
        else:
            req = requests.get(('https://www.netflix.com/api/shakti/' + BUILD + '/metadata?movieid=' + movieid + '&drmSystem=widevine&isWatchlistEnabled=false&isShortformEnabled=false&isVolatileBillboardsEnabled=false&languages=en'),
              cookies=cookies)
    if req.text.strip() == '':
        if os.path.isfile(cookies_nf):
            os.remove(cookies_nf)
        return 'ERROR'
    else:
        if cookies == 'off':
            if os.path.isfile(cookies_nf):
                os.remove(cookies_nf)
            with open(cookies_nf, 'w', encoding='utf8') as (file):
                file.write(str(dict(SESSION.cookies)))
        return json.loads(req.text)


def DownloadAll(nfID_current, seriesName_current, SeasonFolder_current):
    global CurrentHeigh
    global HDR
    global SeasonFolder
    global UHD
    global audioList
    global folderdownloader
    global forced
    global seriesName
    global subtitleChi
    global subtitleDFXP
    global subtitleList
    global videoList
    global videoList_high
    global videoList_medium
    seriesName = seriesName_current
    SeasonFolder = SeasonFolder_current
    if args.onlykeys:
        try:
            keys_video_main = netflix36_keys.GettingKEYS_Netflix(nfID_current)
        except Exception:
            keys_video_main = []

        if keys_video_main != []:
            keys_video_main = list(set(keys_video_main))
            keys_video_main = ['Main KEYS'] + keys_video_main
            print('Done!')
        else:
            print('Error!')
        try:
            keys_video_vp9 = netflix36_keys_vp9.GettingKEYS_Netflix(nfID_current)
        except Exception:
            keys_video_vp9 = []

        if keys_video_vp9 == []:
            print('Error!')
        else:
            keys_video_vp9 = list(set(keys_video_vp9))
            keys_video_vp9 = ['VP9 KEYS'] + keys_video_vp9
            print('Done!')
        try:
            keys_video_high = netflix36_keys_high.GettingKEYS_Netflix(nfID_current)
        except Exception:
            keys_video_high = []

        if keys_video_high == []:
            print('Error!')
        else:
            keys_video_high = list(set(keys_video_high))
            keys_video_high = ['High KEYS'] + keys_video_high
            print('Done!')
        try:
            keys_video_hevc = netflix36_keys_hevc.GettingKEYS_Netflix(nfID_current)
        except Exception:
            keys_video_hevc = []

        if keys_video_hevc == []:
            print('Error!')
        else:
            keys_video_hevc = list(set(keys_video_hevc))
            keys_video_hevc = ['HEVC and HDR-10 KEYS'] + keys_video_hevc
            print('Done!')
        try:
            keys_video_hdr = netflix36_keys_hdr.GettingKEYS_Netflix(nfID_current)
        except Exception:
            keys_video_hdr = []

        if keys_video_hdr == []:
            print('Error!')
        else:
            keys_video_hdr = list(set(keys_video_hdr))
            keys_video_hdr = ['HDR-DV KEYS'] + keys_video_hdr
            print('Done!')
        keys_video = keys_video_main + keys_video_vp9 + keys_video_high + keys_video_hevc + keys_video_hdr
        print('\n' + seriesName)
        with open(keys_file, 'a', encoding='utf8') as (file):
            file.write(seriesName + '\n')
        for key in keys_video:
            print(key)
            with open(keys_file, 'a', encoding='utf8') as (file):
                file.write(key + '\n')

        CurrentHeigh = 'None'
        return (
         str(seriesName), str(SeasonFolder), str(CurrentHeigh))
    else:
        videoList_medium, audioList, subtitleList, subtitleDFXP, subtitleChi, forced, UHD, HDR, HEVC, VP9, HIGH, HIGH_1080p, MAIN = netflix36_MSL_medium.load_manifest(netflix36_MSL_medium(nfID_current), nfID_current)
        if MAIN == False:
            if args.hevc or args.hdr or args.video_vp9:
                videoList_medium = videoList_medium
            else:
                videoList_medium = []
        if HIGH == True:
            if args.hevc or args.hdr or args.video_vp9:
                videoList = videoList_medium
            else:
                videoList_high = netflix36_MSL_high.load_manifest(netflix36_MSL_high(int(nfID_current)), int(nfID_current))
                videoList = videoList_medium + videoList_high
        else:
            videoList = videoList_medium
        videoList = sorted(videoList, key=(lambda k: int(k['Bitrate'])))
        if args.lower:
            del videoList[-1]
        else:
            videoList = videoList
        if ipversion == '4':
            videoList = Ay_Clean_Videolist(videoList, 4)
        elif ipversion == '6':
            videoList = Ay_Clean_Videolist(videoList, 6)
        else:
            audioList = sorted(audioList, key=(lambda k: int(k['Bitrate'])), reverse=True)
            subtitleList = subtitleDFXP + subtitleChi
            print()
            if not args.novideo:
                try:
                    print('VIDEO - Bitrate: ' + str(dict(videoList[(-1)])['Bitrate']) + 'kbps' + ' - Profile: ' + str(dict(videoList[(-1)])['Profile']) + ' - Size: ' + str(format(float(dict(videoList[(-1)])['Size']) / 1073741824, '.2f')) + 'gb' + ' - Dimensions: ' + str(dict(videoList[(-1)])['Width']) + 'x' + str(dict(videoList[(-1)])['Height']))
                except Exception:
                    print('\nThe current quality is not available.')

                print('\n')
            if not args.noaudio:
                for w in audioList:
                    print('AUDIO - Bitrate: ' + str(dict(w)['Bitrate']) + 'kbps' + ' - Profile: ' + str(dict(w)['Profile']) + ' - Size: ' + str(format(float(dict(w)['Size']) / 1058816, '.2f')) + 'mb' + ' - Language: ' + dict(w)['Language'])

                print('\n')
            if not args.nosubs:
                for x in subtitleList:
                    print('SUBTITLE - Profile: ' + str(dict(x)['Profile']) + ' - Language: ' + dict(x)['Language'] + ' - ISO 639-2: ' + str(dict(x)['langAbbrev']))

            print('\nName: ' + seriesName + '\n')
            if MAIN:
                print('Notice: This item is available in Main Video Profile.')
            if HIGH:
                if HIGH_1080p:
                    print('Notice: This item is available in 1080p High Video Profile.')
                else:
                    print('Notice: This item is available in High Video Profile.')
            if VP9:
                print('Notice: This item is available in VP9 Video Profile.')
            if HEVC:
                print('Notice: This item is available in HEVC Video Profile.')
            if HDR:
                print('Notice: This item is available in HDR-10 Video Profile.')
            if UHD:
                print('Notice: This item is available in 4K Ultra HD Video Profile.')
            if forced:
                print('Notice: This item has forced subtitles.')
            CurrentHeigh = str(dict(videoList[(-1)])['Height'])
            if args.noprompt:
                choice = 'y'
            else:
                choice = input('\nDoes this look right? Answer yes to download. (y/n): ')
            if choice.lower() == 'y' or choice.lower() == 'yes':
                if args.hevc:
                    Name1 = folderdownloader + '\\' + str(SeasonFolder) + '\\' + seriesName + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
                    Name2 = folderdownloader + '\\' + seriesName + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
                    Name3 = seriesName + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
                else:
                    if args.hdr:
                        Name1 = folderdownloader + '\\' + str(SeasonFolder) + '\\' + seriesName + ' [' + str(CurrentHeigh) + 'p] [HDR].mkv'
                        Name2 = folderdownloader + '\\' + seriesName + ' [' + str(CurrentHeigh) + 'p] [HDR].mkv'
                        Name3 = seriesName + ' [' + str(CurrentHeigh) + 'p] [HDR].mkv'
                    else:
                        if args.video_vp9:
                            Name1 = folderdownloader + '\\' + str(SeasonFolder) + '\\' + seriesName + ' [' + str(CurrentHeigh) + 'p] [VP9].mkv'
                            Name2 = folderdownloader + '\\' + seriesName + ' [' + str(CurrentHeigh) + 'p] [VP9].mkv'
                            Name3 = seriesName + ' [' + str(CurrentHeigh) + 'p] [VP9].mkv'
                        else:
                            if 'playready-h264hpl' in str(dict(videoList[(-1)])['Profile']) or 'playready-h264shpl' in str(dict(videoList[(-1)])['Profile']):
                                Name1 = folderdownloader + '\\' + str(SeasonFolder) + '\\' + seriesName + ' [' + str(CurrentHeigh) + 'p] [AVC HIGH].mkv'
                                Name2 = folderdownloader + '\\' + seriesName + ' [' + str(CurrentHeigh) + 'p] [AVC HIGH].mkv'
                                Name3 = seriesName + ' [' + str(CurrentHeigh) + 'p] [AVC HIGH].mkv'
                            else:
                                Name1 = folderdownloader + '\\' + str(SeasonFolder) + '\\' + seriesName + ' [' + str(CurrentHeigh) + 'p].mkv'
                                Name2 = folderdownloader + '\\' + seriesName + ' [' + str(CurrentHeigh) + 'p].mkv'
                                Name3 = seriesName + ' [' + str(CurrentHeigh) + 'p].mkv'
                if not os.path.isfile(Name1):
                    if not os.path.isfile(Name2):
                        downloadNetflix(nfID_current, seriesName)
                    print("\nFile '" + str(Name3) + "' already exists.")
            elif choice.lower() == 'n' or choice.lower() == 'no':
                print('Quitting...')
        if netflixType == 'show':
            return (
             str(seriesName), str(SeasonFolder), str(CurrentHeigh))
        return (str(seriesName), str(seriesName), str(CurrentHeigh))


if args.url_season:
    nfID = int(re.search('[0-9]+', args.url_season).group())
else:
    if args.nflxID:
        nfID = int(re.search('[0-9]+', args.nflxID).group())
    else:
        nfID = input('Netflix viewable ID / watch URL: ')
        nfID = int(re.search('[0-9]+', nfID).group())
    if not args.ipversion:
        ipversion = 0
    else:
        ipversion = args.ipversion
if args.all_season:
    episodes = []
    isAEpisode = False
    print('Getting Metadata...')
    if os.path.isfile(cookies_nf):
        with open(cookies_nf, 'r', encoding='utf8') as (file):
            cookies_nf_open = file.read()
        if 'NetflixId' not in cookies_nf_open:
            cookies_nf_open = 'off'
        else:
            cookies_nf_open = json.loads(cookies_nf_open.replace("'", '"'))
    else:
        cookies_nf_open = 'off'
    data = fetch_metadata(str(nfID), cookies_nf_open)
    if data == 'ERROR':
        cookies_nf_open = 'off'
        data = fetch_metadata(str(nfID), cookies_nf_open)
        if data == 'ERROR':
            print('Error in getting metadata, maybe this tittle is not available in your region or your account has too many devices running at the same time.')
            sys.exit(0)
    if args.titlecustom:
        serial_title = ReplaceDontLikeWord(args.titlecustom[0])
    else:
        try:
            serial_title = ReplaceDontLikeWord(data['video']['title'])
        except Exception:
            serial_title = ReplaceDontLikeWord(kanji_to_romaji(data['video']['title']))

        if data['video']['type'] == 'movie':
            netflixType = 'movie'
        else:
            if data['video']['type'] == 'show':
                netflixType = 'show'
            else:
                if data['video']['type'] == 'supplemental':
                    netflixType = 'supplemental'
                else:
                    print(data['video']['type'] + ' is a unrecognized type!')
                    sys.exit(0)
            try:
                if str(data['video']['currentEpisode']) == str(nfID):
                    if netflixType == 'show':
                        isAEpisode = True
            except Exception:
                pass

    if netflixType == 'movie' or netflixType == 'supplemental':
        print('This item dont have seasons!')
        CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(nfID, serial_title, None)
        if args.country_code != None:
            os.system('taskkill /im openvpn.exe /f')
        if args.custom_command:
            print('\n')
            CustomCommand = '"' + folderdownloader + '\\' + str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv' + '"'
            str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
            CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
            stdoutdata, stderrdata = CustomCommand_process.communicate()
            CustomCommand_process.wait()
            sys.exit(0)
        else:
            sys.exit(0)
    else:
        if netflixType == 'show' and isAEpisode == False:
            if args.season:
                seasonMatchNumber = args.season
            else:
                seasonMatchNumber = input('Season: ')
            if args.episodeStart:
                episodeStart = args.episodeStart
            else:
                episodeStart = input('Episode Start: ')
            if isAEpisode == True:
                for season in data['video']['seasons']:
                    for episode in season['episodes']:
                        if str(episode['id']) == str(nfID):
                            if args.season:
                                seasonMatchNumber = args.season
                            else:
                                seasonMatchNumber = str(season['seq'])
                            if args.episodeStart:
                                episodeStart = args.episodeStart
                            else:
                                episodeStart = str(episode['seq'])

            for season in data['video']['seasons']:
                if str(season['seq']) == str(seasonMatchNumber):
                    episode_list = season['episodes']
                    episode_list = sorted(episode_list, key=(lambda x: x['seq']))
                    episode_list = episode_list[int(episodeStart) - 1:]
                    for episode in episode_list:
                        episodes.append((
                         episode['episodeId'],
                         '{} S{}E{}'.format(serial_title, str(season['seq']).zfill(2), str(episode['seq']).zfill(2)),
                         '{} S{}'.format(serial_title, str(season['seq']).zfill(2))))

            for ID, ShowName, FolderName in episodes:
                CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(ID, ShowName, FolderName)

            if args.country_code != None:
                os.system('taskkill /im openvpn.exe /f')
            if args.custom_command:
                print('\n')
                CustomCommand = '"' + folderdownloader + '\\' + str(SeasonFolder) + '"'
                str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
                CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
                stdoutdata, stderrdata = CustomCommand_process.communicate()
                CustomCommand_process.wait()
                sys.exit(0)
            else:
                sys.exit(0)
else:
    account = account_info
    episodes = []
    isAEpisode = False
    print('Getting Metadata...')
    if os.path.isfile(cookies_nf):
        with open(cookies_nf, 'r', encoding='utf8') as (file):
            cookies_nf_open = file.read()
        if 'NetflixId' not in cookies_nf_open:
            cookies_nf_open = 'off'
        else:
            cookies_nf_open = json.loads(cookies_nf_open.replace("'", '"'))
    else:
        cookies_nf_open = 'off'
    data = fetch_metadata(str(nfID), cookies_nf_open)
if data == 'ERROR':
    cookies_nf_open = 'off'
    data = fetch_metadata(str(nfID), cookies_nf_open)
    if data == 'ERROR':
        print('Error in getting metadata, maybe this tittle is not available in your region or your account has too many devices running at the same time.')
        sys.exit(0)
    if args.titlecustom:
        serial_title = ReplaceDontLikeWord(args.titlecustom[0])
    else:
        try:
            serial_title = ReplaceDontLikeWord(data['video']['title'])
        except Exception:
            serial_title = ReplaceDontLikeWord(kanji_to_romaji(data['video']['title']))

        if data['video']['type'] == 'movie':
            netflixType = 'movie'
        else:
            if data['video']['type'] == 'show':
                netflixType = 'show'
            else:
                if data['video']['type'] == 'supplemental':
                    netflixType = 'supplemental'
                else:
                    print(data['video']['type'] + ' is a unrecognized type!')
                    sys.exit(0)
                try:
                    if str(data['video']['currentEpisode']) == str(nfID):
                        if netflixType == 'show':
                            isAEpisode = True
                except Exception:
                    pass

        if netflixType == 'movie' or netflixType == 'supplemental':
            CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(nfID, serial_title, None)
            if args.country_code != None:
                os.system('taskkill /im openvpn.exe /f')
        else:
            if args.custom_command:
                print('\n')
                CustomCommand = '"' + folderdownloader + '\\' + str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv' + '"'
                str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
                CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
                stdoutdata, stderrdata = CustomCommand_process.communicate()
                CustomCommand_process.wait()
                sys.exit(0)
            else:
                sys.exit(0)
else:
    if isAEpisode == False:
        if args.season:
            seasonMatchNumber = args.season
        else:
            seasonMatchNumber = input('Season: ')
        if args.episodeStart:
            episodeStart = args.episodeStart
        else:
            episodeStart = input('Episode Start: ')
    else:
        if isAEpisode == True:
            for season in data['video']['seasons']:
                for episode in season['episodes']:
                    if str(episode['id']) == str(nfID):
                        if args.season:
                            seasonMatchNumber = args.season
                        else:
                            seasonMatchNumber = str(season['seq'])
                        if args.episodeStart:
                            episodeStart = args.episodeStart
                        else:
                            episodeStart = str(episode['seq'])

        for season in data['video']['seasons']:
            if str(season['seq']) == str(seasonMatchNumber):
                episode_list = season['episodes']
                episode_list = sorted(episode_list, key=(lambda x: x['seq']))
                episode_list = episode_list[int(episodeStart) - 1:]
                for episode in episode_list:
                    episodes.append((
                     episode['episodeId'],
                     '{} S{}E{}'.format(serial_title, str(season['seq']).zfill(2), str(episode['seq']).zfill(2)),
                     '{} S{}'.format(serial_title, str(season['seq']).zfill(2))))

        CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(episodes[0][0], episodes[0][1], episodes[0][2])
        if args.country_code != None:
            os.system('taskkill /im openvpn.exe /f')
    if args.custom_command:
        print('\n')
        CustomCommand = '"' + folderdownloader + '\\' + str(SeasonFolder) + '\\' + str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv' + '"'
        str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
        CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
        stdoutdata, stderrdata = CustomCommand_process.communicate()
        CustomCommand_process.wait()
        sys.exit(0)
    else:
        sys.exit(0)