# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\escsm.py
from .enums import MachineState
HZ_CLS = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 4, 0, 5, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
HZ_ST = (
 MachineState.START, MachineState.ERROR, 3, MachineState.START, MachineState.START, MachineState.START, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START, 4, MachineState.ERROR,
 5, MachineState.ERROR, 6, MachineState.ERROR, 5, 5, 4, MachineState.ERROR,
 4, MachineState.ERROR, 4, 4, 4, MachineState.ERROR, 4, MachineState.ERROR,
 4, MachineState.ITS_ME, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START)
HZ_CHAR_LEN_TABLE = (0, 0, 0, 0, 0, 0)
HZ_SM_MODEL = {'class_table':HZ_CLS, 
 'class_factor':6, 
 'state_table':HZ_ST, 
 'char_len_table':HZ_CHAR_LEN_TABLE, 
 'name':'HZ-GB-2312', 
 'language':'Chinese'}
ISO2022CN_CLS = (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
ISO2022CN_ST = (
 MachineState.START, 3, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START,
 MachineState.START, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 4, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 5, 6, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ERROR, MachineState.START)
ISO2022CN_CHAR_LEN_TABLE = (0, 0, 0, 0, 0, 0, 0, 0, 0)
ISO2022CN_SM_MODEL = {'class_table':ISO2022CN_CLS, 
 'class_factor':9, 
 'state_table':ISO2022CN_ST, 
 'char_len_table':ISO2022CN_CHAR_LEN_TABLE, 
 'name':'ISO-2022-CN', 
 'language':'Chinese'}
ISO2022JP_CLS = (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 3, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0,
                 4, 0, 8, 0, 0, 0, 0, 9, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
ISO2022JP_ST = (
 MachineState.START, 3, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START,
 MachineState.START, MachineState.START, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, 5, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 4, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 6, MachineState.ITS_ME, MachineState.ERROR, MachineState.ITS_ME, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ERROR, MachineState.START, MachineState.START)
ISO2022JP_CHAR_LEN_TABLE = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
ISO2022JP_SM_MODEL = {'class_table':ISO2022JP_CLS, 
 'class_factor':10, 
 'state_table':ISO2022JP_ST, 
 'char_len_table':ISO2022JP_CHAR_LEN_TABLE, 
 'name':'ISO-2022-JP', 
 'language':'Japanese'}
ISO2022KR_CLS = (2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
ISO2022KR_ST = (
 MachineState.START, 3, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 4, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 5, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.START, MachineState.START, MachineState.START, MachineState.START)
ISO2022KR_CHAR_LEN_TABLE = (0, 0, 0, 0, 0, 0)
ISO2022KR_SM_MODEL = {'class_table':ISO2022KR_CLS, 
 'class_factor':6, 
 'state_table':ISO2022KR_ST, 
 'char_len_table':ISO2022KR_CHAR_LEN_TABLE, 
 'name':'ISO-2022-KR', 
 'language':'Korean'}