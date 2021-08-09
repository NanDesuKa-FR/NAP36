# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\pywidevine\decrypt\wvdecryptcustom.py
import logging, subprocess, re, base64
from pywidevine.cdm import cdm, deviceconfig

class WvDecrypt(object):
    WV_SYSTEM_ID = [
     237, 239, 139, 169, 121, 214, 74, 206, 163, 200, 39, 220, 213, 29, 33, 237]

    def __init__(self, init_data_b64, cert_data_b64):
        self.init_data_b64 = init_data_b64
        self.cert_data_b64 = cert_data_b64
        self.cdm = cdm.Cdm()

        def check_pssh(pssh_b64):
            pssh = base64.b64decode(pssh_b64)
            if not pssh[12:28] == bytes(self.WV_SYSTEM_ID):
                new_pssh = bytearray([0, 0, 0])
                new_pssh.append(32 + len(pssh))
                new_pssh[4:] = bytearray(b'pssh')
                new_pssh[8:] = [0, 0, 0, 0]
                new_pssh[13:] = self.WV_SYSTEM_ID
                new_pssh[29:] = [0, 0, 0, 0]
                new_pssh[31] = len(pssh)
                new_pssh[32:] = pssh
                return base64.b64encode(new_pssh)
            else:
                return pssh_b64

        self.session = self.cdm.open_session(check_pssh(self.init_data_b64), deviceconfig.DeviceConfig(deviceconfig.device_chromecdm_903))
        if self.cert_data_b64:
            self.cdm.set_service_certificate(self.session, self.cert_data_b64)

    def log_message(self, msg):
        return '{}'.format(msg)

    def start_process(self):
        keyswvdecrypt = []
        try:
            for key in self.cdm.get_keys(self.session):
                if key.type == 'CONTENT':
                    keyswvdecrypt.append(self.log_message('{}:{}'.format(key.kid.hex(), key.key.hex())))

        except Exception:
            return (
             False, keyswvdecrypt)
        else:
            return (
             True, keyswvdecrypt)

    def get_challenge(self):
        return self.cdm.get_license_request(self.session)

    def update_license(self, license_b64):
        self.cdm.provide_license(self.session, license_b64)
        return True