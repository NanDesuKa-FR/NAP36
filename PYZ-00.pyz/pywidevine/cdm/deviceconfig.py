# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\pywidevine\cdm\deviceconfig.py
import os
device_nexus6_lvl1 = {'name':'nexus6_lvl1', 
 'description':'nexus 6 firmware 5.1.1 lvl1 security level', 
 'security_level':1, 
 'session_id_type':'android', 
 'private_key_available':True, 
 'vmp':False, 
 'send_key_control_nonce':True}
device_chromecdm_903 = {'name':'chromecdm_903',  'description':'chrome cdm windows 903', 
 'security_level':3, 
 'session_id_type':'chrome', 
 'private_key_available':True, 
 'vmp':False, 
 'send_key_control_nonce':False}
device_chromecdm_1008 = {'name':'chromecdm_1008',  'description':'chrome cdm windows 1008', 
 'security_level':3, 
 'session_id_type':'chrome', 
 'private_key_available':True, 
 'vmp':False, 
 'send_key_control_nonce':False}
devices_available = [
 device_nexus6_lvl1, device_chromecdm_903, device_chromecdm_1008]
FILES_FOLDER = 'devices'

class DeviceConfig:

    def __init__(self, device):
        self.device_name = device['name']
        self.description = device['description']
        self.security_level = device['security_level']
        self.session_id_type = device['session_id_type']
        self.private_key_available = device['private_key_available']
        self.vmp = device['vmp']
        self.send_key_control_nonce = device['send_key_control_nonce']
        if 'keybox_filename' in device:
            self.keybox_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device['name'], device['keybox_filename'])
        else:
            self.keybox_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device['name'], 'keybox')
        if 'device_cert_filename' in device:
            self.device_cert_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device['name'], device['device_cert_filename'])
        else:
            self.device_cert_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device['name'], 'device_cert')
        if 'device_private_key_filename' in device:
            self.device_private_key_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device['name'], device['device_private_key_filename'])
        else:
            self.device_private_key_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device['name'], 'device_private_key')
        if 'device_client_id_blob_filename' in device:
            self.device_client_id_blob_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device['name'], device['device_client_id_blob_filename'])
        else:
            self.device_client_id_blob_filename = os.path.join(os.path.dirname(__file__), FILES_FOLDER, device['name'], 'device_client_id_blob')

    def __repr__(self):
        return 'DeviceConfig(name={}, description={}, security_level={}, session_id_type={}, private_key_available={}, vmp={})'.format(self.device_name, self.description, self.security_level, self.session_id_type, self.private_key_available, self.vmp)