# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\pywidevine\cdm\session.py


class Session:

    def __init__(self, session_id, init_data, device_config):
        self.session_id = session_id
        self.init_data = init_data
        self.device_config = device_config
        self.device_key = None
        self.session_key = None
        self.derived_keys = {'enc':None,  'auth_1':None, 
         'auth_2':None}
        self.license_request = None
        self.license = None
        self.service_certificate = None
        self.privacy_mode = False
        self.keys = []