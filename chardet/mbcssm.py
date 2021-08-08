# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\mbcssm.py
from .enums import MachineState
BIG5_CLS = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
            3, 0)
BIG5_ST = (
 MachineState.ERROR, MachineState.START, MachineState.START, 3, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ERROR,
 MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START)
BIG5_CHAR_LEN_TABLE = (0, 1, 1, 2, 0)
BIG5_SM_MODEL = {'class_table':BIG5_CLS, 
 'class_factor':5, 
 'state_table':BIG5_ST, 
 'char_len_table':BIG5_CHAR_LEN_TABLE, 
 'name':'Big5'}
CP949_CLS = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4,
             4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1,
             1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
             5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 1, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
             6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7,
             7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7,
             7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 2, 2, 3, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 0)
CP949_ST = (
 MachineState.ERROR, MachineState.START, 3, MachineState.ERROR, MachineState.START, MachineState.START, 4, 5, MachineState.ERROR, 6,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START,
 MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START,
 MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START,
 MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START)
CP949_CHAR_LEN_TABLE = (0, 1, 2, 0, 1, 1, 2, 2, 0, 2)
CP949_SM_MODEL = {'class_table':CP949_CLS, 
 'class_factor':10, 
 'state_table':CP949_ST, 
 'char_len_table':CP949_CHAR_LEN_TABLE, 
 'name':'CP949'}
EUCJP_CLS = (4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4,
             4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
             4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
             4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
             4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
             4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
             5, 5, 5, 1, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 5)
EUCJP_ST = (
 3, 4, 3, 5, MachineState.START, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.START, MachineState.ERROR, MachineState.START, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 3, MachineState.ERROR,
 3, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START)
EUCJP_CHAR_LEN_TABLE = (2, 2, 2, 3, 1, 0)
EUCJP_SM_MODEL = {'class_table':EUCJP_CLS, 
 'class_factor':6, 
 'state_table':EUCJP_ST, 
 'char_len_table':EUCJP_CHAR_LEN_TABLE, 
 'name':'EUC-JP'}
EUCKR_CLS = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 0)
EUCKR_ST = (
 MachineState.ERROR, MachineState.START, 3, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START)
EUCKR_CHAR_LEN_TABLE = (0, 1, 2, 0)
EUCKR_SM_MODEL = {'class_table':EUCKR_CLS, 
 'class_factor':4, 
 'state_table':EUCKR_ST, 
 'char_len_table':EUCKR_CHAR_LEN_TABLE, 
 'name':'EUC-KR'}
EUCTW_CLS = (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
             4, 4, 4, 4, 4, 4, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 0)
EUCTW_ST = (
 MachineState.ERROR, MachineState.ERROR, MachineState.START, 3, 3, 3, 4, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ERROR, MachineState.START, MachineState.ERROR,
 MachineState.START, MachineState.START, MachineState.START, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 5, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.ERROR, MachineState.START, MachineState.START,
 MachineState.START, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START)
EUCTW_CHAR_LEN_TABLE = (0, 0, 1, 2, 2, 2, 3)
EUCTW_SM_MODEL = {'class_table':EUCTW_CLS, 
 'class_factor':7, 
 'state_table':EUCTW_ST, 
 'char_len_table':EUCTW_CHAR_LEN_TABLE, 
 'name':'x-euc-tw'}
GB2312_CLS = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
              2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
              2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
              2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6,
              6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
              6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
              6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
              6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
              6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
              6, 6, 0)
GB2312_ST = (
 MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, 3, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ERROR, MachineState.ERROR, MachineState.START,
 4, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, 5, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.START)
GB2312_CHAR_LEN_TABLE = (0, 1, 1, 1, 1, 1, 2)
GB2312_SM_MODEL = {'class_table':GB2312_CLS, 
 'class_factor':7, 
 'state_table':GB2312_ST, 
 'char_len_table':GB2312_CHAR_LEN_TABLE, 
 'name':'GB2312'}
SJIS_CLS = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3,
            3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0,
            0, 0)
SJIS_ST = (
 MachineState.ERROR, MachineState.START, MachineState.START, 3, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START)
SJIS_CHAR_LEN_TABLE = (0, 1, 1, 2, 0, 0)
SJIS_SM_MODEL = {'class_table':SJIS_CLS, 
 'class_factor':6, 
 'state_table':SJIS_ST, 
 'char_len_table':SJIS_CHAR_LEN_TABLE, 
 'name':'Shift_JIS'}
UCS2BE_CLS = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 4, 5)
UCS2BE_ST = (
 5, 7, 7, MachineState.ERROR, 4, 3, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, 6, 6, 6, 6, MachineState.ERROR, MachineState.ERROR,
 6, 6, 6, 6, 6, MachineState.ITS_ME, 6, 6,
 6, 6, 6, 6, 5, 7, 7, MachineState.ERROR,
 5, 8, 6, 6, MachineState.ERROR, 6, 6, 6,
 6, 6, 6, 6, MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START)
UCS2BE_CHAR_LEN_TABLE = (2, 2, 2, 0, 2, 2)
UCS2BE_SM_MODEL = {'class_table':UCS2BE_CLS, 
 'class_factor':6, 
 'state_table':UCS2BE_ST, 
 'char_len_table':UCS2BE_CHAR_LEN_TABLE, 
 'name':'UTF-16BE'}
UCS2LE_CLS = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 4, 5)
UCS2LE_ST = (
 6, 6, 7, 6, 4, 3, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, 5, 5, 5, MachineState.ERROR, MachineState.ITS_ME, MachineState.ERROR,
 5, 5, 5, MachineState.ERROR, 5, MachineState.ERROR, 6, 6,
 7, 6, 8, 8, 5, 5, 5, MachineState.ERROR,
 5, 5, 5, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 5, 5,
 5, 5, 5, MachineState.ERROR, 5, MachineState.ERROR, MachineState.START, MachineState.START)
UCS2LE_CHAR_LEN_TABLE = (2, 2, 2, 2, 2, 2)
UCS2LE_SM_MODEL = {'class_table':UCS2LE_CLS, 
 'class_factor':6, 
 'state_table':UCS2LE_ST, 
 'char_len_table':UCS2LE_CHAR_LEN_TABLE, 
 'name':'UTF-16LE'}
UTF8_CLS = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5,
            5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
            5, 5, 5, 5, 5, 5, 5, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
            6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 8, 8, 8, 8, 8, 8,
            8, 8, 8, 8, 8, 8, 9, 8, 8, 10, 11, 11, 11, 11, 11, 11, 11, 12, 13, 13,
            13, 14, 15, 0, 0)
UTF8_ST = (
 MachineState.ERROR, MachineState.START, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 12, 10,
 9, 11, 8, 7, 6, 5, 4, 3,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME, MachineState.ITS_ME,
 MachineState.ERROR, MachineState.ERROR, 5, 5, 5, 5, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 5, 5, 5, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, 7, 7, 7, 7, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 7, 7, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, 9, 9, 9, 9, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 9, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, 12, 12, 12, 12, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, 12, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, 12, 12, 12, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.START, MachineState.START, MachineState.START, MachineState.START, MachineState.ERROR, MachineState.ERROR,
 MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR, MachineState.ERROR)
UTF8_CHAR_LEN_TABLE = (0, 1, 0, 0, 0, 0, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6)
UTF8_SM_MODEL = {'class_table':UTF8_CLS, 
 'class_factor':16, 
 'state_table':UTF8_ST, 
 'char_len_table':UTF8_CHAR_LEN_TABLE, 
 'name':'UTF-8'}