# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\primevideo36.py
import hashlib, datetime
from titlecase import titlecase
import html, http.cookiejar, uuid, hashlib, hmac, requests, json, urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, re, subprocess, argparse, os, configparser, xmltodict, time, base64, sys, ffmpy, glob
from time import sleep
from requests import Request, Session
from subprocess import call
from collections import defaultdict
import subprocess as sp
from bs4 import BeautifulSoup
import binascii
from binaries.kanji_to_romaji.kanji_to_romaji_module import convert_hiragana_to_katakana, translate_to_romaji, translate_soukon, translate_long_vowel, translate_soukon_ch, kanji_to_romaji
from pywidevine.clientsconfig.amazonprimevideo import PrimevideoConfig
from pywidevine.decrypt.wvdecryptcustom import WvDecrypt
from pywidevine.muxer.muxer import Muxer
from nap36 import args
currentFile = 'primevideo36'
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
TimeStretch_dll = dirPath + '/binaries/BeHappy/plugins32/TimeStretch.dll'
lsmashsource_dll = dirPath + '/binaries/BeHappy/plugins32/LSMASHSource.dll'
mp4decryptexe = dirPath + '/binaries/mp4decrypt.exe'
mp4dumptexe = dirPath + '/binaries/mp4dump.exe'
ffmpegpath = dirPath + '/binaries/ffmpeg.exe'
ffprobepath = dirPath + '/binaries/ffprobe.exe'
mkvmergeexe = dirPath + '/binaries/mkvmerge.exe'
aria2cexe = dirPath + '/binaries/aria2c.exe'
wvDecrypterexe = dirPath + '/binaries/wvDecrypter/wvDecrypter.exe'
challengeBIN = dirPath + '/binaries/wvDecrypter/challenge.bin'
licenceBIN = dirPath + '/binaries/wvDecrypter/licence.bin'
config_data = dirPath + '/binaries/amz_decrypted/config.xml'
amz_decrypterexe = dirPath + '/binaries/amz_decrypted/amz_decrypter.exe'

def Ay_Download_Subs_DFXP():
    pass


def Ay_Download_Subs_SRT():
    pass


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as (f):
        for chunk in iter(lambda : f.read(65536), b''):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


