# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\pywidevine\decrypt\netflix36_nokeys.py
if __name__ == 'pywidevine.decrypt.netflix36_nokeys':
    import binascii, configparser, argparse, base64, glob, gzip, json, os, pprint, pycountry, random, string, re, requests, sys, time, xml.etree.ElementTree as ET, zlib
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
    from pywidevine.decrypt.wvdecryptcustom import WvDecrypt
    from netflix36 import args

    def generate_esn(prefix):
        """
        generate_esn()
        @param prefix: Prefix of ESN to append generated device ID onto
        @return: ESN to use with MSL API
        """
        return prefix + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))


    username, password, esn_keys, esn_manifest, MANIFEST_ENDPOINT, LICENSE_ENDPOINT = NetflixConfig.configNetflix()
    esn_manifest = esn_keys
    account_info = {'email':username,  'password':password}
    from netflix36 import msl_data_path
    from netflix36 import wvDecrypterexe
    from netflix36 import challengeBIN
    from netflix36 import licenceBIN

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
            global msl_data_path
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
                    self.rsa_key = RSA.generate(2048)
                    self._MSL__save_rsa_keys()
                    self._MSL__perform_key_handshake()

        def load_manifest(self, viewable_id, Profile):
            """
            #Loads the manifets for the given viewable_id and returns a mpd-XML-Manifest
            #:param viewable_id: The id of of the viewable
            #:return: MPD XML Manifest or False if no success
            """
            manifest_request_data = {'method':'manifest', 
             'lookupType':'STANDARD', 
             'viewableIds':[
              viewable_id], 
             'profiles':[
              'dfxp-ls-sdh',
              'webvtt-lssdh-ios8',
              'heaac-2-dash'], 
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
            if 'playready-h264mpl' in Profile or 'playready-h264bpl' in Profile:
                manifest_request_data['profiles'].append('playready-h264bpl30-dash')
                manifest_request_data['profiles'].append('playready-h264mpl30-dash')
                manifest_request_data['profiles'].append('playready-h264mpl31-dash')
                manifest_request_data['profiles'].append('playready-h264mpl40-dash')
                manifest_request_data['profiles'].append('playready-h264hpl30-dash')
                manifest_request_data['profiles'].append('playready-h264hpl31-dash')
                manifest_request_data['profiles'].append('playready-h264hpl40-dash')
            else:
                if 'playready-h264hpl' in Profile:
                    manifest_request_data['profiles'].append('playready-h264hpl30-dash')
                    manifest_request_data['profiles'].append('playready-h264hpl31-dash')
                    manifest_request_data['profiles'].append('playready-h264hpl40-dash')
                else:
                    if 'hevc-main-L' in Profile or 'hevc-main10-L' in Profile:
                        manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc-prk')
                        manifest_request_data['profiles'].append('hevc-main10-L31-dash-cenc-prk')
                        manifest_request_data['profiles'].append('hevc-main10-L40-dash-cenc-prk')
                        manifest_request_data['profiles'].append('hevc-main10-L41-dash-cenc-prk')
                        manifest_request_data['profiles'].append('playready-h264hpl30-dash')
                        manifest_request_data['profiles'].append('playready-h264hpl31-dash')
                        manifest_request_data['profiles'].append('playready-h264hpl40-dash')
                    else:
                        if 'hevc-hdr-main10-L' in Profile:
                            manifest_request_data['profiles'].append('hevc-main10-L30-dash-cenc-prk')
                            manifest_request_data['profiles'].append('hevc-main10-L31-dash-cenc-prk')
                            manifest_request_data['profiles'].append('hevc-main10-L40-dash-cenc-prk')
                            manifest_request_data['profiles'].append('hevc-main10-L41-dash-cenc-prk')
                            manifest_request_data['profiles'].append('playready-h264hpl30-dash')
                            manifest_request_data['profiles'].append('playready-h264hpl31-dash')
                            manifest_request_data['profiles'].append('playready-h264hpl40-dash')
                        else:
                            if 'hevc-dv-main10-L' in Profile or 'hevc-dv5-main10-L' in Profile:
                                manifest_request_data['profiles'].append('hevc-dv-main10-L31-dash-cenc-prk')
                                manifest_request_data['profiles'].append('hevc-dv-main10-L40-dash-cenc-prk')
                                manifest_request_data['profiles'].append('hevc-dv-main10-L41-dash-cenc-prk')
                                manifest_request_data['profiles'].append('hevc-dv-main10-L30-dash-cenc-prk')
                                manifest_request_data['profiles'].append('hevc-dv5-main10-L40-dash-cenc-prk')
                                manifest_request_data['profiles'].append('hevc-dv5-main10-L41-dash-cenc-prk')
                                manifest_request_data['profiles'].append('hevc-dv5-main10-L30-dash-cenc-prk')
                                manifest_request_data['profiles'].append('hevc-dv5-main10-L31-dash-cenc-prk')
                                manifest_request_data['profiles'].append('playready-h264hpl30-dash')
                                manifest_request_data['profiles'].append('playready-h264hpl31-dash')
                                manifest_request_data['profiles'].append('playready-h264hpl40-dash')
                                manifest_request_data['profiles'].append('playready-h264hpl41-dash')
                            else:
                                if 'vp9-profile' in Profile:
                                    manifest_request_data['profiles'].append('vp9-profile0-L21-dash-cenc')
                                    manifest_request_data['profiles'].append('vp9-profile0-L30-dash-cenc')
                                    manifest_request_data['profiles'].append('vp9-profile0-L31-dash-cenc')
                                    manifest_request_data['profiles'].append('vp9-profile0-L40-dash-cenc')
                                    manifest_request_data['profiles'].append('playready-h264hpl30-dash')
                                    manifest_request_data['profiles'].append('playready-h264hpl31-dash')
            request_data = self._MSL__generate_msl_request_data(manifest_request_data)
            resp = self.session.post(self.endpoints['manifest'], request_data)
            resp = self._MSL__parse_chunked_msl_response(resp.text)
            data = self._MSL__decrypt_payload_chunks(resp['payloads'])
            return self._MSL__tranform_to_dash(data)

        def get_license(self, challenge_encoded):
            license_request_data = {'method':'license', 
             'licenseType':'STANDARD',  'clientVersion':'4.0004.899.011', 
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
                print('Error getting license: ' + resp.text)
                sys.exit(0)
            except ValueError:
                resp = self._MSL__parse_chunked_msl_response(resp.text)
                data = self._MSL__decrypt_payload_chunks(resp['payloads'])
                if data['success'] is True:
                    return data['result']['licenses'][0]['data']
                print('Error getting license: ' + json.dumps(data))
                sys.exit(0)

        def compress_lzw(uncompressed):
            """Compress a string to a list of output symbols."""
            dict_size = 256
            dictionary = dict((chr(i), chr(i)) for i in xrange(dict_size))
            w = ''
            result = []
            for c in uncompressed:
                wc = w + c
                if wc in dictionary:
                    w = wc
                else:
                    result.append(dictionary[w])
                    dictionary[wc] = dict_size
                    dict_size += 1
                    w = c

            if w:
                result.append(dictionary[w])
            return result

        def decompress_lzw(compressed):
            """Decompress a list of output ks to a string."""
            dict_size = 256
            dictionary = dict((chr(i), chr(i)) for i in xrange(dict_size))
            w = result = compressed.pop(0)
            for k in compressed:
                if k in dictionary:
                    entry = dictionary[k]
                else:
                    if k == dict_size:
                        entry = w + w[0]
                    else:
                        raise ValueError('Bad compressed k: %s' % k)
                    result += entry
                    dictionary[dict_size] = w + entry[0]
                    dict_size += 1
                    w = entry

            return result

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
            global cert_data_b64_new
            global init_data_b64_new
            global last_drm_context
            global playbackContextId
            self.save_file_(msl_data_path, manifest_file, json.dumps(manifest))
            try:
                manifest = manifest['result']['viewables'][0]
            except Exception:
                pass

            playbackContextId = manifest['playbackContextId']
            last_drm_context = manifest['drmContextId']
            self.last_playback_context = manifest['playbackContextId']
            self.last_drm_context = manifest['drmContextId']
            pssh = ''
            if 'psshb64' in manifest:
                if len(manifest['psshb64']) >= 1:
                    pssh = manifest['psshb64']
                    cert = manifest['cert']
                    init_data_b64_new = pssh
                    cert_data_b64_new = cert
            return (
             init_data_b64_new, cert_data_b64_new)

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
            global account_info
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
             'timestamp':int(time.time())}
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
                encryption_envelope = {'ciphertext':'',  'keyid':esn_manifest + '_' + str(self.sequence_number), 
                 'sha256':'AA==', 
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

        def DecryptAlternative(KID, PSSH, CERTIFICATE, FInput, FOutput, Type):
            Decrypted = False
            kid = KID.replace('-', '').lower()
            import codecs
            for pssh in PSSH:
                pssh_dec = base64.standard_b64decode(pssh).hex()
                if kid in pssh_dec:
                    if Type == 'audio':
                        print('\nDecrypting audio...')
                    else:
                        if Type == 'video':
                            print('\nDecrypting video...')
                        if os.path.isfile(challengeBIN):
                            os.remove(challengeBIN)
                        if os.path.isfile(licenceBIN):
                            os.remove(licenceBIN)
                    wvdecrypt_video = subprocess.Popen([
                     wvDecrypterexe, '--kid', KID, '--pssh', pssh, '--certificate', CERTIFICATE, '--input', FInput,
                     '--output', FOutput])
                    while not os.path.isfile(challengeBIN):
                        time.sleep(1)

                    with open(challengeBIN, 'rb') as (fd):
                        challenge_decoded = fd.read()
                    challenge_encoded = base64.b64encode(challenge_decoded).decode('utf-8')
                    msl = MSL('')
                    license_b64 = msl.get_license(challenge_encoded).encode()
                    with open(licenceBIN, 'wb') as (ld):
                        ld.write(license_b64)
                    stdoutdata, stderrdata = wvdecrypt_video.communicate()
                    if str(wvdecrypt_video.returncode) == '0':
                        if os.path.isfile(challengeBIN):
                            os.remove(challengeBIN)
                        if os.path.isfile(licenceBIN):
                            os.remove(licenceBIN)
                        Decrypted = True
                    else:
                        Decrypted = False

            return Decrypted


    def DecryptAlternative_Netflix(nfID, KID, FInput, FOutput, Type, Profile):
        global manifest_file
        global msl_data_file
        global rsa_key_bin
        rsa_key_bin = 'rsa_nokeys.bin'
        msl_data_file = 'msl_data_nokeys.json'
        manifest_file = 'manifest_nokeys.json'
        if os.path.isfile(msl_data_path + rsa_key_bin):
            os.remove(msl_data_path + rsa_key_bin)
        if os.path.isfile(msl_data_path + msl_data_file):
            os.remove(msl_data_path + msl_data_file)
        if os.path.isfile(msl_data_path + manifest_file):
            os.remove(msl_data_path + manifest_file)
        msl = MSL('')
        pssh_new, cert_new = msl.load_manifest(int(nfID), Profile)
        CorrectDecrypt = False
        CorrectDecrypt = MSL.DecryptAlternative(KID=KID, PSSH=pssh_new, CERTIFICATE=cert_new, FInput=FInput, FOutput=FOutput, Type=Type)
        if os.path.isfile(msl_data_path + rsa_key_bin):
            os.remove(msl_data_path + rsa_key_bin)
        if os.path.isfile(msl_data_path + msl_data_file):
            os.remove(msl_data_path + msl_data_file)
        if os.path.isfile(msl_data_path + manifest_file):
            os.remove(msl_data_path + manifest_file)
        return CorrectDecrypt