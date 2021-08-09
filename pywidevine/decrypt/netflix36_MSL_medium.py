# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\pywidevine\decrypt\netflix36_MSL_medium.py
if __name__ == 'pywidevine.decrypt.netflix36_MSL_medium':
    import binascii, configparser, argparse, base64, glob, gzip, json, os, pprint, pycountry, random, string, re, requests, sys, socket, time, xml.etree.ElementTree as ET, zlib
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
    from pywidevine.clientsconfig.netflix import NetflixConfig

    def generate_esn(prefix):
        """
        generate_esn()
        @param prefix: Prefix of ESN to append generated device ID onto
        @return: ESN to use with MSL API
        """
        return prefix + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))


    username, password, esn_keys, esn_manifest, MANIFEST_ENDPOINT, LICENSE_ENDPOINT = NetflixConfig.configNetflix()
    account_info = {'email':username,  'password':password}
    languageCodes = {'zh-Hans':'zhoS',  'zh-Hant':'zhoT', 
     'pt-BR':'brPor', 
     'es-ES':'euSpa', 
     'en-GB':'enGB', 
     'nl-BE':'nlBE'}
    from netflix36 import args
    from netflix36 import msl_data_path
    from netflix36 import cert_nf

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


    class MSL:
        global current_sessionId
        handshake_performed = False
        last_drm_context = ''
        last_playback_context = ''
        current_message_id = 0
        session = requests.session()
        rndm = random.SystemRandom()
        tokens = []
        current_sessionId = str(time.time()).replace('.', '')[0:-2]
        endpoints = {'manifest':MANIFEST_ENDPOINT, 
         'license':LICENSE_ENDPOINT}

        def __init__(self, test):
            """
            #The Constructor checks for already existing crypto Keys.
            #If they exist it will load the existing keys
            """
            global manifest_file
            global msl_data_file
            global msl_data_path
            global rsa_key_bin
            rsa_key_bin = 'rsa_manifest_medium.bin'
            msl_data_file = 'msl_data_manifest_medium.json'
            manifest_file = 'manifest_medium.json'
            if os.path.isfile(msl_data_path + rsa_key_bin):
                os.remove(msl_data_path + rsa_key_bin)
            if os.path.isfile(msl_data_path + msl_data_file):
                os.remove(msl_data_path + msl_data_file)
            if os.path.isfile(msl_data_path + manifest_file):
                os.remove(msl_data_path + manifest_file)
            else:
                try:
                    os.mkdir(msl_data_path)
                except OSError:
                    pass

                if self.file_exists(msl_data_path, msl_data_file):
                    self._MSL__load_msl_data()
                    self.handshake_performed = True
                else:
                    if self.file_exists(msl_data_path, rsa_key_bin):
                        self._MSL__load_rsa_keys()
                        self._MSL__perform_key_handshake()
                    else:
                        print('Generating Device Keys...')
                        self.rsa_key = RSA.generate(2048)
                        self._MSL__save_rsa_keys()
                        self._MSL__perform_key_handshake()

        def load_manifest(self, viewable_id):
            global HDR
            global HEVC
            global HIGH
            global HIGH_1080p
            global MAIN
            global UHD
            global VP9
            global account_info
            global args
            global b64
            global esn_keys
            if args.hevc:
                print('Getting HEVC Manifest...')
            else:
                if args.hdr:
                    print('Getting HDR-10 Manifest...')
                else:
                    if args.video_vp9:
                        print('Getting VP9 Manifest...')
                    else:
                        print('Getting Main Profile Manifest...')
                    manifest_request_data = {'method':'manifest',  'lookupType':'STANDARD', 
                     'viewableIds':[
                      viewable_id], 
                     'profiles':[
                      'dfxp-ls-sdh',
                      'webvtt-lssdh-ios8'], 
                     'drmSystem':'widevine', 
                     'appId':current_sessionId, 
                     'sessionParams':{'pinCapableClient':False, 
                      'uiplaycontext':'null'}, 
                     'sessionId':current_sessionId, 
                     'trackId':0, 
                     'flavor':'STANDARD', 
                     'secureUrls':True, 
                     'supportPreviewContent':True, 
                     'forceClearStreams':False, 
                     'languages':[
                      'en-US'], 
                     'clientVersion':'4.0004.899.011', 
                     'uiVersion':'akira'}
                    if args.noallregions:
                        manifest_request_data['showAllSubDubTracks'] = False
                    else:
                        manifest_request_data['showAllSubDubTracks'] = True
                    if args.aformat_2ch:
                        if str(args.aformat_2ch[0]) == 'aac':
                            manifest_request_data['profiles'].append('heaac-2-dash')
                        else:
                            if str(args.aformat_2ch[0]) == 'eac3':
                                manifest_request_data['profiles'].append('ddplus-2.0-dash')
                            else:
                                if str(args.aformat_2ch[0]) == 'ogg':
                                    manifest_request_data['profiles'].append('playready-oggvorbis-2-dash')
                                else:
                                    manifest_request_data['profiles'].append('ddplus-2.0-dash')
                    else:
                        manifest_request_data['profiles'].append('ddplus-2.0-dash')
                    ForceDDPlusHQ = False
                    if args.aformat_51ch:
                        if args.only_2ch_audio or str(args.aformat_51ch[0]) == 'aac':
                            manifest_request_data['profiles'].append('heaac-5.1-dash')
                            manifest_request_data['profiles'].append('heaac-5.1hq-dash')
                        else:
                            if str(args.aformat_51ch[0]) == 'eac3':
                                manifest_request_data['profiles'].append('ddplus-5.1-dash')
                                manifest_request_data['profiles'].append('ddplus-5.1hq-dash')
                                ForceDDPlusHQ = True
                            else:
                                if str(args.aformat_51ch[0]) == 'ac3':
                                    manifest_request_data['profiles'].append('dd-5.1-dash')
                                else:
                                    if str(args.aformat_51ch[0]) == 'atmos':
                                        manifest_request_data['profiles'].append('dd-5.1-dash')
                                        manifest_request_data['profiles'].append('ddplus-atmos-dash')
                                    else:
                                        manifest_request_data['profiles'].append('dd-5.1-dash')
                                        manifest_request_data['profiles'].append('ddplus-5.1-dash')
                                        manifest_request_data['profiles'].append('ddplus-5.1hq-dash')
                                        ForceDDPlusHQ = True
                    else:
                        if not args.only_2ch_audio:
                            manifest_request_data['profiles'].append('dd-5.1-dash')
                            manifest_request_data['profiles'].append('ddplus-5.1-dash')
                            manifest_request_data['profiles'].append('ddplus-5.1hq-dash')
                            ForceDDPlusHQ = True
                        HDR = False
                        UHD = False
                        HEVC = False
                        VP9 = False
                        HIGH = False
                        MAIN = False
                        HIGH_1080p = False
                        manifest_request_data['profiles'].append('hevc-main10-L50-dash-cenc')
                        request_data = self._MSL__generate_msl_request_data(manifest_request_data)
                        resp = self.session.post(self.endpoints['manifest'], request_data)
                        try:
                            b64 = base64key_decode(json.loads(resp.text)['errordata'])
                            b64 = json.loads(b64)['errormsg']
                            print(b64)
                            sys.exit(0)
                        except ValueError:
                            b64 = False

                        try:
                            resp.json()
                            return False
                        except ValueError:
                            resp = self._MSL__parse_chunked_msl_response(resp.text)
                            data = self._MSL__decrypt_payload_chunks(resp['payloads'])
                            if 'Unable to create context (due to ContentViewableFailure)' in str(data) or 'Unable to create context (due to ContentException)' in str(data) or "'success': False" in str(data):
                                UHD = False
                            else:
                                UHD = True

                        manifest_request_data['profiles'].pop()
                        manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc')
                        request_data = self._MSL__generate_msl_request_data(manifest_request_data)
                        resp = self.session.post(self.endpoints['manifest'], request_data)
                        try:
                            b64 = base64key_decode(json.loads(resp.text)['errordata'])
                            b64 = json.loads(b64)['errormsg']
                            print(b64)
                            sys.exit(0)
                        except ValueError:
                            b64 = False

                        try:
                            resp.json()
                            return False
                        except ValueError:
                            resp = self._MSL__parse_chunked_msl_response(resp.text)
                            data = self._MSL__decrypt_payload_chunks(resp['payloads'])
                            if 'Unable to create context (due to ContentViewableFailure)' in str(data) or 'Unable to create context (due to ContentException)' in str(data) or "'success': False" in str(data):
                                HEVC = False
                            else:
                                HEVC = True

                        manifest_request_data['profiles'].pop()
                        manifest_request_data['profiles'].append('vp9-profile0-L30-dash-cenc')
                        request_data = self._MSL__generate_msl_request_data(manifest_request_data)
                        resp = self.session.post(self.endpoints['manifest'], request_data)
                        try:
                            b64 = base64key_decode(json.loads(resp.text)['errordata'])
                            b64 = json.loads(b64)['errormsg']
                            sys.exit(0)
                        except ValueError:
                            b64 = False

                        try:
                            resp.json()
                            return False
                        except ValueError:
                            resp = self._MSL__parse_chunked_msl_response(resp.text)
                            data = self._MSL__decrypt_payload_chunks(resp['payloads'])
                            if 'Unable to create context (due to ContentViewableFailure)' in str(data) or 'Unable to create context (due to ContentException)' in str(data) or "'success': False" in str(data):
                                VP9 = False
                            else:
                                VP9 = True

                        manifest_request_data['profiles'].pop()
                        manifest_request_data['profiles'].append('hevc-hdr-main10-L30-dash-cenc-prk')
                        request_data = self._MSL__generate_msl_request_data(manifest_request_data)
                        resp = self.session.post(self.endpoints['manifest'], request_data)
                        try:
                            b64 = base64key_decode(json.loads(resp.text)['errordata'])
                            b64 = json.loads(b64)['errormsg']
                            sys.exit(0)
                        except ValueError:
                            b64 = False

                        try:
                            resp.json()
                            return False
                        except ValueError:
                            resp = self._MSL__parse_chunked_msl_response(resp.text)
                            data = self._MSL__decrypt_payload_chunks(resp['payloads'])
                            if 'Unable to create context (due to ContentViewableFailure)' in str(data) or 'Unable to create context (due to ContentException)' in str(data) or "'success': False" in str(data):
                                HDR = False
                            else:
                                HDR = True

                        manifest_request_data['profiles'].pop()
                        import pywidevine.pymsl as pymsl
                        account = account_info
                        client = pymsl.MslClient({'scheme':'EMAIL_PASSWORD', 
                         'authdata':{'email':account['email'], 
                          'password':account['password']}},
                          esn=esn_keys,
                          drm_system='widevine',
                          profiles=[
                         'playready-h264hpl30-dash',
                         'playready-h264hpl31-dash',
                         'playready-h264hpl40-dash',
                         'playready-h264mpl30-dash',
                         'playready-h264mpl31-dash',
                         'playready-h264mpl40-dash',
                         'heaac-2-dash',
                         'simplesdh'])
                        manifest_keys = client.load_manifest(viewable_id)
                        if 'playready-h264hpl' in str(manifest_keys):
                            HIGH = True
                            MAIN = False
                            if 'playready-h264hpl40-dash' in str(manifest_keys):
                                HIGH_1080p = True
                            else:
                                HIGH_1080p = False
                        else:
                            if 'playready-h264mpl' in str(manifest_keys):
                                MAIN = True
                                HIGH = False
                            else:
                                HIGH = False
                                MAIN = False
                            if args.hdr:
                                if args.customquality:
                                    if int(args.customquality[0]) == 1080:
                                        manifest_request_data['profiles'].append('hevc-hdr-main10-L30-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-hdr-main10-L30-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-hdr-main10-L31-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-hdr-main10-L31-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-hdr-main10-L40-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-hdr-main10-L41-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-hdr-main10-L40-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-hdr-main10-L41-dash-cenc-prk')
                                    elif int(args.customquality[0]) < 1080:
                                        if int(args.customquality[0]) >= 720:
                                            manifest_request_data['profiles'].append('hevc-hdr-main10-L30-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-hdr-main10-L30-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-hdr-main10-L31-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-hdr-main10-L31-dash-cenc-prk')
                                        if int(args.customquality[0]) < 720:
                                            manifest_request_data['profiles'].append('hevc-hdr-main10-L30-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-hdr-main10-L30-dash-cenc-prk')
                                else:
                                    manifest_request_data['profiles'].append('hevc-hdr-main10-L30-dash-cenc')
                                    manifest_request_data['profiles'].append('hevc-hdr-main10-L30-dash-cenc-prk')
                                    manifest_request_data['profiles'].append('hevc-hdr-main10-L31-dash-cenc')
                                    manifest_request_data['profiles'].append('hevc-hdr-main10-L31-dash-cenc-prk')
                                    manifest_request_data['profiles'].append('hevc-hdr-main10-L40-dash-cenc')
                                    manifest_request_data['profiles'].append('hevc-hdr-main10-L41-dash-cenc')
                                    manifest_request_data['profiles'].append('hevc-hdr-main10-L40-dash-cenc-prk')
                                    manifest_request_data['profiles'].append('hevc-hdr-main10-L41-dash-cenc-prk')
                            elif args.hevc:
                                if args.customquality:
                                    if int(args.customquality[0]) == 1080:
                                        manifest_request_data['profiles'].append('hevc-main-L20-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main-L21-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main-L30-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main-L20-L21-dash-cenc-tl')
                                        manifest_request_data['profiles'].append('hevc-main-L21-L30-dash-cenc-tl')
                                        manifest_request_data['profiles'].append('hevc-main10-L20-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main10-L21-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main10-L20-L21-dash-cenc-tl')
                                        manifest_request_data['profiles'].append('hevc-main10-L21-L30-dash-cenc-tl')
                                        manifest_request_data['profiles'].append('hevc-main-L20-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main-L21-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main-L30-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main-L20-L21-dash-cenc-prk-tl')
                                        manifest_request_data['profiles'].append('hevc-main-L21-L30-dash-cenc-prk-tl')
                                        manifest_request_data['profiles'].append('hevc-main10-L20-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main10-L21-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main10-L20-L21-dash-cenc-prk-tl')
                                        manifest_request_data['profiles'].append('hevc-main10-L21-L30-dash-cenc-prk-tl')
                                        manifest_request_data['profiles'].append('hevc-main-L31-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main-L30-L31-dash-cenc-tl')
                                        manifest_request_data['profiles'].append('hevc-main10-L31-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main10-L30-L31-dash-cenc-tl')
                                        manifest_request_data['profiles'].append('hevc-main-L31-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main-L30-L31-dash-cenc-prk-tl')
                                        manifest_request_data['profiles'].append('hevc-main10-L31-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main10-L30-L31-dash-cenc-prk-tl')
                                        manifest_request_data['profiles'].append('hevc-main-L40-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main-L41-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main-L31-L40-dash-cenc-tl')
                                        manifest_request_data['profiles'].append('hevc-main-L40-L41-dash-cenc-tl')
                                        manifest_request_data['profiles'].append('hevc-main10-L40-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main10-L41-dash-cenc')
                                        manifest_request_data['profiles'].append('hevc-main10-L31-L40-dash-cenc-tl')
                                        manifest_request_data['profiles'].append('hevc-main10-L40-L41-dash-cenc-tl')
                                        manifest_request_data['profiles'].append('hevc-main-L40-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main-L41-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main-L31-L40-dash-cenc-prk-tl')
                                        manifest_request_data['profiles'].append('hevc-main-L40-L41-dash-cenc-prk-tl')
                                        manifest_request_data['profiles'].append('hevc-main10-L40-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main10-L41-dash-cenc-prk')
                                        manifest_request_data['profiles'].append('hevc-main10-L31-L40-dash-cenc-prk-tl')
                                        manifest_request_data['profiles'].append('hevc-main10-L40-L41-dash-cenc-prk-tl')
                                    else:
                                        if int(args.customquality[0]) < 1080:
                                            if int(args.customquality[0]) >= 720:
                                                manifest_request_data['profiles'].append('hevc-main-L20-dash-cenc')
                                                manifest_request_data['profiles'].append('hevc-main-L21-dash-cenc')
                                                manifest_request_data['profiles'].append('hevc-main-L30-dash-cenc')
                                                manifest_request_data['profiles'].append('hevc-main-L20-L21-dash-cenc-tl')
                                                manifest_request_data['profiles'].append('hevc-main-L21-L30-dash-cenc-tl')
                                                manifest_request_data['profiles'].append('hevc-main10-L20-dash-cenc')
                                                manifest_request_data['profiles'].append('hevc-main10-L21-dash-cenc')
                                                manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc')
                                                manifest_request_data['profiles'].append('hevc-main10-L20-L21-dash-cenc-tl')
                                                manifest_request_data['profiles'].append('hevc-main10-L21-L30-dash-cenc-tl')
                                                manifest_request_data['profiles'].append('hevc-main-L20-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('hevc-main-L21-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('hevc-main-L30-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('hevc-main-L20-L21-dash-cenc-prk-tl')
                                                manifest_request_data['profiles'].append('hevc-main-L21-L30-dash-cenc-prk-tl')
                                                manifest_request_data['profiles'].append('hevc-main10-L20-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('hevc-main10-L21-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('hevc-main10-L20-L21-dash-cenc-prk-tl')
                                                manifest_request_data['profiles'].append('hevc-main10-L21-L30-dash-cenc-prk-tl')
                                                manifest_request_data['profiles'].append('hevc-main-L31-dash-cenc')
                                                manifest_request_data['profiles'].append('hevc-main-L30-L31-dash-cenc-tl')
                                                manifest_request_data['profiles'].append('hevc-main10-L31-dash-cenc')
                                                manifest_request_data['profiles'].append('hevc-main10-L30-L31-dash-cenc-tl')
                                                manifest_request_data['profiles'].append('hevc-main-L31-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('hevc-main-L30-L31-dash-cenc-prk-tl')
                                                manifest_request_data['profiles'].append('hevc-main10-L31-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('hevc-main10-L30-L31-dash-cenc-prk-tl')
                                        if int(args.customquality[0]) < 720:
                                            manifest_request_data['profiles'].append('hevc-main-L20-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main-L21-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main-L30-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main-L20-L21-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L21-L30-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L20-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main10-L21-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main10-L20-L21-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L21-L30-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L20-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main-L21-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main-L30-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main-L20-L21-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L21-L30-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L20-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main10-L21-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main10-L20-L21-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L21-L30-dash-cenc-prk-tl')
                                        else:
                                            manifest_request_data['profiles'].append('hevc-main-L20-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main-L21-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main-L30-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main-L20-L21-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L21-L30-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L20-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main10-L21-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main10-L20-L21-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L21-L30-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L20-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main-L21-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main-L30-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main-L20-L21-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L21-L30-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L20-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main10-L21-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main10-L20-L21-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L21-L30-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L31-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main-L30-L31-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L31-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main10-L30-L31-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L31-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main-L30-L31-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L31-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main10-L30-L31-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L40-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main-L41-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main-L31-L40-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L40-L41-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L40-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main10-L41-dash-cenc')
                                            manifest_request_data['profiles'].append('hevc-main10-L31-L40-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L40-L41-dash-cenc-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L40-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main-L41-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main-L31-L40-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main-L40-L41-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L40-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main10-L41-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('hevc-main10-L31-L40-dash-cenc-prk-tl')
                                            manifest_request_data['profiles'].append('hevc-main10-L40-L41-dash-cenc-prk-tl')
                                else:
                                    if args.video_vp9:
                                        if args.customquality:
                                            if int(args.customquality[0]) == 1080:
                                                manifest_request_data['profiles'].append('vp9-profile0-L21-dash-cenc')
                                                manifest_request_data['profiles'].append('vp9-profile0-L21-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('vp9-profile0-L30-dash-cenc')
                                                manifest_request_data['profiles'].append('vp9-profile0-L30-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('vp9-profile2-L30-dash-cenc')
                                                manifest_request_data['profiles'].append('vp9-profile2-L30-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('vp9-profile0-L31-dash-cenc')
                                                manifest_request_data['profiles'].append('vp9-profile0-L31-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('vp9-profile2-L31-dash-cenc')
                                                manifest_request_data['profiles'].append('vp9-profile2-L31-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('vp9-profile0-L40-dash-cenc')
                                                manifest_request_data['profiles'].append('vp9-profile0-L40-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('vp9-profile2-L40-dash-cenc')
                                                manifest_request_data['profiles'].append('vp9-profile2-L41-dash-cenc')
                                                manifest_request_data['profiles'].append('vp9-profile2-L40-dash-cenc-prk')
                                                manifest_request_data['profiles'].append('vp9-profile2-L41-dash-cenc-prk')
                                            elif int(args.customquality[0]) < 1080:
                                                if int(args.customquality[0]) >= 720:
                                                    manifest_request_data['profiles'].append('vp9-profile0-L21-dash-cenc')
                                                    manifest_request_data['profiles'].append('vp9-profile0-L21-dash-cenc-prk')
                                                    manifest_request_data['profiles'].append('vp9-profile0-L30-dash-cenc')
                                                    manifest_request_data['profiles'].append('vp9-profile0-L30-dash-cenc-prk')
                                                    manifest_request_data['profiles'].append('vp9-profile2-L30-dash-cenc')
                                                    manifest_request_data['profiles'].append('vp9-profile2-L30-dash-cenc-prk')
                                                    manifest_request_data['profiles'].append('vp9-profile0-L31-dash-cenc')
                                                    manifest_request_data['profiles'].append('vp9-profile0-L31-dash-cenc-prk')
                                                    manifest_request_data['profiles'].append('vp9-profile2-L31-dash-cenc')
                                                    manifest_request_data['profiles'].append('vp9-profile2-L31-dash-cenc-prk')
                                                if int(args.customquality[0]) < 720:
                                                    manifest_request_data['profiles'].append('vp9-profile0-L21-dash-cenc')
                                                    manifest_request_data['profiles'].append('vp9-profile0-L21-dash-cenc-prk')
                                                    manifest_request_data['profiles'].append('vp9-profile0-L30-dash-cenc')
                                                    manifest_request_data['profiles'].append('vp9-profile0-L30-dash-cenc-prk')
                                                    manifest_request_data['profiles'].append('vp9-profile2-L30-dash-cenc')
                                                    manifest_request_data['profiles'].append('vp9-profile2-L30-dash-cenc-prk')
                                        else:
                                            manifest_request_data['profiles'].append('vp9-profile0-L21-dash-cenc')
                                            manifest_request_data['profiles'].append('vp9-profile0-L21-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('vp9-profile0-L30-dash-cenc')
                                            manifest_request_data['profiles'].append('vp9-profile0-L30-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('vp9-profile2-L30-dash-cenc')
                                            manifest_request_data['profiles'].append('vp9-profile2-L30-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('vp9-profile0-L31-dash-cenc')
                                            manifest_request_data['profiles'].append('vp9-profile0-L31-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('vp9-profile2-L31-dash-cenc')
                                            manifest_request_data['profiles'].append('vp9-profile2-L31-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('vp9-profile0-L40-dash-cenc')
                                            manifest_request_data['profiles'].append('vp9-profile0-L40-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('vp9-profile2-L40-dash-cenc')
                                            manifest_request_data['profiles'].append('vp9-profile2-L41-dash-cenc')
                                            manifest_request_data['profiles'].append('vp9-profile2-L40-dash-cenc-prk')
                                            manifest_request_data['profiles'].append('vp9-profile2-L41-dash-cenc-prk')
                                    else:
                                        if args.customquality:
                                            if int(args.customquality[0]) == 1080:
                                                manifest_request_data['profiles'].append('playready-h264bpl30-dash')
                                                manifest_request_data['profiles'].append('playready-h264mpl22-dash')
                                                manifest_request_data['profiles'].append('playready-h264mpl30-dash')
                                                manifest_request_data['profiles'].append('playready-h264mpl31-dash')
                                                manifest_request_data['profiles'].append('playready-h264mpl40-dash')
                                                manifest_request_data['profiles'].append('playready-h264mpl41-dash')
                                                manifest_request_data['profiles'].append('playready-h264bpl30-dash-prk')
                                                manifest_request_data['profiles'].append('playready-h264mpl22-dash-prk')
                                                manifest_request_data['profiles'].append('playready-h264mpl30-dash-prk')
                                                manifest_request_data['profiles'].append('playready-h264mpl31-dash-prk')
                                                manifest_request_data['profiles'].append('playready-h264mpl40-dash-prk')
                                                manifest_request_data['profiles'].append('playready-h264mpl41-dash-prk')
                                            elif int(args.customquality[0]) < 1080:
                                                if int(args.customquality[0]) >= 720:
                                                    manifest_request_data['profiles'].append('playready-h264bpl30-dash')
                                                    manifest_request_data['profiles'].append('playready-h264mpl22-dash')
                                                    manifest_request_data['profiles'].append('playready-h264mpl30-dash')
                                                    manifest_request_data['profiles'].append('playready-h264mpl31-dash')
                                                    manifest_request_data['profiles'].append('playready-h264bpl30-dash-prk')
                                                    manifest_request_data['profiles'].append('playready-h264mpl22-dash-prk')
                                                    manifest_request_data['profiles'].append('playready-h264mpl30-dash-prk')
                                                    manifest_request_data['profiles'].append('playready-h264mpl31-dash-prk')
                                                if int(args.customquality[0]) < 720:
                                                    manifest_request_data['profiles'].append('playready-h264bpl30-dash')
                                                    manifest_request_data['profiles'].append('playready-h264mpl22-dash')
                                                    manifest_request_data['profiles'].append('playready-h264mpl30-dash')
                                                    manifest_request_data['profiles'].append('playready-h264bpl30-dash-prk')
                                                    manifest_request_data['profiles'].append('playready-h264mpl22-dash-prk')
                                                    manifest_request_data['profiles'].append('playready-h264mpl30-dash-prk')
                                        else:
                                            manifest_request_data['profiles'].append('playready-h264bpl30-dash')
                                            manifest_request_data['profiles'].append('playready-h264mpl22-dash')
                                            manifest_request_data['profiles'].append('playready-h264mpl30-dash')
                                            manifest_request_data['profiles'].append('playready-h264mpl31-dash')
                                            manifest_request_data['profiles'].append('playready-h264mpl40-dash')
                                            manifest_request_data['profiles'].append('playready-h264mpl41-dash')
                                            manifest_request_data['profiles'].append('playready-h264bpl30-dash-prk')
                                            manifest_request_data['profiles'].append('playready-h264mpl22-dash-prk')
                                            manifest_request_data['profiles'].append('playready-h264mpl30-dash-prk')
                                            manifest_request_data['profiles'].append('playready-h264mpl31-dash-prk')
                                            manifest_request_data['profiles'].append('playready-h264mpl40-dash-prk')
                                            manifest_request_data['profiles'].append('playready-h264mpl41-dash-prk')
                            else:
                                if args.forceaudiohq:
                                    if ForceDDPlusHQ == True:
                                        ddplus51hq = False
                                        count = 1
                                        while ddplus51hq == False:
                                            request_data = self._MSL__generate_msl_request_data(manifest_request_data)
                                            resp = self.session.post(self.endpoints['manifest'], request_data)
                                            resp = self._MSL__parse_chunked_msl_response(str(resp.text))
                                            data = self._MSL__decrypt_payload_chunks(resp['payloads'])
                                            print(count)
                                            if 'ddplus-5.1-dash' in str(data):
                                                if 'ddplus-5.1hq-' in str(data):
                                                    ddplus51hq = True
                                                    print('encontrado')
                                                    print(data)
                                                    return self._MSL__tranform_to_dash(data)
                                                count = count + 1
                                                time.sleep(0.5)
                                                ddplus51hq = False
                                            else:
                                                ddplus51hq = True
                                                return self._MSL__tranform_to_dash(data)

                                    else:
                                        request_data = self._MSL__generate_msl_request_data(manifest_request_data)
                                        resp = self.session.post(self.endpoints['manifest'], request_data)
                                        resp = self._MSL__parse_chunked_msl_response(str(resp.text))
                                        data = self._MSL__decrypt_payload_chunks(resp['payloads'])
                                        return self._MSL__tranform_to_dash(data)
                                else:
                                    request_data = self._MSL__generate_msl_request_data(manifest_request_data)
                                    resp = self.session.post(self.endpoints['manifest'], request_data)
                                    resp = self._MSL__parse_chunked_msl_response(str(resp.text))
                                    data = self._MSL__decrypt_payload_chunks(resp['payloads'])
                                    return self._MSL__tranform_to_dash(data)

        def get_license(self, challenge):
            challenge_encoded = base64.b64encode(challenge).decode('utf-8')
            license_request_data = {'method':'license', 
             'licenseType':'STANDARD', 
             'clientVersion':'4.0004.899.011', 
             'uiVersion':'akira', 
             'languages':[
              'en-US'], 
             'playbackContextId':playbackContextId, 
             'drmContextIds':[
              last_drm_context], 
             'challenges':[
              {'dataBase64':challenge_encoded, 
               'sessionId':current_sessionId}], 
             'clientTime':int(time.time()), 
             'xid':int((int(time.time()) + 0.1612) * 1000)}
            request_data = self._MSL__generate_msl_request_data(license_request_data)
            resp = self.session.post(self.endpoints['license'], request_data)
            try:
                resp.json()
                exit(1)
            except ValueError:
                resp = self._MSL__parse_chunked_msl_response(resp.text)
                data = self._MSL__decrypt_payload_chunks(resp['payloads'])
                if data['success'] is True:
                    return data['result']['licenses'][0]['data']
                exit(1)

        def __decrypt_payload_chunks(self, payloadchunks):
            decrypted_payload = ''
            for chunk in payloadchunks:
                payloadchunk = json.JSONDecoder().decode(chunk)
                payload = payloadchunk.get('payload')
                decoded_payload = base64.standard_b64decode(str(payload))
                decoded_payload = decoded_payload.decode('utf-8')
                encryption_envelope = json.JSONDecoder().decode(decoded_payload)
                cipher = AES.new(self.encryption_key, AES.MODE_CBC, base64.standard_b64decode(encryption_envelope['iv']))
                ciphertext = encryption_envelope.get('ciphertext')
                plaintext = cipher.decrypt(base64.standard_b64decode(ciphertext))
                plaintext = plaintext.decode('utf-8')
                paddingtemp = Padding.unpad(plaintext.encode('utf-8'), 16)
                plaintext = json.JSONDecoder().decode(paddingtemp.decode('utf-8'))
                data = plaintext.get('data')
                if plaintext.get('compressionalgo') == 'GZIP':
                    decoded_data = base64.standard_b64decode(data)
                    data = zlib.decompress(decoded_data, 16 + zlib.MAX_WBITS)
                else:
                    data = base64.standard_b64decode(data)
                decrypted_payload += data.decode('utf-8')

            decrypted_payload = json.JSONDecoder().decode(decrypted_payload)[1]['payload']['data']
            decrypted_payload = base64.standard_b64decode(decrypted_payload)
            return json.JSONDecoder().decode(decrypted_payload.decode('utf-8'))

        def __tranform_to_dash(self, manifest):
            global audioList
            global cert_data_b64_new
            global forced
            global init_data_b64_new
            global last_drm_context
            global playbackContextId
            global subtitleChi
            global subtitleDFXP
            global subtitleList
            global videoList
            self.save_file_(msl_data_path, manifest_file, json.dumps(manifest))
            try:
                manifest = manifest['result']['viewables'][0]
            except Exception:
                pass

            try:
                playbackContextId = manifest['playbackContextId']
                last_drm_context = manifest['drmContextId']
                self.last_playback_context = manifest['playbackContextId']
                self.last_drm_context = manifest['drmContextId']
            except Exception:
                if args.hdr:
                    print('This item dont have HDR.')
                else:
                    if args.hevc:
                        print('This item dont have HEVC.')
                    else:
                        print('Unexpected shit happened while transofmring to DASH.')
                sys.exit(0)

            pssh = ''
            if 'psshb64' in manifest:
                if len(manifest['psshb64']) >= 1:
                    pssh = manifest['psshb64']
                    cert = manifest['cert']
                    init_data_b64_new = pssh
                    cert_data_b64_new = cert
            for pssh_new in init_data_b64_new:
                pssh_dec = base64.standard_b64decode(pssh_new).hex()
                kid_new = pssh_dec[72:]

            videoList = []
            for video_track in manifest['videoTracks']:
                for downloadable in video_track['downloadables']:
                    videoDict = {'Type':'video', 
                     'Height':downloadable['height'], 
                     'Width':downloadable['width'], 
                     'Size':downloadable['size'], 
                     'Url':next(iter(downloadable['urls'].values())), 
                     'Bitrate':str(downloadable['bitrate']), 
                     'Profile':downloadable['contentProfile'], 
                     'formatCode':str(abs(hash(str(next(iter(downloadable['urls'].values())))) % 100000000))}
                    if args.customquality:
                        if str(args.customquality[0]) in str(videoDict['Height']):
                            videoList.append(videoDict)
                    else:
                        videoList.append(videoDict)

                videoList = sorted(videoList, key=(lambda k: int(k['Bitrate'])))

            audioList = []
            audioQuality = dict()
            for audio_track in manifest['audioTracks']:
                new_audio_lang = None
                lang_audio = audio_track['language'].replace(' [Original]', '')
                for downloadable in audio_track['downloadables']:
                    if lang_audio not in audioQuality or audioQuality[lang_audio] < downloadable['bitrate']:
                        audioQuality[lang_audio] = downloadable['bitrate']
                        new_audio_lang = downloadable
                        audioList = [x for x in audioList if x['Language'].replace(' [Original]', '') is not lang_audio]

                downloadable = new_audio_lang
                if not (args.audiolang and audio_track['language'].replace(' [Original]', '') not in args.audiolang):
                    if not downloadable:
                        continue
                    else:
                        audioDict = {'Type':'audio', 
                         'Language':audio_track['language'].replace(' [Original]', ''), 
                         'Size':downloadable['size'], 
                         'Url':next(iter(downloadable['urls'].values())), 
                         'Bitrate':str(downloadable['bitrate']), 
                         'Profile':downloadable['contentProfile'], 
                         'formatCode':str(abs(hash(str(next(iter(downloadable['urls'].values())))) % 100000000))}
                        audioList.append(audioDict)
                    audioList = sorted(audioList, key=(lambda k: int(k['Bitrate'])), reverse=True)

            subtitleList = []
            subtitleDFXP = []
            subtitleChi = []
            forced = False
            for text_track in manifest['textTracks']:
                if 'downloadables' in text_track:
                    if text_track['downloadables'] is None:
                        continue
                    for downloadable in text_track['downloadables']:
                        code = text_track['bcp47']
                        lang_code = code[:code.index('-')] if '-' in code else code
                        try:
                            lang = pycountry.languages.get(alpha_2=lang_code)
                        except KeyError:
                            lang = pycountry.languages.get(alpha_3=lang_code)

                        forced = False
                        try:
                            code = languageCodes[code]
                            lang = code
                        except KeyError:
                            lang = lang.alpha_3

                        if text_track['language'] == 'Off':
                            forced = True
                        subtitleDict = {'Type':text_track['trackType'], 
                         'Language':text_track['language'], 
                         'langAbbrev':lang, 
                         'Url':next(iter(downloadable['urls'].values())), 
                         'Profile':downloadable['contentProfile'], 
                         'formatCode':str(abs(hash(str(next(iter(downloadable['urls'].values())))) % 100000000))}
                        if forced and args.forcedlang and lang not in args.forcedlang or args.sublang:
                            if text_track['language'] not in args.sublang:
                                if not forced:
                                    continue
                        if subtitleDict['Language'] != 'Off':
                            if subtitleDict['Profile'] == 'dfxp-ls-sdh':
                                subtitleDFXP.append(subtitleDict)
                            if subtitleDict['Language'] == 'Off' and subtitleDict['Profile'] == 'dfxp-ls-sdh':
                                subtitleDFXP.append(subtitleDict)

                    for downloadable in text_track['downloadables']:
                        code = text_track['bcp47']
                        lang_code = code[:code.index('-')] if '-' in code else code
                        try:
                            lang = pycountry.languages.get(alpha_2=lang_code)
                        except KeyError:
                            lang = pycountry.languages.get(alpha_3=lang_code)

                        forced = False
                        try:
                            code = languageCodes[code]
                            lang = code
                        except KeyError:
                            lang = lang.alpha_3

                        if text_track['language'] == 'Off':
                            forced = True
                        subtitleDict = {'Type':text_track['trackType'],  'Language':text_track['language'], 
                         'langAbbrev':lang, 
                         'Url':next(iter(downloadable['urls'].values())), 
                         'Profile':downloadable['contentProfile'], 
                         'formatCode':str(abs(hash(str(next(iter(downloadable['urls'].values())))) % 100000000))}
                        if forced and args.forcedlang and lang not in args.forcedlang or args.sublang:
                            if text_track['language'] not in args.sublang:
                                if not forced:
                                    continue
                        if subtitleDict['Language'] != 'Off':
                            if subtitleDict['Profile'] == 'webvtt-lssdh-ios8':
                                if not re.search(str(subtitleDict['Language']), str(subtitleDFXP)):
                                    subtitleChi.append(subtitleDict)
                            if subtitleDict['Language'] == 'Off' and subtitleDict['Profile'] == 'webvtt-lssdh-ios8':
                                re.search(str(subtitleDict['langAbbrev']), str(subtitleDFXP)) or subtitleChi.append(subtitleDict)

            return (
             videoList, audioList, subtitleList, subtitleDFXP, subtitleChi, forced, UHD, HDR, HEVC, VP9, HIGH, HIGH_1080p, MAIN)

        def __get_base_url(self, urls):
            for key in urls:
                return urls[key]

        def __parse_chunked_msl_response(self, message):
            header = message.split('}}')[0] + '}}'
            payloads = re.split(',"signature":"[0-9A-Za-z=/+]+"}', message.split('}}')[1])
            payloads = [x + '}' for x in payloads][:-1]
            return {'header':header, 
             'payloads':payloads}

        def __generate_msl_request_data(self, data):
            header_encryption_envelope = self._MSL__encrypt(self._MSL__generate_msl_header())
            header = {'headerdata':base64.standard_b64encode(header_encryption_envelope.encode('utf-8')).decode('utf-8'), 
             'signature':self._MSL__sign(header_encryption_envelope).decode('utf-8'), 
             'mastertoken':self.mastertoken}
            serialized_data = json.dumps(data)
            serialized_data = serialized_data.replace('"', '\\"')
            serialized_data = '[{},{"headers":{},"path":"/cbp/cadmium-29","payload":{"data":"' + serialized_data + '"},"query":""}]\n'
            compressed_data = self._MSL__compress_data(serialized_data)
            first_payload = {'messageid':self.current_message_id, 
             'data':compressed_data.decode('utf-8'), 
             'compressionalgo':'GZIP', 
             'sequencenumber':1, 
             'endofmsg':True}
            first_payload_encryption_envelope = self._MSL__encrypt(json.dumps(first_payload))
            first_payload_chunk = {'payload':base64.standard_b64encode(first_payload_encryption_envelope.encode('utf-8')).decode('utf-8'), 
             'signature':self._MSL__sign(first_payload_encryption_envelope).decode('utf-8')}
            request_data = json.dumps(header) + json.dumps(first_payload_chunk)
            return request_data

        def __compress_data(self, data):
            out = BytesIO()
            with gzip.GzipFile(fileobj=out, mode='w') as (f):
                f.write(data.encode('utf-8'))
            return base64.standard_b64encode(out.getvalue())

        def __generate_msl_header(self, is_handshake=False, is_key_request=False, compressionalgo='GZIP', encrypt=True, esn=None):
            """
            #Function that generates a MSL header dict
            #:return: The base64 encoded JSON String of the header
            """
            global esn_manifest
            self.current_message_id = self.rndm.randint(0, pow(2, 52))
            header_data = {'sender':esn_manifest, 
             'handshake':is_handshake, 
             'nonreplayable':False, 
             'capabilities':{'languages':[
               'en-US'], 
              'compressionalgos':[],  'encoderformats':[
               'JSON']}, 
             'recipient':'Netflix', 
             'renewable':True, 
             'messageid':self.current_message_id, 
             'timestamp':time.time()}
            if compressionalgo is not '':
                header_data['capabilities']['compressionalgos'].append(compressionalgo)
            else:
                if is_key_request:
                    public_key = base64.standard_b64encode(self.rsa_key.publickey().exportKey(format='DER')).decode('utf-8')
                    header_data['keyrequestdata'] = [
                     {'scheme':'ASYMMETRIC_WRAPPED', 
                      'keydata':{'publickey':public_key, 
                       'mechanism':'JWK_RSA', 
                       'keypairid':'superKeyPair'}}]
                else:
                    if 'usertoken' in self.tokens:
                        pass
                    else:
                        account = account_info
                        header_data['userauthdata'] = {'scheme':'EMAIL_PASSWORD', 
                         'authdata':{'email':account['email'], 
                          'password':account['password']}}
            return json.dumps(header_data)

        def __encrypt(self, plaintext):
            """
            Encrypt the given Plaintext with the encryption key
            :param plaintext:
            :return: Serialized JSON String of the encryption Envelope
            """
            iv = get_random_bytes(16)
            try:
                encryption_envelope = {'ciphertext':'', 
                 'keyid':esn_manifest + '_' + str(self.sequence_number),  'sha256':'AA==', 
                 'iv':base64.standard_b64encode(iv).decode('utf-8')}
            except Exception:
                print('ESN is invalid.')
                sys.exit(0)

            plaintext = Padding.pad(plaintext.encode('utf-8'), 16)
            cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv)
            ciphertext = cipher.encrypt(plaintext)
            encryption_envelope['ciphertext'] = base64.standard_b64encode(ciphertext).decode('utf-8')
            return json.dumps(encryption_envelope)

        def __sign(self, text):
            """
            Calculates the HMAC signature for the given text with the current sign key and SHA256
            :param text:
            :return: Base64 encoded signature
            """
            signature = HMAC.new(self.sign_key, text.encode('utf-8'), SHA256).digest()
            return base64.standard_b64encode(signature)

        def __perform_key_handshake(self):
            header = self._MSL__generate_msl_header(is_key_request=True, is_handshake=True, compressionalgo='', encrypt=False)
            request = {'entityauthdata':{'scheme':'NONE', 
              'authdata':{'identity': esn_manifest}}, 
             'headerdata':base64.standard_b64encode(header.encode('utf-8')).decode('utf-8'), 
             'signature':''}
            resp = self.session.post(self.endpoints['manifest'], json.dumps(request, sort_keys=True))
            if resp.status_code == 200:
                resp = resp.json()
                if 'errordata' in resp:
                    return False
                self._MSL__parse_crypto_keys(json.JSONDecoder().decode(base64.standard_b64decode(resp['headerdata']).decode('utf-8')))

        def __parse_crypto_keys(self, headerdata):
            self._MSL__set_master_token(headerdata['keyresponsedata']['mastertoken'])
            encrypted_encryption_key = base64.standard_b64decode(headerdata['keyresponsedata']['keydata']['encryptionkey'])
            encrypted_sign_key = base64.standard_b64decode(headerdata['keyresponsedata']['keydata']['hmackey'])
            cipher_rsa = PKCS1_OAEP.new(self.rsa_key)
            encryption_key_data = json.JSONDecoder().decode(cipher_rsa.decrypt(encrypted_encryption_key).decode('utf-8'))
            self.encryption_key = base64key_decode(encryption_key_data['k'])
            sign_key_data = json.JSONDecoder().decode(cipher_rsa.decrypt(encrypted_sign_key).decode('utf-8'))
            self.sign_key = base64key_decode(sign_key_data['k'])
            self._MSL__save_msl_data()
            self.handshake_performed = True

        def __load_msl_data(self):
            msl_data = json.JSONDecoder().decode(self.load_file(msl_data_path, msl_data_file).decode('utf-8'))
            master_token = json.JSONDecoder().decode(base64.standard_b64decode(msl_data['tokens']['mastertoken']['tokendata']).decode('utf-8'))
            valid_until = datetime.utcfromtimestamp(int(master_token['expiration']))
            present = datetime.now()
            difference = valid_until - present
            difference = difference.total_seconds() / 60 / 60
            if difference < 10:
                self._MSL__load_rsa_keys()
                self._MSL__perform_key_handshake()
                return
            self._MSL__set_master_token(msl_data['tokens']['mastertoken'])
            self.encryption_key = base64.standard_b64decode(msl_data['encryption_key'])
            self.sign_key = base64.standard_b64decode(msl_data['sign_key'])

        def __save_msl_data(self):
            """
            Saves the keys and tokens in json file
            :return:
            """
            data = {'encryption_key':base64.standard_b64encode(self.encryption_key).decode('utf-8'), 
             'sign_key':base64.standard_b64encode(self.sign_key).decode('utf-8'), 
             'tokens':{'mastertoken': self.mastertoken}}
            serialized_data = json.JSONEncoder().encode(data)
            self.save_file(msl_data_path, msl_data_file, serialized_data.encode('utf-8'))

        def __set_master_token(self, master_token):
            self.mastertoken = master_token
            self.sequence_number = json.JSONDecoder().decode(base64.standard_b64decode(master_token['tokendata']).decode('utf-8'))['sequencenumber']

        def __set_userid_token(self, userid_token):
            self.useridtoken = userid_token

        def __load_rsa_keys(self):
            loaded_key = self.load_file(msl_data_path, rsa_key_bin)
            self.rsa_key = RSA.importKey(loaded_key)

        def __save_rsa_keys(self):
            encrypted_key = self.rsa_key.exportKey()
            self.save_file(msl_data_path, rsa_key_bin, encrypted_key)

        @staticmethod
        def file_exists(msl_data_path, filename):
            """
            #Checks if a given file exists
            #:param filename: The filename
            #:return: True if so
            """
            return os.path.isfile(msl_data_path + filename)

        @staticmethod
        def save_file(msl_data_path, filename, content):
            """
            #Saves the given content under given filename
            #:param filename: The filename
            #:param content: The content of the file
            """
            with open(msl_data_path + filename, 'wb') as (file_):
                file_.write(content)
                file_.flush()
                file_.close()

        @staticmethod
        def save_file_(msl_data_path, filename, content):
            """
            #Saves the given content under given filename
            #:param filename: The filename
            #:param content: The content of the file
            """
            with open(msl_data_path + filename, 'w') as (file_):
                file_.write(content)
                file_.flush()
                file_.close()

        @staticmethod
        def load_file(msl_data_path, filename):
            """
            #Loads the content of a given filename
            #:param filename: The file to load
            #:return: The content of the file
            """
            with open(msl_data_path + filename, 'rb') as (file_):
                file_content = file_.read()
                file_.close()
            return file_content