hash_dec_exe = md5(wvDecrypterexe)
if __name__ == 'primevideo36':
    if not os.path.exists(dirPath + '/KEYS'):
        os.makedirs(dirPath + '/KEYS')
    else:
        keys_file = dirPath + '/KEYS/KEYS_AMAZON_PRIMEVIDEO.txt'
        try:
            keys_file_amazon_primevideo = open(keys_file, 'r')
            keys_file_txt = keys_file_amazon_primevideo.readlines()
        except Exception:
            with open(keys_file, 'a', encoding='utf8') as (file):
                file.write('##### Una KEY por linea. (One KEY for line.) #####\n')
            keys_file_amazon_primevideo = open(keys_file, 'r')
            keys_file_txt = keys_file_amazon_primevideo.readlines()

        SubtitleEditexe = dirPath + '/binaries/SubtitleEdit.exe'
        if args.chapterslang:
            chapterslang = args.chapterslang[0]
        else:
            chapterslang = 'en-US'
        if args.titlelang:
            titlelang = args.titlelang[0].replace('-', '_')
        else:
            titlelang = 'en_US'

    def ReplaceCodeLanguages(X):
        X = X.replace('_subtitle_dialog_0', '').replace('_narrative_dialog_0', '').replace('_caption_dialog_0', '').replace('_dialog_0', '').replace('_descriptive_0', '_descriptive').replace('_descriptive', '').replace('_sdh', '-sdh').replace('es-es', 'es').replace('en-es', 'es').replace('kn-in', 'kn').replace('gu-in', 'gu').replace('ja-jp', 'ja').replace('mni-in', 'mni').replace('si-in', 'si').replace('as-in', 'as').replace('ml-in', 'ml').replace('hy-hy', 'hy').replace('sv-sv', 'sv').replace('da-da', 'da').replace('fi-fi', 'fi').replace('nb-nb', 'nb').replace('is-is', 'is').replace('uk-uk', 'uk').replace('hu-hu', 'hu').replace('bg-bg', 'bg').replace('hr-hr', 'hr').replace('lt-lt', 'lt').replace('et-et', 'et').replace('el-el', 'el').replace('he-he', 'he').replace('ar-ar', 'ar').replace('fa-fa', 'fa').replace('ro-ro', 'ro').replace('sr-sr', 'sr').replace('cs-cs', 'cs').replace('sk-sk', 'sk').replace('mk-mk', 'mk').replace('hi-hi', 'hi').replace('bn-bn', 'bn').replace('ur-ur', 'ur').replace('pa-pa', 'pa').replace('ta-ta', 'ta').replace('te-te', 'te').replace('mr-mr', 'mr').replace('kn-kn', 'kn').replace('gu-gu', 'gu').replace('ml-ml', 'ml').replace('si-si', 'si').replace('as-as', 'as').replace('mni-mni', 'mni').replace('tl-tl', 'tl').replace('id-id', 'id').replace('ms-ms', 'ms').replace('vi-vi', 'vi').replace('th-th', 'th').replace('km-km', 'km').replace('ko-ko', 'ko').replace('zh-zh', 'zh').replace('ja-ja', 'ja').replace('ru-ru', 'ru').replace('tr-tr', 'tr').replace('it-it', 'it').replace('es-mx', 'es-la').replace('ar-sa', 'ar').replace('zh-cn', 'zh').replace('nl-nl', 'nl').replace('pl-pl', 'pl').replace('pt-pt', 'pt').replace('hi-in', 'hi').replace('mr-in', 'mr').replace('bn-in', 'bn').replace('te-in', 'te').replace('cmn-hans', 'zh-hans').replace('cmn-hant', 'zh-hant').replace('ko-kr', 'ko').replace('es-419', 'es-la').replace('en-us', 'en').replace('en-gb', 'en').replace('fr-fr', 'fr').replace('de-de', 'de').replace('las-419', 'es-la').replace('ar-ae', 'ar').replace('da-dk', 'da').replace('yue-hant', 'yue').replace('bn-in', 'bn').replace('ur-in', 'ur').replace('ta-in', 'ta').replace('sl-si', 'sl').replace('cs-cz', 'cs').replace('hi-jp', 'hi').replace('-001', '').replace('en-US', 'en').replace('deu', 'de').replace('eng', 'en').replace('ca-es', 'cat').replace('eu-es', 'fcustomquality')
        return X


    def ReplaceChapters(X):
        pattern1 = re.compile('(?:[A-Z]*)(?:[A-Za-z_ -=]*)( )')
        X = pattern1.sub('', X)
        return X


    def ReplaceASIN(X):
        pattern1 = re.compile('(?:[A-Za-z0-9]*)(,)')
        X = pattern1.sub('', X)
        return X


    def ReplaceChaptersNumber(X):
        pattern1 = re.compile('(\\d+)(\\.)( )')
        X = pattern1.sub('', X)
        return X


    def list_to_str(list, separator, lastseparator):
        list_str = ''
        audio_or_subs_num = len(list)
        listcounter = 1
        for x in list:
            if len(list) == 1:
                list_str = str(x)
            else:
                if list_str != '':
                    if listcounter < int(audio_or_subs_num):
                        list_str = list_str + separator + str(x)
                else:
                    if listcounter == int(audio_or_subs_num):
                        list_str = list_str + lastseparator + str(x)
                    if list_str == '':
                        list_str = str(x)
                listcounter = listcounter + 1

        return list_str


    def ReplaceSubs1(X):
        pattern1 = re.compile('(?!<i>|<b>|<u>|<\\/i>|<\\/b>|<\\/u>)(<)(?:[A-Za-z0-9_ -=]*)(>)')
        pattern2 = re.compile('(?!<\\/i>|<\\/b>|<\\/u>)(<\\/)(?:[A-Za-z0-9_ -=]*)(>)')
        X = X.replace('&rlm;', '').replace('{\\an1}', '').replace('{\\an2}', '').replace('{\\an3}', '').replace('{\\an4}', '').replace('{\\an5}', '').replace('{\\an6}', '').replace('{\\an7}', '').replace('{\\an8}', '').replace('{\\an9}', '').replace('?', '?').replace('\xad', '?')
        X = pattern1.sub('', X)
        X = pattern2.sub('', X)
        return X


    def ReplaceSubs2(X):
        pattern1 = re.compile('(?!<i>|<b>|<u>|<\\/i>|<\\/b>|<\\/u>)(<)(?:[A-Za-z0-9_ -=]*)(>)')
        pattern2 = re.compile('(?!<\\/i>|<\\/b>|<\\/u>)(<\\/)(?:[A-Za-z0-9_ -=]*)(>)')
        X = X.replace('&rlm;', '').replace('{\\an1}', '').replace('{\\an2}', '').replace('{\\an3}', '').replace('{\\an4}', '').replace('{\\an6}', '').replace('{\\an7}', '').replace('{\\an9}', '').replace('?', '?').replace('\xad', '?')
        X = pattern1.sub('', X)
        X = pattern2.sub('', X)
        return X


    def ReplaceDontLikeWord(X):
        try:
            X = X.replace(' : ', ' - ').replace(': ', ' - ').replace(':', ' - ').replace('&', 'and').replace('+', '').replace(';', '').replace('????', 'o').replace('[', '').replace("'", '').replace(']', '').replace('/', '').replace('//', '').replace('?', "'").replace('*', 'x').replace('<', '').replace('>', '').replace('|', '').replace('~', '').replace('#', '').replace('%', '').replace('{', '').replace('}', '').replace(',', '').replace('?', '').encode('latin-1').decode('latin-1')
        except Exception:
            X = X.decode('utf-8').replace(' : ', ' - ').replace(': ', ' - ').replace(':', ' - ').replace('&', 'and').replace('+', '').replace(';', '').replace('????', 'o').replace('[', '').replace("'", '').replace(']', '').replace('/', '').replace('//', '').replace('?', "'").replace('*', 'x').replace('<', '').replace('>', '').replace('|', '').replace('~', '').replace('#', '').replace('%', '').replace('{', '').replace('}', '').replace(',', '').replace('?', '').encode('latin-1').decode('latin-1')

        return titlecase(X)


    def find_str(s, char):
        return s.find(char)


    def getKeyId(name):
        mp4dump = subprocess.Popen([mp4dumptexe, name], stdout=(subprocess.PIPE))
        mp4dump = str(mp4dump.stdout.read())
        A = find_str(mp4dump, 'default_KID')
        KEY_ID_ORI = ''
        KEY_ID_ORI = mp4dump[A:A + 63].replace('default_KID = ', '').replace('[', '').replace(']', '').replace(' ', '')
        if KEY_ID_ORI == '' or KEY_ID_ORI == "'":
            KEY_ID_ORI = 'nothing'
        return KEY_ID_ORI


    def substring(s, start, end):
        return s[start:end]


    def alphanumericSort(l):
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key=alphanum_key)


    def downloadFile(link, file_name):
        print('\n' + file_name)
        aria_command = [aria2cexe, link,
         '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"',
         '--header="Range: bytes=0-"',
         '--header="DNT: 1"',
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


    def merge_lists(l1, l2, key):
        merged = {}
        for item in l1 + l2:
            if item[key] in merged:
                merged[item[key]].update(item)
            else:
                merged[item[key]] = item

        return merged.values()


    def pp_json(json_thing, sort=True, indents=4):
        if type(json_thing) is str:
            print(json.dumps((json.loads(json_thing)), sort_keys=sort, indent=indents))
        else:
            print(json.dumps(json_thing, sort_keys=sort, indent=indents))


    def get_cookies():
        global cookies_file
        try:
            cj = http.cookiejar.MozillaCookieJar(dirPath + '/cookies/' + cookies_file)
            cj.load()
        except Exception:
            print('\nCookies not found! Please dump the cookies with the Chrome extension https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg and place the generated file in ' + dirPath + '/cookies/' + cookies_file)
            print('\nWarning, do not click on "download all cookies", you have to click on "click here".\n')
            sys.exit(0)

        cookies = str()
        for cookie in cj:
            cookie.value = urllib.parse.unquote(html.unescape(cookie.value))
            cookies = cookies + cookie.name + '=' + cookie.value + ';'

        cookies = list(cookies)
        del cookies[-1]
        cookies = ''.join(cookies)
        return cookies


    def get_cookies_v2():
        global email
        global password
        global site_base_url
        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        AMAZON_LOGIN_URL = 'https://{base_url}/gp/sign-in.html'
        PRIMEVIDEO_LOGIN_URL = 'https://{base_url}/auth-redirect'
        if region == 'ps' or region == 'ps-int':
            url = PRIMEVIDEO_LOGIN_URL.format(base_url=site_base_url)
        else:
            url = AMAZON_LOGIN_URL.format(base_url=site_base_url)
        headers = HEADERS.copy()
        session = requests.Session()
        resp = session.get(url=url, headers=headers)
        headers['Referer'] = resp.url
        headers['Accept-Language'] = 'en-US,en;q=0.9,en;q=0.8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        form = soup.find('form', attrs={'name': 'signIn'})
        payload = {}
        for data in form.findAll('input'):
            if data.attrs['type'] == 'hidden':
                payload[data.attrs['name']] = data.attrs.get('value') and data.attrs['value']

        payload['email'] = email
        payload['password'] = password
        resp = session.post(url=(form.attrs['action']), headers=headers,
          data=payload)
        cj = session.cookies
        cookies = str()
        for cookie in cj:
            cookie.value = urllib.parse.unquote(html.unescape(cookie.value))
            cookies = cookies + cookie.name + '=' + cookie.value + ';'

        cookies = list(cookies)
        del cookies[-1]
        cookies = ''.join(cookies)
        return cookies


    def getLicenseTemp(asin, clientId):
        global deviceID
        global licurl
        global marketplace_id
        global params
        global url
        global video_base_url
        if region == 'ps' or region == 'ps-int':
            url = 'https://' + video_base_url + '/cdp/catalog/GetPlaybackResources'
            params = dict(asin=asin, consumptionType='Streaming',
              desiredResources='AudioVideoUrls,PlaybackUrls,CatalogMetadata,ForcedNarratives,SubtitlePresets,SubtitleUrls,TransitionTimecodes,TrickplayUrls,CuepointPlaylist,XRayMetadata,PlaybackSettings',
              deviceID=deviceID,
              deviceTypeID='AOAGZA014O5RE',
              firmware='1',
              gascEnabled='true',
              marketplaceID=marketplace_id,
              resourceUsage='CacheResources',
              audioTrackId='all',
              videoMaterialType='Feature',
              operatingSystemName='Windows',
              operatingSystemVersion='10.0',
              deviceDrmOverride='CENC',
              deviceStreamingTechnologyOverride='DASH',
              deviceProtocolOverride='Https',
              supportedDRMKeyScheme='DUAL_KEY',
              deviceBitrateAdaptationsOverride='CVBR,CBR',
              titleDecorationScheme='primary-content',
              subtitleFormat='TTMLv2',
              languageFeature='MLFv2',
              uxLocale=titlelang,
              xrayDeviceClass='normal',
              xrayPlaybackMode='playback',
              xrayToken='INCEPTION_LITE_FILMO_V2',
              playbackSettingsFormatVersion='1.0.0',
              clientId=clientId)
        else:
            url = 'https://' + video_base_url + '/cdp/catalog/GetPlaybackResources'
            params = dict(asin=asin, consumptionType='Streaming',
              desiredResources='AudioVideoUrls,PlaybackUrls,CatalogMetadata,ForcedNarratives,SubtitlePresets,SubtitleUrls,TransitionTimecodes,TrickplayUrls,CuepointPlaylist,XRayMetadata,PlaybackSettings',
              deviceID=deviceID,
              deviceTypeID='AOAGZA014O5RE',
              firmware='1',
              gascEnabled='false',
              marketplaceID=marketplace_id,
              resourceUsage='CacheResources',
              audioTrackId='all',
              videoMaterialType='Feature',
              operatingSystemName='Windows',
              operatingSystemVersion='10.0',
              clientId=clientId,
              deviceDrmOverride='CENC',
              deviceStreamingTechnologyOverride='DASH',
              deviceProtocolOverride='Https',
              supportedDRMKeyScheme='DUAL_KEY',
              deviceBitrateAdaptationsOverride='CVBR,CBR',
              titleDecorationScheme='primary-content',
              subtitleFormat='TTMLv2',
              languageFeature='MLFv2',
              uxLocale=titlelang,
              xrayDeviceClass='normal',
              xrayPlaybackMode='playback',
              xrayToken='INCEPTION_LITE_FILMO_V2',
              playbackSettingsFormatVersion='1.0.0')
        if args.hevc:
            params['deviceVideoCodecOverride'] = 'H265'
        else:
            if args.atmos:
                params['deviceVideoQualityOverride'] = 'UHD'
                params['deviceHdrFormatsOverride'] = 'Hdr10'
        resp = requests.get(url=url, params=params, headers=custom_headers_GetPlaybackResources)
        Error_Not_Avaiable = False
        try:
            data = json.loads(resp.text)
            licurl = url + '?' + urllib.parse.urlencode(params).replace('AudioVideoUrls%2CPlaybackUrls%2CCatalogMetadata%2CForcedNarratives%2CSubtitlePresets%2CSubtitleUrls%2CTransitionTimecodes%2CTrickplayUrls%2CCuepointPlaylist%2CXRayMetadata%2CPlaybackSettings', 'Widevine2License')
            return data
        except ValueError:
            print(data)
            print('\nEpisode or Movie not available yet in your region. Possible VPN error.')
            Error_Not_Avaiable = True


    def get_license(challenge):
        custom_headers_license = {'Accept':'application/json',  'Accept-Encoding':'gzip, deflate, br', 
         'Accept-Language':'es,ca;q=0.9,en;q=0.8', 
         'Cache-Control':'no-cache', 
         'Connection':'keep-alive', 
         'Content-Type':'application/x-www-form-urlencoded', 
         'Pragma':'no-cache', 
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 
         'Cookie':cookies}
        challenge_encoded = base64.b64encode(challenge)
        license_form_data = dict(widevine2Challenge=challenge_encoded, includeHdcpTestKeyInLicense='true')
        license_res = requests.Session().post(url=licurl, data=license_form_data, headers=custom_headers_license)
        license_res_json = json.loads(license_res.text)
        try:
            license_base64 = license_res_json['widevine2License']['license']
            license_decoded = base64.b64decode(license_base64)
            return license_base64
        except Exception:
            print('Error getting license!')
            print(license_res_json)
            sys.exit(0)


    def getXray(asin, clientId, serviceToken):
        global params2
        global url2
        if region == 'ps' or region == 'ps-int':
            url2 = 'https://' + video_base_url + '/swift/page/xray'
            params2 = dict(firmware='1', format='json',
              gascEnabled='true',
              deviceID=deviceID,
              deviceTypeID='AOAGZA014O5RE',
              marketplaceId=marketplace_id,
              decorationScheme='none',
              version='inception-v2',
              featureScheme='INCEPTION_LITE_FILMO_V2',
              uxLocale=chapterslang,
              pageType='xray',
              pageId='fullScreen',
              serviceToken=serviceToken)
        else:
            url2 = 'https://' + video_base_url + '/swift/page/xray'
            params2 = dict(firmware='1', format='json',
              gascEnabled='false',
              deviceID=deviceID,
              deviceTypeID='AOAGZA014O5RE',
              marketplaceId=marketplace_id,
              decorationScheme='none',
              version='inception-v2',
              featureScheme='INCEPTION_LITE_FILMO_V2',
              uxLocale='en-US',
              pageType='xray',
              pageId='fullScreen',
              serviceToken=serviceToken)
        resp2 = requests.get(url=url2, params=params2, headers=custom_headers_GetPlaybackResources)
        try:
            data2 = json.loads(resp2.text)
            return data2
        except ValueError:
            data2 = None
            nochpaters = True
            return data2


    def do_decrypt(init_data_b64, cert_data_b64):
        wvdecrypt = WvDecrypt(init_data_b64=init_data_b64, cert_data_b64=cert_data_b64)
        chal = wvdecrypt.get_challenge()
        license_b64 = get_license(chal)
        wvdecrypt.update_license(license_b64)
        wvdecrypt.start_process()
        Correct, keyswvdecrypt = wvdecrypt.start_process()
        return (
         Correct, keyswvdecrypt)


    def DownloadAll--- This code section failed: ---

 L. 537         0  LOAD_CODE                <code_object GetKey>
                2  LOAD_STR                 'DownloadAll.<locals>.GetKey'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'GetKey'

 L. 545         8  LOAD_CODE                <code_object DecryptAudio>
               10  LOAD_STR                 'DownloadAll.<locals>.DecryptAudio'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  STORE_FAST               'DecryptAudio'

 L. 573        16  LOAD_CODE                <code_object DecryptVideo>
               18  LOAD_STR                 'DownloadAll.<locals>.DecryptVideo'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  STORE_FAST               'DecryptVideo'

 L. 600        24  LOAD_CLOSURE             'asin'
               26  LOAD_CLOSURE             'audio_pssh'
               28  LOAD_CLOSURE             'video_pssh'
               30  BUILD_TUPLE_3         3 
               32  LOAD_CODE                <code_object DecryptAlternativeConfig>
               34  LOAD_STR                 'DownloadAll.<locals>.DecryptAlternativeConfig'
               36  MAKE_FUNCTION_8          'closure'
               38  STORE_FAST               'DecryptAlternativeConfig'

 L. 657        40  LOAD_CLOSURE             'seriesName'
               42  BUILD_TUPLE_1         1 
               44  LOAD_CODE                <code_object DecryptAlternative>
               46  LOAD_STR                 'DownloadAll.<locals>.DecryptAlternative'
               48  MAKE_FUNCTION_8          'closure'
               50  STORE_FAST               'DecryptAlternative'

 L. 675        52  LOAD_CODE                <code_object getKeyId_v2>
               54  LOAD_STR                 'DownloadAll.<locals>.getKeyId_v2'
               56  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               58  STORE_DEREF              'getKeyId_v2'

 L. 686        60  LOAD_CODE                <code_object Get_PSSH>
               62  LOAD_STR                 'DownloadAll.<locals>.Get_PSSH'
               64  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               66  STORE_FAST               'Get_PSSH'

 L. 707        68  LOAD_CODE                <code_object get_license>
               70  LOAD_STR                 'DownloadAll.<locals>.get_license'
               72  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               74  STORE_DEREF              'get_license'

 L. 727        76  LOAD_CLOSURE             'getKeyId_v2'
               78  LOAD_CLOSURE             'get_license'
               80  BUILD_TUPLE_2         2 
               82  LOAD_CODE                <code_object DecryptAlternativeV2>
               84  LOAD_STR                 'DownloadAll.<locals>.DecryptAlternativeV2'
               86  MAKE_FUNCTION_8          'closure'
               88  STORE_FAST               'DecryptAlternativeV2'

 L. 822        90  LOAD_CLOSURE             'seriesName'
               92  BUILD_TUPLE_1         1 
               94  LOAD_CODE                <code_object GettingMPD>
               96  LOAD_STR                 'DownloadAll.<locals>.GettingMPD'
               98  MAKE_FUNCTION_8          'closure'
              100  STORE_FAST               'GettingMPD'

 L. 938       102  LOAD_CLOSURE             'OnlyOneAudio'
              104  LOAD_CLOSURE             'OnlyOneAudioID'
              106  BUILD_TUPLE_2         2 
              108  LOAD_CODE                <code_object ParsingMPD>
              110  LOAD_STR                 'DownloadAll.<locals>.ParsingMPD'
              112  MAKE_FUNCTION_8          'closure'
              114  STORE_FAST               'ParsingMPD'

 L.1488       116  LOAD_CODE                <code_object getLicense>
              118  LOAD_STR                 'DownloadAll.<locals>.getLicense'
              120  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              122  STORE_FAST               'getLicense'

 L.1574       124  LOAD_GLOBAL              region
              126  LOAD_STR                 'ps'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_TRUE    140  'to 140'
              132  LOAD_GLOBAL              region
              134  LOAD_STR                 'ps-int'
              136  COMPARE_OP               ==
            138_0  COME_FROM           130  '130'
              138  POP_JUMP_IF_FALSE   192  'to 192'

 L.1575       140  LOAD_STR                 'https://'
              142  LOAD_GLOBAL              video_base_url
              144  BINARY_ADD       
              146  LOAD_STR                 '/cdp/catalog/GetPlaybackResources'
              148  BINARY_ADD       
              150  STORE_GLOBAL             url2

 L.1576       152  LOAD_GLOBAL              dict
              154  LOAD_DEREF               'asin'

 L.1577       156  LOAD_STR                 'Streaming'

 L.1578       158  LOAD_STR                 'Widevine2License'

 L.1579       160  LOAD_GLOBAL              deviceID

 L.1580       162  LOAD_STR                 'AOAGZA014O5RE'

 L.1581       164  LOAD_STR                 '1'

 L.1582       166  LOAD_STR                 'true'

 L.1583       168  LOAD_GLOBAL              marketplace_id

 L.1584       170  LOAD_STR                 'CacheResources'

 L.1585       172  LOAD_STR                 'Feature'

 L.1586       174  LOAD_GLOBAL              clientId

 L.1587       176  LOAD_STR                 'Windows'

 L.1588       178  LOAD_STR                 '10.0'

 L.1589       180  LOAD_STR                 'CENC'

 L.1590       182  LOAD_STR                 'DASH'
              184  LOAD_CONST               ('asin', 'consumptionType', 'desiredResources', 'deviceID', 'deviceTypeID', 'firmware', 'gascEnabled', 'marketplaceID', 'resourceUsage', 'videoMaterialType', 'clientId', 'operatingSystemName', 'operatingSystemVersion', 'deviceDrmOverride', 'deviceStreamingTechnologyOverride')
              186  CALL_FUNCTION_KW_15    15  '15 total positional and keyword args'
              188  STORE_GLOBAL             params2
              190  JUMP_FORWARD        242  'to 242'
              192  ELSE                     '242'

 L.1592       192  LOAD_STR                 'https://'
              194  LOAD_GLOBAL              video_base_url
              196  BINARY_ADD       
              198  LOAD_STR                 '/cdp/catalog/GetPlaybackResources'
              200  BINARY_ADD       
              202  STORE_GLOBAL             url2

 L.1593       204  LOAD_GLOBAL              dict
              206  LOAD_DEREF               'asin'

 L.1594       208  LOAD_STR                 'Streaming'

 L.1595       210  LOAD_STR                 'Widevine2License'

 L.1596       212  LOAD_GLOBAL              deviceID

 L.1597       214  LOAD_STR                 'AOAGZA014O5RE'

 L.1598       216  LOAD_STR                 '1'

 L.1599       218  LOAD_STR                 'false'

 L.1600       220  LOAD_GLOBAL              marketplace_id

 L.1601       222  LOAD_STR                 'ImmediateConsumption'

 L.1602       224  LOAD_STR                 'Feature'

 L.1603       226  LOAD_GLOBAL              clientId

 L.1604       228  LOAD_STR                 'Windows'

 L.1605       230  LOAD_STR                 '10.0'

 L.1606       232  LOAD_STR                 'CENC'

 L.1607       234  LOAD_STR                 'DASH'
              236  LOAD_CONST               ('asin', 'consumptionType', 'desiredResources', 'deviceID', 'deviceTypeID', 'firmware', 'gascEnabled', 'marketplaceID', 'resourceUsage', 'videoMaterialType', 'clientId', 'operatingSystemName', 'operatingSystemVersion', 'deviceDrmOverride', 'deviceStreamingTechnologyOverride')
              238  CALL_FUNCTION_KW_15    15  '15 total positional and keyword args'
              240  STORE_GLOBAL             params2
            242_0  COME_FROM           190  '190'

 L.1608       242  LOAD_GLOBAL              args
              244  LOAD_ATTR                hevc
              246  POP_JUMP_IF_FALSE   260  'to 260'

 L.1609       250  LOAD_STR                 'H265'
              252  LOAD_GLOBAL              params2
              254  LOAD_STR                 'deviceVideoCodecOverride'
              256  STORE_SUBSCR     
              258  JUMP_FORWARD        284  'to 284'
              260  ELSE                     '284'

 L.1611       260  LOAD_GLOBAL              args
              262  LOAD_ATTR                atmos
              264  POP_JUMP_IF_FALSE   284  'to 284'

 L.1612       268  LOAD_STR                 'UHD'
              270  LOAD_GLOBAL              params2
              272  LOAD_STR                 'deviceVideoQualityOverride'
              274  STORE_SUBSCR     

 L.1613       276  LOAD_STR                 'Hdr10'
              278  LOAD_GLOBAL              params2
              280  LOAD_STR                 'deviceHdrFormatsOverride'
              282  STORE_SUBSCR     
            284_0  COME_FROM           264  '264'
            284_1  COME_FROM           258  '258'

 L.1614       284  LOAD_GLOBAL              url2
              286  LOAD_STR                 '?'
              288  BINARY_ADD       
              290  LOAD_GLOBAL              urllib
              292  LOAD_ATTR                parse
              294  LOAD_ATTR                urlencode
              296  LOAD_GLOBAL              params2
              298  CALL_FUNCTION_1       1  '1 positional argument'
              300  BINARY_ADD       
              302  STORE_GLOBAL             licurl2

 L.1615       304  LOAD_GLOBAL              args
              306  LOAD_ATTR                retry
              308  POP_JUMP_IF_FALSE   554  'to 554'

 L.1616       312  LOAD_CONST               0
              314  STORE_FAST               'attempt_number'

 L.1617       316  LOAD_CONST               True
              318  STORE_FAST               'error'

 L.1618       320  SETUP_LOOP          480  'to 480'
              322  LOAD_FAST                'error'
              324  LOAD_CONST               True
              326  COMPARE_OP               ==
              328  POP_JUMP_IF_FALSE   478  'to 478'

 L.1619       332  LOAD_FAST                'getLicense'
              334  LOAD_DEREF               'asin'
              336  LOAD_GLOBAL              clientId
              338  CALL_FUNCTION_2       2  '2 positional arguments'
              340  STORE_FAST               'data'

 L.1620       342  SETUP_EXCEPT        380  'to 380'

 L.1621       344  LOAD_FAST                'data'
              346  LOAD_STR                 'audioVideoUrls'
              348  BINARY_SUBSCR    
              350  LOAD_STR                 'avCdnUrlSets'
              352  BINARY_SUBSCR    
              354  LOAD_CONST               0
              356  BINARY_SUBSCR    
              358  LOAD_STR                 'avUrlInfoList'
              360  BINARY_SUBSCR    
              362  LOAD_CONST               0
              364  BINARY_SUBSCR    
              366  LOAD_STR                 'url'
              368  BINARY_SUBSCR    
              370  POP_TOP          

 L.1622       372  LOAD_CONST               False
              374  STORE_FAST               'error'
              376  POP_BLOCK        
              378  JUMP_FORWARD        474  'to 474'
            380_0  COME_FROM_EXCEPT    342  '342'

 L.1623       380  DUP_TOP          
              382  LOAD_GLOBAL              Exception
              384  COMPARE_OP               exception-match
              386  POP_JUMP_IF_FALSE   472  'to 472'
              390  POP_TOP          
              392  POP_TOP          
              394  POP_TOP          

 L.1624       396  LOAD_FAST                'attempt_number'
              398  LOAD_CONST               0
              400  COMPARE_OP               ==
              402  POP_JUMP_IF_FALSE   420  'to 420'

 L.1625       406  LOAD_GLOBAL              print
              408  CALL_FUNCTION_0       0  '0 positional arguments'
              410  POP_TOP          

 L.1626       412  LOAD_GLOBAL              print
              414  LOAD_STR                 'No MPD found! Trying again...'
              416  CALL_FUNCTION_1       1  '1 positional argument'
              418  POP_TOP          
            420_0  COME_FROM           402  '402'

 L.1627       420  LOAD_FAST                'attempt_number'
              422  LOAD_CONST               1
              424  INPLACE_ADD      
              426  STORE_FAST               'attempt_number'

 L.1628       428  LOAD_GLOBAL              sys
              430  LOAD_ATTR                stdout
              432  LOAD_ATTR                write
              434  LOAD_STR                 'Attempt %d...\r'
              436  LOAD_FAST                'attempt_number'
              438  BINARY_MODULO    
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  POP_TOP          

 L.1629       444  LOAD_GLOBAL              sys
              446  LOAD_ATTR                stdout
              448  LOAD_ATTR                flush
              450  CALL_FUNCTION_0       0  '0 positional arguments'
              452  POP_TOP          

 L.1630       454  LOAD_GLOBAL              time
              456  LOAD_ATTR                sleep
              458  LOAD_CONST               15
              460  CALL_FUNCTION_1       1  '1 positional argument'
              462  POP_TOP          

 L.1631       464  LOAD_CONST               True
              466  STORE_FAST               'error'
              468  POP_EXCEPT       
              470  JUMP_FORWARD        474  'to 474'
              472  END_FINALLY      
            474_0  COME_FROM           470  '470'
            474_1  COME_FROM           378  '378'
              474  JUMP_BACK           322  'to 322'
            478_0  COME_FROM           328  '328'
              478  POP_BLOCK        
            480_0  COME_FROM_LOOP      320  '320'

 L.1633       480  LOAD_GLOBAL              datetime
              482  LOAD_ATTR                datetime
              484  LOAD_ATTR                now
              486  CALL_FUNCTION_0       0  '0 positional arguments'
              488  STORE_FAST               'time_now'

 L.1634       490  LOAD_FAST                'attempt_number'
              492  LOAD_CONST               0
              494  COMPARE_OP               !=
              496  POP_JUMP_IF_FALSE   564  'to 564'

 L.1635       500  LOAD_GLOBAL              print
              502  CALL_FUNCTION_0       0  '0 positional arguments'
              504  POP_TOP          

 L.1636       506  LOAD_GLOBAL              print

 L.1637       508  LOAD_STR                 'Episode found at '
              510  LOAD_GLOBAL              str
              512  LOAD_FAST                'time_now'
              514  LOAD_ATTR                hour
              516  CALL_FUNCTION_1       1  '1 positional argument'
              518  BINARY_ADD       
              520  LOAD_STR                 ':'
              522  BINARY_ADD       
              524  LOAD_GLOBAL              str
              526  LOAD_FAST                'time_now'
              528  LOAD_ATTR                minute
              530  CALL_FUNCTION_1       1  '1 positional argument'
              532  BINARY_ADD       
              534  LOAD_STR                 ':'
              536  BINARY_ADD       
              538  LOAD_GLOBAL              str

 L.1638       540  LOAD_FAST                'time_now'
              542  LOAD_ATTR                second
              544  CALL_FUNCTION_1       1  '1 positional argument'
              546  BINARY_ADD       
              548  CALL_FUNCTION_1       1  '1 positional argument'
              550  POP_TOP          
              552  JUMP_FORWARD        564  'to 564'
              554  ELSE                     '564'

 L.1640       554  LOAD_FAST                'getLicense'
              556  LOAD_DEREF               'asin'
              558  LOAD_GLOBAL              clientId
              560  CALL_FUNCTION_2       2  '2 positional arguments'
              562  STORE_FAST               'data'
            564_0  COME_FROM           552  '552'
            564_1  COME_FROM           496  '496'

 L.1641       564  LOAD_CONST               False
              566  STORE_FAST               'nochapters'

 L.1643       568  LOAD_FAST                'data'
              570  LOAD_STR                 'catalogMetadata'
              572  BINARY_SUBSCR    
              574  LOAD_STR                 'catalog'
              576  BINARY_SUBSCR    
              578  LOAD_STR                 'type'
              580  BINARY_SUBSCR    
              582  LOAD_STR                 'MOVIE'
              584  COMPARE_OP               ==
              586  POP_JUMP_IF_FALSE   596  'to 596'

 L.1644       590  LOAD_STR                 'movie'
              592  STORE_FAST               'amazonType'
              594  JUMP_FORWARD        642  'to 642'
              596  ELSE                     '642'

 L.1646       596  LOAD_FAST                'data'
              598  LOAD_STR                 'catalogMetadata'
              600  BINARY_SUBSCR    
              602  LOAD_STR                 'catalog'
              604  BINARY_SUBSCR    
              606  LOAD_STR                 'type'
              608  BINARY_SUBSCR    
              610  LOAD_STR                 'EPISODE'
              612  COMPARE_OP               ==
              614  POP_JUMP_IF_FALSE   624  'to 624'

 L.1647       618  LOAD_STR                 'show'
              620  STORE_FAST               'amazonType'
              622  JUMP_FORWARD        642  'to 642'
              624  ELSE                     '642'

 L.1649       624  LOAD_GLOBAL              print
              626  LOAD_STR                 'Unrecognized type!'
              628  CALL_FUNCTION_1       1  '1 positional argument'
              630  POP_TOP          

 L.1650       632  LOAD_GLOBAL              sys
              634  LOAD_ATTR                exit
              636  LOAD_CONST               0
              638  CALL_FUNCTION_1       1  '1 positional argument'
              640  POP_TOP          
            642_0  COME_FROM           622  '622'
            642_1  COME_FROM           594  '594'

 L.1651       642  BUILD_LIST_0          0 
              644  STORE_GLOBAL             seriesList

 L.1652       646  LOAD_CONST               False
              648  STORE_FAST               'bonus'

 L.1654       650  LOAD_FAST                'amazonType'
              652  LOAD_STR                 'show'
              654  COMPARE_OP               ==
              656  POP_JUMP_IF_FALSE  1580  'to 1580'

 L.1655       660  LOAD_FAST                'data'
              662  LOAD_STR                 'catalogMetadata'
              664  BINARY_SUBSCR    
              666  LOAD_STR                 'catalog'
              668  BINARY_SUBSCR    
              670  LOAD_STR                 'episodeNumber'
              672  BINARY_SUBSCR    
              674  LOAD_CONST               0
              676  COMPARE_OP               ==
              678  POP_JUMP_IF_FALSE   758  'to 758'

 L.1656       682  SETUP_EXCEPT        708  'to 708'

 L.1657       684  LOAD_GLOBAL              ReplaceDontLikeWord
              686  LOAD_FAST                'data'
              688  LOAD_STR                 'catalogMetadata'
              690  BINARY_SUBSCR    
              692  LOAD_STR                 'catalog'
              694  BINARY_SUBSCR    
              696  LOAD_STR                 'title'
              698  BINARY_SUBSCR    
              700  CALL_FUNCTION_1       1  '1 positional argument'
              702  STORE_FAST               'titleBonus'
              704  POP_BLOCK        
              706  JUMP_FORWARD        754  'to 754'
            708_0  COME_FROM_EXCEPT    682  '682'

 L.1658       708  DUP_TOP          
              710  LOAD_GLOBAL              Exception
              712  COMPARE_OP               exception-match
              714  POP_JUMP_IF_FALSE   752  'to 752'
              718  POP_TOP          
              720  POP_TOP          
              722  POP_TOP          

 L.1659       724  LOAD_GLOBAL              ReplaceDontLikeWord

 L.1660       726  LOAD_GLOBAL              kanji_to_romaji
              728  LOAD_FAST                'data'
              730  LOAD_STR                 'catalogMetadata'
              732  BINARY_SUBSCR    
              734  LOAD_STR                 'catalog'
              736  BINARY_SUBSCR    
              738  LOAD_STR                 'title'
              740  BINARY_SUBSCR    
              742  CALL_FUNCTION_1       1  '1 positional argument'
              744  CALL_FUNCTION_1       1  '1 positional argument'
              746  STORE_FAST               'titleBonus'
              748  POP_EXCEPT       
              750  JUMP_FORWARD        754  'to 754'
              752  END_FINALLY      
            754_0  COME_FROM           750  '750'
            754_1  COME_FROM           706  '706'

 L.1662       754  LOAD_CONST               True
              756  STORE_FAST               'bonus'
            758_0  COME_FROM           678  '678'

 L.1664       758  LOAD_FAST                'data'
              760  LOAD_STR                 'catalogMetadata'
              762  BINARY_SUBSCR    
              764  LOAD_STR                 'catalog'
              766  BINARY_SUBSCR    
              768  LOAD_STR                 'episodeNumber'
              770  BINARY_SUBSCR    
              772  STORE_FAST               'NumEpisode'

 L.1665       774  LOAD_FAST                'data'
              776  LOAD_STR                 'catalogMetadata'
              778  BINARY_SUBSCR    
              780  LOAD_STR                 'family'
              782  BINARY_SUBSCR    
              784  LOAD_STR                 'tvAncestors'
              786  BINARY_SUBSCR    
              788  LOAD_CONST               0
              790  BINARY_SUBSCR    
              792  LOAD_STR                 'catalog'
              794  BINARY_SUBSCR    
              796  LOAD_STR                 'seasonNumber'
              798  BINARY_SUBSCR    
              800  STORE_FAST               'NumSeason'

 L.1666       802  LOAD_GLOBAL              args
              804  LOAD_ATTR                titlecustom
              806  POP_JUMP_IF_FALSE   826  'to 826'

 L.1667       810  LOAD_GLOBAL              ReplaceDontLikeWord
              812  LOAD_GLOBAL              args
              814  LOAD_ATTR                titlecustom
              816  LOAD_CONST               0
              818  BINARY_SUBSCR    
              820  CALL_FUNCTION_1       1  '1 positional argument'
              822  STORE_FAST               'SerieTitle'
              824  JUMP_FORWARD        922  'to 922'
              826  ELSE                     '922'

 L.1669       826  SETUP_EXCEPT        864  'to 864'

 L.1670       828  LOAD_GLOBAL              ReplaceDontLikeWord

 L.1671       830  LOAD_FAST                'data'
              832  LOAD_STR                 'catalogMetadata'
              834  BINARY_SUBSCR    
              836  LOAD_STR                 'family'
              838  BINARY_SUBSCR    
              840  LOAD_STR                 'tvAncestors'
              842  BINARY_SUBSCR    
              844  LOAD_CONST               1
              846  BINARY_SUBSCR    
              848  LOAD_STR                 'catalog'
              850  BINARY_SUBSCR    
              852  LOAD_STR                 'title'
              854  BINARY_SUBSCR    
              856  CALL_FUNCTION_1       1  '1 positional argument'
              858  STORE_FAST               'SerieTitle'
              860  POP_BLOCK        
              862  JUMP_FORWARD        922  'to 922'
            864_0  COME_FROM_EXCEPT    826  '826'

 L.1672       864  DUP_TOP          
              866  LOAD_GLOBAL              Exception
              868  COMPARE_OP               exception-match
              870  POP_JUMP_IF_FALSE   920  'to 920'
              874  POP_TOP          
              876  POP_TOP          
              878  POP_TOP          

 L.1673       880  LOAD_GLOBAL              ReplaceDontLikeWord
              882  LOAD_GLOBAL              kanji_to_romaji

 L.1674       884  LOAD_FAST                'data'
              886  LOAD_STR                 'catalogMetadata'
              888  BINARY_SUBSCR    
              890  LOAD_STR                 'family'
              892  BINARY_SUBSCR    
              894  LOAD_STR                 'tvAncestors'
              896  BINARY_SUBSCR    
              898  LOAD_CONST               1
              900  BINARY_SUBSCR    
              902  LOAD_STR                 'catalog'
              904  BINARY_SUBSCR    
              906  LOAD_STR                 'title'
              908  BINARY_SUBSCR    
              910  CALL_FUNCTION_1       1  '1 positional argument'
              912  CALL_FUNCTION_1       1  '1 positional argument'
              914  STORE_FAST               'SerieTitle'
              916  POP_EXCEPT       
              918  JUMP_FORWARD        922  'to 922'
              920  END_FINALLY      
            922_0  COME_FROM           918  '918'
            922_1  COME_FROM           862  '862'
            922_2  COME_FROM           824  '824'

 L.1676       922  LOAD_GLOBAL              int
              924  LOAD_FAST                'NumSeason'
              926  CALL_FUNCTION_1       1  '1 positional argument'
              928  LOAD_CONST               10
              930  COMPARE_OP               >=
              932  POP_JUMP_IF_FALSE  1260  'to 1260'

 L.1677       936  LOAD_GLOBAL              int
              938  LOAD_FAST                'NumEpisode'
              940  CALL_FUNCTION_1       1  '1 positional argument'
              942  LOAD_CONST               10
              944  COMPARE_OP               >=
              946  POP_JUMP_IF_FALSE  1104  'to 1104'

 L.1678       950  LOAD_FAST                'bonus'
              952  LOAD_CONST               True
              954  COMPARE_OP               ==
              956  POP_JUMP_IF_FALSE  1030  'to 1030'

 L.1679       960  LOAD_FAST                'SerieTitle'
              962  LOAD_STR                 ' S'
              964  BINARY_ADD       
              966  LOAD_GLOBAL              str
              968  LOAD_FAST                'NumSeason'
              970  CALL_FUNCTION_1       1  '1 positional argument'
              972  BINARY_ADD       
              974  LOAD_STR                 ' - '
              976  BINARY_ADD       
              978  LOAD_FAST                'titleBonus'
              980  BINARY_ADD       
              982  STORE_FAST               'seriesName2'

 L.1680       984  LOAD_FAST                'SerieTitle'
              986  LOAD_STR                 ' S'
              988  BINARY_ADD       
              990  LOAD_GLOBAL              str
              992  LOAD_FAST                'NumSeason'
              994  CALL_FUNCTION_1       1  '1 positional argument'
              996  BINARY_ADD       
              998  LOAD_STR                 'E0'
             1000  BINARY_ADD       
             1002  LOAD_GLOBAL              str
             1004  LOAD_FAST                'NumEpisode'
             1006  CALL_FUNCTION_1       1  '1 positional argument'
             1008  BINARY_ADD       
             1010  STORE_DEREF              'seriesName'

 L.1681      1012  LOAD_FAST                'SerieTitle'
             1014  LOAD_STR                 ' S'
             1016  BINARY_ADD       
             1018  LOAD_GLOBAL              str
             1020  LOAD_FAST                'NumSeason'
             1022  CALL_FUNCTION_1       1  '1 positional argument'
             1024  BINARY_ADD       
             1026  STORE_FAST               'seriesName3'
             1028  JUMP_FORWARD       1102  'to 1102'
             1030  ELSE                     '1102'

 L.1683      1030  LOAD_FAST                'SerieTitle'
             1032  LOAD_STR                 ' S'
             1034  BINARY_ADD       
             1036  LOAD_GLOBAL              str
             1038  LOAD_FAST                'NumSeason'
             1040  CALL_FUNCTION_1       1  '1 positional argument'
             1042  BINARY_ADD       
             1044  LOAD_STR                 'E0'
             1046  BINARY_ADD       
             1048  LOAD_GLOBAL              str
             1050  LOAD_FAST                'NumEpisode'
             1052  CALL_FUNCTION_1       1  '1 positional argument'
             1054  BINARY_ADD       
             1056  STORE_FAST               'seriesName2'

 L.1684      1058  LOAD_FAST                'SerieTitle'
             1060  LOAD_STR                 ' S'
             1062  BINARY_ADD       
             1064  LOAD_GLOBAL              str
             1066  LOAD_FAST                'NumSeason'
             1068  CALL_FUNCTION_1       1  '1 positional argument'
             1070  BINARY_ADD       
             1072  LOAD_STR                 'E0'
             1074  BINARY_ADD       
             1076  LOAD_GLOBAL              str
             1078  LOAD_FAST                'NumEpisode'
             1080  CALL_FUNCTION_1       1  '1 positional argument'
             1082  BINARY_ADD       
             1084  STORE_DEREF              'seriesName'

 L.1685      1086  LOAD_FAST                'SerieTitle'
             1088  LOAD_STR                 ' S'
             1090  BINARY_ADD       
             1092  LOAD_GLOBAL              str
             1094  LOAD_FAST                'NumSeason'
             1096  CALL_FUNCTION_1       1  '1 positional argument'
             1098  BINARY_ADD       
             1100  STORE_FAST               'seriesName3'
           1102_0  COME_FROM          1028  '1028'
             1102  JUMP_FORWARD       1256  'to 1256'
             1104  ELSE                     '1256'

 L.1687      1104  LOAD_FAST                'bonus'
             1106  LOAD_CONST               True
             1108  COMPARE_OP               ==
             1110  POP_JUMP_IF_FALSE  1184  'to 1184'

 L.1688      1114  LOAD_FAST                'SerieTitle'
             1116  LOAD_STR                 ' S'
             1118  BINARY_ADD       
             1120  LOAD_GLOBAL              str
             1122  LOAD_FAST                'NumSeason'
             1124  CALL_FUNCTION_1       1  '1 positional argument'
             1126  BINARY_ADD       
             1128  LOAD_STR                 ' - '
             1130  BINARY_ADD       
             1132  LOAD_FAST                'titleBonus'
             1134  BINARY_ADD       
             1136  STORE_FAST               'seriesName2'

 L.1689      1138  LOAD_FAST                'SerieTitle'
             1140  LOAD_STR                 ' S'
             1142  BINARY_ADD       
             1144  LOAD_GLOBAL              str
             1146  LOAD_FAST                'NumSeason'
             1148  CALL_FUNCTION_1       1  '1 positional argument'
             1150  BINARY_ADD       
             1152  LOAD_STR                 'E0'
             1154  BINARY_ADD       
             1156  LOAD_GLOBAL              str
             1158  LOAD_FAST                'NumEpisode'
             1160  CALL_FUNCTION_1       1  '1 positional argument'
             1162  BINARY_ADD       
             1164  STORE_DEREF              'seriesName'

 L.1690      1166  LOAD_FAST                'SerieTitle'
             1168  LOAD_STR                 ' S'
             1170  BINARY_ADD       
             1172  LOAD_GLOBAL              str
             1174  LOAD_FAST                'NumSeason'
             1176  CALL_FUNCTION_1       1  '1 positional argument'
             1178  BINARY_ADD       
             1180  STORE_FAST               'seriesName3'
             1182  JUMP_FORWARD       1256  'to 1256'
             1184  ELSE                     '1256'

 L.1692      1184  LOAD_FAST                'SerieTitle'
             1186  LOAD_STR                 ' S'
             1188  BINARY_ADD       
             1190  LOAD_GLOBAL              str
             1192  LOAD_FAST                'NumSeason'
             1194  CALL_FUNCTION_1       1  '1 positional argument'
             1196  BINARY_ADD       
             1198  LOAD_STR                 'E0'
             1200  BINARY_ADD       
             1202  LOAD_GLOBAL              str
             1204  LOAD_FAST                'NumEpisode'
             1206  CALL_FUNCTION_1       1  '1 positional argument'
             1208  BINARY_ADD       
             1210  STORE_FAST               'seriesName2'

 L.1693      1212  LOAD_FAST                'SerieTitle'
             1214  LOAD_STR                 ' S'
             1216  BINARY_ADD       
             1218  LOAD_GLOBAL              str
             1220  LOAD_FAST                'NumSeason'
             1222  CALL_FUNCTION_1       1  '1 positional argument'
             1224  BINARY_ADD       
             1226  LOAD_STR                 'E0'
             1228  BINARY_ADD       
             1230  LOAD_GLOBAL              str
             1232  LOAD_FAST                'NumEpisode'
             1234  CALL_FUNCTION_1       1  '1 positional argument'
             1236  BINARY_ADD       
             1238  STORE_DEREF              'seriesName'

 L.1694      1240  LOAD_FAST                'SerieTitle'
             1242  LOAD_STR                 ' S'
             1244  BINARY_ADD       
             1246  LOAD_GLOBAL              str
             1248  LOAD_FAST                'NumSeason'
             1250  CALL_FUNCTION_1       1  '1 positional argument'
             1252  BINARY_ADD       
             1254  STORE_FAST               'seriesName3'
           1256_0  COME_FROM          1182  '1182'
           1256_1  COME_FROM          1102  '1102'
             1256  JUMP_FORWARD       1580  'to 1580'
             1260  ELSE                     '1580'

 L.1696      1260  LOAD_GLOBAL              int
             1262  LOAD_FAST                'NumEpisode'
             1264  CALL_FUNCTION_1       1  '1 positional argument'
             1266  LOAD_CONST               10
             1268  COMPARE_OP               >=
             1270  POP_JUMP_IF_FALSE  1428  'to 1428'

 L.1697      1274  LOAD_FAST                'bonus'
             1276  LOAD_CONST               True
             1278  COMPARE_OP               ==
             1280  POP_JUMP_IF_FALSE  1354  'to 1354'

 L.1698      1284  LOAD_FAST                'SerieTitle'
             1286  LOAD_STR                 ' S0'
             1288  BINARY_ADD       
             1290  LOAD_GLOBAL              str
             1292  LOAD_FAST                'NumSeason'
             1294  CALL_FUNCTION_1       1  '1 positional argument'
             1296  BINARY_ADD       
             1298  LOAD_STR                 ' - '
             1300  BINARY_ADD       
             1302  LOAD_FAST                'titleBonus'
             1304  BINARY_ADD       
             1306  STORE_FAST               'seriesName2'

 L.1699      1308  LOAD_FAST                'SerieTitle'
             1310  LOAD_STR                 ' S0'
             1312  BINARY_ADD       
             1314  LOAD_GLOBAL              str
             1316  LOAD_FAST                'NumSeason'
             1318  CALL_FUNCTION_1       1  '1 positional argument'
             1320  BINARY_ADD       
             1322  LOAD_STR                 'E'
             1324  BINARY_ADD       
             1326  LOAD_GLOBAL              str
             1328  LOAD_FAST                'NumEpisode'
             1330  CALL_FUNCTION_1       1  '1 positional argument'
             1332  BINARY_ADD       
             1334  STORE_DEREF              'seriesName'

 L.1700      1336  LOAD_FAST                'SerieTitle'
             1338  LOAD_STR                 ' S0'
             1340  BINARY_ADD       
             1342  LOAD_GLOBAL              str
             1344  LOAD_FAST                'NumSeason'
             1346  CALL_FUNCTION_1       1  '1 positional argument'
             1348  BINARY_ADD       
             1350  STORE_FAST               'seriesName3'
             1352  JUMP_FORWARD       1426  'to 1426'
             1354  ELSE                     '1426'

 L.1702      1354  LOAD_FAST                'SerieTitle'
             1356  LOAD_STR                 ' S0'
             1358  BINARY_ADD       
             1360  LOAD_GLOBAL              str
             1362  LOAD_FAST                'NumSeason'
             1364  CALL_FUNCTION_1       1  '1 positional argument'
             1366  BINARY_ADD       
             1368  LOAD_STR                 'E'
             1370  BINARY_ADD       
             1372  LOAD_GLOBAL              str
             1374  LOAD_FAST                'NumEpisode'
             1376  CALL_FUNCTION_1       1  '1 positional argument'
             1378  BINARY_ADD       
             1380  STORE_FAST               'seriesName2'

 L.1703      1382  LOAD_FAST                'SerieTitle'
             1384  LOAD_STR                 ' S0'
             1386  BINARY_ADD       
             1388  LOAD_GLOBAL              str
             1390  LOAD_FAST                'NumSeason'
             1392  CALL_FUNCTION_1       1  '1 positional argument'
             1394  BINARY_ADD       
             1396  LOAD_STR                 'E'
             1398  BINARY_ADD       
             1400  LOAD_GLOBAL              str
             1402  LOAD_FAST                'NumEpisode'
             1404  CALL_FUNCTION_1       1  '1 positional argument'
             1406  BINARY_ADD       
             1408  STORE_DEREF              'seriesName'

 L.1704      1410  LOAD_FAST                'SerieTitle'
             1412  LOAD_STR                 ' S0'
             1414  BINARY_ADD       
             1416  LOAD_GLOBAL              str
             1418  LOAD_FAST                'NumSeason'
             1420  CALL_FUNCTION_1       1  '1 positional argument'
             1422  BINARY_ADD       
             1424  STORE_FAST               'seriesName3'
           1426_0  COME_FROM          1352  '1352'
             1426  JUMP_FORWARD       1580  'to 1580'
             1428  ELSE                     '1580'

 L.1706      1428  LOAD_FAST                'bonus'
             1430  LOAD_CONST               True
             1432  COMPARE_OP               ==
             1434  POP_JUMP_IF_FALSE  1508  'to 1508'

 L.1707      1438  LOAD_FAST                'SerieTitle'
             1440  LOAD_STR                 ' S0'
             1442  BINARY_ADD       
             1444  LOAD_GLOBAL              str
             1446  LOAD_FAST                'NumSeason'
             1448  CALL_FUNCTION_1       1  '1 positional argument'
             1450  BINARY_ADD       
             1452  LOAD_STR                 ' - '
             1454  BINARY_ADD       
             1456  LOAD_FAST                'titleBonus'
             1458  BINARY_ADD       
             1460  STORE_FAST               'seriesName2'

 L.1708      1462  LOAD_FAST                'SerieTitle'
             1464  LOAD_STR                 ' S0'
             1466  BINARY_ADD       
             1468  LOAD_GLOBAL              str
             1470  LOAD_FAST                'NumSeason'
             1472  CALL_FUNCTION_1       1  '1 positional argument'
             1474  BINARY_ADD       
             1476  LOAD_STR                 'E0'
             1478  BINARY_ADD       
             1480  LOAD_GLOBAL              str
             1482  LOAD_FAST                'NumEpisode'
             1484  CALL_FUNCTION_1       1  '1 positional argument'
             1486  BINARY_ADD       
             1488  STORE_DEREF              'seriesName'

 L.1709      1490  LOAD_FAST                'SerieTitle'
             1492  LOAD_STR                 ' S0'
             1494  BINARY_ADD       
             1496  LOAD_GLOBAL              str
             1498  LOAD_FAST                'NumSeason'
             1500  CALL_FUNCTION_1       1  '1 positional argument'
             1502  BINARY_ADD       
             1504  STORE_FAST               'seriesName3'
             1506  JUMP_FORWARD       1580  'to 1580'
             1508  ELSE                     '1580'

 L.1711      1508  LOAD_FAST                'SerieTitle'
             1510  LOAD_STR                 ' S0'
             1512  BINARY_ADD       
             1514  LOAD_GLOBAL              str
             1516  LOAD_FAST                'NumSeason'
             1518  CALL_FUNCTION_1       1  '1 positional argument'
             1520  BINARY_ADD       
             1522  LOAD_STR                 'E0'
             1524  BINARY_ADD       
             1526  LOAD_GLOBAL              str
             1528  LOAD_FAST                'NumEpisode'
             1530  CALL_FUNCTION_1       1  '1 positional argument'
             1532  BINARY_ADD       
             1534  STORE_FAST               'seriesName2'

 L.1712      1536  LOAD_FAST                'SerieTitle'
             1538  LOAD_STR                 ' S0'
             1540  BINARY_ADD       
             1542  LOAD_GLOBAL              str
             1544  LOAD_FAST                'NumSeason'
             1546  CALL_FUNCTION_1       1  '1 positional argument'
             1548  BINARY_ADD       
             1550  LOAD_STR                 'E0'
             1552  BINARY_ADD       
             1554  LOAD_GLOBAL              str
             1556  LOAD_FAST                'NumEpisode'
             1558  CALL_FUNCTION_1       1  '1 positional argument'
             1560  BINARY_ADD       
             1562  STORE_DEREF              'seriesName'

 L.1713      1564  LOAD_FAST                'SerieTitle'
             1566  LOAD_STR                 ' S0'
             1568  BINARY_ADD       
             1570  LOAD_GLOBAL              str
             1572  LOAD_FAST                'NumSeason'
             1574  CALL_FUNCTION_1       1  '1 positional argument'
             1576  BINARY_ADD       
             1578  STORE_FAST               'seriesName3'
           1580_0  COME_FROM          1506  '1506'
           1580_1  COME_FROM          1426  '1426'
           1580_2  COME_FROM          1256  '1256'
           1580_3  COME_FROM           656  '656'

 L.1715      1580  LOAD_FAST                'amazonType'
             1582  LOAD_STR                 'movie'
             1584  COMPARE_OP               ==
             1586  POP_JUMP_IF_FALSE  1702  'to 1702'

 L.1716      1590  LOAD_GLOBAL              args
             1592  LOAD_ATTR                titlecustom
             1594  POP_JUMP_IF_FALSE  1614  'to 1614'

 L.1717      1598  LOAD_GLOBAL              ReplaceDontLikeWord
             1600  LOAD_GLOBAL              args
             1602  LOAD_ATTR                titlecustom
             1604  LOAD_CONST               0
             1606  BINARY_SUBSCR    
             1608  CALL_FUNCTION_1       1  '1 positional argument'
             1610  STORE_FAST               'SerieTitle'
             1612  JUMP_FORWARD       1694  'to 1694'
             1614  ELSE                     '1694'

 L.1719      1614  SETUP_EXCEPT       1640  'to 1640'

 L.1720      1616  LOAD_GLOBAL              ReplaceDontLikeWord
             1618  LOAD_FAST                'data'
             1620  LOAD_STR                 'catalogMetadata'
             1622  BINARY_SUBSCR    
             1624  LOAD_STR                 'catalog'
             1626  BINARY_SUBSCR    
             1628  LOAD_STR                 'title'
             1630  BINARY_SUBSCR    
             1632  CALL_FUNCTION_1       1  '1 positional argument'
             1634  STORE_FAST               'SerieTitle'
             1636  POP_BLOCK        
             1638  JUMP_FORWARD       1686  'to 1686'
           1640_0  COME_FROM_EXCEPT   1614  '1614'

 L.1721      1640  DUP_TOP          
             1642  LOAD_GLOBAL              Exception
             1644  COMPARE_OP               exception-match
             1646  POP_JUMP_IF_FALSE  1684  'to 1684'
             1650  POP_TOP          
             1652  POP_TOP          
             1654  POP_TOP          

 L.1722      1656  LOAD_GLOBAL              ReplaceDontLikeWord
             1658  LOAD_GLOBAL              kanji_to_romaji
             1660  LOAD_FAST                'data'
             1662  LOAD_STR                 'catalogMetadata'
             1664  BINARY_SUBSCR    
             1666  LOAD_STR                 'catalog'
             1668  BINARY_SUBSCR    
             1670  LOAD_STR                 'title'
             1672  BINARY_SUBSCR    
             1674  CALL_FUNCTION_1       1  '1 positional argument'
             1676  CALL_FUNCTION_1       1  '1 positional argument'
             1678  STORE_FAST               'SerieTitle'
             1680  POP_EXCEPT       
             1682  JUMP_FORWARD       1686  'to 1686'
             1684  END_FINALLY      
           1686_0  COME_FROM          1682  '1682'
           1686_1  COME_FROM          1638  '1638'

 L.1724      1686  LOAD_FAST                'SerieTitle'
             1688  STORE_DEREF              'seriesName'

 L.1725      1690  LOAD_FAST                'SerieTitle'
             1692  STORE_FAST               'seriesName2'
           1694_0  COME_FROM          1612  '1612'

 L.1726      1694  LOAD_GLOBAL              args
             1696  LOAD_ATTR                nochpaters
             1698  POP_JUMP_IF_TRUE   1702  'to 1702'
           1702_0  COME_FROM          1698  '1698'
           1702_1  COME_FROM          1586  '1586'

 L.1728      1702  SETUP_EXCEPT       1744  'to 1744'

 L.1729      1704  LOAD_FAST                'data'
             1706  LOAD_STR                 'returnedTitleRendition'
             1708  BINARY_SUBSCR    
             1710  LOAD_STR                 'contentId'
             1712  BINARY_SUBSCR    
             1714  STORE_FAST               'contentId'

 L.1730      1716  LOAD_STR                 '{"consumptionType":"Streaming","deviceClass":"normal","playbackMode":"playback","vcid":"'
             1718  LOAD_FAST                'contentId'
             1720  BINARY_ADD       
             1722  LOAD_STR                 '"}'
             1724  BINARY_ADD       
             1726  STORE_GLOBAL             serviceToken

 L.1731      1728  LOAD_GLOBAL              getXray
             1730  LOAD_DEREF               'asin'
             1732  LOAD_GLOBAL              clientId
             1734  LOAD_GLOBAL              serviceToken
             1736  CALL_FUNCTION_3       3  '3 positional arguments'
             1738  STORE_FAST               'data2'
             1740  POP_BLOCK        
             1742  JUMP_FORWARD       1770  'to 1770'
           1744_0  COME_FROM_EXCEPT   1702  '1702'

 L.1732      1744  DUP_TOP          
             1746  LOAD_GLOBAL              Exception
             1748  COMPARE_OP               exception-match
             1750  POP_JUMP_IF_FALSE  1768  'to 1768'
             1754  POP_TOP          
             1756  POP_TOP          
             1758  POP_TOP          

 L.1733      1760  LOAD_CONST               True
             1762  STORE_FAST               'nochapters'
             1764  POP_EXCEPT       
             1766  JUMP_FORWARD       1770  'to 1770'
             1768  END_FINALLY      
           1770_0  COME_FROM          1766  '1766'
           1770_1  COME_FROM          1742  '1742'

 L.1735      1770  LOAD_FAST                'nochapters'
             1772  LOAD_CONST               False
             1774  COMPARE_OP               ==
             1776  POP_JUMP_IF_FALSE  2046  'to 2046'

 L.1736      1780  BUILD_LIST_0          0 
             1782  STORE_FAST               'ChapterList'

 L.1737      1784  SETUP_EXCEPT       2020  'to 2020'

 L.1738      1786  SETUP_LOOP         1952  'to 1952'
             1788  LOAD_FAST                'data2'
             1790  LOAD_STR                 'page'
             1792  BINARY_SUBSCR    
             1794  LOAD_STR                 'sections'
             1796  BINARY_SUBSCR    
             1798  LOAD_STR                 'center'
             1800  BINARY_SUBSCR    
             1802  LOAD_STR                 'widgets'
             1804  BINARY_SUBSCR    
             1806  LOAD_STR                 'widgetList'
             1808  BINARY_SUBSCR    
             1810  GET_ITER         
             1812  FOR_ITER           1950  'to 1950'
             1814  STORE_FAST               'x'

 L.1739      1816  LOAD_FAST                'x'
             1818  LOAD_STR                 'tabType'
             1820  BINARY_SUBSCR    
             1822  LOAD_STR                 'scenesTab'
             1824  COMPARE_OP               ==
             1826  POP_JUMP_IF_FALSE  1812  'to 1812'

 L.1740      1830  SETUP_LOOP         1946  'to 1946'
             1832  LOAD_FAST                'x'
             1834  LOAD_STR                 'widgets'
             1836  BINARY_SUBSCR    
             1838  LOAD_STR                 'widgetList'
             1840  BINARY_SUBSCR    
             1842  GET_ITER         
             1844  FOR_ITER           1944  'to 1944'
             1846  STORE_FAST               'y'

 L.1741      1848  LOAD_FAST                'y'
             1850  LOAD_STR                 'items'
             1852  BINARY_SUBSCR    
             1854  LOAD_STR                 'itemList'
             1856  BINARY_SUBSCR    
             1858  LOAD_CONST               0
             1860  BINARY_SUBSCR    
             1862  LOAD_STR                 'blueprint'
             1864  BINARY_SUBSCR    
             1866  LOAD_STR                 'id'
             1868  BINARY_SUBSCR    
             1870  LOAD_STR                 'XraySceneItem'
             1872  COMPARE_OP               ==
             1874  POP_JUMP_IF_FALSE  1844  'to 1844'

 L.1742      1878  SETUP_LOOP         1940  'to 1940'
             1880  LOAD_FAST                'y'
             1882  LOAD_STR                 'items'
             1884  BINARY_SUBSCR    
             1886  LOAD_STR                 'itemList'
             1888  BINARY_SUBSCR    
             1890  GET_ITER         
             1892  FOR_ITER           1938  'to 1938'
             1894  STORE_FAST               'z'

 L.1744      1896  LOAD_FAST                'z'
             1898  LOAD_STR                 'textMap'
             1900  BINARY_SUBSCR    
             1902  LOAD_STR                 'PRIMARY'
             1904  BINARY_SUBSCR    
             1906  LOAD_GLOBAL              ReplaceChapters
             1908  LOAD_FAST                'z'
             1910  LOAD_STR                 'textMap'
             1912  BINARY_SUBSCR    
             1914  LOAD_STR                 'TERTIARY'
             1916  BINARY_SUBSCR    
             1918  CALL_FUNCTION_1       1  '1 positional argument'
             1920  BUILD_TUPLE_2         2 
             1922  STORE_FAST               'ChapterDict'

 L.1745      1924  LOAD_FAST                'ChapterList'
             1926  LOAD_ATTR                append
             1928  LOAD_FAST                'ChapterDict'
             1930  CALL_FUNCTION_1       1  '1 positional argument'
             1932  POP_TOP          
             1934  JUMP_BACK          1892  'to 1892'
             1938  POP_BLOCK        
           1940_0  COME_FROM_LOOP     1878  '1878'
             1940  JUMP_BACK          1844  'to 1844'
             1944  POP_BLOCK        
           1946_0  COME_FROM_LOOP     1830  '1830'
             1946  JUMP_BACK          1812  'to 1812'
             1950  POP_BLOCK        
           1952_0  COME_FROM_LOOP     1786  '1786'

 L.1747      1952  LOAD_GLOBAL              defaultdict
             1954  LOAD_GLOBAL              list
             1956  CALL_FUNCTION_1       1  '1 positional argument'
             1958  STORE_FAST               'ChaptersList_new'

 L.1748      1960  SETUP_LOOP         1994  'to 1994'
             1962  LOAD_FAST                'ChapterList'
             1964  GET_ITER         
             1966  FOR_ITER           1992  'to 1992'
             1968  UNPACK_SEQUENCE_2     2 
             1970  STORE_FAST               'ChapterName'
             1972  STORE_FAST               'ChapterTime'

 L.1749      1974  LOAD_FAST                'ChaptersList_new'
             1976  LOAD_FAST                'ChapterName'
             1978  BINARY_SUBSCR    
             1980  LOAD_ATTR                append
             1982  LOAD_FAST                'ChapterTime'
             1984  CALL_FUNCTION_1       1  '1 positional argument'
             1986  POP_TOP          
             1988  JUMP_BACK          1966  'to 1966'
             1992  POP_BLOCK        
           1994_0  COME_FROM_LOOP     1960  '1960'

 L.1751      1994  LOAD_GLOBAL              str
             1996  LOAD_FAST                'ChaptersList_new'
             1998  LOAD_ATTR                items
             2000  CALL_FUNCTION_0       0  '0 positional arguments'
             2002  CALL_FUNCTION_1       1  '1 positional argument'
             2004  LOAD_STR                 'dict_items([])'
             2006  COMPARE_OP               ==
             2008  POP_JUMP_IF_FALSE  2016  'to 2016'

 L.1752      2012  LOAD_CONST               True
             2014  STORE_FAST               'nochapters'
           2016_0  COME_FROM          2008  '2008'
             2016  POP_BLOCK        
             2018  JUMP_FORWARD       2046  'to 2046'
           2020_0  COME_FROM_EXCEPT   1784  '1784'

 L.1753      2020  DUP_TOP          
             2022  LOAD_GLOBAL              Exception
             2024  COMPARE_OP               exception-match
             2026  POP_JUMP_IF_FALSE  2044  'to 2044'
             2030  POP_TOP          
             2032  POP_TOP          
             2034  POP_TOP          

 L.1754      2036  LOAD_CONST               True
             2038  STORE_FAST               'nochapters'
             2040  POP_EXCEPT       
             2042  JUMP_FORWARD       2046  'to 2046'
             2044  END_FINALLY      
           2046_0  COME_FROM          2042  '2042'
           2046_1  COME_FROM          2018  '2018'
           2046_2  COME_FROM          1776  '1776'

 L.1756      2046  BUILD_LIST_0          0 
             2048  STORE_GLOBAL             AudioListAll

 L.1757      2050  LOAD_CONST               False
             2052  STORE_DEREF              'OnlyOneAudio'

 L.1758      2054  LOAD_CONST               False
             2056  STORE_FAST               'Error_Not_Available'

 L.1759      2058  SETUP_EXCEPT       2212  'to 2212'

 L.1760      2060  SETUP_LOOP         2178  'to 2178'
             2062  LOAD_FAST                'data'
             2064  LOAD_STR                 'audioVideoUrls'
             2066  BINARY_SUBSCR    
             2068  LOAD_STR                 'audioTrackMetadata'
             2070  BINARY_SUBSCR    
             2072  GET_ITER         
             2074  FOR_ITER           2176  'to 2176'
             2076  STORE_FAST               'audios_track'

 L.1761      2078  SETUP_EXCEPT       2112  'to 2112'

 L.1762      2080  LOAD_FAST                'audios_track'
             2082  LOAD_STR                 'languageCode'
             2084  BINARY_SUBSCR    

 L.1763      2086  LOAD_FAST                'audios_track'
             2088  LOAD_STR                 'displayName'
             2090  BINARY_SUBSCR    

 L.1764      2092  LOAD_GLOBAL              ReplaceCodeLanguages
             2094  LOAD_FAST                'audios_track'
             2096  LOAD_STR                 'audioTrackId'
             2098  BINARY_SUBSCR    
             2100  CALL_FUNCTION_1       1  '1 positional argument'
             2102  LOAD_CONST               ('AudioCode', 'AudioName', 'AudioID')
             2104  BUILD_CONST_KEY_MAP_3     3 
             2106  STORE_FAST               'AudioListDict'
             2108  POP_BLOCK        
             2110  JUMP_FORWARD       2162  'to 2162'
           2112_0  COME_FROM_EXCEPT   2078  '2078'

 L.1765      2112  DUP_TOP          
             2114  LOAD_GLOBAL              Exception
             2116  COMPARE_OP               exception-match
             2118  POP_JUMP_IF_FALSE  2160  'to 2160'
             2122  POP_TOP          
             2124  POP_TOP          
             2126  POP_TOP          

 L.1766      2128  LOAD_FAST                'audios_track'
             2130  LOAD_STR                 'languageCode'
             2132  BINARY_SUBSCR    

 L.1767      2134  LOAD_FAST                'audios_track'
             2136  LOAD_STR                 'displayName'
             2138  BINARY_SUBSCR    

 L.1768      2140  LOAD_GLOBAL              ReplaceCodeLanguages
             2142  LOAD_FAST                'audios_track'
             2144  LOAD_STR                 'languageCode'
             2146  BINARY_SUBSCR    
             2148  CALL_FUNCTION_1       1  '1 positional argument'
             2150  LOAD_CONST               ('AudioCode', 'AudioName', 'AudioID')
             2152  BUILD_CONST_KEY_MAP_3     3 
             2154  STORE_FAST               'AudioListDict'
             2156  POP_EXCEPT       
             2158  JUMP_FORWARD       2162  'to 2162'
             2160  END_FINALLY      
           2162_0  COME_FROM          2158  '2158'
           2162_1  COME_FROM          2110  '2110'

 L.1770      2162  LOAD_GLOBAL              AudioListAll
             2164  LOAD_ATTR                append
             2166  LOAD_FAST                'AudioListDict'
             2168  CALL_FUNCTION_1       1  '1 positional argument'
             2170  POP_TOP          
             2172  JUMP_BACK          2074  'to 2074'
             2176  POP_BLOCK        
           2178_0  COME_FROM_LOOP     2060  '2060'

 L.1772      2178  LOAD_GLOBAL              len
             2180  LOAD_GLOBAL              AudioListAll
             2182  CALL_FUNCTION_1       1  '1 positional argument'
             2184  LOAD_CONST               1
             2186  COMPARE_OP               ==
             2188  POP_JUMP_IF_FALSE  2208  'to 2208'

 L.1773      2192  LOAD_CONST               True
             2194  STORE_DEREF              'OnlyOneAudio'

 L.1774      2196  LOAD_GLOBAL              AudioListAll
             2198  LOAD_CONST               0
             2200  BINARY_SUBSCR    
             2202  LOAD_STR                 'AudioID'
             2204  BINARY_SUBSCR    
             2206  STORE_DEREF              'OnlyOneAudioID'
           2208_0  COME_FROM          2188  '2188'
             2208  POP_BLOCK        
             2210  JUMP_FORWARD       2254  'to 2254'
           2212_0  COME_FROM_EXCEPT   2058  '2058'

 L.1776      2212  DUP_TOP          
             2214  LOAD_GLOBAL              KeyError
             2216  COMPARE_OP               exception-match
             2218  POP_JUMP_IF_FALSE  2252  'to 2252'
             2222  POP_TOP          
             2224  POP_TOP          
             2226  POP_TOP          

 L.1777      2228  LOAD_GLOBAL              print
             2230  LOAD_FAST                'data'
             2232  CALL_FUNCTION_1       1  '1 positional argument'
             2234  POP_TOP          

 L.1778      2236  LOAD_GLOBAL              print
             2238  LOAD_STR                 '\nEpisode or Movie not available yet in your region. Possible VPN error.'
             2240  CALL_FUNCTION_1       1  '1 positional argument'
             2242  POP_TOP          

 L.1779      2244  LOAD_CONST               True
             2246  STORE_FAST               'Error_Not_Available'
             2248  POP_EXCEPT       
             2250  JUMP_FORWARD       2254  'to 2254'
             2252  END_FINALLY      
           2254_0  COME_FROM          2250  '2250'
           2254_1  COME_FROM          2210  '2210'

 L.1781      2254  LOAD_CONST               False
             2256  STORE_FAST               'nosubs'

 L.1782      2258  LOAD_CONST               False
             2260  STORE_FAST               'nosubsfor'

 L.1783      2262  LOAD_GLOBAL              args
             2264  LOAD_ATTR                nosubs
             2266  POP_JUMP_IF_FALSE  2280  'to 2280'

 L.1784      2270  LOAD_CONST               True
             2272  STORE_FAST               'nosubs'

 L.1785      2274  LOAD_CONST               True
             2276  STORE_FAST               'nosubsfor'
             2278  JUMP_FORWARD       2288  'to 2288'
             2280  ELSE                     '2288'

 L.1787      2280  LOAD_FAST                'nosubs'
             2282  STORE_FAST               'nosubs'

 L.1788      2284  LOAD_FAST                'nosubs'
             2286  STORE_FAST               'nosubsfor'
           2288_0  COME_FROM          2278  '2278'

 L.1789      2288  BUILD_LIST_0          0 
             2290  STORE_GLOBAL             subsList

 L.1790      2292  BUILD_LIST_0          0 
             2294  STORE_GLOBAL             subsForList

 L.1791      2296  LOAD_GLOBAL              args
             2298  LOAD_ATTR                nosubs
             2300  POP_JUMP_IF_TRUE   2314  'to 2314'

 L.1792      2304  LOAD_FAST                'nosubs'
             2306  LOAD_CONST               True
             2308  COMPARE_OP               !=
             2310  POP_JUMP_IF_FALSE  2314  'to 2314'
           2314_0  COME_FROM          2310  '2310'
           2314_1  COME_FROM          2300  '2300'

 L.1794      2314  SETUP_EXCEPT       2522  'to 2522'

 L.1795      2316  SETUP_LOOP         2518  'to 2518'
             2318  LOAD_FAST                'data'
             2320  LOAD_STR                 'subtitleUrls'
             2322  BINARY_SUBSCR    
             2324  GET_ITER         
             2326  FOR_ITER           2516  'to 2516'
             2328  STORE_FAST               'subs_track'

 L.1796      2330  SETUP_EXCEPT       2370  'to 2370'

 L.1797      2332  LOAD_FAST                'subs_track'
             2334  LOAD_STR                 'languageCode'
             2336  BINARY_SUBSCR    

 L.1798      2338  LOAD_FAST                'subs_track'
             2340  LOAD_STR                 'displayName'
             2342  BINARY_SUBSCR    

 L.1799      2344  LOAD_GLOBAL              ReplaceCodeLanguages
             2346  LOAD_FAST                'subs_track'
             2348  LOAD_STR                 'timedTextTrackId'
             2350  BINARY_SUBSCR    
             2352  CALL_FUNCTION_1       1  '1 positional argument'

 L.1800      2354  LOAD_FAST                'subs_track'
             2356  LOAD_STR                 'url'
             2358  BINARY_SUBSCR    
             2360  LOAD_CONST               ('SubsCode', 'SubsName', 'SubsID', 'subs_urls')
             2362  BUILD_CONST_KEY_MAP_4     4 
             2364  STORE_FAST               'subsDict'
             2366  POP_BLOCK        
             2368  JUMP_FORWARD       2426  'to 2426'
           2370_0  COME_FROM_EXCEPT   2330  '2330'

 L.1801      2370  DUP_TOP          
             2372  LOAD_GLOBAL              Exception
             2374  COMPARE_OP               exception-match
             2376  POP_JUMP_IF_FALSE  2424  'to 2424'
             2380  POP_TOP          
             2382  POP_TOP          
             2384  POP_TOP          

 L.1802      2386  LOAD_FAST                'subs_track'
             2388  LOAD_STR                 'languageCode'
             2390  BINARY_SUBSCR    

 L.1803      2392  LOAD_FAST                'subs_track'
             2394  LOAD_STR                 'displayName'
             2396  BINARY_SUBSCR    

 L.1804      2398  LOAD_GLOBAL              ReplaceCodeLanguages
             2400  LOAD_FAST                'subs_track'
             2402  LOAD_STR                 'languageCode'
             2404  BINARY_SUBSCR    
             2406  CALL_FUNCTION_1       1  '1 positional argument'

 L.1805      2408  LOAD_FAST                'subs_track'
             2410  LOAD_STR                 'url'
             2412  BINARY_SUBSCR    
             2414  LOAD_CONST               ('SubsCode', 'SubsName', 'SubsID', 'subs_urls')
             2416  BUILD_CONST_KEY_MAP_4     4 
             2418  STORE_FAST               'subsDict'
             2420  POP_EXCEPT       
             2422  JUMP_FORWARD       2426  'to 2426'
             2424  END_FINALLY      
           2426_0  COME_FROM          2422  '2422'
           2426_1  COME_FROM          2368  '2368'

 L.1807      2426  LOAD_GLOBAL              args
             2428  LOAD_ATTR                sublang
             2430  POP_JUMP_IF_FALSE  2498  'to 2498'

 L.1808      2434  LOAD_GLOBAL              str
             2436  LOAD_FAST                'subsDict'
             2438  LOAD_STR                 'SubsID'
             2440  BINARY_SUBSCR    
             2442  CALL_FUNCTION_1       1  '1 positional argument'
             2444  LOAD_GLOBAL              list
             2446  LOAD_GLOBAL              args
             2448  LOAD_ATTR                sublang
             2450  CALL_FUNCTION_1       1  '1 positional argument'
             2452  COMPARE_OP               in
             2454  POP_JUMP_IF_FALSE  2468  'to 2468'

 L.1809      2458  LOAD_GLOBAL              subsList
             2460  LOAD_ATTR                append
             2462  LOAD_FAST                'subsDict'
             2464  CALL_FUNCTION_1       1  '1 positional argument'
             2466  POP_TOP          
           2468_0  COME_FROM          2454  '2454'

 L.1810      2468  LOAD_GLOBAL              str
             2470  LOAD_FAST                'subsDict'
             2472  LOAD_STR                 'SubsID'
             2474  BINARY_SUBSCR    
             2476  CALL_FUNCTION_1       1  '1 positional argument'
             2478  LOAD_GLOBAL              list
             2480  LOAD_GLOBAL              args
             2482  LOAD_ATTR                sublang
             2484  CALL_FUNCTION_1       1  '1 positional argument'
             2486  COMPARE_OP               not-in
             2488  POP_JUMP_IF_FALSE  2512  'to 2512'

 L.1811      2492  CONTINUE           2326  'to 2326'
             2496  JUMP_FORWARD       2512  'to 2512'
             2498  ELSE                     '2512'

 L.1813      2498  LOAD_GLOBAL              subsList
             2500  LOAD_ATTR                append
             2502  LOAD_FAST                'subsDict'
             2504  CALL_FUNCTION_1       1  '1 positional argument'
             2506  POP_TOP          

 L.1814      2508  CONTINUE           2326  'to 2326'
           2512_0  COME_FROM          2496  '2496'
           2512_1  COME_FROM          2488  '2488'
             2512  JUMP_BACK          2326  'to 2326'
             2516  POP_BLOCK        
           2518_0  COME_FROM_LOOP     2316  '2316'
             2518  POP_BLOCK        
             2520  JUMP_FORWARD       2548  'to 2548'
           2522_0  COME_FROM_EXCEPT   2314  '2314'

 L.1816      2522  DUP_TOP          
             2524  LOAD_GLOBAL              Exception
             2526  COMPARE_OP               exception-match
             2528  POP_JUMP_IF_FALSE  2546  'to 2546'
             2532  POP_TOP          
             2534  POP_TOP          
             2536  POP_TOP          

 L.1817      2538  LOAD_CONST               True
             2540  STORE_FAST               'nosubs'
             2542  POP_EXCEPT       
             2544  JUMP_FORWARD       2548  'to 2548'
             2546  END_FINALLY      
           2548_0  COME_FROM          2544  '2544'
           2548_1  COME_FROM          2520  '2520'

 L.1819      2548  LOAD_FAST                'nosubsfor'
             2550  LOAD_CONST               True
             2552  COMPARE_OP               !=
             2554  POP_JUMP_IF_FALSE  2792  'to 2792'

 L.1820      2558  SETUP_EXCEPT       2766  'to 2766'

 L.1821      2560  SETUP_LOOP         2762  'to 2762'
             2562  LOAD_FAST                'data'
             2564  LOAD_STR                 'forcedNarratives'
             2566  BINARY_SUBSCR    
             2568  GET_ITER         
             2570  FOR_ITER           2760  'to 2760'
             2572  STORE_FAST               'subsFor_track'

 L.1822      2574  SETUP_EXCEPT       2614  'to 2614'

 L.1823      2576  LOAD_FAST                'subsFor_track'
             2578  LOAD_STR                 'languageCode'
             2580  BINARY_SUBSCR    

 L.1824      2582  LOAD_FAST                'subsFor_track'
             2584  LOAD_STR                 'displayName'
             2586  BINARY_SUBSCR    

 L.1825      2588  LOAD_GLOBAL              ReplaceCodeLanguages
             2590  LOAD_FAST                'subsFor_track'
             2592  LOAD_STR                 'timedTextTrackId'
             2594  BINARY_SUBSCR    
             2596  CALL_FUNCTION_1       1  '1 positional argument'

 L.1826      2598  LOAD_FAST                'subsFor_track'
             2600  LOAD_STR                 'url'
             2602  BINARY_SUBSCR    
             2604  LOAD_CONST               ('SubsForCode', 'SubsForName', 'SubsForID', 'subsFor_urls')
             2606  BUILD_CONST_KEY_MAP_4     4 
             2608  STORE_FAST               'subsForDict'
             2610  POP_BLOCK        
             2612  JUMP_FORWARD       2670  'to 2670'
           2614_0  COME_FROM_EXCEPT   2574  '2574'

 L.1827      2614  DUP_TOP          
             2616  LOAD_GLOBAL              Exception
             2618  COMPARE_OP               exception-match
             2620  POP_JUMP_IF_FALSE  2668  'to 2668'
             2624  POP_TOP          
             2626  POP_TOP          
             2628  POP_TOP          

 L.1828      2630  LOAD_FAST                'subsFor_track'
             2632  LOAD_STR                 'languageCode'
             2634  BINARY_SUBSCR    

 L.1829      2636  LOAD_FAST                'subsFor_track'
             2638  LOAD_STR                 'displayName'
             2640  BINARY_SUBSCR    

 L.1830      2642  LOAD_GLOBAL              ReplaceCodeLanguages
             2644  LOAD_FAST                'subsFor_track'
             2646  LOAD_STR                 'languageCode'
             2648  BINARY_SUBSCR    
             2650  CALL_FUNCTION_1       1  '1 positional argument'

 L.1831      2652  LOAD_FAST                'subsFor_track'
             2654  LOAD_STR                 'url'
             2656  BINARY_SUBSCR    
             2658  LOAD_CONST               ('SubsForCode', 'SubsForName', 'SubsForID', 'subsFor_urls')
             2660  BUILD_CONST_KEY_MAP_4     4 
             2662  STORE_FAST               'subsForDict'
             2664  POP_EXCEPT       
             2666  JUMP_FORWARD       2670  'to 2670'
             2668  END_FINALLY      
           2670_0  COME_FROM          2666  '2666'
           2670_1  COME_FROM          2612  '2612'

 L.1833      2670  LOAD_GLOBAL              args
             2672  LOAD_ATTR                forcedlang
             2674  POP_JUMP_IF_FALSE  2742  'to 2742'

 L.1834      2678  LOAD_GLOBAL              str
             2680  LOAD_FAST                'subsForDict'
             2682  LOAD_STR                 'SubsForID'
             2684  BINARY_SUBSCR    
             2686  CALL_FUNCTION_1       1  '1 positional argument'
             2688  LOAD_GLOBAL              list
             2690  LOAD_GLOBAL              args
             2692  LOAD_ATTR                forcedlang
             2694  CALL_FUNCTION_1       1  '1 positional argument'
             2696  COMPARE_OP               in
             2698  POP_JUMP_IF_FALSE  2712  'to 2712'

 L.1835      2702  LOAD_GLOBAL              subsForList
             2704  LOAD_ATTR                append
             2706  LOAD_FAST                'subsForDict'
             2708  CALL_FUNCTION_1       1  '1 positional argument'
             2710  POP_TOP          
           2712_0  COME_FROM          2698  '2698'

 L.1836      2712  LOAD_GLOBAL              str
             2714  LOAD_FAST                'subsForDict'
             2716  LOAD_STR                 'SubsForID'
             2718  BINARY_SUBSCR    
             2720  CALL_FUNCTION_1       1  '1 positional argument'
             2722  LOAD_GLOBAL              list
             2724  LOAD_GLOBAL              args
             2726  LOAD_ATTR                forcedlang
             2728  CALL_FUNCTION_1       1  '1 positional argument'
             2730  COMPARE_OP               not-in
             2732  POP_JUMP_IF_FALSE  2756  'to 2756'

 L.1837      2736  CONTINUE           2570  'to 2570'
             2740  JUMP_FORWARD       2756  'to 2756'
             2742  ELSE                     '2756'

 L.1839      2742  LOAD_GLOBAL              subsForList
             2744  LOAD_ATTR                append
             2746  LOAD_FAST                'subsForDict'
             2748  CALL_FUNCTION_1       1  '1 positional argument'
             2750  POP_TOP          

 L.1840      2752  CONTINUE           2570  'to 2570'
           2756_0  COME_FROM          2740  '2740'
           2756_1  COME_FROM          2732  '2732'
             2756  JUMP_BACK          2570  'to 2570'
             2760  POP_BLOCK        
           2762_0  COME_FROM_LOOP     2560  '2560'
             2762  POP_BLOCK        
             2764  JUMP_FORWARD       2792  'to 2792'
           2766_0  COME_FROM_EXCEPT   2558  '2558'

 L.1842      2766  DUP_TOP          
             2768  LOAD_GLOBAL              Exception
             2770  COMPARE_OP               exception-match
             2772  POP_JUMP_IF_FALSE  2790  'to 2790'
             2776  POP_TOP          
             2778  POP_TOP          
             2780  POP_TOP          

 L.1843      2782  LOAD_CONST               True
             2784  STORE_FAST               'nosubsfor'
             2786  POP_EXCEPT       
             2788  JUMP_FORWARD       2792  'to 2792'
             2790  END_FINALLY      
           2792_0  COME_FROM          2788  '2788'
           2792_1  COME_FROM          2764  '2764'
           2792_2  COME_FROM          2554  '2554'

 L.1845      2792  LOAD_FAST                'Error_Not_Available'
             2794  LOAD_CONST               False
             2796  COMPARE_OP               ==
             2798  POP_JUMP_IF_FALSE  3062  'to 3062'

 L.1846      2802  LOAD_GLOBAL              print
             2804  LOAD_STR                 '\nGetting MPD...'
             2806  CALL_FUNCTION_1       1  '1 positional argument'
             2808  POP_TOP          

 L.1847      2810  LOAD_FAST                'GettingMPD'
             2812  LOAD_FAST                'data'
             2814  CALL_FUNCTION_1       1  '1 positional argument'
             2816  UNPACK_SEQUENCE_3     3 
             2818  STORE_FAST               'mpd_url'
             2820  STORE_FAST               'base_url'
             2822  STORE_FAST               'mpd'

 L.1849      2824  LOAD_GLOBAL              print
             2826  LOAD_STR                 '\nParsing MPD...'
             2828  CALL_FUNCTION_1       1  '1 positional argument'
             2830  POP_TOP          

 L.1850      2832  LOAD_GLOBAL              args
             2834  LOAD_ATTR                customquality
             2836  POP_JUMP_IF_FALSE  2856  'to 2856'

 L.1851      2840  LOAD_GLOBAL              str
             2842  LOAD_GLOBAL              args
             2844  LOAD_ATTR                customquality
             2846  LOAD_CONST               0
             2848  BINARY_SUBSCR    
             2850  CALL_FUNCTION_1       1  '1 positional argument'
             2852  STORE_FAST               'height'
             2854  JUMP_FORWARD       2860  'to 2860'
             2856  ELSE                     '2860'

 L.1853      2856  LOAD_CONST               None
             2858  STORE_FAST               'height'
           2860_0  COME_FROM          2854  '2854'

 L.1855      2860  LOAD_FAST                'ParsingMPD'
             2862  LOAD_FAST                'mpd'
             2864  LOAD_FAST                'height'
             2866  CALL_FUNCTION_2       2  '2 positional arguments'
             2868  UNPACK_SEQUENCE_6     6 
             2870  STORE_FAST               'height_all'
             2872  STORE_FAST               'video_urls'
             2874  STORE_FAST               'audioList'
             2876  STORE_FAST               'novideo'
             2878  STORE_DEREF              'video_pssh'
             2880  STORE_DEREF              'audio_pssh'

 L.1856      2882  LOAD_GLOBAL              alphanumericSort
             2884  LOAD_GLOBAL              list
             2886  LOAD_GLOBAL              set
             2888  LOAD_FAST                'height_all'
             2890  CALL_FUNCTION_1       1  '1 positional argument'
             2892  CALL_FUNCTION_1       1  '1 positional argument'
             2894  CALL_FUNCTION_1       1  '1 positional argument'
             2896  STORE_FAST               'height_all_ord'

 L.1857      2898  LOAD_CONST               False
             2900  STORE_FAST               'errorinheight'

 L.1858      2902  SETUP_EXCEPT       2926  'to 2926'

 L.1859      2904  LOAD_FAST                'base_url'
             2906  LOAD_GLOBAL              alphanumericSort
             2908  LOAD_FAST                'video_urls'
             2910  CALL_FUNCTION_1       1  '1 positional argument'
             2912  LOAD_CONST               -1
             2916  BINARY_SUBSCR    
             2918  BINARY_ADD       
             2920  STORE_FAST               'video_url'
             2922  POP_BLOCK        
             2924  JUMP_FORWARD       3062  'to 3062'
           2926_0  COME_FROM_EXCEPT   2902  '2902'

 L.1860      2926  DUP_TOP          
             2928  LOAD_GLOBAL              Exception
             2930  COMPARE_OP               exception-match
             2932  POP_JUMP_IF_FALSE  3060  'to 3060'
             2936  POP_TOP          
             2938  POP_TOP          
             2940  POP_TOP          

 L.1861      2942  LOAD_GLOBAL              list_to_str
             2944  LOAD_FAST                'height_all_ord'
             2946  LOAD_STR                 'p, '
             2948  LOAD_STR                 ' and '
             2950  LOAD_CONST               ('list', 'separator', 'lastseparator')
             2952  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2954  STORE_FAST               'listheightprint'

 L.1862      2956  LOAD_GLOBAL              print
             2958  LOAD_STR                 '\nThis quality is not available, the available ones are: '
             2960  LOAD_FAST                'listheightprint'
             2962  BINARY_ADD       
             2964  LOAD_STR                 '.'
             2966  BINARY_ADD       
             2968  CALL_FUNCTION_1       1  '1 positional argument'
             2970  POP_TOP          

 L.1863      2972  LOAD_GLOBAL              input
             2974  LOAD_STR                 'Enter a correct quality (without p): '
             2976  CALL_FUNCTION_1       1  '1 positional argument'
             2978  STORE_FAST               'height'

 L.1864      2980  LOAD_CONST               True
             2982  STORE_FAST               'errorinheight'

 L.1865      2984  LOAD_FAST                'ParsingMPD'
             2986  LOAD_FAST                'mpd'
             2988  LOAD_FAST                'height'
             2990  CALL_FUNCTION_2       2  '2 positional arguments'
             2992  UNPACK_SEQUENCE_6     6 
             2994  STORE_FAST               'height_all'
             2996  STORE_FAST               'video_urls'
             2998  STORE_FAST               'audioList'
             3000  STORE_FAST               'novideo'
             3002  STORE_DEREF              'video_pssh'
             3004  STORE_DEREF              'audio_pssh'

 L.1866      3006  SETUP_EXCEPT       3030  'to 3030'

 L.1867      3008  LOAD_FAST                'base_url'
             3010  LOAD_GLOBAL              alphanumericSort
             3012  LOAD_FAST                'video_urls'
             3014  CALL_FUNCTION_1       1  '1 positional argument'
             3016  LOAD_CONST               -1
             3020  BINARY_SUBSCR    
             3022  BINARY_ADD       
             3024  STORE_FAST               'video_url'
             3026  POP_BLOCK        
             3028  JUMP_FORWARD       3056  'to 3056'
           3030_0  COME_FROM_EXCEPT   3006  '3006'

 L.1868      3030  DUP_TOP          
             3032  LOAD_GLOBAL              Exception
             3034  COMPARE_OP               exception-match
             3036  POP_JUMP_IF_FALSE  3054  'to 3054'
             3040  POP_TOP          
             3042  POP_TOP          
             3044  POP_TOP          

 L.1869      3046  LOAD_CONST               True
             3048  STORE_FAST               'novideo'
             3050  POP_EXCEPT       
             3052  JUMP_FORWARD       3056  'to 3056'
             3054  END_FINALLY      
           3056_0  COME_FROM          3052  '3052'
           3056_1  COME_FROM          3028  '3028'
             3056  POP_EXCEPT       
             3058  JUMP_FORWARD       3062  'to 3062'
             3060  END_FINALLY      
           3062_0  COME_FROM          3058  '3058'
           3062_1  COME_FROM          2924  '2924'
           3062_2  COME_FROM          2798  '2798'

 L.1871      3062  LOAD_FAST                'Error_Not_Available'
             3064  LOAD_CONST               True
             3066  COMPARE_OP               ==
             3068  POP_JUMP_IF_FALSE  3200  'to 3200'

 L.1872      3072  LOAD_FAST                'amazonType'
             3074  LOAD_STR                 'show'
             3076  COMPARE_OP               ==
             3078  POP_JUMP_IF_FALSE  3200  'to 3200'

 L.1873      3082  SETUP_EXCEPT       3096  'to 3096'

 L.1874      3084  LOAD_GLOBAL              str
             3086  LOAD_FAST                'heightp'
             3088  CALL_FUNCTION_1       1  '1 positional argument'
             3090  STORE_FAST               'CurrentHeigh'
             3092  POP_BLOCK        
             3094  JUMP_FORWARD       3122  'to 3122'
           3096_0  COME_FROM_EXCEPT   3082  '3082'

 L.1875      3096  DUP_TOP          
             3098  LOAD_GLOBAL              Exception
             3100  COMPARE_OP               exception-match
             3102  POP_JUMP_IF_FALSE  3120  'to 3120'
             3106  POP_TOP          
             3108  POP_TOP          
             3110  POP_TOP          

 L.1876      3112  LOAD_STR                 'Unknown'
             3114  STORE_FAST               'CurrentHeigh'
             3116  POP_EXCEPT       
             3118  JUMP_FORWARD       3122  'to 3122'
             3120  END_FINALLY      
           3122_0  COME_FROM          3118  '3118'
           3122_1  COME_FROM          3094  '3094'

 L.1878      3122  LOAD_DEREF               'seriesName'
             3124  STORE_FAST               'CurrentName'

 L.1880      3126  LOAD_GLOBAL              str
             3128  LOAD_FAST                'CurrentName'
             3130  CALL_FUNCTION_1       1  '1 positional argument'
             3132  LOAD_GLOBAL              str
             3134  LOAD_FAST                'seriesName3'
             3136  CALL_FUNCTION_1       1  '1 positional argument'
             3138  LOAD_GLOBAL              str
             3140  LOAD_FAST                'CurrentHeigh'
             3142  CALL_FUNCTION_1       1  '1 positional argument'
             3144  BUILD_TUPLE_3         3 
             3146  RETURN_VALUE     

 L.1883      3148  DUP_TOP          
             3150  LOAD_GLOBAL              Exception
             3152  COMPARE_OP               exception-match
             3154  POP_JUMP_IF_FALSE  3172  'to 3172'
             3158  POP_TOP          
             3160  POP_TOP          
             3162  POP_TOP          

 L.1884      3164  LOAD_STR                 'Unknown'
             3166  STORE_FAST               'CurrentHeigh'
             3168  POP_EXCEPT       
             3170  JUMP_FORWARD       3174  'to 3174'
             3172  END_FINALLY      
           3174_0  COME_FROM          3170  '3170'

 L.1886      3174  LOAD_DEREF               'seriesName'
             3176  STORE_FAST               'CurrentName'

 L.1888      3178  LOAD_GLOBAL              str
             3180  LOAD_FAST                'CurrentName'
             3182  CALL_FUNCTION_1       1  '1 positional argument'
             3184  LOAD_GLOBAL              str
             3186  LOAD_FAST                'CurrentName'
             3188  CALL_FUNCTION_1       1  '1 positional argument'
             3190  LOAD_GLOBAL              str
             3192  LOAD_FAST                'CurrentHeigh'
             3194  CALL_FUNCTION_1       1  '1 positional argument'
             3196  BUILD_TUPLE_3         3 
             3198  RETURN_END_IF    
           3200_0  COME_FROM          3078  '3078'
           3200_1  COME_FROM          3068  '3068'

 L.1890      3200  LOAD_GLOBAL              defaultdict
             3202  LOAD_GLOBAL              list
             3204  CALL_FUNCTION_1       1  '1 positional argument'
             3206  STORE_FAST               'audioList_new'

 L.1891      3208  LOAD_CONST               False
             3210  STORE_FAST               'noaudio'

 L.1893      3212  LOAD_GLOBAL              args
             3214  LOAD_ATTR                audiolang
             3216  POP_JUMP_IF_FALSE  3226  'to 3226'

 L.1894      3220  LOAD_CONST               False
             3222  STORE_FAST               'noaudio'
             3224  JUMP_FORWARD       3230  'to 3230'
             3226  ELSE                     '3230'

 L.1896      3226  LOAD_FAST                'noaudio'
             3228  STORE_FAST               'noaudio'
           3230_0  COME_FROM          3224  '3224'

 L.1898      3230  LOAD_GLOBAL              args
             3232  LOAD_ATTR                noaudio
             3234  POP_JUMP_IF_FALSE  3244  'to 3244'

 L.1899      3238  LOAD_CONST               True
             3240  STORE_FAST               'noaudio'
             3242  JUMP_FORWARD       3248  'to 3248'
             3244  ELSE                     '3248'

 L.1901      3244  LOAD_FAST                'noaudio'
             3246  STORE_FAST               'noaudio'
           3248_0  COME_FROM          3242  '3242'

 L.1902      3248  SETUP_LOOP         3336  'to 3336'
             3250  LOAD_FAST                'audioList'
             3252  GET_ITER         
             3254  FOR_ITER           3334  'to 3334'
             3256  UNPACK_SEQUENCE_2     2 
             3258  STORE_FAST               'audioTrackId'
             3260  STORE_FAST               'BaseURL'

 L.1903      3262  LOAD_GLOBAL              args
             3264  LOAD_ATTR                audiolang
             3266  POP_JUMP_IF_FALSE  3312  'to 3312'

 L.1904      3270  LOAD_GLOBAL              str
             3272  LOAD_FAST                'audioTrackId'
             3274  CALL_FUNCTION_1       1  '1 positional argument'
             3276  LOAD_GLOBAL              list
             3278  LOAD_GLOBAL              args
             3280  LOAD_ATTR                audiolang
             3282  CALL_FUNCTION_1       1  '1 positional argument'
             3284  COMPARE_OP               in
             3286  POP_JUMP_IF_FALSE  3254  'to 3254'

 L.1905      3290  LOAD_FAST                'audioList_new'
             3292  LOAD_FAST                'audioTrackId'
             3294  BINARY_SUBSCR    
             3296  LOAD_ATTR                append
             3298  LOAD_FAST                'BaseURL'
             3300  CALL_FUNCTION_1       1  '1 positional argument'
             3302  POP_TOP          
             3304  JUMP_FORWARD       3310  'to 3310'

 L.1907      3306  CONTINUE           3254  'to 3254'
           3310_0  COME_FROM          3304  '3304'
             3310  JUMP_FORWARD       3330  'to 3330'
             3312  ELSE                     '3330'

 L.1909      3312  LOAD_FAST                'audioList_new'
             3314  LOAD_FAST                'audioTrackId'
             3316  BINARY_SUBSCR    
             3318  LOAD_ATTR                append
             3320  LOAD_FAST                'BaseURL'
             3322  CALL_FUNCTION_1       1  '1 positional argument'
             3324  POP_TOP          

 L.1910      3326  CONTINUE           3254  'to 3254'
           3330_0  COME_FROM          3310  '3310'
             3330  JUMP_BACK          3254  'to 3254'
             3334  POP_BLOCK        
           3336_0  COME_FROM_LOOP     3248  '3248'

 L.1912      3336  LOAD_GLOBAL              str
             3338  LOAD_FAST                'audioList_new'
             3340  LOAD_ATTR                items
             3342  CALL_FUNCTION_0       0  '0 positional arguments'
             3344  CALL_FUNCTION_1       1  '1 positional argument'
             3346  LOAD_STR                 'dict_items([])'
             3348  COMPARE_OP               ==
             3350  POP_JUMP_IF_FALSE  3366  'to 3366'

 L.1913      3354  LOAD_GLOBAL              print
             3356  LOAD_STR                 '\nThere is no audio available for download.'
             3358  CALL_FUNCTION_1       1  '1 positional argument'
             3360  POP_TOP          

 L.1914      3362  LOAD_CONST               True
             3364  STORE_FAST               'noaudio'
           3366_0  COME_FROM          3350  '3350'

 L.1916      3366  BUILD_LIST_0          0 
             3368  STORE_FAST               'listaudios'

 L.1917      3370  SETUP_LOOP         3448  'to 3448'
             3372  LOAD_FAST                'audioList_new'
             3374  LOAD_ATTR                items
             3376  CALL_FUNCTION_0       0  '0 positional arguments'
             3378  GET_ITER         
             3380  FOR_ITER           3446  'to 3446'
             3382  UNPACK_SEQUENCE_2     2 
             3384  STORE_FAST               'k'
             3386  STORE_FAST               'v'

 L.1918      3388  LOAD_FAST                'listaudios'
             3390  LOAD_ATTR                append
             3392  LOAD_FAST                'k'
             3394  CALL_FUNCTION_1       1  '1 positional argument'
             3396  POP_TOP          

 L.1920      3398  LOAD_GLOBAL              list_to_str
             3400  LOAD_FAST                'listaudios'
             3402  LOAD_STR                 ', '
             3404  LOAD_STR                 ' and '
             3406  LOAD_CONST               ('list', 'separator', 'lastseparator')
             3408  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             3410  STORE_FAST               'listaudiosprint'

 L.1921      3412  LOAD_GLOBAL              print
             3414  LOAD_STR                 '\nAudios that will be downloaded: '
             3416  LOAD_FAST                'listaudiosprint'
             3418  BINARY_ADD       
             3420  LOAD_STR                 '.'
             3422  BINARY_ADD       
             3424  CALL_FUNCTION_1       1  '1 positional argument'
             3426  POP_TOP          

 L.1922      3428  LOAD_CONST               False
             3430  STORE_FAST               'noprotection'

 L.1923      3432  LOAD_DEREF               'audio_pssh'
             3434  POP_JUMP_IF_TRUE   3380  'to 3380'

 L.1924      3438  LOAD_CONST               True
             3440  STORE_FAST               'noprotection'
             3442  JUMP_BACK          3380  'to 3380'
             3446  POP_BLOCK        
           3448_0  COME_FROM_LOOP     3370  '3370'

 L.1926      3448  LOAD_GLOBAL              args
             3450  LOAD_ATTR                customquality
             3452  POP_JUMP_IF_FALSE  3502  'to 3502'

 L.1927      3456  LOAD_FAST                'errorinheight'
             3458  LOAD_CONST               True
             3460  COMPARE_OP               ==
             3462  POP_JUMP_IF_FALSE  3470  'to 3470'

 L.1928      3466  LOAD_FAST                'height'
             3468  STORE_FAST               'heightp'
           3470_0  COME_FROM          3462  '3462'

 L.1929      3470  LOAD_GLOBAL              args
             3472  LOAD_ATTR                customquality
             3474  POP_JUMP_IF_FALSE  3502  'to 3502'

 L.1930      3478  LOAD_FAST                'errorinheight'
             3480  LOAD_CONST               False
             3482  COMPARE_OP               ==
             3484  POP_JUMP_IF_FALSE  3492  'to 3492'

 L.1931      3488  LOAD_FAST                'height'
             3490  STORE_FAST               'heightp'
           3492_0  COME_FROM          3484  '3484'

 L.1932      3492  LOAD_FAST                'height_all_ord'
             3494  LOAD_CONST               -1
             3498  BINARY_SUBSCR    
             3500  STORE_FAST               'heightp'
           3502_0  COME_FROM          3474  '3474'
           3502_1  COME_FROM          3452  '3452'

 L.1934      3502  LOAD_FAST                'amazonType'
             3504  LOAD_STR                 'show'
             3506  COMPARE_OP               ==
             3508  POP_JUMP_IF_FALSE  3678  'to 3678'

 L.1935      3512  LOAD_DEREF               'seriesName'
             3514  STORE_FAST               'CurrentName'

 L.1936      3516  LOAD_GLOBAL              str
             3518  LOAD_FAST                'heightp'
             3520  CALL_FUNCTION_1       1  '1 positional argument'
             3522  STORE_FAST               'CurrentHeigh'

 L.1937      3524  LOAD_GLOBAL              args
             3526  LOAD_ATTR                hevc
             3528  POP_JUMP_IF_FALSE  3578  'to 3578'

 L.1939      3532  LOAD_GLOBAL              folderdownloader
             3534  LOAD_STR                 '\\'
             3536  BINARY_ADD       
             3538  LOAD_GLOBAL              str
             3540  LOAD_FAST                'seriesName3'
             3542  CALL_FUNCTION_1       1  '1 positional argument'
             3544  BINARY_ADD       
             3546  LOAD_STR                 '\\'
             3548  BINARY_ADD       
             3550  LOAD_GLOBAL              str
             3552  LOAD_FAST                'CurrentName'
             3554  CALL_FUNCTION_1       1  '1 positional argument'
             3556  BINARY_ADD       
             3558  LOAD_STR                 ' ['
             3560  BINARY_ADD       
             3562  LOAD_GLOBAL              str
             3564  LOAD_FAST                'CurrentHeigh'
             3566  CALL_FUNCTION_1       1  '1 positional argument'
             3568  BINARY_ADD       
             3570  LOAD_STR                 'p] [HEVC].mkv'
             3572  BINARY_ADD       
             3574  STORE_FAST               'VideoOutputName'
             3576  JUMP_FORWARD       3676  'to 3676'
             3578  ELSE                     '3676'

 L.1941      3578  LOAD_GLOBAL              args
             3580  LOAD_ATTR                atmos
             3582  POP_JUMP_IF_FALSE  3632  'to 3632'

 L.1944      3586  LOAD_GLOBAL              folderdownloader
             3588  LOAD_STR                 '\\'
             3590  BINARY_ADD       
             3592  LOAD_GLOBAL              str
             3594  LOAD_FAST                'seriesName3'
             3596  CALL_FUNCTION_1       1  '1 positional argument'
             3598  BINARY_ADD       
             3600  LOAD_STR                 '\\'
             3602  BINARY_ADD       
             3604  LOAD_GLOBAL              str
             3606  LOAD_FAST                'CurrentName'
             3608  CALL_FUNCTION_1       1  '1 positional argument'
             3610  BINARY_ADD       
             3612  LOAD_STR                 ' ['
             3614  BINARY_ADD       
             3616  LOAD_GLOBAL              str
             3618  LOAD_FAST                'CurrentHeigh'
             3620  CALL_FUNCTION_1       1  '1 positional argument'
             3622  BINARY_ADD       
             3624  LOAD_STR                 'p] [HEVC-atmos].mkv'
             3626  BINARY_ADD       
             3628  STORE_FAST               'VideoOutputName'
             3630  JUMP_FORWARD       3676  'to 3676'
             3632  ELSE                     '3676'

 L.1948      3632  LOAD_GLOBAL              folderdownloader
             3634  LOAD_STR                 '\\'
             3636  BINARY_ADD       
             3638  LOAD_GLOBAL              str
             3640  LOAD_FAST                'seriesName3'
             3642  CALL_FUNCTION_1       1  '1 positional argument'
             3644  BINARY_ADD       
             3646  LOAD_STR                 '\\'
             3648  BINARY_ADD       
             3650  LOAD_GLOBAL              str
             3652  LOAD_FAST                'CurrentName'
             3654  CALL_FUNCTION_1       1  '1 positional argument'
             3656  BINARY_ADD       
             3658  LOAD_STR                 ' ['
             3660  BINARY_ADD       
             3662  LOAD_GLOBAL              str
             3664  LOAD_FAST                'CurrentHeigh'
             3666  CALL_FUNCTION_1       1  '1 positional argument'
             3668  BINARY_ADD       
             3670  LOAD_STR                 'p].mkv'
             3672  BINARY_ADD       
             3674  STORE_FAST               'VideoOutputName'
           3676_0  COME_FROM          3630  '3630'
           3676_1  COME_FROM          3576  '3576'
             3676  JUMP_FORWARD       3806  'to 3806'
             3678  ELSE                     '3806'

 L.1950      3678  LOAD_DEREF               'seriesName'
             3680  STORE_FAST               'CurrentName'

 L.1951      3682  LOAD_GLOBAL              str
             3684  LOAD_FAST                'heightp'
             3686  CALL_FUNCTION_1       1  '1 positional argument'
             3688  STORE_FAST               'CurrentHeigh'

 L.1952      3690  LOAD_GLOBAL              args
             3692  LOAD_ATTR                hevc
             3694  POP_JUMP_IF_FALSE  3732  'to 3732'

 L.1954      3698  LOAD_GLOBAL              folderdownloader
             3700  LOAD_STR                 '\\'
             3702  BINARY_ADD       
             3704  LOAD_GLOBAL              str
             3706  LOAD_FAST                'CurrentName'
             3708  CALL_FUNCTION_1       1  '1 positional argument'
             3710  BINARY_ADD       
             3712  LOAD_STR                 ' ['
             3714  BINARY_ADD       
             3716  LOAD_GLOBAL              str
             3718  LOAD_FAST                'CurrentHeigh'
             3720  CALL_FUNCTION_1       1  '1 positional argument'
             3722  BINARY_ADD       
             3724  LOAD_STR                 'p] [HEVC].mkv'
             3726  BINARY_ADD       
             3728  STORE_FAST               'VideoOutputName'
             3730  JUMP_FORWARD       3806  'to 3806'
             3732  ELSE                     '3806'

 L.1956      3732  LOAD_GLOBAL              args
             3734  LOAD_ATTR                atmos
             3736  POP_JUMP_IF_FALSE  3774  'to 3774'

 L.1958      3740  LOAD_GLOBAL              folderdownloader
             3742  LOAD_STR                 '\\'
             3744  BINARY_ADD       
             3746  LOAD_GLOBAL              str
             3748  LOAD_FAST                'CurrentName'
             3750  CALL_FUNCTION_1       1  '1 positional argument'
             3752  BINARY_ADD       
             3754  LOAD_STR                 ' ['
             3756  BINARY_ADD       
             3758  LOAD_GLOBAL              str
             3760  LOAD_FAST                'CurrentHeigh'
             3762  CALL_FUNCTION_1       1  '1 positional argument'
             3764  BINARY_ADD       
             3766  LOAD_STR                 'p] [HEVC-atmos].mkv'
             3768  BINARY_ADD       
             3770  STORE_FAST               'VideoOutputName'
             3772  JUMP_FORWARD       3806  'to 3806'
             3774  ELSE                     '3806'

 L.1961      3774  LOAD_GLOBAL              folderdownloader
             3776  LOAD_STR                 '\\'
             3778  BINARY_ADD       
             3780  LOAD_GLOBAL              str
             3782  LOAD_FAST                'CurrentName'
             3784  CALL_FUNCTION_1       1  '1 positional argument'
             3786  BINARY_ADD       
             3788  LOAD_STR                 ' ['
             3790  BINARY_ADD       
             3792  LOAD_GLOBAL              str
             3794  LOAD_FAST                'CurrentHeigh'
             3796  CALL_FUNCTION_1       1  '1 positional argument'
             3798  BINARY_ADD       
             3800  LOAD_STR                 'p].mkv'
             3802  BINARY_ADD       
             3804  STORE_FAST               'VideoOutputName'
           3806_0  COME_FROM          3772  '3772'
           3806_1  COME_FROM          3730  '3730'
           3806_2  COME_FROM          3676  '3676'

 L.1963      3806  LOAD_GLOBAL              os
             3808  LOAD_ATTR                path
             3810  LOAD_ATTR                isfile
             3812  LOAD_FAST                'VideoOutputName'
             3814  CALL_FUNCTION_1       1  '1 positional argument'
             3816  POP_JUMP_IF_TRUE   5288  'to 5288'

 L.1964      3820  LOAD_GLOBAL              args
             3822  LOAD_ATTR                nosubs
             3824  POP_JUMP_IF_TRUE   4698  'to 4698'

 L.1965      3828  LOAD_GLOBAL              subsList
             3830  BUILD_LIST_0          0 
             3832  COMPARE_OP               !=
             3834  POP_JUMP_IF_FALSE  4032  'to 4032'

 L.1966      3838  LOAD_GLOBAL              print
             3840  LOAD_STR                 '\nDownloading subtitles...'
             3842  CALL_FUNCTION_1       1  '1 positional argument'
             3844  POP_TOP          

 L.1967      3846  SETUP_LOOP         4040  'to 4040'
             3848  LOAD_GLOBAL              subsList
             3850  GET_ITER         
             3852  FOR_ITER           4028  'to 4028'
             3854  STORE_FAST               'z'

 L.1968      3856  LOAD_GLOBAL              str
             3858  LOAD_GLOBAL              dict
             3860  LOAD_FAST                'z'
             3862  CALL_FUNCTION_1       1  '1 positional argument'
             3864  LOAD_STR                 'SubsID'
             3866  BINARY_SUBSCR    
             3868  CALL_FUNCTION_1       1  '1 positional argument'
             3870  STORE_FAST               'langAbbrev'

 L.1969      3872  LOAD_GLOBAL              os
             3874  LOAD_ATTR                path
             3876  LOAD_ATTR                isfile
             3878  LOAD_DEREF               'seriesName'
             3880  LOAD_STR                 ' '
             3882  BINARY_ADD       
             3884  LOAD_STR                 '('
             3886  BINARY_ADD       
             3888  LOAD_FAST                'langAbbrev'
             3890  BINARY_ADD       
             3892  LOAD_STR                 ')'
             3894  BINARY_ADD       
             3896  LOAD_STR                 '.srt'
             3898  BINARY_ADD       
             3900  CALL_FUNCTION_1       1  '1 positional argument'
             3902  POP_JUMP_IF_TRUE   3940  'to 3940'
             3906  LOAD_GLOBAL              os
             3908  LOAD_ATTR                path
             3910  LOAD_ATTR                isfile

 L.1970      3912  LOAD_DEREF               'seriesName'
             3914  LOAD_STR                 ' '
             3916  BINARY_ADD       
             3918  LOAD_STR                 '('
             3920  BINARY_ADD       
             3922  LOAD_FAST                'langAbbrev'
             3924  BINARY_ADD       
             3926  LOAD_STR                 ')'
             3928  BINARY_ADD       
             3930  LOAD_STR                 '.dfxp'
             3932  BINARY_ADD       
             3934  CALL_FUNCTION_1       1  '1 positional argument'
           3936_0  COME_FROM          3902  '3902'
             3936  POP_JUMP_IF_FALSE  3974  'to 3974'

 L.1971      3940  LOAD_GLOBAL              print

 L.1972      3942  LOAD_DEREF               'seriesName'
             3944  LOAD_STR                 ' '
             3946  BINARY_ADD       
             3948  LOAD_STR                 '('
             3950  BINARY_ADD       
             3952  LOAD_FAST                'langAbbrev'
             3954  BINARY_ADD       
             3956  LOAD_STR                 ')'
             3958  BINARY_ADD       
             3960  LOAD_STR                 ' has already been successfully downloaded previously.'
             3962  BINARY_ADD       
             3964  CALL_FUNCTION_1       1  '1 positional argument'
             3966  POP_TOP          

 L.1973      3968  CONTINUE           3852  'to 3852'
             3972  JUMP_FORWARD       4024  'to 4024'
             3974  ELSE                     '4024'

 L.1975      3974  LOAD_GLOBAL              downloadFile2
             3976  LOAD_GLOBAL              str
             3978  LOAD_GLOBAL              dict
             3980  LOAD_FAST                'z'
             3982  CALL_FUNCTION_1       1  '1 positional argument'
             3984  LOAD_STR                 'subs_urls'
             3986  BINARY_SUBSCR    
             3988  CALL_FUNCTION_1       1  '1 positional argument'

 L.1976      3990  LOAD_DEREF               'seriesName'
             3992  LOAD_STR                 ' '
             3994  BINARY_ADD       
             3996  LOAD_STR                 '('
             3998  BINARY_ADD       
             4000  LOAD_FAST                'langAbbrev'
             4002  BINARY_ADD       
             4004  LOAD_STR                 ')'
             4006  BINARY_ADD       
             4008  LOAD_STR                 '.dfxp'
             4010  BINARY_ADD       
             4012  CALL_FUNCTION_2       2  '2 positional arguments'
             4014  POP_TOP          

 L.1977      4016  LOAD_GLOBAL              print
             4018  LOAD_STR                 'Downloaded!'
             4020  CALL_FUNCTION_1       1  '1 positional argument'
             4022  POP_TOP          
           4024_0  COME_FROM          3972  '3972'
             4024  JUMP_BACK          3852  'to 3852'
             4028  POP_BLOCK        
           4030_0  COME_FROM_LOOP     3846  '3846'
             4030  JUMP_FORWARD       4040  'to 4040'
             4032  ELSE                     '4040'

 L.1980      4032  LOAD_GLOBAL              print
             4034  LOAD_STR                 '\nNo subtitles available.'
             4036  CALL_FUNCTION_1       1  '1 positional argument'
             4038  POP_TOP          
           4040_0  COME_FROM          4030  '4030'

 L.1982      4040  LOAD_GLOBAL              subsForList
             4042  BUILD_LIST_0          0 
             4044  COMPARE_OP               !=
             4046  POP_JUMP_IF_FALSE  4276  'to 4276'

 L.1983      4050  LOAD_GLOBAL              print
             4052  LOAD_STR                 '\nDownloading forced subtitles...'
             4054  CALL_FUNCTION_1       1  '1 positional argument'
             4056  POP_TOP          

 L.1984      4058  SETUP_LOOP         4284  'to 4284'
             4060  LOAD_GLOBAL              subsForList
             4062  GET_ITER         
             4064  FOR_ITER           4272  'to 4272'
             4066  STORE_FAST               'z'

 L.1985      4068  LOAD_GLOBAL              str
             4070  LOAD_GLOBAL              dict
             4072  LOAD_FAST                'z'
             4074  CALL_FUNCTION_1       1  '1 positional argument'
             4076  LOAD_STR                 'SubsForID'
             4078  BINARY_SUBSCR    
             4080  CALL_FUNCTION_1       1  '1 positional argument'
             4082  STORE_FAST               'langAbbrev'

 L.1986      4084  LOAD_GLOBAL              os
             4086  LOAD_ATTR                path
             4088  LOAD_ATTR                isfile

 L.1987      4090  LOAD_DEREF               'seriesName'
             4092  LOAD_STR                 ' '
             4094  BINARY_ADD       
             4096  LOAD_STR                 '('
             4098  BINARY_ADD       
             4100  LOAD_FAST                'langAbbrev'
             4102  BINARY_ADD       
             4104  LOAD_STR                 ')'
             4106  BINARY_ADD       
             4108  LOAD_STR                 ' '
             4110  BINARY_ADD       
             4112  LOAD_STR                 'Forced'
             4114  BINARY_ADD       
             4116  LOAD_STR                 '.srt'
             4118  BINARY_ADD       
             4120  CALL_FUNCTION_1       1  '1 positional argument'
             4122  POP_JUMP_IF_TRUE   4168  'to 4168'
             4126  LOAD_GLOBAL              os
             4128  LOAD_ATTR                path
             4130  LOAD_ATTR                isfile

 L.1988      4132  LOAD_DEREF               'seriesName'
             4134  LOAD_STR                 ' '
             4136  BINARY_ADD       
             4138  LOAD_STR                 '('
             4140  BINARY_ADD       
             4142  LOAD_FAST                'langAbbrev'
             4144  BINARY_ADD       
             4146  LOAD_STR                 ')'
             4148  BINARY_ADD       
             4150  LOAD_STR                 ' '
             4152  BINARY_ADD       
             4154  LOAD_STR                 'Forced'
             4156  BINARY_ADD       
             4158  LOAD_STR                 '.dfxp'
             4160  BINARY_ADD       
             4162  CALL_FUNCTION_1       1  '1 positional argument'
           4164_0  COME_FROM          4122  '4122'
             4164  POP_JUMP_IF_FALSE  4210  'to 4210'

 L.1989      4168  LOAD_GLOBAL              print

 L.1990      4170  LOAD_DEREF               'seriesName'
             4172  LOAD_STR                 ' '
             4174  BINARY_ADD       
             4176  LOAD_STR                 '('
             4178  BINARY_ADD       
             4180  LOAD_FAST                'langAbbrev'
             4182  BINARY_ADD       
             4184  LOAD_STR                 ')'
             4186  BINARY_ADD       
             4188  LOAD_STR                 ' '
             4190  BINARY_ADD       
             4192  LOAD_STR                 'Forced'
             4194  BINARY_ADD       
             4196  LOAD_STR                 ' has already been successfully downloaded previously.'
             4198  BINARY_ADD       
             4200  CALL_FUNCTION_1       1  '1 positional argument'
             4202  POP_TOP          

 L.1991      4204  CONTINUE           4064  'to 4064'
             4208  JUMP_FORWARD       4268  'to 4268'
             4210  ELSE                     '4268'

 L.1993      4210  LOAD_GLOBAL              downloadFile2
             4212  LOAD_GLOBAL              str
             4214  LOAD_GLOBAL              dict
             4216  LOAD_FAST                'z'
             4218  CALL_FUNCTION_1       1  '1 positional argument'
             4220  LOAD_STR                 'subsFor_urls'
             4222  BINARY_SUBSCR    
             4224  CALL_FUNCTION_1       1  '1 positional argument'

 L.1994      4226  LOAD_DEREF               'seriesName'
             4228  LOAD_STR                 ' '
             4230  BINARY_ADD       
             4232  LOAD_STR                 '('
             4234  BINARY_ADD       
             4236  LOAD_FAST                'langAbbrev'
             4238  BINARY_ADD       
             4240  LOAD_STR                 ')'
             4242  BINARY_ADD       
             4244  LOAD_STR                 ' '
             4246  BINARY_ADD       
             4248  LOAD_STR                 'Forced'
             4250  BINARY_ADD       
             4252  LOAD_STR                 '.dfxp'
             4254  BINARY_ADD       
             4256  CALL_FUNCTION_2       2  '2 positional arguments'
             4258  POP_TOP          

 L.1995      4260  LOAD_GLOBAL              print
             4262  LOAD_STR                 'Downloaded!'
             4264  CALL_FUNCTION_1       1  '1 positional argument'
             4266  POP_TOP          
           4268_0  COME_FROM          4208  '4208'
             4268  JUMP_BACK          4064  'to 4064'
             4272  POP_BLOCK        
           4274_0  COME_FROM_LOOP     4058  '4058'
             4274  JUMP_FORWARD       4284  'to 4284'
             4276  ELSE                     '4284'

 L.1998      4276  LOAD_GLOBAL              print
             4278  LOAD_STR                 '\nNo forced subtitles available.'
             4280  CALL_FUNCTION_1       1  '1 positional argument'
             4282  POP_TOP          
           4284_0  COME_FROM          4274  '4274'

 L.2000      4284  LOAD_GLOBAL              subsForList
             4286  BUILD_LIST_0          0 
             4288  COMPARE_OP               !=
             4290  POP_JUMP_IF_TRUE   4304  'to 4304'
             4294  LOAD_GLOBAL              subsList
             4296  BUILD_LIST_0          0 
             4298  COMPARE_OP               !=
           4300_0  COME_FROM          4290  '4290'
             4300  POP_JUMP_IF_FALSE  4698  'to 4698'

 L.2001      4304  LOAD_CONST               False
             4306  STORE_FAST               'subsinfolder'

 L.2002      4308  LOAD_CONST               False
             4310  STORE_FAST               'subsinfolderFOR'

 L.2003      4312  SETUP_LOOP         4390  'to 4390'
             4314  LOAD_GLOBAL              subsForList
             4316  GET_ITER         
             4318  FOR_ITER           4388  'to 4388'
             4320  STORE_FAST               'z'

 L.2004      4322  LOAD_GLOBAL              str
             4324  LOAD_GLOBAL              dict
             4326  LOAD_FAST                'z'
             4328  CALL_FUNCTION_1       1  '1 positional argument'
             4330  LOAD_STR                 'SubsForID'
             4332  BINARY_SUBSCR    
             4334  CALL_FUNCTION_1       1  '1 positional argument'
             4336  STORE_FAST               'langAbbrev'

 L.2005      4338  LOAD_GLOBAL              os
             4340  LOAD_ATTR                path
             4342  LOAD_ATTR                isfile
             4344  LOAD_DEREF               'seriesName'
             4346  LOAD_STR                 ' '
             4348  BINARY_ADD       
             4350  LOAD_STR                 '('
             4352  BINARY_ADD       
             4354  LOAD_FAST                'langAbbrev'
             4356  BINARY_ADD       
             4358  LOAD_STR                 ')'
             4360  BINARY_ADD       
             4362  LOAD_STR                 ' '
             4364  BINARY_ADD       
             4366  LOAD_STR                 'Forced'
             4368  BINARY_ADD       
             4370  LOAD_STR                 '.dfxp'
             4372  BINARY_ADD       
             4374  CALL_FUNCTION_1       1  '1 positional argument'
             4376  POP_JUMP_IF_FALSE  4318  'to 4318'

 L.2006      4380  LOAD_CONST               True
             4382  STORE_FAST               'subsinfolderFOR'
             4384  JUMP_BACK          4318  'to 4318'
             4388  POP_BLOCK        
           4390_0  COME_FROM_LOOP     4312  '4312'

 L.2008      4390  SETUP_LOOP         4460  'to 4460'
             4392  LOAD_GLOBAL              subsList
             4394  GET_ITER         
             4396  FOR_ITER           4458  'to 4458'
             4398  STORE_FAST               'z'

 L.2009      4400  LOAD_GLOBAL              str
             4402  LOAD_GLOBAL              dict
             4404  LOAD_FAST                'z'
             4406  CALL_FUNCTION_1       1  '1 positional argument'
             4408  LOAD_STR                 'SubsID'
             4410  BINARY_SUBSCR    
             4412  CALL_FUNCTION_1       1  '1 positional argument'
             4414  STORE_FAST               'langAbbrev'

 L.2010      4416  LOAD_GLOBAL              os
             4418  LOAD_ATTR                path
             4420  LOAD_ATTR                isfile
             4422  LOAD_DEREF               'seriesName'
             4424  LOAD_STR                 ' '
             4426  BINARY_ADD       
             4428  LOAD_STR                 '('
             4430  BINARY_ADD       
             4432  LOAD_FAST                'langAbbrev'
             4434  BINARY_ADD       
             4436  LOAD_STR                 ')'
             4438  BINARY_ADD       
             4440  LOAD_STR                 '.dfxp'
             4442  BINARY_ADD       
             4444  CALL_FUNCTION_1       1  '1 positional argument'
             4446  POP_JUMP_IF_FALSE  4396  'to 4396'

 L.2011      4450  LOAD_CONST               True
             4452  STORE_FAST               'subsinfolder'
             4454  JUMP_BACK          4396  'to 4396'
             4458  POP_BLOCK        
           4460_0  COME_FROM_LOOP     4390  '4390'

 L.2013      4460  LOAD_FAST                'subsinfolder'
             4462  LOAD_CONST               True
             4464  COMPARE_OP               ==
             4466  POP_JUMP_IF_TRUE   4480  'to 4480'
             4470  LOAD_FAST                'subsinfolderFOR'
             4472  LOAD_CONST               True
             4474  COMPARE_OP               ==
           4476_0  COME_FROM          4466  '4466'
             4476  POP_JUMP_IF_FALSE  4698  'to 4698'

 L.2014      4480  LOAD_GLOBAL              print
             4482  LOAD_STR                 '\nConverting subtitles...'
             4484  CALL_FUNCTION_1       1  '1 positional argument'
             4486  POP_TOP          

 L.2015      4488  LOAD_GLOBAL              subprocess
             4490  LOAD_ATTR                Popen

 L.2016      4492  LOAD_GLOBAL              SubtitleEditexe
             4494  LOAD_STR                 '/convert'
             4496  LOAD_DEREF               'seriesName'
             4498  LOAD_STR                 '*.dfxp'
             4500  BINARY_ADD       
             4502  LOAD_STR                 'srt'
             4504  BUILD_LIST_4          4 
             4506  CALL_FUNCTION_1       1  '1 positional argument'
             4508  STORE_FAST               'SubtitleEdit_process'

 L.2017      4510  LOAD_FAST                'SubtitleEdit_process'
             4512  LOAD_ATTR                communicate
             4514  CALL_FUNCTION_0       0  '0 positional arguments'
             4516  UNPACK_SEQUENCE_2     2 
             4518  STORE_FAST               'stdoutdata'
             4520  STORE_FAST               'stderrdata'

 L.2018      4522  LOAD_FAST                'SubtitleEdit_process'
             4524  LOAD_ATTR                wait
             4526  CALL_FUNCTION_0       0  '0 positional arguments'
             4528  POP_TOP          

 L.2019      4530  SETUP_LOOP         4654  'to 4654'
             4532  LOAD_GLOBAL              glob
             4534  LOAD_ATTR                glob
             4536  LOAD_DEREF               'seriesName'
             4538  LOAD_STR                 '*.srt'
             4540  BINARY_ADD       
             4542  CALL_FUNCTION_1       1  '1 positional argument'
             4544  GET_ITER         
             4546  FOR_ITER           4652  'to 4652'
             4548  STORE_FAST               'f'

 L.2020      4550  LOAD_GLOBAL              open
             4552  LOAD_FAST                'f'
             4554  LOAD_STR                 'r+'
             4556  LOAD_STR                 'utf-8'
             4558  LOAD_CONST               ('encoding',)
             4560  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4562  SETUP_WITH         4578  'to 4578'
             4564  STORE_FAST               'x'

 L.2021      4566  LOAD_FAST                'x'
             4568  LOAD_ATTR                read
             4570  CALL_FUNCTION_0       0  '0 positional arguments'
             4572  STORE_FAST               'old'
             4574  POP_BLOCK        
             4576  LOAD_CONST               None
           4578_0  COME_FROM_WITH     4562  '4562'
             4578  WITH_CLEANUP_START
             4580  WITH_CLEANUP_FINISH
             4582  END_FINALLY      

 L.2022      4584  LOAD_GLOBAL              open
             4586  LOAD_FAST                'f'
             4588  LOAD_STR                 'w+'
             4590  LOAD_STR                 'utf-8'
             4592  LOAD_CONST               ('encoding',)
             4594  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4596  SETUP_WITH         4642  'to 4642'
             4598  STORE_FAST               'x'

 L.2023      4600  LOAD_GLOBAL              args
             4602  LOAD_ATTR                nocleansubs
             4604  POP_JUMP_IF_TRUE   4624  'to 4624'

 L.2024      4608  LOAD_FAST                'x'
             4610  LOAD_ATTR                write
             4612  LOAD_GLOBAL              ReplaceSubs1
             4614  LOAD_FAST                'old'
             4616  CALL_FUNCTION_1       1  '1 positional argument'
             4618  CALL_FUNCTION_1       1  '1 positional argument'
             4620  POP_TOP          
             4622  JUMP_FORWARD       4638  'to 4638'
             4624  ELSE                     '4638'

 L.2026      4624  LOAD_FAST                'x'
             4626  LOAD_ATTR                write
             4628  LOAD_GLOBAL              ReplaceSubs2
             4630  LOAD_FAST                'old'
             4632  CALL_FUNCTION_1       1  '1 positional argument'
             4634  CALL_FUNCTION_1       1  '1 positional argument'
             4636  POP_TOP          
           4638_0  COME_FROM          4622  '4622'
             4638  POP_BLOCK        
             4640  LOAD_CONST               None
           4642_0  COME_FROM_WITH     4596  '4596'
             4642  WITH_CLEANUP_START
             4644  WITH_CLEANUP_FINISH
             4646  END_FINALLY      
             4648  JUMP_BACK          4546  'to 4546'
             4652  POP_BLOCK        
           4654_0  COME_FROM_LOOP     4530  '4530'

 L.2028      4654  SETUP_LOOP         4690  'to 4690'
             4656  LOAD_GLOBAL              glob
             4658  LOAD_ATTR                glob
             4660  LOAD_DEREF               'seriesName'
             4662  LOAD_STR                 '*.dfxp'
             4664  BINARY_ADD       
             4666  CALL_FUNCTION_1       1  '1 positional argument'
             4668  GET_ITER         
             4670  FOR_ITER           4688  'to 4688'
             4672  STORE_FAST               'f'

 L.2029      4674  LOAD_GLOBAL              os
             4676  LOAD_ATTR                remove
             4678  LOAD_FAST                'f'
             4680  CALL_FUNCTION_1       1  '1 positional argument'
             4682  POP_TOP          
             4684  JUMP_BACK          4670  'to 4670'
             4688  POP_BLOCK        
           4690_0  COME_FROM_LOOP     4654  '4654'

 L.2031      4690  LOAD_GLOBAL              print
             4692  LOAD_STR                 'Done!'
             4694  CALL_FUNCTION_1       1  '1 positional argument'
             4696  POP_TOP          
           4698_0  COME_FROM          4476  '4476'
           4698_1  COME_FROM          4300  '4300'
           4698_2  COME_FROM          3824  '3824'

 L.2033      4698  LOAD_GLOBAL              args
             4700  LOAD_ATTR                nochpaters
             4702  POP_JUMP_IF_TRUE   5288  'to 5288'

 L.2034      4706  LOAD_FAST                'nochapters'
             4708  LOAD_CONST               False
             4710  COMPARE_OP               ==
             4712  POP_JUMP_IF_FALSE  4994  'to 4994'

 L.2035      4716  LOAD_GLOBAL              print
             4718  LOAD_STR                 '\nGenerating Chapters file...'
             4720  CALL_FUNCTION_1       1  '1 positional argument'
             4722  POP_TOP          

 L.2036      4724  LOAD_GLOBAL              os
             4726  LOAD_ATTR                path
             4728  LOAD_ATTR                isfile
             4730  LOAD_DEREF               'seriesName'
             4732  LOAD_STR                 ' Chapters.txt'
             4734  BINARY_ADD       
             4736  CALL_FUNCTION_1       1  '1 positional argument'
             4738  POP_JUMP_IF_FALSE  4760  'to 4760'

 L.2037      4742  LOAD_GLOBAL              print

 L.2038      4744  LOAD_DEREF               'seriesName'
             4746  LOAD_STR                 ' Chapters.txt'
             4748  BINARY_ADD       
             4750  LOAD_STR                 ' has already been successfully downloaded previously.'
             4752  BINARY_ADD       
             4754  CALL_FUNCTION_1       1  '1 positional argument'
             4756  POP_TOP          
             4758  JUMP_FORWARD       4992  'to 4992'
             4760  ELSE                     '4992'

 L.2040      4760  LOAD_CONST               1
             4762  STORE_FAST               'count'

 L.2041      4764  LOAD_GLOBAL              open
             4766  LOAD_DEREF               'seriesName'
             4768  LOAD_STR                 ' Chapters.txt'
             4770  BINARY_ADD       
             4772  LOAD_STR                 'a'
             4774  LOAD_STR                 'utf-8'
             4776  LOAD_CONST               ('encoding',)
             4778  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             4780  SETUP_WITH         4978  'to 4978'
             4782  STORE_FAST               'f'

 L.2042      4784  SETUP_LOOP         4974  'to 4974'
             4786  LOAD_FAST                'ChaptersList_new'
             4788  LOAD_ATTR                items
             4790  CALL_FUNCTION_0       0  '0 positional arguments'
             4792  GET_ITER         
             4794  FOR_ITER           4972  'to 4972'
             4796  UNPACK_SEQUENCE_2     2 
             4798  STORE_FAST               'k'
             4800  STORE_FAST               'v'

 L.2043      4802  LOAD_GLOBAL              int
             4804  LOAD_FAST                'count'
             4806  CALL_FUNCTION_1       1  '1 positional argument'
             4808  LOAD_CONST               10
             4810  COMPARE_OP               >=
             4812  POP_JUMP_IF_FALSE  4826  'to 4826'

 L.2044      4816  LOAD_GLOBAL              str
             4818  LOAD_FAST                'count'
             4820  CALL_FUNCTION_1       1  '1 positional argument'
             4822  STORE_FAST               'ChapterNumber'
             4824  JUMP_FORWARD       4838  'to 4838'
             4826  ELSE                     '4838'

 L.2046      4826  LOAD_STR                 '0'
             4828  LOAD_GLOBAL              str
             4830  LOAD_FAST                'count'
             4832  CALL_FUNCTION_1       1  '1 positional argument'
             4834  BINARY_ADD       
             4836  STORE_FAST               'ChapterNumber'
           4838_0  COME_FROM          4824  '4824'

 L.2047      4838  LOAD_GLOBAL              str
             4840  LOAD_FAST                'k'
             4842  CALL_FUNCTION_1       1  '1 positional argument'
             4844  LOAD_ATTR                replace
             4846  LOAD_STR                 "['"
             4848  LOAD_STR                 ''
             4850  CALL_FUNCTION_2       2  '2 positional arguments'
             4852  LOAD_ATTR                replace
             4854  LOAD_STR                 "']"
             4856  LOAD_STR                 ''
             4858  CALL_FUNCTION_2       2  '2 positional arguments'
             4860  LOAD_ATTR                replace
             4862  LOAD_STR                 '?'
             4864  LOAD_STR                 "'"
             4866  CALL_FUNCTION_2       2  '2 positional arguments'
             4868  STORE_FAST               'ChapterName'

 L.2048      4870  LOAD_GLOBAL              str
             4872  LOAD_FAST                'v'
             4874  CALL_FUNCTION_1       1  '1 positional argument'
             4876  LOAD_ATTR                replace
             4878  LOAD_STR                 "['"
             4880  LOAD_STR                 ''
             4882  CALL_FUNCTION_2       2  '2 positional arguments'
             4884  LOAD_ATTR                replace
             4886  LOAD_STR                 "']"
             4888  LOAD_STR                 ''
             4890  CALL_FUNCTION_2       2  '2 positional arguments'
             4892  LOAD_STR                 '.000'
             4894  BINARY_ADD       
             4896  STORE_FAST               'ChapterTime'

 L.2049      4898  LOAD_FAST                'f'
             4900  LOAD_ATTR                write

 L.2051      4902  LOAD_STR                 'CHAPTER'
             4904  LOAD_FAST                'ChapterNumber'
             4906  BINARY_ADD       
             4908  LOAD_STR                 '='
             4910  BINARY_ADD       
             4912  LOAD_FAST                'ChapterTime'
             4914  BINARY_ADD       
             4916  LOAD_STR                 '\n'
             4918  BINARY_ADD       
             4920  LOAD_STR                 'CHAPTER'
             4922  BINARY_ADD       
             4924  LOAD_FAST                'ChapterNumber'
             4926  BINARY_ADD       
             4928  LOAD_STR                 'NAME='
             4930  BINARY_ADD       
             4932  LOAD_GLOBAL              ReplaceChaptersNumber
             4934  LOAD_FAST                'ChapterName'
             4936  CALL_FUNCTION_1       1  '1 positional argument'
             4938  LOAD_ATTR                encode
             4940  LOAD_STR                 'latin-1'
             4942  CALL_FUNCTION_1       1  '1 positional argument'
             4944  LOAD_ATTR                decode
             4946  LOAD_STR                 'latin-1'
             4948  CALL_FUNCTION_1       1  '1 positional argument'
             4950  BINARY_ADD       
             4952  LOAD_STR                 '\n'
             4954  BINARY_ADD       
             4956  CALL_FUNCTION_1       1  '1 positional argument'
             4958  POP_TOP          

 L.2052      4960  LOAD_FAST                'count'
             4962  LOAD_CONST               1
             4964  BINARY_ADD       
             4966  STORE_FAST               'count'
             4968  JUMP_BACK          4794  'to 4794'
             4972  POP_BLOCK        
           4974_0  COME_FROM_LOOP     4784  '4784'
             4974  POP_BLOCK        
             4976  LOAD_CONST               None
           4978_0  COME_FROM_WITH     4780  '4780'
             4978  WITH_CLEANUP_START
             4980  WITH_CLEANUP_FINISH
             4982  END_FINALLY      

 L.2054      4984  LOAD_GLOBAL              print
             4986  LOAD_STR                 'Done!'
             4988  CALL_FUNCTION_1       1  '1 positional argument'
             4990  POP_TOP          
           4992_0  COME_FROM          4758  '4758'
             4992  JUMP_FORWARD       5002  'to 5002'
             4994  ELSE                     '5002'

 L.2056      4994  LOAD_GLOBAL              print
             4996  LOAD_STR                 '\nNo chapters available.'
             4998  CALL_FUNCTION_1       1  '1 positional argument'
             5000  POP_TOP          
           5002_0  COME_FROM          4992  '4992'

 L.2057      5002  LOAD_FAST                'bonus'
             5004  LOAD_CONST               True
             5006  COMPARE_OP               ==
             5008  POP_JUMP_IF_FALSE  5262  'to 5262'

 L.2058      5012  LOAD_GLOBAL              args
             5014  LOAD_ATTR                novideo
             5016  POP_JUMP_IF_FALSE  5262  'to 5262'

 L.2059      5020  LOAD_GLOBAL              args
             5022  LOAD_ATTR                noaudio
             5024  POP_JUMP_IF_FALSE  5262  'to 5262'

 L.2060      5028  LOAD_FAST                'nosubs'
             5030  LOAD_CONST               False
             5032  COMPARE_OP               ==
             5034  POP_JUMP_IF_FALSE  5122  'to 5122'

 L.2061      5038  SETUP_LOOP         5122  'to 5122'
             5040  LOAD_GLOBAL              subsList
             5042  GET_ITER         
             5044  FOR_ITER           5120  'to 5120'
             5046  STORE_FAST               'z'

 L.2062      5048  LOAD_GLOBAL              str
             5050  LOAD_GLOBAL              dict
             5052  LOAD_FAST                'z'
             5054  CALL_FUNCTION_1       1  '1 positional argument'
             5056  LOAD_STR                 'SubsID'
             5058  BINARY_SUBSCR    
             5060  CALL_FUNCTION_1       1  '1 positional argument'
             5062  STORE_FAST               'langAbbrev'

 L.2063      5064  LOAD_GLOBAL              os
             5066  LOAD_ATTR                rename
             5068  LOAD_DEREF               'seriesName'
             5070  LOAD_STR                 ' '
             5072  BINARY_ADD       
             5074  LOAD_STR                 '('
             5076  BINARY_ADD       
             5078  LOAD_FAST                'langAbbrev'
             5080  BINARY_ADD       
             5082  LOAD_STR                 ')'
             5084  BINARY_ADD       
             5086  LOAD_STR                 '.srt'
             5088  BINARY_ADD       

 L.2064      5090  LOAD_FAST                'seriesName2'
             5092  LOAD_STR                 ' '
             5094  BINARY_ADD       
             5096  LOAD_STR                 '('
             5098  BINARY_ADD       
             5100  LOAD_FAST                'langAbbrev'
             5102  BINARY_ADD       
             5104  LOAD_STR                 ')'
             5106  BINARY_ADD       
             5108  LOAD_STR                 '.srt'
             5110  BINARY_ADD       
             5112  CALL_FUNCTION_2       2  '2 positional arguments'
             5114  POP_TOP          
             5116  JUMP_BACK          5044  'to 5044'
             5120  POP_BLOCK        
           5122_0  COME_FROM_LOOP     5038  '5038'
           5122_1  COME_FROM          5034  '5034'

 L.2066      5122  LOAD_FAST                'nosubsfor'
             5124  LOAD_CONST               False
             5126  COMPARE_OP               ==
             5128  POP_JUMP_IF_FALSE  5232  'to 5232'

 L.2067      5132  SETUP_LOOP         5232  'to 5232'
             5134  LOAD_GLOBAL              subsForList
             5136  GET_ITER         
             5138  FOR_ITER           5230  'to 5230'
             5140  STORE_FAST               'z'

 L.2068      5142  LOAD_GLOBAL              str
             5144  LOAD_GLOBAL              dict
             5146  LOAD_FAST                'z'
             5148  CALL_FUNCTION_1       1  '1 positional argument'
             5150  LOAD_STR                 'SubsForID'
             5152  BINARY_SUBSCR    
             5154  CALL_FUNCTION_1       1  '1 positional argument'
             5156  STORE_FAST               'langAbbrev'

 L.2069      5158  LOAD_GLOBAL              os
             5160  LOAD_ATTR                rename
             5162  LOAD_DEREF               'seriesName'
             5164  LOAD_STR                 ' '
             5166  BINARY_ADD       
             5168  LOAD_STR                 '('
             5170  BINARY_ADD       
             5172  LOAD_FAST                'langAbbrev'
             5174  BINARY_ADD       
             5176  LOAD_STR                 ')'
             5178  BINARY_ADD       
             5180  LOAD_STR                 ' '
             5182  BINARY_ADD       
             5184  LOAD_STR                 'Forced'
             5186  BINARY_ADD       
             5188  LOAD_STR                 '.srt'
             5190  BINARY_ADD       

 L.2070      5192  LOAD_FAST                'seriesName2'
             5194  LOAD_STR                 ' '
             5196  BINARY_ADD       
             5198  LOAD_STR                 '('
             5200  BINARY_ADD       
             5202  LOAD_FAST                'langAbbrev'
             5204  BINARY_ADD       
             5206  LOAD_STR                 ')'
             5208  BINARY_ADD       
             5210  LOAD_STR                 ' '
             5212  BINARY_ADD       
             5214  LOAD_STR                 'Forced'
             5216  BINARY_ADD       
             5218  LOAD_STR                 '.srt'
             5220  BINARY_ADD       
             5222  CALL_FUNCTION_2       2  '2 positional arguments'
             5224  POP_TOP          
             5226  JUMP_BACK          5138  'to 5138'
             5230  POP_BLOCK        
           5232_0  COME_FROM_LOOP     5132  '5132'
           5232_1  COME_FROM          5128  '5128'

 L.2072      5232  LOAD_FAST                'nochapters'
             5234  LOAD_CONST               False
             5236  COMPARE_OP               ==
             5238  POP_JUMP_IF_FALSE  5262  'to 5262'

 L.2073      5242  LOAD_GLOBAL              os
             5244  LOAD_ATTR                rename
             5246  LOAD_DEREF               'seriesName'
             5248  LOAD_STR                 ' Chapters.txt'
             5250  BINARY_ADD       
             5252  LOAD_FAST                'seriesName2'
             5254  LOAD_STR                 ' Chapters.txt'
             5256  BINARY_ADD       
             5258  CALL_FUNCTION_2       2  '2 positional arguments'
             5260  POP_TOP          
           5262_0  COME_FROM          5238  '5238'
           5262_1  COME_FROM          5024  '5024'
           5262_2  COME_FROM          5016  '5016'
           5262_3  COME_FROM          5008  '5008'

 L.2074      5262  LOAD_GLOBAL              args
             5264  LOAD_ATTR                novideo
             5266  POP_JUMP_IF_TRUE   5288  'to 5288'

 L.2075      5270  LOAD_FAST                'novideo'
             5272  LOAD_CONST               False
             5274  COMPARE_OP               ==
             5276  POP_JUMP_IF_FALSE  5288  'to 5288'

 L.2076      5280  LOAD_GLOBAL              print
             5282  LOAD_STR                 '\nDownloading video...'
             5284  CALL_FUNCTION_1       1  '1 positional argument'
             5286  POP_TOP          
           5288_0  COME_FROM          5276  '5276'
           5288_1  COME_FROM          5266  '5266'
           5288_2  COME_FROM          4702  '4702'
           5288_3  COME_FROM          3816  '3816'

 L.2077      5288  LOAD_GLOBAL              args
             5290  LOAD_ATTR                hevc
             5292  POP_JUMP_IF_FALSE  5338  'to 5338'

 L.2078      5296  LOAD_DEREF               'seriesName'
             5298  LOAD_STR                 ' ['
             5300  BINARY_ADD       
             5302  LOAD_GLOBAL              str
             5304  LOAD_FAST                'heightp'
             5306  CALL_FUNCTION_1       1  '1 positional argument'
             5308  BINARY_ADD       
             5310  LOAD_STR                 'p] [HEVC].mp4'
             5312  BINARY_ADD       
             5314  STORE_FAST               'inputVideo'

 L.2079      5316  LOAD_DEREF               'seriesName'
             5318  LOAD_STR                 ' ['
             5320  BINARY_ADD       
             5322  LOAD_GLOBAL              str
             5324  LOAD_FAST                'heightp'
             5326  CALL_FUNCTION_1       1  '1 positional argument'
             5328  BINARY_ADD       
             5330  LOAD_STR                 'p] [HEVC].h265'
             5332  BINARY_ADD       
             5334  STORE_FAST               'inputVideoDemuxed'
             5336  JUMP_FORWARD       5508  'to 5508'
             5338  ELSE                     '5508'

 L.2081      5338  LOAD_GLOBAL              args
             5340  LOAD_ATTR                atmos
             5342  POP_JUMP_IF_FALSE  5388  'to 5388'

 L.2082      5346  LOAD_DEREF               'seriesName'
             5348  LOAD_STR                 ' ['
             5350  BINARY_ADD       
             5352  LOAD_GLOBAL              str
             5354  LOAD_FAST                'heightp'
             5356  CALL_FUNCTION_1       1  '1 positional argument'
             5358  BINARY_ADD       
             5360  LOAD_STR                 'p] [HEVC-atmos].mp4'
             5362  BINARY_ADD       
             5364  STORE_FAST               'inputVideo'

 L.2083      5366  LOAD_DEREF               'seriesName'
             5368  LOAD_STR                 ' ['
             5370  BINARY_ADD       
             5372  LOAD_GLOBAL              str
             5374  LOAD_FAST                'heightp'
             5376  CALL_FUNCTION_1       1  '1 positional argument'
             5378  BINARY_ADD       
             5380  LOAD_STR                 'p] [HEVC-atmos].h265'
             5382  BINARY_ADD       
             5384  STORE_FAST               'inputVideoDemuxed'
             5386  JUMP_FORWARD       5428  'to 5428'
             5388  ELSE                     '5428'

 L.2085      5388  LOAD_DEREF               'seriesName'
             5390  LOAD_STR                 ' ['
             5392  BINARY_ADD       
             5394  LOAD_GLOBAL              str
             5396  LOAD_FAST                'heightp'
             5398  CALL_FUNCTION_1       1  '1 positional argument'
             5400  BINARY_ADD       
             5402  LOAD_STR                 'p].mp4'
             5404  BINARY_ADD       
             5406  STORE_FAST               'inputVideo'

 L.2086      5408  LOAD_DEREF               'seriesName'
             5410  LOAD_STR                 ' ['
             5412  BINARY_ADD       
             5414  LOAD_GLOBAL              str
             5416  LOAD_FAST                'heightp'
             5418  CALL_FUNCTION_1       1  '1 positional argument'
             5420  BINARY_ADD       
             5422  LOAD_STR                 'p].h264'
             5424  BINARY_ADD       
             5426  STORE_FAST               'inputVideoDemuxed'
           5428_0  COME_FROM          5386  '5386'

 L.2087      5428  LOAD_GLOBAL              os
             5430  LOAD_ATTR                path
             5432  LOAD_ATTR                isfile
             5434  LOAD_FAST                'inputVideo'
             5436  CALL_FUNCTION_1       1  '1 positional argument'
             5438  POP_JUMP_IF_FALSE  5462  'to 5462'
             5442  LOAD_GLOBAL              os
             5444  LOAD_ATTR                path
             5446  LOAD_ATTR                isfile
             5448  LOAD_FAST                'inputVideo'
             5450  LOAD_STR                 '.aria2'
             5452  BINARY_ADD       
             5454  CALL_FUNCTION_1       1  '1 positional argument'
             5456  UNARY_NOT        
           5458_0  COME_FROM          5438  '5438'
             5458  POP_JUMP_IF_TRUE   5476  'to 5476'
             5462  LOAD_GLOBAL              os
             5464  LOAD_ATTR                path
             5466  LOAD_ATTR                isfile

 L.2088      5468  LOAD_FAST                'inputVideoDemuxed'
             5470  CALL_FUNCTION_1       1  '1 positional argument'
           5472_0  COME_FROM          5458  '5458'
             5472  POP_JUMP_IF_FALSE  5494  'to 5494'

 L.2089      5476  LOAD_GLOBAL              print
             5478  LOAD_STR                 '\n'
             5480  LOAD_FAST                'inputVideo'
             5482  BINARY_ADD       
             5484  LOAD_STR                 '\nFile has already been successfully downloaded previously.'
             5486  BINARY_ADD       
             5488  CALL_FUNCTION_1       1  '1 positional argument'
             5490  POP_TOP          
             5492  JUMP_FORWARD       5508  'to 5508'
             5494  ELSE                     '5508'

 L.2091      5494  LOAD_GLOBAL              downloadFile
             5496  LOAD_GLOBAL              str
             5498  LOAD_FAST                'video_url'
             5500  CALL_FUNCTION_1       1  '1 positional argument'
             5502  LOAD_FAST                'inputVideo'
             5504  CALL_FUNCTION_2       2  '2 positional arguments'
             5506  POP_TOP          
           5508_0  COME_FROM          5492  '5492'
           5508_1  COME_FROM          5336  '5336'

 L.2093      5508  LOAD_GLOBAL              args
             5510  LOAD_ATTR                noaudio
             5512  POP_JUMP_IF_TRUE   5978  'to 5978'

 L.2094      5516  LOAD_FAST                'noaudio'
             5518  LOAD_CONST               False
             5520  COMPARE_OP               ==
             5522  POP_JUMP_IF_FALSE  5978  'to 5978'

 L.2095      5526  LOAD_FAST                'noprotection'
             5528  LOAD_CONST               True
             5530  COMPARE_OP               ==
             5532  POP_JUMP_IF_FALSE  5758  'to 5758'

 L.2096      5536  LOAD_GLOBAL              print
             5538  LOAD_STR                 '\nDownloading audios...'
             5540  CALL_FUNCTION_1       1  '1 positional argument'
             5542  POP_TOP          

 L.2097      5544  SETUP_LOOP         5756  'to 5756'
             5546  LOAD_FAST                'audioList_new'
             5548  LOAD_ATTR                items
             5550  CALL_FUNCTION_0       0  '0 positional arguments'
             5552  GET_ITER         
             5554  FOR_ITER           5754  'to 5754'
             5556  UNPACK_SEQUENCE_2     2 
             5558  STORE_FAST               'k'
             5560  STORE_FAST               'v'

 L.2098      5562  LOAD_GLOBAL              str
             5564  LOAD_FAST                'k'
             5566  CALL_FUNCTION_1       1  '1 positional argument'
             5568  STORE_FAST               'langAbbrev'

 L.2099      5570  LOAD_DEREF               'seriesName'
             5572  LOAD_STR                 ' '
             5574  BINARY_ADD       
             5576  LOAD_STR                 '('
             5578  BINARY_ADD       
             5580  LOAD_FAST                'langAbbrev'
             5582  BINARY_ADD       
             5584  LOAD_STR                 ')'
             5586  BINARY_ADD       
             5588  LOAD_STR                 '.mp4'
             5590  BINARY_ADD       
             5592  STORE_FAST               'inputAudio'

 L.2100      5594  LOAD_DEREF               'seriesName'
             5596  LOAD_STR                 ' '
             5598  BINARY_ADD       
             5600  LOAD_STR                 '('
             5602  BINARY_ADD       
             5604  LOAD_FAST                'langAbbrev'
             5606  BINARY_ADD       
             5608  LOAD_STR                 ')'
             5610  BINARY_ADD       
             5612  LOAD_STR                 '.eac3'
             5614  BINARY_ADD       
             5616  STORE_FAST               'inputAudio2'

 L.2101      5618  LOAD_DEREF               'seriesName'
             5620  LOAD_STR                 ' '
             5622  BINARY_ADD       
             5624  LOAD_STR                 '('
             5626  BINARY_ADD       
             5628  LOAD_FAST                'langAbbrev'
             5630  BINARY_ADD       
             5632  LOAD_STR                 ')'
             5634  BINARY_ADD       
             5636  LOAD_STR                 '_original.eac3'
             5638  BINARY_ADD       
             5640  STORE_FAST               'originalAudio'

 L.2102      5642  LOAD_GLOBAL              os
             5644  LOAD_ATTR                path
             5646  LOAD_ATTR                isfile
             5648  LOAD_FAST                'inputAudio'
             5650  CALL_FUNCTION_1       1  '1 positional argument'
             5652  POP_JUMP_IF_FALSE  5676  'to 5676'
             5656  LOAD_GLOBAL              os
             5658  LOAD_ATTR                path
             5660  LOAD_ATTR                isfile

 L.2103      5662  LOAD_FAST                'inputAudio'
             5664  LOAD_STR                 '.aria2'
             5666  BINARY_ADD       
             5668  CALL_FUNCTION_1       1  '1 positional argument'
             5670  UNARY_NOT        
           5672_0  COME_FROM          5652  '5652'
             5672  POP_JUMP_IF_TRUE   5704  'to 5704'
             5676  LOAD_GLOBAL              os
             5678  LOAD_ATTR                path
             5680  LOAD_ATTR                isfile

 L.2104      5682  LOAD_FAST                'inputAudio2'
             5684  CALL_FUNCTION_1       1  '1 positional argument'
             5686  POP_JUMP_IF_TRUE   5704  'to 5704'
             5690  LOAD_GLOBAL              os
             5692  LOAD_ATTR                path
             5694  LOAD_ATTR                isfile
             5696  LOAD_FAST                'originalAudio'
             5698  CALL_FUNCTION_1       1  '1 positional argument'
           5700_0  COME_FROM          5686  '5686'
           5700_1  COME_FROM          5672  '5672'
             5700  POP_JUMP_IF_FALSE  5722  'to 5722'

 L.2105      5704  LOAD_GLOBAL              print
             5706  LOAD_STR                 '\n'
             5708  LOAD_FAST                'inputAudio'
             5710  BINARY_ADD       
             5712  LOAD_STR                 '\nFile has already been successfully downloaded previously.'
             5714  BINARY_ADD       
             5716  CALL_FUNCTION_1       1  '1 positional argument'
             5718  POP_TOP          
             5720  JUMP_FORWARD       5750  'to 5750'
             5722  ELSE                     '5750'

 L.2107      5722  LOAD_GLOBAL              downloadFile
             5724  LOAD_GLOBAL              str
             5726  LOAD_FAST                'base_url'
             5728  LOAD_GLOBAL              alphanumericSort
             5730  LOAD_FAST                'v'
             5732  CALL_FUNCTION_1       1  '1 positional argument'
             5734  LOAD_CONST               -1
             5738  BINARY_SUBSCR    
             5740  BINARY_ADD       
             5742  CALL_FUNCTION_1       1  '1 positional argument'
             5744  LOAD_FAST                'inputAudio'
             5746  CALL_FUNCTION_2       2  '2 positional arguments'
             5748  POP_TOP          
           5750_0  COME_FROM          5720  '5720'
             5750  JUMP_BACK          5554  'to 5554'
             5754  POP_BLOCK        
           5756_0  COME_FROM_LOOP     5544  '5544'
             5756  JUMP_FORWARD       5978  'to 5978'
             5758  ELSE                     '5978'

 L.2110      5758  LOAD_GLOBAL              print
             5760  LOAD_STR                 '\nDownloading audios...'
             5762  CALL_FUNCTION_1       1  '1 positional argument'
             5764  POP_TOP          

 L.2111      5766  SETUP_LOOP         5978  'to 5978'
             5768  LOAD_FAST                'audioList_new'
             5770  LOAD_ATTR                items
             5772  CALL_FUNCTION_0       0  '0 positional arguments'
             5774  GET_ITER         
             5776  FOR_ITER           5976  'to 5976'
             5778  UNPACK_SEQUENCE_2     2 
             5780  STORE_FAST               'k'
             5782  STORE_FAST               'v'

 L.2112      5784  LOAD_GLOBAL              str
             5786  LOAD_FAST                'k'
             5788  CALL_FUNCTION_1       1  '1 positional argument'
             5790  STORE_FAST               'langAbbrev'

 L.2113      5792  LOAD_DEREF               'seriesName'
             5794  LOAD_STR                 ' '
             5796  BINARY_ADD       
             5798  LOAD_STR                 '('
             5800  BINARY_ADD       
             5802  LOAD_FAST                'langAbbrev'
             5804  BINARY_ADD       
             5806  LOAD_STR                 ')'
             5808  BINARY_ADD       
             5810  LOAD_STR                 '.mp4'
             5812  BINARY_ADD       
             5814  STORE_FAST               'inputAudio'

 L.2114      5816  LOAD_DEREF               'seriesName'
             5818  LOAD_STR                 ' '
             5820  BINARY_ADD       
             5822  LOAD_STR                 '('
             5824  BINARY_ADD       
             5826  LOAD_FAST                'langAbbrev'
             5828  BINARY_ADD       
             5830  LOAD_STR                 ')'
             5832  BINARY_ADD       
             5834  LOAD_STR                 '.eac3'
             5836  BINARY_ADD       
             5838  STORE_FAST               'inputAudio2'

 L.2115      5840  LOAD_DEREF               'seriesName'
             5842  LOAD_STR                 ' '
             5844  BINARY_ADD       
             5846  LOAD_STR                 '('
             5848  BINARY_ADD       
             5850  LOAD_FAST                'langAbbrev'
             5852  BINARY_ADD       
             5854  LOAD_STR                 ')'
             5856  BINARY_ADD       
             5858  LOAD_STR                 '_original.eac3'
             5860  BINARY_ADD       
             5862  STORE_FAST               'originalAudio'

 L.2116      5864  LOAD_GLOBAL              os
             5866  LOAD_ATTR                path
             5868  LOAD_ATTR                isfile
             5870  LOAD_FAST                'inputAudio'
             5872  CALL_FUNCTION_1       1  '1 positional argument'
             5874  POP_JUMP_IF_FALSE  5898  'to 5898'
             5878  LOAD_GLOBAL              os
             5880  LOAD_ATTR                path
             5882  LOAD_ATTR                isfile

 L.2117      5884  LOAD_FAST                'inputAudio'
             5886  LOAD_STR                 '.aria2'
             5888  BINARY_ADD       
             5890  CALL_FUNCTION_1       1  '1 positional argument'
             5892  UNARY_NOT        
           5894_0  COME_FROM          5874  '5874'
             5894  POP_JUMP_IF_TRUE   5926  'to 5926'
             5898  LOAD_GLOBAL              os
             5900  LOAD_ATTR                path
             5902  LOAD_ATTR                isfile

 L.2118      5904  LOAD_FAST                'inputAudio2'
             5906  CALL_FUNCTION_1       1  '1 positional argument'
             5908  POP_JUMP_IF_TRUE   5926  'to 5926'
             5912  LOAD_GLOBAL              os
             5914  LOAD_ATTR                path
             5916  LOAD_ATTR                isfile
             5918  LOAD_FAST                'originalAudio'
             5920  CALL_FUNCTION_1       1  '1 positional argument'
           5922_0  COME_FROM          5908  '5908'
           5922_1  COME_FROM          5894  '5894'
             5922  POP_JUMP_IF_FALSE  5944  'to 5944'

 L.2119      5926  LOAD_GLOBAL              print
             5928  LOAD_STR                 '\n'
             5930  LOAD_FAST                'inputAudio'
             5932  BINARY_ADD       
             5934  LOAD_STR                 '\nFile has already been successfully downloaded previously.'
             5936  BINARY_ADD       
             5938  CALL_FUNCTION_1       1  '1 positional argument'
             5940  POP_TOP          
             5942  JUMP_FORWARD       5972  'to 5972'
             5944  ELSE                     '5972'

 L.2121      5944  LOAD_GLOBAL              downloadFile
             5946  LOAD_GLOBAL              str
             5948  LOAD_FAST                'base_url'
             5950  LOAD_GLOBAL              alphanumericSort
             5952  LOAD_FAST                'v'
             5954  CALL_FUNCTION_1       1  '1 positional argument'
             5956  LOAD_CONST               -1
             5960  BINARY_SUBSCR    
             5962  BINARY_ADD       
             5964  CALL_FUNCTION_1       1  '1 positional argument'
             5966  LOAD_FAST                'inputAudio'
             5968  CALL_FUNCTION_2       2  '2 positional arguments'
             5970  POP_TOP          
           5972_0  COME_FROM          5942  '5942'
             5972  JUMP_BACK          5776  'to 5776'
             5976  POP_BLOCK        
           5978_0  COME_FROM_LOOP     5766  '5766'
           5978_1  COME_FROM          5756  '5756'
           5978_2  COME_FROM          5522  '5522'
           5978_3  COME_FROM          5512  '5512'

 L.2123      5978  LOAD_GLOBAL              args
             5980  LOAD_ATTR                novideo
             5982  UNARY_NOT        
             5984  POP_JUMP_IF_FALSE  5998  'to 5998'
             5988  LOAD_FAST                'novideo'
             5990  LOAD_CONST               False
             5992  COMPARE_OP               ==
           5994_0  COME_FROM          5984  '5984'
             5994  POP_JUMP_IF_TRUE   6018  'to 6018'
             5998  LOAD_GLOBAL              args
             6000  LOAD_ATTR                noaudio
             6002  UNARY_NOT        
             6004  POP_JUMP_IF_FALSE  6060  'to 6060'
             6008  LOAD_FAST                'noaudio'
             6010  LOAD_CONST               False
             6012  COMPARE_OP               ==
           6014_0  COME_FROM          6004  '6004'
           6014_1  COME_FROM          5994  '5994'
             6014  POP_JUMP_IF_FALSE  6060  'to 6060'

 L.2124      6018  LOAD_GLOBAL              print
             6020  LOAD_STR                 '\nGetting KEYS from txt...'
             6022  CALL_FUNCTION_1       1  '1 positional argument'
             6024  POP_TOP          

 L.2125      6026  BUILD_LIST_0          0 
             6028  STORE_FAST               'keys_video'

 L.2126      6030  BUILD_LIST_0          0 
             6032  STORE_FAST               'keys_audio'

 L.2127      6034  LOAD_GLOBAL              keys_file_txt
             6036  STORE_FAST               'keys_video'

 L.2128      6038  LOAD_FAST                'noprotection'
             6040  LOAD_CONST               False
             6042  COMPARE_OP               ==
             6044  POP_JUMP_IF_FALSE  6052  'to 6052'

 L.2129      6048  LOAD_GLOBAL              keys_file_txt
             6050  STORE_FAST               'keys_audio'
           6052_0  COME_FROM          6044  '6044'

 L.2130      6052  LOAD_GLOBAL              print
             6054  LOAD_STR                 'Done!'
             6056  CALL_FUNCTION_1       1  '1 positional argument'
             6058  POP_TOP          
           6060_0  COME_FROM          6014  '6014'

 L.2132      6060  LOAD_CONST               False
             6062  STORE_FAST               'CorrectDecryptVideo'

 L.2133      6064  LOAD_CONST               False
             6066  STORE_FAST               'CorrectDecryptAudio'

 L.2134      6068  LOAD_GLOBAL              os
             6070  LOAD_ATTR                path
             6072  LOAD_ATTR                isfile
             6074  LOAD_GLOBAL              config_data
             6076  CALL_FUNCTION_1       1  '1 positional argument'
             6078  POP_JUMP_IF_FALSE  6092  'to 6092'

 L.2135      6082  LOAD_GLOBAL              os
             6084  LOAD_ATTR                remove
             6086  LOAD_GLOBAL              config_data
             6088  CALL_FUNCTION_1       1  '1 positional argument'
             6090  POP_TOP          
           6092_0  COME_FROM          6078  '6078'

 L.2136      6092  LOAD_GLOBAL              args
             6094  LOAD_ATTR                novideo
             6096  POP_JUMP_IF_TRUE   6110  'to 6110'

 L.2137      6100  LOAD_FAST                'novideo'
             6102  LOAD_CONST               False
             6104  COMPARE_OP               ==
             6106  POP_JUMP_IF_FALSE  6110  'to 6110'
           6110_0  COME_FROM          6106  '6106'
           6110_1  COME_FROM          6096  '6096'

 L.2140      6110  LOAD_GLOBAL              args
             6112  LOAD_ATTR                hevc
             6114  POP_JUMP_IF_FALSE  6204  'to 6204'

 L.2141      6118  LOAD_DEREF               'seriesName'
             6120  LOAD_STR                 ' ['
             6122  BINARY_ADD       
             6124  LOAD_GLOBAL              str
             6126  LOAD_FAST                'heightp'
             6128  CALL_FUNCTION_1       1  '1 positional argument'
             6130  BINARY_ADD       
             6132  LOAD_STR                 'p] [HEVC].mp4'
             6134  BINARY_ADD       
             6136  STORE_FAST               'inputVideo'

 L.2142      6138  LOAD_DEREF               'seriesName'
             6140  LOAD_STR                 ' ['
             6142  BINARY_ADD       
             6144  LOAD_GLOBAL              str
             6146  LOAD_FAST                'heightp'
             6148  CALL_FUNCTION_1       1  '1 positional argument'
             6150  BINARY_ADD       
             6152  LOAD_STR                 'p] [HEVC]'
             6154  BINARY_ADD       
             6156  LOAD_STR                 '_dec.mp4'
             6158  BINARY_ADD       
             6160  STORE_FAST               'outputVideoTemp'

 L.2143      6162  LOAD_DEREF               'seriesName'
             6164  LOAD_STR                 ' ['
             6166  BINARY_ADD       
             6168  LOAD_GLOBAL              str
             6170  LOAD_FAST                'heightp'
             6172  CALL_FUNCTION_1       1  '1 positional argument'
             6174  BINARY_ADD       
             6176  LOAD_STR                 'p] [HEVC].mp4'
             6178  BINARY_ADD       
             6180  STORE_FAST               'outputVideo'

 L.2144      6182  LOAD_DEREF               'seriesName'
             6184  LOAD_STR                 ' ['
             6186  BINARY_ADD       
             6188  LOAD_GLOBAL              str
             6190  LOAD_FAST                'heightp'
             6192  CALL_FUNCTION_1       1  '1 positional argument'
             6194  BINARY_ADD       
             6196  LOAD_STR                 'p] [HEVC].h265'
             6198  BINARY_ADD       
             6200  STORE_FAST               'outputVideoDemuxed'
             6202  JUMP_FORWARD       6382  'to 6382'
             6204  ELSE                     '6382'

 L.2146      6204  LOAD_GLOBAL              args
             6206  LOAD_ATTR                atmos
             6208  POP_JUMP_IF_FALSE  6298  'to 6298'

 L.2147      6212  LOAD_DEREF               'seriesName'
             6214  LOAD_STR                 ' ['
             6216  BINARY_ADD       
             6218  LOAD_GLOBAL              str
             6220  LOAD_FAST                'heightp'
             6222  CALL_FUNCTION_1       1  '1 positional argument'
             6224  BINARY_ADD       
             6226  LOAD_STR                 'p] [HEVC-atmos].mp4'
             6228  BINARY_ADD       
             6230  STORE_FAST               'inputVideo'

 L.2148      6232  LOAD_DEREF               'seriesName'
             6234  LOAD_STR                 ' ['
             6236  BINARY_ADD       
             6238  LOAD_GLOBAL              str
             6240  LOAD_FAST                'heightp'
             6242  CALL_FUNCTION_1       1  '1 positional argument'
             6244  BINARY_ADD       
             6246  LOAD_STR                 'p] [HEVC-atmos]'
             6248  BINARY_ADD       
             6250  LOAD_STR                 '_dec.mp4'
             6252  BINARY_ADD       
             6254  STORE_FAST               'outputVideoTemp'

 L.2149      6256  LOAD_DEREF               'seriesName'
             6258  LOAD_STR                 ' ['
             6260  BINARY_ADD       
             6262  LOAD_GLOBAL              str
             6264  LOAD_FAST                'heightp'
             6266  CALL_FUNCTION_1       1  '1 positional argument'
             6268  BINARY_ADD       
             6270  LOAD_STR                 'p] [HEVC-atmos].mp4'
             6272  BINARY_ADD       
             6274  STORE_FAST               'outputVideo'

 L.2150      6276  LOAD_DEREF               'seriesName'
             6278  LOAD_STR                 ' ['
             6280  BINARY_ADD       
             6282  LOAD_GLOBAL              str
             6284  LOAD_FAST                'heightp'
             6286  CALL_FUNCTION_1       1  '1 positional argument'
             6288  BINARY_ADD       
             6290  LOAD_STR                 'p] [HEVC-atmos].h265'
             6292  BINARY_ADD       
             6294  STORE_FAST               'outputVideoDemuxed'
             6296  JUMP_FORWARD       6382  'to 6382'
             6298  ELSE                     '6382'

 L.2152      6298  LOAD_DEREF               'seriesName'
             6300  LOAD_STR                 ' ['
             6302  BINARY_ADD       
             6304  LOAD_GLOBAL              str
             6306  LOAD_FAST                'heightp'
             6308  CALL_FUNCTION_1       1  '1 positional argument'
             6310  BINARY_ADD       
             6312  LOAD_STR                 'p].mp4'
             6314  BINARY_ADD       
             6316  STORE_FAST               'inputVideo'

 L.2153      6318  LOAD_DEREF               'seriesName'
             6320  LOAD_STR                 ' ['
             6322  BINARY_ADD       
             6324  LOAD_GLOBAL              str
             6326  LOAD_FAST                'heightp'
             6328  CALL_FUNCTION_1       1  '1 positional argument'
             6330  BINARY_ADD       
             6332  LOAD_STR                 'p]'
             6334  BINARY_ADD       
             6336  LOAD_STR                 '_dec.mp4'
             6338  BINARY_ADD       
             6340  STORE_FAST               'outputVideoTemp'

 L.2154      6342  LOAD_DEREF               'seriesName'
             6344  LOAD_STR                 ' ['
             6346  BINARY_ADD       
             6348  LOAD_GLOBAL              str
             6350  LOAD_FAST                'heightp'
             6352  CALL_FUNCTION_1       1  '1 positional argument'
             6354  BINARY_ADD       
             6356  LOAD_STR                 'p].mp4'
             6358  BINARY_ADD       
             6360  STORE_FAST               'outputVideo'

 L.2155      6362  LOAD_DEREF               'seriesName'
             6364  LOAD_STR                 ' ['
             6366  BINARY_ADD       
             6368  LOAD_GLOBAL              str
             6370  LOAD_FAST                'heightp'
             6372  CALL_FUNCTION_1       1  '1 positional argument'
             6374  BINARY_ADD       
             6376  LOAD_STR                 'p].h264'
             6378  BINARY_ADD       
             6380  STORE_FAST               'outputVideoDemuxed'
           6382_0  COME_FROM          6296  '6296'
           6382_1  COME_FROM          6202  '6202'

 L.2157      6382  LOAD_GLOBAL              os
             6384  LOAD_ATTR                path
             6386  LOAD_ATTR                isfile
             6388  LOAD_FAST                'inputVideo'
             6390  CALL_FUNCTION_1       1  '1 positional argument'
             6392  POP_JUMP_IF_FALSE  6468  'to 6468'

 L.2158      6396  LOAD_FAST                'DecryptVideo'
             6398  LOAD_FAST                'inputVideo'
             6400  LOAD_FAST                'outputVideoTemp'

 L.2159      6402  LOAD_FAST                'outputVideo'
             6404  LOAD_FAST                'keys_video'
             6406  LOAD_CONST               ('inputVideo', 'outputVideoTemp', 'outputVideo', 'keys_video')
             6408  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             6410  STORE_FAST               'CorrectDecryptVideo'

 L.2160      6412  LOAD_FAST                'CorrectDecryptVideo'
             6414  LOAD_CONST               False
             6416  COMPARE_OP               ==
             6418  POP_JUMP_IF_TRUE   6432  'to 6432'
             6422  LOAD_FAST                'CorrectDecryptVideo'
             6424  LOAD_CONST               None
             6426  COMPARE_OP               ==
           6428_0  COME_FROM          6418  '6418'
             6428  POP_JUMP_IF_FALSE  6464  'to 6464'

 L.2161      6432  LOAD_GLOBAL              print
             6434  LOAD_STR                 '\nKEY for '
             6436  LOAD_FAST                'inputVideo'
             6438  BINARY_ADD       
             6440  LOAD_STR                 ' is not in txt.'
             6442  BINARY_ADD       
             6444  CALL_FUNCTION_1       1  '1 positional argument'
             6446  POP_TOP          

 L.2162      6448  LOAD_FAST                'DecryptAlternativeV2'
             6450  LOAD_DEREF               'video_pssh'
             6452  LOAD_FAST                'inputVideo'
             6454  LOAD_STR                 'video'
             6456  LOAD_CONST               ('PSSH', 'FInput', 'Type')
             6458  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             6460  STORE_FAST               'CorrectDecryptVideo'
             6462  JUMP_FORWARD       6468  'to 6468'
             6464  ELSE                     '6468'

 L.2164      6464  LOAD_CONST               True
             6466  STORE_FAST               'CorrectDecryptVideo'
           6468_0  COME_FROM          6462  '6462'
           6468_1  COME_FROM          6392  '6392'

 L.2166      6468  LOAD_GLOBAL              args
             6470  LOAD_ATTR                noaudio
             6472  POP_JUMP_IF_TRUE   7060  'to 7060'

 L.2167      6476  LOAD_FAST                'noaudio'
             6478  LOAD_CONST               False
             6480  COMPARE_OP               ==
             6482  POP_JUMP_IF_FALSE  7060  'to 7060'

 L.2168      6486  LOAD_FAST                'noprotection'
             6488  LOAD_CONST               True
             6490  COMPARE_OP               ==
             6492  POP_JUMP_IF_FALSE  6870  'to 6870'

 L.2169      6496  SETUP_LOOP         7060  'to 7060'
             6500  LOAD_FAST                'audioList_new'
             6502  LOAD_ATTR                items
             6504  CALL_FUNCTION_0       0  '0 positional arguments'
             6506  GET_ITER         
             6508  FOR_ITER           6866  'to 6866'
             6512  UNPACK_SEQUENCE_2     2 
             6514  STORE_FAST               'k'
             6516  STORE_FAST               'v'

 L.2170      6518  LOAD_GLOBAL              str
             6520  LOAD_FAST                'k'
             6522  CALL_FUNCTION_1       1  '1 positional argument'
             6524  STORE_FAST               'langAbbrev'

 L.2171      6526  LOAD_DEREF               'seriesName'
             6528  LOAD_STR                 ' '
             6530  BINARY_ADD       
             6532  LOAD_STR                 '('
             6534  BINARY_ADD       
             6536  LOAD_FAST                'langAbbrev'
             6538  BINARY_ADD       
             6540  LOAD_STR                 ')'
             6542  BINARY_ADD       
             6544  LOAD_STR                 '.mp4'
             6546  BINARY_ADD       
             6548  STORE_FAST               'inputAudio'

 L.2172      6550  LOAD_DEREF               'seriesName'
             6552  LOAD_STR                 ' '
             6554  BINARY_ADD       
             6556  LOAD_STR                 '('
             6558  BINARY_ADD       
             6560  LOAD_FAST                'langAbbrev'
             6562  BINARY_ADD       
             6564  LOAD_STR                 ')'
             6566  BINARY_ADD       
             6568  LOAD_STR                 '.eac3'
             6570  BINARY_ADD       
             6572  STORE_FAST               'outputAudio'

 L.2173      6574  LOAD_DEREF               'seriesName'
             6576  LOAD_STR                 ' '
             6578  BINARY_ADD       
             6580  LOAD_STR                 '('
             6582  BINARY_ADD       
             6584  LOAD_FAST                'langAbbrev'
             6586  BINARY_ADD       
             6588  LOAD_STR                 ')'
             6590  BINARY_ADD       
             6592  LOAD_STR                 '.m4a'
             6594  BINARY_ADD       
             6596  STORE_FAST               'outputAudio_aac'

 L.2174      6598  LOAD_GLOBAL              os
             6600  LOAD_ATTR                path
             6602  LOAD_ATTR                isfile
             6604  LOAD_FAST                'inputAudio'
             6606  CALL_FUNCTION_1       1  '1 positional argument'
             6608  POP_JUMP_IF_FALSE  6858  'to 6858'

 L.2175      6612  LOAD_GLOBAL              print
             6614  LOAD_STR                 '\nDemuxing audio...'
             6616  CALL_FUNCTION_1       1  '1 positional argument'
             6618  POP_TOP          

 L.2176      6620  LOAD_GLOBAL              subprocess
             6622  LOAD_ATTR                Popen

 L.2177      6624  LOAD_GLOBAL              ffprobepath
             6626  LOAD_STR                 '-v'
             6628  LOAD_STR                 'quiet'
             6630  LOAD_STR                 '-print_format'
             6632  LOAD_STR                 'json'
             6634  LOAD_STR                 '-show_format'

 L.2178      6636  LOAD_STR                 '-show_streams'
             6638  LOAD_FAST                'inputAudio'
             6640  BUILD_LIST_8          8 
             6642  LOAD_GLOBAL              subprocess
             6644  LOAD_ATTR                PIPE
             6646  LOAD_CONST               ('stdout',)
             6648  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             6650  STORE_FAST               'mediainfo'

 L.2179      6652  LOAD_GLOBAL              json
             6654  LOAD_ATTR                load
             6656  LOAD_FAST                'mediainfo'
             6658  LOAD_ATTR                stdout
             6660  CALL_FUNCTION_1       1  '1 positional argument'
             6662  STORE_FAST               'mediainfo'

 L.2180      6664  LOAD_FAST                'mediainfo'
             6666  LOAD_STR                 'streams'
             6668  BINARY_SUBSCR    
             6670  LOAD_CONST               0
             6672  BINARY_SUBSCR    
             6674  LOAD_STR                 'codec_name'
             6676  BINARY_SUBSCR    
             6678  STORE_FAST               'codec_name'

 L.2181      6680  LOAD_FAST                'codec_name'
             6682  LOAD_STR                 'aac'
             6684  COMPARE_OP               ==
             6686  POP_JUMP_IF_FALSE  6774  'to 6774'

 L.2182      6690  LOAD_GLOBAL              print
             6692  LOAD_FAST                'inputAudio'
             6694  LOAD_STR                 ' -> '
             6696  BINARY_ADD       
             6698  LOAD_FAST                'outputAudio_aac'
             6700  BINARY_ADD       
             6702  CALL_FUNCTION_1       1  '1 positional argument'
             6704  POP_TOP          

 L.2183      6706  LOAD_GLOBAL              ffmpy
             6708  LOAD_ATTR                FFmpeg
             6710  LOAD_GLOBAL              ffmpegpath
             6712  LOAD_FAST                'inputAudio'
             6714  LOAD_CONST               None
             6716  BUILD_MAP_1           1 

 L.2184      6718  LOAD_FAST                'outputAudio_aac'
             6720  LOAD_STR                 '-c copy'
             6722  BUILD_MAP_1           1 

 L.2185      6724  LOAD_STR                 '-y -hide_banner -loglevel warning'
             6726  LOAD_CONST               ('executable', 'inputs', 'outputs', 'global_options')
             6728  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             6730  STORE_FAST               'ff'

 L.2186      6732  LOAD_FAST                'ff'
             6734  LOAD_ATTR                run
             6736  CALL_FUNCTION_0       0  '0 positional arguments'
             6738  POP_TOP          

 L.2187      6740  LOAD_GLOBAL              time
             6742  LOAD_ATTR                sleep
             6744  LOAD_CONST               0.05
             6746  CALL_FUNCTION_1       1  '1 positional argument'
             6748  POP_TOP          

 L.2188      6750  LOAD_GLOBAL              os
             6752  LOAD_ATTR                remove
             6754  LOAD_FAST                'inputAudio'
             6756  CALL_FUNCTION_1       1  '1 positional argument'
             6758  POP_TOP          

 L.2189      6760  LOAD_GLOBAL              print
             6762  LOAD_STR                 '\nDone!'
             6764  CALL_FUNCTION_1       1  '1 positional argument'
             6766  POP_TOP          

 L.2190      6768  LOAD_CONST               True
             6770  STORE_FAST               'CorrectDecryptAudio'
             6772  JUMP_FORWARD       6856  'to 6856'
             6774  ELSE                     '6856'

 L.2192      6774  LOAD_GLOBAL              print
             6776  LOAD_FAST                'inputAudio'
             6778  LOAD_STR                 ' -> '
             6780  BINARY_ADD       
             6782  LOAD_FAST                'outputAudio'
             6784  BINARY_ADD       
             6786  CALL_FUNCTION_1       1  '1 positional argument'
             6788  POP_TOP          

 L.2193      6790  LOAD_GLOBAL              ffmpy
             6792  LOAD_ATTR                FFmpeg
             6794  LOAD_GLOBAL              ffmpegpath
             6796  LOAD_FAST                'inputAudio'
             6798  LOAD_CONST               None
             6800  BUILD_MAP_1           1 

 L.2194      6802  LOAD_FAST                'outputAudio'
             6804  LOAD_STR                 '-c copy'
             6806  BUILD_MAP_1           1 

 L.2195      6808  LOAD_STR                 '-y -hide_banner -loglevel warning'
             6810  LOAD_CONST               ('executable', 'inputs', 'outputs', 'global_options')
             6812  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             6814  STORE_FAST               'ff'

 L.2196      6816  LOAD_FAST                'ff'
             6818  LOAD_ATTR                run
             6820  CALL_FUNCTION_0       0  '0 positional arguments'
             6822  POP_TOP          

 L.2197      6824  LOAD_GLOBAL              time
             6826  LOAD_ATTR                sleep
             6828  LOAD_CONST               0.05
             6830  CALL_FUNCTION_1       1  '1 positional argument'
             6832  POP_TOP          

 L.2198      6834  LOAD_GLOBAL              os
             6836  LOAD_ATTR                remove
             6838  LOAD_FAST                'inputAudio'
             6840  CALL_FUNCTION_1       1  '1 positional argument'
             6842  POP_TOP          

 L.2199      6844  LOAD_GLOBAL              print
             6846  LOAD_STR                 '\nDone!'
             6848  CALL_FUNCTION_1       1  '1 positional argument'
             6850  POP_TOP          

 L.2200      6852  LOAD_CONST               True
             6854  STORE_FAST               'CorrectDecryptAudio'
           6856_0  COME_FROM          6772  '6772'
             6856  JUMP_FORWARD       6862  'to 6862'
             6858  ELSE                     '6862'

 L.2202      6858  LOAD_CONST               True
             6860  STORE_FAST               'CorrectDecryptAudio'
           6862_0  COME_FROM          6856  '6856'
             6862  JUMP_BACK          6508  'to 6508'
             6866  POP_BLOCK        
           6868_0  COME_FROM_LOOP     6496  '6496'
             6868  JUMP_FORWARD       7060  'to 7060'
             6870  ELSE                     '7060'

 L.2205      6870  SETUP_LOOP         7060  'to 7060'
             6872  LOAD_FAST                'audioList_new'
             6874  LOAD_ATTR                items
             6876  CALL_FUNCTION_0       0  '0 positional arguments'
             6878  GET_ITER         
             6880  FOR_ITER           7058  'to 7058'
             6882  UNPACK_SEQUENCE_2     2 
             6884  STORE_FAST               'k'
             6886  STORE_FAST               'v'

 L.2206      6888  LOAD_GLOBAL              str
             6890  LOAD_FAST                'k'
             6892  CALL_FUNCTION_1       1  '1 positional argument'
             6894  STORE_FAST               'langAbbrev'

 L.2207      6896  LOAD_DEREF               'seriesName'
             6898  LOAD_STR                 ' '
             6900  BINARY_ADD       
             6902  LOAD_STR                 '('
             6904  BINARY_ADD       
             6906  LOAD_FAST                'langAbbrev'
             6908  BINARY_ADD       
             6910  LOAD_STR                 ')'
             6912  BINARY_ADD       
             6914  LOAD_STR                 '.mp4'
             6916  BINARY_ADD       
             6918  STORE_FAST               'inputAudio'

 L.2208      6920  LOAD_DEREF               'seriesName'
             6922  LOAD_STR                 ' '
             6924  BINARY_ADD       
             6926  LOAD_STR                 '('
             6928  BINARY_ADD       
             6930  LOAD_FAST                'langAbbrev'
             6932  BINARY_ADD       
             6934  LOAD_STR                 ')'
             6936  BINARY_ADD       
             6938  LOAD_STR                 '_dec.mp4'
             6940  BINARY_ADD       
             6942  STORE_FAST               'outputAudioTemp'

 L.2209      6944  LOAD_DEREF               'seriesName'
             6946  LOAD_STR                 ' '
             6948  BINARY_ADD       
             6950  LOAD_STR                 '('
             6952  BINARY_ADD       
             6954  LOAD_FAST                'langAbbrev'
             6956  BINARY_ADD       
             6958  LOAD_STR                 ')'
             6960  BINARY_ADD       
             6962  LOAD_STR                 '.eac3'
             6964  BINARY_ADD       
             6966  STORE_FAST               'outputAudio'

 L.2210      6968  LOAD_GLOBAL              os
             6970  LOAD_ATTR                path
             6972  LOAD_ATTR                isfile
             6974  LOAD_FAST                'inputAudio'
             6976  CALL_FUNCTION_1       1  '1 positional argument'
             6978  POP_JUMP_IF_FALSE  6880  'to 6880'

 L.2211      6982  LOAD_FAST                'DecryptAudio'
             6984  LOAD_FAST                'inputAudio'

 L.2212      6986  LOAD_FAST                'outputAudioTemp'

 L.2213      6988  LOAD_FAST                'outputAudio'

 L.2214      6990  LOAD_FAST                'keys_audio'
             6992  LOAD_CONST               ('inputAudio', 'outputAudioTemp', 'outputAudio', 'keys_audio')
             6994  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             6996  STORE_FAST               'CorrectDecryptAudio'

 L.2215      6998  LOAD_FAST                'CorrectDecryptAudio'
             7000  LOAD_CONST               False
             7002  COMPARE_OP               ==
             7004  POP_JUMP_IF_TRUE   7018  'to 7018'
             7008  LOAD_FAST                'CorrectDecryptAudio'
             7010  LOAD_CONST               None
             7012  COMPARE_OP               ==
           7014_0  COME_FROM          7004  '7004'
             7014  POP_JUMP_IF_FALSE  7050  'to 7050'

 L.2216      7018  LOAD_GLOBAL              print
             7020  LOAD_STR                 '\nKEY for '
             7022  LOAD_FAST                'inputAudio'
             7024  BINARY_ADD       
             7026  LOAD_STR                 ' is not in txt.'
             7028  BINARY_ADD       
             7030  CALL_FUNCTION_1       1  '1 positional argument'
             7032  POP_TOP          

 L.2217      7034  LOAD_FAST                'DecryptAlternativeV2'
             7036  LOAD_DEREF               'audio_pssh'

 L.2218      7038  LOAD_FAST                'inputAudio'

 L.2219      7040  LOAD_STR                 'audio'
             7042  LOAD_CONST               ('PSSH', 'FInput', 'Type')
             7044  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             7046  STORE_FAST               'CorrectDecryptAudio'
             7048  JUMP_FORWARD       7054  'to 7054'
             7050  ELSE                     '7054'

 L.2221      7050  LOAD_CONST               True
             7052  STORE_FAST               'CorrectDecryptAudio'
           7054_0  COME_FROM          7048  '7048'
             7054  JUMP_BACK          6880  'to 6880'
             7058  POP_BLOCK        
           7060_0  COME_FROM_LOOP     6870  '6870'
           7060_1  COME_FROM          6868  '6868'
           7060_2  COME_FROM          6482  '6482'
           7060_3  COME_FROM          6472  '6472'

 L.2223      7060  LOAD_GLOBAL              args
             7062  LOAD_ATTR                nomux
             7064  POP_JUMP_IF_FALSE  7634  'to 7634'

 L.2224      7068  LOAD_FAST                'bonus'
             7070  LOAD_CONST               True
             7072  COMPARE_OP               ==
             7074  POP_JUMP_IF_FALSE  7634  'to 7634'

 L.2225      7078  LOAD_GLOBAL              args
             7080  LOAD_ATTR                novideo
             7082  POP_JUMP_IF_TRUE   7170  'to 7170'

 L.2226      7086  LOAD_FAST                'novideo'
             7088  LOAD_CONST               False
             7090  COMPARE_OP               ==
             7092  POP_JUMP_IF_FALSE  7170  'to 7170'

 L.2227      7096  LOAD_GLOBAL              os
             7098  LOAD_ATTR                path
             7100  LOAD_ATTR                isfile
             7102  LOAD_DEREF               'seriesName'
             7104  LOAD_STR                 ' ['
             7106  BINARY_ADD       
             7108  LOAD_GLOBAL              str
             7110  LOAD_FAST                'heightp'
             7112  CALL_FUNCTION_1       1  '1 positional argument'
             7114  BINARY_ADD       
             7116  LOAD_STR                 'p].mp4'
             7118  BINARY_ADD       
             7120  CALL_FUNCTION_1       1  '1 positional argument'
             7122  POP_JUMP_IF_FALSE  7170  'to 7170'

 L.2228      7126  LOAD_GLOBAL              os
             7128  LOAD_ATTR                rename
             7130  LOAD_DEREF               'seriesName'
             7132  LOAD_STR                 ' ['
             7134  BINARY_ADD       
             7136  LOAD_GLOBAL              str
             7138  LOAD_FAST                'heightp'
             7140  CALL_FUNCTION_1       1  '1 positional argument'
             7142  BINARY_ADD       
             7144  LOAD_STR                 'p].mp4'
             7146  BINARY_ADD       

 L.2229      7148  LOAD_FAST                'seriesName2'
             7150  LOAD_STR                 ' ['
             7152  BINARY_ADD       
             7154  LOAD_GLOBAL              str
             7156  LOAD_FAST                'heightp'
             7158  CALL_FUNCTION_1       1  '1 positional argument'
             7160  BINARY_ADD       
             7162  LOAD_STR                 'p].mp4'
             7164  BINARY_ADD       
             7166  CALL_FUNCTION_2       2  '2 positional arguments'
             7168  POP_TOP          
           7170_0  COME_FROM          7122  '7122'
           7170_1  COME_FROM          7092  '7092'
           7170_2  COME_FROM          7082  '7082'

 L.2230      7170  LOAD_FAST                'nosubs'
             7172  LOAD_CONST               False
             7174  COMPARE_OP               ==
             7176  POP_JUMP_IF_FALSE  7298  'to 7298'

 L.2231      7180  SETUP_LOOP         7298  'to 7298'
             7182  LOAD_GLOBAL              subsList
             7184  GET_ITER         
             7186  FOR_ITER           7296  'to 7296'
             7188  STORE_FAST               'z'

 L.2232      7190  LOAD_GLOBAL              str
             7192  LOAD_GLOBAL              dict
             7194  LOAD_FAST                'z'
             7196  CALL_FUNCTION_1       1  '1 positional argument'
             7198  LOAD_STR                 'SubsID'
             7200  BINARY_SUBSCR    
             7202  CALL_FUNCTION_1       1  '1 positional argument'
             7204  STORE_FAST               'langAbbrev'

 L.2233      7206  LOAD_GLOBAL              os
             7208  LOAD_ATTR                path
             7210  LOAD_ATTR                isfile
             7212  LOAD_DEREF               'seriesName'
             7214  LOAD_STR                 ' '
             7216  BINARY_ADD       
             7218  LOAD_STR                 '('
             7220  BINARY_ADD       
             7222  LOAD_FAST                'langAbbrev'
             7224  BINARY_ADD       
             7226  LOAD_STR                 ')'
             7228  BINARY_ADD       
             7230  LOAD_STR                 '.srt'
             7232  BINARY_ADD       
             7234  CALL_FUNCTION_1       1  '1 positional argument'
             7236  POP_JUMP_IF_FALSE  7186  'to 7186'

 L.2234      7240  LOAD_GLOBAL              os
             7242  LOAD_ATTR                rename
             7244  LOAD_DEREF               'seriesName'
             7246  LOAD_STR                 ' '
             7248  BINARY_ADD       
             7250  LOAD_STR                 '('
             7252  BINARY_ADD       
             7254  LOAD_FAST                'langAbbrev'
             7256  BINARY_ADD       
             7258  LOAD_STR                 ')'
             7260  BINARY_ADD       
             7262  LOAD_STR                 '.srt'
             7264  BINARY_ADD       

 L.2235      7266  LOAD_FAST                'seriesName2'
             7268  LOAD_STR                 ' '
             7270  BINARY_ADD       
             7272  LOAD_STR                 '('
             7274  BINARY_ADD       
             7276  LOAD_FAST                'langAbbrev'
             7278  BINARY_ADD       
             7280  LOAD_STR                 ')'
             7282  BINARY_ADD       
             7284  LOAD_STR                 '.srt'
             7286  BINARY_ADD       
             7288  CALL_FUNCTION_2       2  '2 positional arguments'
             7290  POP_TOP          
             7292  JUMP_BACK          7186  'to 7186'
             7296  POP_BLOCK        
           7298_0  COME_FROM_LOOP     7180  '7180'
           7298_1  COME_FROM          7176  '7176'

 L.2237      7298  LOAD_FAST                'nosubsfor'
             7300  LOAD_CONST               False
             7302  COMPARE_OP               ==
             7304  POP_JUMP_IF_FALSE  7450  'to 7450'

 L.2238      7308  SETUP_LOOP         7450  'to 7450'
             7310  LOAD_GLOBAL              subsForList
             7312  GET_ITER         
             7314  FOR_ITER           7448  'to 7448'
             7316  STORE_FAST               'z'

 L.2239      7318  LOAD_GLOBAL              str
             7320  LOAD_GLOBAL              dict
             7322  LOAD_FAST                'z'
             7324  CALL_FUNCTION_1       1  '1 positional argument'
             7326  LOAD_STR                 'SubsForID'
             7328  BINARY_SUBSCR    
             7330  CALL_FUNCTION_1       1  '1 positional argument'
             7332  STORE_FAST               'langAbbrev'

 L.2240      7334  LOAD_GLOBAL              os
             7336  LOAD_ATTR                path
             7338  LOAD_ATTR                isfile

 L.2241      7340  LOAD_DEREF               'seriesName'
             7342  LOAD_STR                 ' '
             7344  BINARY_ADD       
             7346  LOAD_STR                 '('
             7348  BINARY_ADD       
             7350  LOAD_FAST                'langAbbrev'
             7352  BINARY_ADD       
             7354  LOAD_STR                 ')'
             7356  BINARY_ADD       
             7358  LOAD_STR                 ' '
             7360  BINARY_ADD       
             7362  LOAD_STR                 'Forced'
             7364  BINARY_ADD       
             7366  LOAD_STR                 '.srt'
             7368  BINARY_ADD       
             7370  CALL_FUNCTION_1       1  '1 positional argument'
             7372  POP_JUMP_IF_FALSE  7314  'to 7314'

 L.2242      7376  LOAD_GLOBAL              os
             7378  LOAD_ATTR                rename

 L.2243      7380  LOAD_DEREF               'seriesName'
             7382  LOAD_STR                 ' '
             7384  BINARY_ADD       
             7386  LOAD_STR                 '('
             7388  BINARY_ADD       
             7390  LOAD_FAST                'langAbbrev'
             7392  BINARY_ADD       
             7394  LOAD_STR                 ')'
             7396  BINARY_ADD       
             7398  LOAD_STR                 ' '
             7400  BINARY_ADD       
             7402  LOAD_STR                 'Forced'
             7404  BINARY_ADD       
             7406  LOAD_STR                 '.srt'
             7408  BINARY_ADD       

 L.2244      7410  LOAD_FAST                'seriesName2'
             7412  LOAD_STR                 ' '
             7414  BINARY_ADD       
             7416  LOAD_STR                 '('
             7418  BINARY_ADD       
             7420  LOAD_FAST                'langAbbrev'
             7422  BINARY_ADD       
             7424  LOAD_STR                 ')'
             7426  BINARY_ADD       
             7428  LOAD_STR                 ' '
             7430  BINARY_ADD       
             7432  LOAD_STR                 'Forced'
             7434  BINARY_ADD       
             7436  LOAD_STR                 '.srt'
             7438  BINARY_ADD       
             7440  CALL_FUNCTION_2       2  '2 positional arguments'
             7442  POP_TOP          
             7444  JUMP_BACK          7314  'to 7314'
             7448  POP_BLOCK        
           7450_0  COME_FROM_LOOP     7308  '7308'
           7450_1  COME_FROM          7304  '7304'

 L.2246      7450  LOAD_GLOBAL              args
             7452  LOAD_ATTR                noaudio
             7454  POP_JUMP_IF_TRUE   7586  'to 7586'

 L.2247      7458  LOAD_FAST                'noaudio'
             7460  LOAD_CONST               False
             7462  COMPARE_OP               ==
             7464  POP_JUMP_IF_FALSE  7586  'to 7586'

 L.2248      7468  SETUP_LOOP         7586  'to 7586'
             7470  LOAD_FAST                'audioList_new'
             7472  LOAD_ATTR                items
             7474  CALL_FUNCTION_0       0  '0 positional arguments'
             7476  GET_ITER         
             7478  FOR_ITER           7584  'to 7584'
             7480  UNPACK_SEQUENCE_2     2 
             7482  STORE_FAST               'k'
             7484  STORE_FAST               'v'

 L.2249      7486  LOAD_GLOBAL              str
             7488  LOAD_FAST                'k'
             7490  CALL_FUNCTION_1       1  '1 positional argument'
             7492  STORE_FAST               'langAbbrev'

 L.2250      7494  LOAD_GLOBAL              os
             7496  LOAD_ATTR                path
             7498  LOAD_ATTR                isfile
             7500  LOAD_DEREF               'seriesName'
             7502  LOAD_STR                 ' '
             7504  BINARY_ADD       
             7506  LOAD_STR                 '('
             7508  BINARY_ADD       
             7510  LOAD_FAST                'langAbbrev'
             7512  BINARY_ADD       
             7514  LOAD_STR                 ')'
             7516  BINARY_ADD       
             7518  LOAD_STR                 '.eac3'
             7520  BINARY_ADD       
             7522  CALL_FUNCTION_1       1  '1 positional argument'
             7524  POP_JUMP_IF_FALSE  7478  'to 7478'

 L.2251      7528  LOAD_GLOBAL              os
             7530  LOAD_ATTR                rename
             7532  LOAD_DEREF               'seriesName'
             7534  LOAD_STR                 ' '
             7536  BINARY_ADD       
             7538  LOAD_STR                 '('
             7540  BINARY_ADD       
             7542  LOAD_FAST                'langAbbrev'
             7544  BINARY_ADD       
             7546  LOAD_STR                 ')'
             7548  BINARY_ADD       
             7550  LOAD_STR                 '.eac3'
             7552  BINARY_ADD       

 L.2252      7554  LOAD_FAST                'seriesName2'
             7556  LOAD_STR                 ' '
             7558  BINARY_ADD       
             7560  LOAD_STR                 '('
             7562  BINARY_ADD       
             7564  LOAD_FAST                'langAbbrev'
             7566  BINARY_ADD       
             7568  LOAD_STR                 ')'
             7570  BINARY_ADD       
             7572  LOAD_STR                 '.eac3'
             7574  BINARY_ADD       
             7576  CALL_FUNCTION_2       2  '2 positional arguments'
             7578  POP_TOP          
             7580  JUMP_BACK          7478  'to 7478'
             7584  POP_BLOCK        
           7586_0  COME_FROM_LOOP     7468  '7468'
           7586_1  COME_FROM          7464  '7464'
           7586_2  COME_FROM          7454  '7454'

 L.2254      7586  LOAD_FAST                'nochapters'
             7588  LOAD_CONST               False
             7590  COMPARE_OP               ==
             7592  POP_JUMP_IF_FALSE  7634  'to 7634'

 L.2255      7596  LOAD_GLOBAL              os
             7598  LOAD_ATTR                path
             7600  LOAD_ATTR                isfile
             7602  LOAD_DEREF               'seriesName'
             7604  LOAD_STR                 ' Chapters.txt'
             7606  BINARY_ADD       
             7608  CALL_FUNCTION_1       1  '1 positional argument'
             7610  POP_JUMP_IF_FALSE  7634  'to 7634'

 L.2256      7614  LOAD_GLOBAL              os
             7616  LOAD_ATTR                rename
             7618  LOAD_DEREF               'seriesName'
             7620  LOAD_STR                 ' Chapters.txt'
             7622  BINARY_ADD       
             7624  LOAD_FAST                'seriesName2'
             7626  LOAD_STR                 ' Chapters.txt'
             7628  BINARY_ADD       
             7630  CALL_FUNCTION_2       2  '2 positional arguments'
             7632  POP_TOP          
           7634_0  COME_FROM          7610  '7610'
           7634_1  COME_FROM          7592  '7592'
           7634_2  COME_FROM          7074  '7074'
           7634_3  COME_FROM          7064  '7064'

 L.2258      7634  LOAD_GLOBAL              args
             7636  LOAD_ATTR                noaudio
             7638  POP_JUMP_IF_TRUE   8258  'to 8258'

 L.2259      7642  LOAD_FAST                'noaudio'
             7644  LOAD_CONST               False
             7646  COMPARE_OP               ==
             7648  POP_JUMP_IF_FALSE  8258  'to 8258'

 L.2260      7652  LOAD_GLOBAL              args
             7654  LOAD_ATTR                fpitch
             7656  POP_JUMP_IF_FALSE  8258  'to 8258'

 L.2261      7660  LOAD_GLOBAL              args
             7662  LOAD_ATTR                sourcefps
             7664  POP_JUMP_IF_FALSE  7684  'to 7684'

 L.2262      7668  LOAD_GLOBAL              float
             7670  LOAD_GLOBAL              args
             7672  LOAD_ATTR                sourcefps
             7674  LOAD_CONST               0
             7676  BINARY_SUBSCR    
             7678  CALL_FUNCTION_1       1  '1 positional argument'
             7680  STORE_FAST               'sourcefps'
             7682  JUMP_FORWARD       7692  'to 7692'
             7684  ELSE                     '7692'

 L.2264      7684  LOAD_GLOBAL              float
             7686  LOAD_CONST               23.976
             7688  CALL_FUNCTION_1       1  '1 positional argument'
             7690  STORE_FAST               'sourcefps'
           7692_0  COME_FROM          7682  '7682'

 L.2265      7692  LOAD_GLOBAL              args
             7694  LOAD_ATTR                targetfps
             7696  POP_JUMP_IF_FALSE  7716  'to 7716'

 L.2266      7700  LOAD_GLOBAL              float
             7702  LOAD_GLOBAL              args
             7704  LOAD_ATTR                targetfps
             7706  LOAD_CONST               0
             7708  BINARY_SUBSCR    
             7710  CALL_FUNCTION_1       1  '1 positional argument'
             7712  STORE_FAST               'targetfps'
             7714  JUMP_FORWARD       7724  'to 7724'
             7716  ELSE                     '7724'

 L.2268      7716  LOAD_GLOBAL              float
             7718  LOAD_CONST               25
             7720  CALL_FUNCTION_1       1  '1 positional argument'
             7722  STORE_FAST               'targetfps'
           7724_0  COME_FROM          7714  '7714'

 L.2269      7724  LOAD_GLOBAL              float
             7726  LOAD_FAST                'targetfps'
             7728  LOAD_CONST               100
             7730  BINARY_MULTIPLY  
             7732  LOAD_FAST                'sourcefps'
             7734  BINARY_TRUE_DIVIDE
             7736  CALL_FUNCTION_1       1  '1 positional argument'
             7738  STORE_FAST               'pitch'

 L.2270      7740  LOAD_GLOBAL              round
             7742  LOAD_FAST                'pitch'
             7744  LOAD_CONST               4
             7746  CALL_FUNCTION_2       2  '2 positional arguments'
             7748  STORE_FAST               'pitch'

 L.2271      7750  SETUP_LOOP         8258  'to 8258'
             7754  LOAD_FAST                'audioList_new'
             7756  LOAD_ATTR                items
             7758  CALL_FUNCTION_0       0  '0 positional arguments'
             7760  GET_ITER         
             7762  FOR_ITER           8256  'to 8256'
             7766  UNPACK_SEQUENCE_2     2 
             7768  STORE_FAST               'k'
             7770  STORE_FAST               'v'

 L.2272      7772  LOAD_GLOBAL              str
             7774  LOAD_FAST                'k'
             7776  CALL_FUNCTION_1       1  '1 positional argument'
             7778  STORE_FAST               'langAbbrev'

 L.2273      7780  LOAD_GLOBAL              str
             7782  LOAD_FAST                'langAbbrev'
             7784  CALL_FUNCTION_1       1  '1 positional argument'
             7786  LOAD_GLOBAL              list
             7788  LOAD_GLOBAL              args
             7790  LOAD_ATTR                fpitch
             7792  CALL_FUNCTION_1       1  '1 positional argument'
             7794  COMPARE_OP               in
             7796  POP_JUMP_IF_FALSE  7762  'to 7762'

 L.2274      7800  LOAD_DEREF               'seriesName'
             7802  LOAD_STR                 ' '
             7804  BINARY_ADD       
             7806  LOAD_STR                 '('
             7808  BINARY_ADD       
             7810  LOAD_FAST                'langAbbrev'
             7812  BINARY_ADD       
             7814  LOAD_STR                 ')'
             7816  BINARY_ADD       
             7818  LOAD_STR                 '.eac3'
             7820  BINARY_ADD       
             7822  STORE_FAST               'inputAudio'

 L.2275      7824  LOAD_DEREF               'seriesName'
             7826  LOAD_STR                 ' '
             7828  BINARY_ADD       
             7830  LOAD_STR                 '('
             7832  BINARY_ADD       
             7834  LOAD_FAST                'langAbbrev'
             7836  BINARY_ADD       
             7838  LOAD_STR                 ')'
             7840  BINARY_ADD       
             7842  LOAD_STR                 '.eac3'
             7844  BINARY_ADD       
             7846  STORE_FAST               'outputAudio'

 L.2276      7848  LOAD_DEREF               'seriesName'
             7850  LOAD_STR                 ' '
             7852  BINARY_ADD       
             7854  LOAD_STR                 '('
             7856  BINARY_ADD       
             7858  LOAD_FAST                'langAbbrev'
             7860  BINARY_ADD       
             7862  LOAD_STR                 ')'
             7864  BINARY_ADD       
             7866  LOAD_STR                 '_original.eac3'
             7868  BINARY_ADD       
             7870  STORE_FAST               'originalAudio'

 L.2277      7872  LOAD_DEREF               'seriesName'
             7874  LOAD_STR                 ' '
             7876  BINARY_ADD       
             7878  LOAD_STR                 '('
             7880  BINARY_ADD       
             7882  LOAD_FAST                'langAbbrev'
             7884  BINARY_ADD       
             7886  LOAD_STR                 ')'
             7888  BINARY_ADD       
             7890  LOAD_STR                 '_original.eac3.lwi'
             7892  BINARY_ADD       
             7894  STORE_FAST               'originalAudio_index'

 L.2278      7896  LOAD_FAST                'originalAudio'
             7898  LOAD_STR                 '.avs'
             7900  BINARY_ADD       
             7902  STORE_FAST               'avsfile'

 L.2279      7904  LOAD_GLOBAL              os
             7906  LOAD_ATTR                path
             7908  LOAD_ATTR                isfile
             7910  LOAD_FAST                'inputAudio'
             7912  CALL_FUNCTION_1       1  '1 positional argument'
             7914  POP_JUMP_IF_FALSE  8058  'to 8058'

 L.2280      7918  LOAD_GLOBAL              os
             7920  LOAD_ATTR                path
             7922  LOAD_ATTR                isfile
             7924  LOAD_FAST                'originalAudio'
             7926  CALL_FUNCTION_1       1  '1 positional argument'
             7928  POP_JUMP_IF_TRUE   8058  'to 8058'

 L.2281      7932  LOAD_GLOBAL              os
             7934  LOAD_ATTR                rename
             7936  LOAD_FAST                'inputAudio'
             7938  LOAD_FAST                'originalAudio'
             7940  CALL_FUNCTION_2       2  '2 positional arguments'
             7942  POP_TOP          

 L.2282      7944  LOAD_GLOBAL              os
             7946  LOAD_ATTR                path
             7948  LOAD_ATTR                isfile
             7950  LOAD_FAST                'avsfile'
             7952  CALL_FUNCTION_1       1  '1 positional argument'
             7954  POP_JUMP_IF_TRUE   8058  'to 8058'

 L.2283      7958  LOAD_GLOBAL              open
             7960  LOAD_FAST                'avsfile'
             7962  LOAD_STR                 'w+'
             7964  LOAD_STR                 'utf-8'
             7966  LOAD_CONST               ('encoding',)
             7968  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             7970  SETUP_WITH         8052  'to 8052'
             7972  STORE_FAST               'f'

 L.2284      7974  LOAD_FAST                'f'
             7976  LOAD_ATTR                write
             7978  LOAD_STR                 'LoadPlugin("'
             7980  LOAD_GLOBAL              TimeStretch_dll
             7982  BINARY_ADD       
             7984  LOAD_STR                 '")'
             7986  BINARY_ADD       
             7988  LOAD_STR                 '\n'
             7990  BINARY_ADD       
             7992  CALL_FUNCTION_1       1  '1 positional argument'
             7994  POP_TOP          

 L.2285      7996  LOAD_FAST                'f'
             7998  LOAD_ATTR                write
             8000  LOAD_STR                 'LoadPlugin("'
             8002  LOAD_GLOBAL              lsmashsource_dll
             8004  BINARY_ADD       
             8006  LOAD_STR                 '")'
             8008  BINARY_ADD       
             8010  LOAD_STR                 '\n'
             8012  BINARY_ADD       
             8014  CALL_FUNCTION_1       1  '1 positional argument'
             8016  POP_TOP          

 L.2286      8018  LOAD_FAST                'f'
             8020  LOAD_ATTR                write

 L.2288      8022  LOAD_STR                 'TimeStretchPlugin(LWLibavAudioSource("'
             8024  LOAD_FAST                'originalAudio'
             8026  BINARY_ADD       
             8028  LOAD_STR                 '"), pitch='
             8030  BINARY_ADD       
             8032  LOAD_GLOBAL              str
             8034  LOAD_FAST                'pitch'
             8036  CALL_FUNCTION_1       1  '1 positional argument'
             8038  BINARY_ADD       
             8040  LOAD_STR                 ')'
             8042  BINARY_ADD       
             8044  CALL_FUNCTION_1       1  '1 positional argument'
             8046  POP_TOP          
             8048  POP_BLOCK        
             8050  LOAD_CONST               None
           8052_0  COME_FROM_WITH     7970  '7970'
             8052  WITH_CLEANUP_START
             8054  WITH_CLEANUP_FINISH
             8056  END_FINALLY      
           8058_0  COME_FROM          7954  '7954'
           8058_1  COME_FROM          7928  '7928'
           8058_2  COME_FROM          7914  '7914'

 L.2289      8058  LOAD_GLOBAL              os
             8060  LOAD_ATTR                path
             8062  LOAD_ATTR                isfile
             8064  LOAD_FAST                'originalAudio'
             8066  CALL_FUNCTION_1       1  '1 positional argument'
             8068  JUMP_IF_FALSE_OR_POP  8082  'to 8082'
             8072  LOAD_GLOBAL              os
             8074  LOAD_ATTR                path
             8076  LOAD_ATTR                isfile
             8078  LOAD_FAST                'outputAudio'
             8080  CALL_FUNCTION_1       1  '1 positional argument'
           8082_0  COME_FROM          8068  '8068'
             8082  POP_JUMP_IF_TRUE   7762  'to 7762'

 L.2290      8086  LOAD_GLOBAL              print
             8088  LOAD_STR                 '\nFixing pitch of '
             8090  LOAD_FAST                'langAbbrev'
             8092  BINARY_ADD       
             8094  LOAD_STR                 '...'
             8096  BINARY_ADD       
             8098  CALL_FUNCTION_1       1  '1 positional argument'
             8100  POP_TOP          

 L.2291      8102  LOAD_GLOBAL              print
             8104  LOAD_GLOBAL              str
             8106  LOAD_FAST                'sourcefps'
             8108  CALL_FUNCTION_1       1  '1 positional argument'
             8110  LOAD_STR                 ' -> '
             8112  BINARY_ADD       
             8114  LOAD_GLOBAL              str
             8116  LOAD_FAST                'targetfps'
             8118  CALL_FUNCTION_1       1  '1 positional argument'
             8120  BINARY_ADD       
             8122  CALL_FUNCTION_1       1  '1 positional argument'
             8124  POP_TOP          

 L.2292      8126  LOAD_GLOBAL              subprocess
             8128  LOAD_ATTR                Popen

 L.2293      8130  LOAD_GLOBAL              ffprobepath
             8132  LOAD_STR                 '-v'
             8134  LOAD_STR                 'quiet'
             8136  LOAD_STR                 '-print_format'
             8138  LOAD_STR                 'json'

 L.2294      8140  LOAD_STR                 '-show_format'
             8142  LOAD_STR                 '-show_streams'
             8144  LOAD_FAST                'originalAudio'
             8146  BUILD_LIST_8          8 

 L.2295      8148  LOAD_GLOBAL              subprocess
             8150  LOAD_ATTR                PIPE
             8152  LOAD_CONST               ('stdout',)
             8154  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             8156  STORE_FAST               'mediainfo'

 L.2296      8158  LOAD_GLOBAL              json
             8160  LOAD_ATTR                load
             8162  LOAD_FAST                'mediainfo'
             8164  LOAD_ATTR                stdout
             8166  CALL_FUNCTION_1       1  '1 positional argument'
             8168  STORE_FAST               'mediainfo'

 L.2297      8170  LOAD_GLOBAL              int

 L.2298      8172  LOAD_GLOBAL              float
             8174  LOAD_FAST                'mediainfo'
             8176  LOAD_STR                 'streams'
             8178  BINARY_SUBSCR    
             8180  LOAD_CONST               0
             8182  BINARY_SUBSCR    
             8184  LOAD_STR                 'bit_rate'
             8186  BINARY_SUBSCR    
             8188  CALL_FUNCTION_1       1  '1 positional argument'
             8190  LOAD_CONST               1000
             8192  BINARY_TRUE_DIVIDE
             8194  CALL_FUNCTION_1       1  '1 positional argument'
             8196  STORE_FAST               'audio_bitrate'

 L.2299      8198  LOAD_GLOBAL              ffmpy
             8200  LOAD_ATTR                FFmpeg
             8202  LOAD_GLOBAL              ffmpegpath
             8204  LOAD_FAST                'avsfile'
             8206  LOAD_CONST               None
             8208  BUILD_MAP_1           1 

 L.2300      8210  LOAD_FAST                'outputAudio'

 L.2301      8212  LOAD_STR                 '-c:a eac3 -b:a '
             8214  LOAD_GLOBAL              str
             8216  LOAD_FAST                'audio_bitrate'
             8218  CALL_FUNCTION_1       1  '1 positional argument'
             8220  BINARY_ADD       
             8222  LOAD_STR                 'k -room_type -1 -copyright 1 -original 1 -mixing_level -1 -dialnorm -31'
             8224  BINARY_ADD       
             8226  BUILD_MAP_1           1 

 L.2302      8228  LOAD_STR                 '-y -hide_banner -loglevel warning'
             8230  LOAD_CONST               ('executable', 'inputs', 'outputs', 'global_options')
             8232  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             8234  STORE_FAST               'ff'

 L.2303      8236  LOAD_FAST                'ff'
             8238  LOAD_ATTR                run
             8240  CALL_FUNCTION_0       0  '0 positional arguments'
             8242  POP_TOP          

 L.2304      8244  LOAD_GLOBAL              print
             8246  LOAD_STR                 'Done!'
             8248  CALL_FUNCTION_1       1  '1 positional argument'
             8250  POP_TOP          
             8252  JUMP_BACK          7762  'to 7762'
             8256  POP_BLOCK        
           8258_0  COME_FROM_LOOP     7750  '7750'
           8258_1  COME_FROM          7656  '7656'
           8258_2  COME_FROM          7648  '7648'
           8258_3  COME_FROM          7638  '7638'

 L.2306      8258  LOAD_GLOBAL              args
             8260  LOAD_ATTR                nomux
             8262  POP_JUMP_IF_TRUE   8786  'to 8786'

 L.2307      8266  LOAD_GLOBAL              args
             8268  LOAD_ATTR                novideo
             8270  POP_JUMP_IF_TRUE   8786  'to 8786'

 L.2308      8274  LOAD_FAST                'novideo'
             8276  LOAD_CONST               False
             8278  COMPARE_OP               ==
             8280  POP_JUMP_IF_FALSE  8786  'to 8786'

 L.2309      8284  LOAD_GLOBAL              args
             8286  LOAD_ATTR                noaudio
             8288  POP_JUMP_IF_TRUE   8786  'to 8786'

 L.2310      8292  LOAD_FAST                'noaudio'
             8294  LOAD_CONST               False
             8296  COMPARE_OP               ==
             8298  POP_JUMP_IF_FALSE  8742  'to 8742'

 L.2311      8302  LOAD_FAST                'CorrectDecryptVideo'
             8304  LOAD_CONST               True
             8306  COMPARE_OP               ==
             8308  POP_JUMP_IF_FALSE  8786  'to 8786'

 L.2312      8312  LOAD_FAST                'CorrectDecryptAudio'
             8314  LOAD_CONST               True
             8316  COMPARE_OP               ==
             8318  POP_JUMP_IF_FALSE  8714  'to 8714'

 L.2313      8322  LOAD_GLOBAL              print
             8324  LOAD_STR                 '\n\nMuxing...'
             8326  CALL_FUNCTION_1       1  '1 positional argument'
             8328  POP_TOP          

 L.2314      8330  LOAD_GLOBAL              str
             8332  LOAD_FAST                'heightp'
             8334  CALL_FUNCTION_1       1  '1 positional argument'
             8336  STORE_FAST               'CurrentHeigh'

 L.2315      8338  LOAD_DEREF               'seriesName'
             8340  STORE_FAST               'CurrentName'

 L.2316      8342  LOAD_FAST                'amazonType'
             8344  LOAD_STR                 'show'
             8346  COMPARE_OP               ==
             8348  POP_JUMP_IF_FALSE  8372  'to 8372'

 L.2317      8352  LOAD_GLOBAL              Muxer
             8354  LOAD_FAST                'CurrentName'
             8356  LOAD_FAST                'seriesName3'

 L.2318      8358  LOAD_FAST                'CurrentHeigh'

 L.2319      8360  LOAD_FAST                'amazonType'

 L.2320      8362  LOAD_GLOBAL              mkvmergeexe
             8364  LOAD_CONST               ('CurrentName', 'SeasonFolder', 'CurrentHeigh', 'Type', 'mkvmergeexe')
             8366  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             8368  STORE_FAST               'MKV_Muxer'
             8370  JUMP_FORWARD       8390  'to 8390'
             8372  ELSE                     '8390'

 L.2322      8372  LOAD_GLOBAL              Muxer
             8374  LOAD_FAST                'CurrentName'
             8376  LOAD_CONST               None

 L.2323      8378  LOAD_FAST                'CurrentHeigh'

 L.2324      8380  LOAD_FAST                'amazonType'

 L.2325      8382  LOAD_GLOBAL              mkvmergeexe
             8384  LOAD_CONST               ('CurrentName', 'SeasonFolder', 'CurrentHeigh', 'Type', 'mkvmergeexe')
             8386  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             8388  STORE_FAST               'MKV_Muxer'
           8390_0  COME_FROM          8370  '8370'

 L.2326      8390  LOAD_GLOBAL              args
             8392  LOAD_ATTR                langtag
             8394  POP_JUMP_IF_FALSE  8422  'to 8422'

 L.2327      8398  LOAD_FAST                'MKV_Muxer'
             8400  LOAD_ATTR                AmazonAndPrimeVideoMuxer
             8402  LOAD_GLOBAL              str
             8404  LOAD_GLOBAL              args
             8406  LOAD_ATTR                langtag
             8408  LOAD_CONST               0
             8410  BINARY_SUBSCR    
             8412  CALL_FUNCTION_1       1  '1 positional argument'
             8414  LOAD_CONST               ('lang',)
             8416  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             8418  POP_TOP          
             8420  JUMP_FORWARD       8434  'to 8434'
             8422  ELSE                     '8434'

 L.2329      8422  LOAD_FAST                'MKV_Muxer'
             8424  LOAD_ATTR                AmazonAndPrimeVideoMuxer
             8426  LOAD_STR                 'English'
             8428  LOAD_CONST               ('lang',)
             8430  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             8432  POP_TOP          
           8434_0  COME_FROM          8420  '8420'

 L.2330      8434  LOAD_GLOBAL              args
             8436  LOAD_ATTR                keep
             8438  POP_JUMP_IF_FALSE  8446  'to 8446'

 L.2331      8442  JUMP_FORWARD       8706  'to 8706'
             8446  ELSE                     '8706'

 L.2333      8446  LOAD_GLOBAL              os
             8448  LOAD_ATTR                system

 L.2334      8450  LOAD_STR                 'if exist "'
             8452  LOAD_FAST                'CurrentName'
             8454  BINARY_ADD       
             8456  LOAD_STR                 '*.mp4" (del /q /f "'
             8458  BINARY_ADD       
             8460  LOAD_FAST                'CurrentName'
             8462  BINARY_ADD       
             8464  LOAD_STR                 '*.mp4")'
             8466  BINARY_ADD       
             8468  CALL_FUNCTION_1       1  '1 positional argument'
             8470  POP_TOP          

 L.2335      8472  LOAD_GLOBAL              os
             8474  LOAD_ATTR                system

 L.2336      8476  LOAD_STR                 'if exist "'
             8478  LOAD_FAST                'CurrentName'
             8480  BINARY_ADD       
             8482  LOAD_STR                 '*.m4a" (del /q /f "'
             8484  BINARY_ADD       
             8486  LOAD_FAST                'CurrentName'
             8488  BINARY_ADD       
             8490  LOAD_STR                 '*.m4a")'
             8492  BINARY_ADD       
             8494  CALL_FUNCTION_1       1  '1 positional argument'
             8496  POP_TOP          

 L.2337      8498  LOAD_GLOBAL              os
             8500  LOAD_ATTR                system

 L.2338      8502  LOAD_STR                 'if exist "'
             8504  LOAD_FAST                'CurrentName'
             8506  BINARY_ADD       
             8508  LOAD_STR                 '*.h264" (del /q /f "'
             8510  BINARY_ADD       
             8512  LOAD_FAST                'CurrentName'
             8514  BINARY_ADD       
             8516  LOAD_STR                 '*.h264")'
             8518  BINARY_ADD       
             8520  CALL_FUNCTION_1       1  '1 positional argument'
             8522  POP_TOP          

 L.2339      8524  LOAD_GLOBAL              os
             8526  LOAD_ATTR                system

 L.2340      8528  LOAD_STR                 'if exist "'
             8530  LOAD_FAST                'CurrentName'
             8532  BINARY_ADD       
             8534  LOAD_STR                 '*.h265" (del /q /f "'
             8536  BINARY_ADD       
             8538  LOAD_FAST                'CurrentName'
             8540  BINARY_ADD       
             8542  LOAD_STR                 '*.h265")'
             8544  BINARY_ADD       
             8546  CALL_FUNCTION_1       1  '1 positional argument'
             8548  POP_TOP          

 L.2341      8550  LOAD_GLOBAL              os
             8552  LOAD_ATTR                system

 L.2342      8554  LOAD_STR                 'if exist "'
             8556  LOAD_FAST                'CurrentName'
             8558  BINARY_ADD       
             8560  LOAD_STR                 '*.eac3" (del /q /f "'
             8562  BINARY_ADD       
             8564  LOAD_FAST                'CurrentName'
             8566  BINARY_ADD       
             8568  LOAD_STR                 '*.eac3")'
             8570  BINARY_ADD       
             8572  CALL_FUNCTION_1       1  '1 positional argument'
             8574  POP_TOP          

 L.2343      8576  LOAD_GLOBAL              os
             8578  LOAD_ATTR                system

 L.2344      8580  LOAD_STR                 'if exist "'
             8582  LOAD_FAST                'CurrentName'
             8584  BINARY_ADD       
             8586  LOAD_STR                 '*.srt" (del /q /f "'
             8588  BINARY_ADD       
             8590  LOAD_FAST                'CurrentName'
             8592  BINARY_ADD       
             8594  LOAD_STR                 '*.srt")'
             8596  BINARY_ADD       
             8598  CALL_FUNCTION_1       1  '1 positional argument'
             8600  POP_TOP          

 L.2345      8602  LOAD_GLOBAL              os
             8604  LOAD_ATTR                system

 L.2346      8606  LOAD_STR                 'if exist "'
             8608  LOAD_FAST                'CurrentName'
             8610  BINARY_ADD       
             8612  LOAD_STR                 '*.txt" (del /q /f "'
             8614  BINARY_ADD       
             8616  LOAD_FAST                'CurrentName'
             8618  BINARY_ADD       
             8620  LOAD_STR                 '*.txt")'
             8622  BINARY_ADD       
             8624  CALL_FUNCTION_1       1  '1 positional argument'
             8626  POP_TOP          

 L.2347      8628  LOAD_GLOBAL              os
             8630  LOAD_ATTR                system

 L.2348      8632  LOAD_STR                 'if exist "'
             8634  LOAD_FAST                'CurrentName'
             8636  BINARY_ADD       
             8638  LOAD_STR                 '*.avs" (del /q /f "'
             8640  BINARY_ADD       
             8642  LOAD_FAST                'CurrentName'
             8644  BINARY_ADD       
             8646  LOAD_STR                 '*.avs")'
             8648  BINARY_ADD       
             8650  CALL_FUNCTION_1       1  '1 positional argument'
             8652  POP_TOP          

 L.2349      8654  LOAD_GLOBAL              os
             8656  LOAD_ATTR                system

 L.2350      8658  LOAD_STR                 'if exist "'
             8660  LOAD_FAST                'CurrentName'
             8662  BINARY_ADD       
             8664  LOAD_STR                 '*.lwi" (del /q /f "'
             8666  BINARY_ADD       
             8668  LOAD_FAST                'CurrentName'
             8670  BINARY_ADD       
             8672  LOAD_STR                 '*.lwi")'
             8674  BINARY_ADD       
             8676  CALL_FUNCTION_1       1  '1 positional argument'
             8678  POP_TOP          

 L.2351      8680  LOAD_GLOBAL              os
             8682  LOAD_ATTR                system

 L.2352      8684  LOAD_STR                 'if exist "'
             8686  LOAD_FAST                'CurrentName'
             8688  BINARY_ADD       
             8690  LOAD_STR                 '*.mpd" (del /q /f "'
             8692  BINARY_ADD       
             8694  LOAD_FAST                'CurrentName'
             8696  BINARY_ADD       
             8698  LOAD_STR                 '*.mpd")'
             8700  BINARY_ADD       
             8702  CALL_FUNCTION_1       1  '1 positional argument'
             8704  POP_TOP          
           8706_0  COME_FROM          8442  '8442'

 L.2353      8706  LOAD_GLOBAL              print
             8708  LOAD_STR                 'Done!'
             8710  CALL_FUNCTION_1       1  '1 positional argument'
             8712  POP_TOP          
           8714_0  COME_FROM          8318  '8318'

 L.2354      8714  LOAD_GLOBAL              os
             8716  LOAD_ATTR                system
             8718  LOAD_STR                 'if exist "'
             8720  LOAD_FAST                'CurrentName'
             8722  BINARY_ADD       
             8724  LOAD_STR                 '*.mpd" (del /q /f "'
             8726  BINARY_ADD       
             8728  LOAD_FAST                'CurrentName'
             8730  BINARY_ADD       
             8732  LOAD_STR                 '*.mpd")'
             8734  BINARY_ADD       
             8736  CALL_FUNCTION_1       1  '1 positional argument'
             8738  POP_TOP          
             8740  JUMP_FORWARD       8786  'to 8786'
             8742  ELSE                     '8786'

 L.2356      8742  LOAD_GLOBAL              args
             8744  LOAD_ATTR                keep
             8746  POP_JUMP_IF_FALSE  8752  'to 8752'

 L.2357      8750  JUMP_FORWARD       8762  'to 8762'
             8752  ELSE                     '8762'

 L.2359      8752  LOAD_GLOBAL              os
             8754  LOAD_ATTR                remove
             8756  LOAD_GLOBAL              mpd_file
             8758  CALL_FUNCTION_1       1  '1 positional argument'
             8760  POP_TOP          
           8762_0  COME_FROM          8750  '8750'

 L.2360      8762  LOAD_GLOBAL              print
             8764  LOAD_STR                 "File '"
             8768  LOAD_GLOBAL              str
             8770  LOAD_FAST                'VideoOutputName'
             8772  CALL_FUNCTION_1       1  '1 positional argument'
             8774  BINARY_ADD       
             8776  LOAD_STR                 "' already exists."
             8780  BINARY_ADD       
             8782  CALL_FUNCTION_1       1  '1 positional argument'
             8784  POP_TOP          
           8786_0  COME_FROM          8740  '8740'
           8786_1  COME_FROM          8308  '8308'
           8786_2  COME_FROM          8288  '8288'
           8786_3  COME_FROM          8280  '8280'
           8786_4  COME_FROM          8270  '8270'
           8786_5  COME_FROM          8262  '8262'

 L.2362      8786  LOAD_FAST                'amazonType'
             8788  LOAD_STR                 'show'
             8790  COMPARE_OP               ==
             8792  POP_JUMP_IF_FALSE  8914  'to 8914'

 L.2363      8796  SETUP_EXCEPT       8810  'to 8810'

 L.2364      8798  LOAD_GLOBAL              str
             8800  LOAD_FAST                'heightp'
             8802  CALL_FUNCTION_1       1  '1 positional argument'
             8804  STORE_FAST               'CurrentHeigh'
             8806  POP_BLOCK        
             8808  JUMP_FORWARD       8836  'to 8836'
           8810_0  COME_FROM_EXCEPT   8796  '8796'

 L.2365      8810  DUP_TOP          
             8812  LOAD_GLOBAL              Exception
             8814  COMPARE_OP               exception-match
             8816  POP_JUMP_IF_FALSE  8834  'to 8834'
             8820  POP_TOP          
             8822  POP_TOP          
             8824  POP_TOP          

 L.2366      8826  LOAD_STR                 'Unknown'
             8828  STORE_FAST               'CurrentHeigh'
             8830  POP_EXCEPT       
             8832  JUMP_FORWARD       8836  'to 8836'
             8834  END_FINALLY      
           8836_0  COME_FROM          8832  '8832'
           8836_1  COME_FROM          8808  '8808'

 L.2368      8836  LOAD_DEREF               'seriesName'
             8838  STORE_FAST               'CurrentName'

 L.2370      8840  LOAD_GLOBAL              str
             8842  LOAD_FAST                'CurrentName'
             8844  CALL_FUNCTION_1       1  '1 positional argument'
             8846  LOAD_GLOBAL              str
             8848  LOAD_FAST                'seriesName3'
             8850  CALL_FUNCTION_1       1  '1 positional argument'
             8852  LOAD_GLOBAL              str
             8854  LOAD_FAST                'CurrentHeigh'
             8856  CALL_FUNCTION_1       1  '1 positional argument'
             8858  BUILD_TUPLE_3         3 
             8860  RETURN_VALUE     

 L.2373      8862  DUP_TOP          
             8864  LOAD_GLOBAL              Exception
             8866  COMPARE_OP               exception-match
             8868  POP_JUMP_IF_FALSE  8886  'to 8886'
             8872  POP_TOP          
             8874  POP_TOP          
             8876  POP_TOP          

 L.2374      8878  LOAD_STR                 'Unknown'
             8880  STORE_FAST               'CurrentHeigh'
             8882  POP_EXCEPT       
             8884  JUMP_FORWARD       8888  'to 8888'
             8886  END_FINALLY      
           8888_0  COME_FROM          8884  '8884'

 L.2376      8888  LOAD_DEREF               'seriesName'
             8890  STORE_FAST               'CurrentName'

 L.2378      8892  LOAD_GLOBAL              str
             8894  LOAD_FAST                'CurrentName'
             8896  CALL_FUNCTION_1       1  '1 positional argument'
             8898  LOAD_GLOBAL              str
             8900  LOAD_FAST                'CurrentName'
             8902  CALL_FUNCTION_1       1  '1 positional argument'
             8904  LOAD_GLOBAL              str
             8906  LOAD_FAST                'CurrentHeigh'
             8908  CALL_FUNCTION_1       1  '1 positional argument'
             8910  BUILD_TUPLE_3         3 
             8912  RETURN_END_IF    
           8914_0  COME_FROM          8792  '8792'

Parse error at or near `DUP_TOP' instruction at offset 3148


    def SearchASINPrimeVideo(url):
        custom_headers_season = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
         'accept-encoding':'gzip, deflate, br', 
         'cache-control':'no-cache', 
         'accept-language':'en-US,en;q=0.9,en;q=0.8', 
         'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 
         'upgrade-insecure-requests':'1'}
        html_data = requests.get(url, headers=custom_headers_season)
        html_data = html_data.text
        rg = re.compile('(<script id="av-wconf-dv-web-player-cfg" type="application/json">)(.*)(</script><script type="text/javascript">P\\.when\\("av-widget-config"\\)\\.execute\\(function\\(widgetConfig\\){widgetConfig\\.declare\\("dv-web-player-cfg"\\);}\\);</script>)')
        rg2 = re.compile("(spty=')(.*)(')(.*)(pti=')")
        m = rg.search(html_data)
        m2 = rg2.search(html_data)
        conf_webplayer_json = json.loads(m.group(2))
        if m2:
            if m2.group(2) == 'Movie':
                amazonTypeTemp = 'movie'
            else:
                amazonTypeTemp = 'show'
            try:
                amazonTypeTemp = amazonTypeTemp
            except Exception:
                print('Error in URL.')
                sys.exit(0)

            if amazonTypeTemp == 'movie':
                asinMovie = conf_webplayer_json['pageTitleID']
                return (
                 asinMovie, amazonTypeTemp)
            else:
                A = find_str(html_data, '<!-- MarkAF -->')
                B = find_str(html_data, '<!-- MarkCF -->')
                listasinall = html_data[A:B]
                listasinall = re.split('div', listasinall)
                asinList = []
                listasin = []
                for x in listasinall:
                    if 'ep-list-selector' in str(x):
                        listasin.append(x)

                for y in listasin:
                    A = find_str(str(y), '" value="')
                    B = find_str(str(y), '"/><label class="')
                    asinList.append(y[A + 9:B])

                return (
                 asinList, amazonTypeTemp)


    def SearchASINAmazon(url):
        global clientId
        custom_headers_season = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',  'accept-encoding':'gzip, deflate, br', 
         'cache-control':'max-age=0', 
         'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 
         'upgrade-insecure-requests':'1', 
         'cookie':cookies}
        html_data = requests.get(url, headers=custom_headers_season)
        html_data = html_data.text
        A = find_str(html_data, 'dv-episode-list')
        B = find_str(html_data, '<div class="a-section">')
        listasinall = html_data[A:B]
        listasinall = re.split('div', listasinall)
        asinList = []
        for y in listasinall:
            if 'data-asin' in y:
                A = find_str(str(y), 'data-asin')
                asinList.append(y[A:A + 23].replace('data-asin', '').replace('=', '').replace(' ', '').replace("'", '').replace('"', '').replace('\n', '').replace('\t', '').replace('\\n', '').replace('\\t', '').replace('/\n', '').replace('/\t', ''))

        if not asinList == []:
            try:
                datatemp = getLicenseTemp(asinList[0], clientId)
                if datatemp['catalogMetadata']['catalog']['type'] == 'MOVIE':
                    amazonTypeTemp = 'movie'
                else:
                    if datatemp['catalogMetadata']['catalog']['type'] == 'EPISODE':
                        amazonTypeTemp = 'show'
                    else:
                        print('Unrecognized type!')
                        sys.exit(0)
            except Exception:
                print('Error in cookies or in URL.')
                sys.exit(0)

            return (
             asinList, amazonTypeTemp)
        else:
            A = find_str(html_data, 'pageTitleID')
            B = find_str(html_data, '","autoplay":')
            asinMovie = html_data[A + 14:B]
            try:
                datatemp = getLicenseTemp(asinMovie, clientId)
                if datatemp['catalogMetadata']['catalog']['type'] == 'MOVIE':
                    amazonTypeTemp = 'movie'
                else:
                    if datatemp['catalogMetadata']['catalog']['type'] == 'EPISODE':
                        amazonTypeTemp = 'show'
                    else:
                        print('Unrecognized type!')
                        sys.exit(0)
            except Exception:
                print('Error in cookies or in URL.')
                sys.exit(0)

            return (
             asinMovie, amazonTypeTemp)


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
if args.region == 'ps':
    video_base_url, site_base_url, marketplace_id, cookies_file, clientId, email, password = PrimevideoConfig.configPrimeVieo()
    region = 'ps'
elif args.region == 'ps-int':
    video_base_url, site_base_url, marketplace_id, cookies_file, clientId, email, password = PrimevideoConfig.configPrimeVieoInternational()
    region = 'ps-int'
elif args.region == 'us':
    video_base_url, site_base_url, marketplace_id, cookies_file, clientId, email, password = PrimevideoConfig.configAmazonUS()
    region = 'us'
elif args.region == 'jp':
    video_base_url, site_base_url, marketplace_id, cookies_file, clientId, email, password = PrimevideoConfig.configAmazonJP()
    region = 'jp'
else:
    if args.region == 'uk':
        video_base_url, site_base_url, marketplace_id, cookies_file, clientId, email, password = PrimevideoConfig.configAmazonUK()
        region = 'uk'
    elif args.region == 'de':
        video_base_url, site_base_url, marketplace_id, cookies_file, clientId, email, password = PrimevideoConfig.configAmazonDE()
        region = 'de'
    else:
        cookies = get_cookies()
        custom_headers_GetPlaybackResources = {'Accept':'application/json',  'Accept-Encoding':'gzip, deflate, br', 
         'Accept-Language':'es,ca;q=0.9,en;q=0.8', 
         'Cache-Control':'no-cache', 
         'Connection':'keep-alive', 
         'Content-Type':'application/x-www-form-urlencoded', 
         'Pragma':'no-cache', 
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 
         'Cookie':cookies}
        UserAgent = str('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36').encode('utf-8')
        deviceID = hmac.new(UserAgent, uuid.uuid4().bytes, hashlib.sha224).hexdigest()
        if args.url_season:
            url_season = str(args.url_season)
        if not args.url_season:
            if not args.asin:
                url_season = input('Enter the Amazon PrimeVideo url (with https): ')
        if not args.url_season:
            if args.asin:
                asin = args.asin
                try:
                    datatemp = getLicenseTemp(asin, clientId)
                    if datatemp['catalogMetadata']['catalog']['type'] == 'MOVIE':
                        amazonTypeTemp = 'movie'
                    else:
                        if datatemp['catalogMetadata']['catalog']['type'] == 'EPISODE':
                            amazonTypeTemp = 'show'
                        else:
                            print('Unrecognized type!')
                            sys.exit(0)
                except Exception:
                    print('Error in cookies or in URL.')
                    sys.exit(0)

                try:
                    CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(asin)
                    if args.country_code != None:
                        os.system('taskkill /im openvpn.exe /f')
                except Exception:
                    print('No more episodes to download.')
                    if args.country_code != None:
                        os.system('taskkill /im openvpn.exe /f')
                    sys.exit(0)

                if args.custom_command:
                    print('\n')
                    if args.hevc:
                        CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
                    else:
                        if args.atmos:
                            CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC-atmos].mkv'
                        else:
                            CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv'
                        if amazonTypeTemp == 'show':
                            CustomCommand = '"' + folderdownloader + '\\' + str(SeasonFolder) + '\\' + CurrentName_out + '"'
                        else:
                            CustomCommand = '"' + folderdownloader + '\\' + CurrentName_out + '"'
                        str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
                        CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
                        stdoutdata, stderrdata = CustomCommand_process.communicate()
                        CustomCommand_process.wait()
                        sys.exit(0)
                else:
                    sys.exit(0)
    if args.all_season:
        if region == 'ps' or region == 'ps-int':
            print('\nSearching asins...')
            ASINS, amazonTypeTemp = SearchASINPrimeVideo(url=url_season)
            print('Done!')
            if amazonTypeTemp == 'movie':
                print('Movie dont have seasons!')
                try:
                    CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(ASINS)
                    if args.country_code != None:
                        os.system('taskkill /im openvpn.exe /f')
                except Exception:
                    print('No more episodes to download.')
                    if args.country_code != None:
                        os.system('taskkill /im openvpn.exe /f')
                    sys.exit(0)

                if args.custom_command:
                    print('\n')
                    if args.hevc:
                        CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
                    else:
                        if args.atmos:
                            CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC-atmos].mkv'
                        else:
                            CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv'
                        CustomCommand = '"' + folderdownloader + '\\' + CurrentName_out + '"'
                        str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
                        CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
                        stdoutdata, stderrdata = CustomCommand_process.communicate()
                        CustomCommand_process.wait()
                        sys.exit(0)
                else:
                    sys.exit(0)
            else:
                if not args.episodeStart:
                    episodeStart = int(input('Episode Start: '))
                else:
                    episodeStart = int(args.episodeStart)
                asinList2 = []
                count = 0
                for x in ASINS:
                    if count >= episodeStart - 1:
                        asinList2.append(x)
                    count = count + 1

                CurrentHeigh2 = ''
                CurrentName2 = ''
                SeasonFolder2 = ''
                for y in asinList2:
                    try:
                        CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(y)
                    except Exception:
                        print('No more episodes to download.')
                        if args.country_code != None:
                            os.system('taskkill /im openvpn.exe /f')
                        sys.exit(0)

                    if CurrentHeigh != 'Unknown':
                        CurrentHeigh2 = CurrentHeigh
                        CurrentName2 = CurrentName
                        SeasonFolder2 = SeasonFolder

                if args.country_code != None:
                    os.system('taskkill /im openvpn.exe /f')
                if args.custom_command:
                    print('\n')
                    if args.hevc:
                        CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
                    else:
                        if args.atmos:
                            CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC-atmos].mkv'
                        else:
                            CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv'
                        CustomCommand = '"' + folderdownloader + '\\' + str(SeasonFolder) + '"'
                        str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
                        CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
                        stdoutdata, stderrdata = CustomCommand_process.communicate()
                        CustomCommand_process.wait()
                        sys.exit(0)
                else:
                    sys.exit(0)
            if not args.all_season and (region == 'ps' or region == 'ps-int'):
                print('\nSearching asins...')
                ASINS, amazonTypeTemp = SearchASINPrimeVideo(url=url_season)
                print('Done!')
                if amazonTypeTemp == 'movie':
                    try:
                        CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(ASINS)
                        if args.country_code != None:
                            os.system('taskkill /im openvpn.exe /f')
                    except Exception:
                        print('No more episodes to download.')
                        if args.country_code != None:
                            os.system('taskkill /im openvpn.exe /f')
                        sys.exit(0)

                    if args.custom_command:
                        print('\n')
                        if args.hevc:
                            CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
                        else:
                            if args.atmos:
                                CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC-atmos].mkv'
                            else:
                                CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv'
                    else:
                        CustomCommand = '"' + folderdownloader + '\\' + CurrentName_out + '"'
                        str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
                        CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
                        stdoutdata, stderrdata = CustomCommand_process.communicate()
                        CustomCommand_process.wait()
                        sys.exit(0)
                else:
                    sys.exit(0)
    else:
        if not args.episodeStart:
            episodeStart = int(input('Episode Start: '))
        else:
            episodeStart = int(args.episodeStart)
        asinList2 = []
        count = 0
        for x in ASINS:
            if count == episodeStart - 1:
                asinList2.append(x)
            count = count + 1

        asin2 = str(asinList2[0])
        try:
            CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(asin2)
            if args.country_code != None:
                os.system('taskkill /im openvpn.exe /f')
        except Exception:
            print('No more episodes to download.')
            if args.country_code != None:
                os.system('taskkill /im openvpn.exe /f')
            sys.exit(0)

        if args.custom_command:
            print('\n')
            if args.hevc:
                CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
            else:
                if args.atmos:
                    CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC-atmos].mkv'
                else:
                    CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv'
                CustomCommand = '"' + folderdownloader + '\\' + str(SeasonFolder) + '\\' + CurrentName_out + '"'
                str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
                CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
                stdoutdata, stderrdata = CustomCommand_process.communicate()
                CustomCommand_process.wait()
                sys.exit(0)
        else:
            sys.exit(0)
if args.all_season:
    if region != 'ps' or region != 'ps-int':
        print('\nSearching asins...')
        ASINS, amazonTypeTemp = SearchASINAmazon(url=url_season)
        print('\nDone!')
        if amazonTypeTemp == 'movie':
            print('\nMovie dont have seasons!')
            try:
                CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(ASINS)
                if args.country_code != None:
                    os.system('taskkill /im openvpn.exe /f')
            except Exception:
                print('No more episodes to download.')
                if args.country_code != None:
                    os.system('taskkill /im openvpn.exe /f')
                sys.exit(0)

            if args.custom_command:
                print('\n')
                if args.hevc:
                    CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
                else:
                    if args.atmos:
                        CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC-atmos].mkv'
                    else:
                        CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv'
                    CustomCommand = '"' + folderdownloader + '\\' + CurrentName_out + '"'
                    str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
                    CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
                    stdoutdata, stderrdata = CustomCommand_process.communicate()
                    CustomCommand_process.wait()
                    sys.exit(0)
            else:
                sys.exit(0)
        else:
            if not args.episodeStart:
                episodeStart = int(input('Episode Start: '))
            else:
                episodeStart = int(args.episodeStart)
            asinList2 = []
            count = 0
            for x in ASINS:
                if count >= episodeStart - 1:
                    asinList2.append(x)
                count = count + 1

            for y in asinList2:
                try:
                    CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(y)
                except Exception:
                    print('No more episodes to download.')
                    if args.country_code != None:
                        os.system('taskkill /im openvpn.exe /f')
                    sys.exit(0)

            if args.country_code != None:
                os.system('taskkill /im openvpn.exe /f')
            if args.custom_command:
                print('\n')
                if args.hevc:
                    CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
                else:
                    if args.atmos:
                        CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC-atmos].mkv'
                    else:
                        CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv'
                    CustomCommand = '"' + folderdownloader + '\\' + str(SeasonFolder) + '"'
                    str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
                    CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
                    stdoutdata, stderrdata = CustomCommand_process.communicate()
                    CustomCommand_process.wait()
                    sys.exit(0)
            else:
                sys.exit(0)
        if not args.all_season and (region != 'ps' or region != 'ps-int'):
            print('\nSearching asins...')
            ASINS, amazonTypeTemp = SearchASINAmazon(url=url_season)
            print('\nDone!')
            if amazonTypeTemp == 'movie':
                try:
                    CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(ASINS)
                    if args.country_code != None:
                        os.system('taskkill /im openvpn.exe /f')
                except Exception:
                    print('No more episodes to download.')
                    if args.country_code != None:
                        os.system('taskkill /im openvpn.exe /f')
                    sys.exit(0)

                if args.custom_command:
                    print('\n')
                    if args.hevc:
                        CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
                    else:
                        if args.atmos:
                            CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC-atmos].mkv'
                        else:
                            CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv'
                else:
                    CustomCommand = '"' + folderdownloader + '\\' + CurrentName_out + '"'
                    str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
                    CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
                    stdoutdata, stderrdata = CustomCommand_process.communicate()
                    CustomCommand_process.wait()
                    sys.exit(0)
            else:
                sys.exit(0)
else:
    if not args.episodeStart:
        episodeStart = int(input('Episode Start: '))
    else:
        episodeStart = int(args.episodeStart)
    asinList2 = []
    count = 0
    for x in ASINS:
        if count == episodeStart - 1:
            asinList2.append(x)
        count = count + 1

    asin2 = str(asinList2[0])
    try:
        CurrentName, SeasonFolder, CurrentHeigh = DownloadAll(asin2)
        if args.country_code != None:
            os.system('taskkill /im openvpn.exe /f')
    except Exception:
        print('No more episodes to download.')
        if args.country_code != None:
            os.system('taskkill /im openvpn.exe /f')
        sys.exit(0)

    if args.custom_command:
        print('\n')
        if args.hevc:
            CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC].mkv'
        else:
            if args.atmos:
                CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p] [HEVC-atmos].mkv'
            else:
                CurrentName_out = str(CurrentName) + ' [' + str(CurrentHeigh) + 'p].mkv'
            CustomCommand = '"' + folderdownloader + '\\' + str(SeasonFolder) + '\\' + CurrentName_out + '"'
            str(args.custom_command[0]) + ' --file-folder ' + CustomCommand
            CustomCommand_process = subprocess.Popen(str(args.custom_command[0]) + ' --file-folder ' + CustomCommand)
            stdoutdata, stderrdata = CustomCommand_process.communicate()
            CustomCommand_process.wait()
            sys.exit(0)
    else:
        sys.exit(0)
# global folderdownloader ## Warning: Unused global