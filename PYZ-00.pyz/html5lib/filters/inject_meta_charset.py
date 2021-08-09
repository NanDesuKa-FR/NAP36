# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\html5lib\filters\inject_meta_charset.py
from __future__ import absolute_import, division, unicode_literals
from . import base

class Filter(base.Filter):
    __doc__ = 'Injects ``<meta charset=ENCODING>`` tag into head of document'

    def __init__(self, source, encoding):
        """Creates a Filter

        :arg source: the source token stream

        :arg encoding: the encoding to set

        """
        base.Filter.__init__(self, source)
        self.encoding = encoding

    def __iter__--- This code section failed: ---

 L.  20         0  LOAD_STR                 'pre_head'
                2  STORE_FAST               'state'

 L.  21         4  LOAD_FAST                'self'
                6  LOAD_ATTR                encoding
                8  LOAD_CONST               None
               10  COMPARE_OP               is
               12  STORE_FAST               'meta_found'

 L.  22        14  BUILD_LIST_0          0 
               16  STORE_FAST               'pending'

 L.  24        18  SETUP_LOOP          480  'to 480'
               22  LOAD_GLOBAL              base
               24  LOAD_ATTR                Filter
               26  LOAD_ATTR                __iter__
               28  LOAD_FAST                'self'
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  GET_ITER         
               34  FOR_ITER            478  'to 478'
               38  STORE_FAST               'token'

 L.  25        40  LOAD_FAST                'token'
               42  LOAD_STR                 'type'
               44  BINARY_SUBSCR    
               46  STORE_FAST               'type'

 L.  26        48  LOAD_FAST                'type'
               50  LOAD_STR                 'StartTag'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    80  'to 80'

 L.  27        56  LOAD_FAST                'token'
               58  LOAD_STR                 'name'
               60  BINARY_SUBSCR    
               62  LOAD_ATTR                lower
               64  CALL_FUNCTION_0       0  '0 positional arguments'
               66  LOAD_STR                 'head'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L.  28        72  LOAD_STR                 'in_head'
               74  STORE_FAST               'state'
             76_0  COME_FROM            70  '70'
               76  JUMP_FORWARD        448  'to 448'
               80  ELSE                     '448'

 L.  30        80  LOAD_FAST                'type'
               82  LOAD_STR                 'EmptyTag'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   342  'to 342'

 L.  31        90  LOAD_FAST                'token'
               92  LOAD_STR                 'name'
               94  BINARY_SUBSCR    
               96  LOAD_ATTR                lower
               98  CALL_FUNCTION_0       0  '0 positional arguments'
              100  LOAD_STR                 'meta'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   258  'to 258'

 L.  33       108  LOAD_CONST               False
              110  STORE_FAST               'has_http_equiv_content_type'

 L.  34       112  SETUP_LOOP          340  'to 340'
              114  LOAD_FAST                'token'
              116  LOAD_STR                 'data'
              118  BINARY_SUBSCR    
              120  LOAD_ATTR                items
              122  CALL_FUNCTION_0       0  '0 positional arguments'
              124  GET_ITER         
              126  FOR_ITER            214  'to 214'
              128  UNPACK_SEQUENCE_2     2 
              130  UNPACK_SEQUENCE_2     2 
              132  STORE_FAST               'namespace'
              134  STORE_FAST               'name'
              136  STORE_FAST               'value'

 L.  35       138  LOAD_FAST                'namespace'
              140  LOAD_CONST               None
              142  COMPARE_OP               is-not
              144  POP_JUMP_IF_FALSE   150  'to 150'

 L.  36       146  CONTINUE            126  'to 126'
              148  JUMP_BACK           126  'to 126'
              150  ELSE                     '212'

 L.  37       150  LOAD_FAST                'name'
              152  LOAD_ATTR                lower
              154  CALL_FUNCTION_0       0  '0 positional arguments'
              156  LOAD_STR                 'charset'
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   188  'to 188'

 L.  38       162  LOAD_FAST                'self'
              164  LOAD_ATTR                encoding
              166  LOAD_FAST                'token'
              168  LOAD_STR                 'data'
              170  BINARY_SUBSCR    
              172  LOAD_FAST                'namespace'
              174  LOAD_FAST                'name'
              176  BUILD_TUPLE_2         2 
              178  STORE_SUBSCR     

 L.  39       180  LOAD_CONST               True
              182  STORE_FAST               'meta_found'

 L.  40       184  BREAK_LOOP       
              186  JUMP_BACK           126  'to 126'
              188  ELSE                     '212'

 L.  41       188  LOAD_FAST                'name'
              190  LOAD_STR                 'http-equiv'
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   126  'to 126'
              196  LOAD_FAST                'value'
              198  LOAD_ATTR                lower
              200  CALL_FUNCTION_0       0  '0 positional arguments'
              202  LOAD_STR                 'content-type'
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   126  'to 126'

 L.  42       208  LOAD_CONST               True
              210  STORE_FAST               'has_http_equiv_content_type'
              212  JUMP_BACK           126  'to 126'
              214  POP_BLOCK        

 L.  44       216  LOAD_FAST                'has_http_equiv_content_type'
              218  JUMP_IF_FALSE_OR_POP   230  'to 230'
              220  LOAD_CONST               (None, 'content')
              222  LOAD_FAST                'token'
              224  LOAD_STR                 'data'
              226  BINARY_SUBSCR    
              228  COMPARE_OP               in
            230_0  COME_FROM           218  '218'
              230  POP_JUMP_IF_FALSE   340  'to 340'

 L.  45       234  LOAD_STR                 'text/html; charset=%s'
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                encoding
              240  BINARY_MODULO    
              242  LOAD_FAST                'token'
              244  LOAD_STR                 'data'
              246  BINARY_SUBSCR    
              248  LOAD_CONST               (None, 'content')
              250  STORE_SUBSCR     

 L.  46       252  LOAD_CONST               True
              254  STORE_FAST               'meta_found'
            256_0  COME_FROM_LOOP      112  '112'
              256  JUMP_FORWARD        340  'to 340'
              258  ELSE                     '340'

 L.  48       258  LOAD_FAST                'token'
              260  LOAD_STR                 'name'
              262  BINARY_SUBSCR    
              264  LOAD_ATTR                lower
              266  CALL_FUNCTION_0       0  '0 positional arguments'
              268  LOAD_STR                 'head'
              270  COMPARE_OP               ==
              272  POP_JUMP_IF_FALSE   448  'to 448'
              276  LOAD_FAST                'meta_found'
              278  UNARY_NOT        
              280  POP_JUMP_IF_FALSE   448  'to 448'

 L.  50       284  LOAD_STR                 'StartTag'
              286  LOAD_STR                 'head'

 L.  51       288  LOAD_FAST                'token'
              290  LOAD_STR                 'data'
              292  BINARY_SUBSCR    
              294  LOAD_CONST               ('type', 'name', 'data')
              296  BUILD_CONST_KEY_MAP_3     3 
              298  YIELD_VALUE      
              300  POP_TOP          

 L.  52       302  LOAD_STR                 'EmptyTag'
              304  LOAD_STR                 'meta'

 L.  53       306  LOAD_CONST               (None, 'charset')
              308  LOAD_FAST                'self'
              310  LOAD_ATTR                encoding
              312  BUILD_MAP_1           1 
              314  LOAD_CONST               ('type', 'name', 'data')
              316  BUILD_CONST_KEY_MAP_3     3 
              318  YIELD_VALUE      
              320  POP_TOP          

 L.  54       322  LOAD_STR                 'EndTag'
              324  LOAD_STR                 'head'
              326  LOAD_CONST               ('type', 'name')
              328  BUILD_CONST_KEY_MAP_2     2 
              330  YIELD_VALUE      
              332  POP_TOP          

 L.  55       334  LOAD_CONST               True
              336  STORE_FAST               'meta_found'

 L.  56       338  CONTINUE             34  'to 34'
            340_0  COME_FROM           256  '256'
            340_1  COME_FROM           230  '230'
              340  JUMP_FORWARD        448  'to 448'
              342  ELSE                     '448'

 L.  58       342  LOAD_FAST                'type'
              344  LOAD_STR                 'EndTag'
              346  COMPARE_OP               ==
              348  POP_JUMP_IF_FALSE   448  'to 448'

 L.  59       352  LOAD_FAST                'token'
              354  LOAD_STR                 'name'
              356  BINARY_SUBSCR    
              358  LOAD_ATTR                lower
              360  CALL_FUNCTION_0       0  '0 positional arguments'
              362  LOAD_STR                 'head'
              364  COMPARE_OP               ==
              366  POP_JUMP_IF_FALSE   448  'to 448'
              370  LOAD_FAST                'pending'
              372  POP_JUMP_IF_FALSE   448  'to 448'

 L.  61       376  LOAD_FAST                'pending'
              378  LOAD_ATTR                pop
              380  LOAD_CONST               0
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  YIELD_VALUE      
              386  POP_TOP          

 L.  62       388  LOAD_FAST                'meta_found'
              390  POP_JUMP_IF_TRUE    414  'to 414'

 L.  63       394  LOAD_STR                 'EmptyTag'
              396  LOAD_STR                 'meta'

 L.  64       398  LOAD_CONST               (None, 'charset')
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                encoding
              404  BUILD_MAP_1           1 
              406  LOAD_CONST               ('type', 'name', 'data')
              408  BUILD_CONST_KEY_MAP_3     3 
              410  YIELD_VALUE      
              412  POP_TOP          
            414_0  COME_FROM           390  '390'

 L.  65       414  SETUP_LOOP          440  'to 440'
              416  LOAD_FAST                'pending'
              418  POP_JUMP_IF_FALSE   438  'to 438'

 L.  66       422  LOAD_FAST                'pending'
              424  LOAD_ATTR                pop
              426  LOAD_CONST               0
              428  CALL_FUNCTION_1       1  '1 positional argument'
              430  YIELD_VALUE      
              432  POP_TOP          
              434  JUMP_BACK           416  'to 416'
            438_0  COME_FROM           418  '418'
              438  POP_BLOCK        
            440_0  COME_FROM_LOOP      414  '414'

 L.  67       440  LOAD_CONST               True
              442  STORE_FAST               'meta_found'

 L.  68       444  LOAD_STR                 'post_head'
              446  STORE_FAST               'state'
            448_0  COME_FROM           372  '372'
            448_1  COME_FROM           366  '366'
            448_2  COME_FROM           348  '348'
            448_3  COME_FROM           340  '340'
            448_4  COME_FROM           272  '272'
            448_5  COME_FROM            76  '76'

 L.  70       448  LOAD_FAST                'state'
              450  LOAD_STR                 'in_head'
              452  COMPARE_OP               ==
              454  POP_JUMP_IF_FALSE   470  'to 470'

 L.  71       458  LOAD_FAST                'pending'
              460  LOAD_ATTR                append
              462  LOAD_FAST                'token'
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  POP_TOP          
              468  JUMP_BACK            34  'to 34'
              470  ELSE                     '476'

 L.  73       470  LOAD_FAST                'token'
              472  YIELD_VALUE      
              474  POP_TOP          
              476  JUMP_BACK            34  'to 34'
              478  POP_BLOCK        
            480_0  COME_FROM_LOOP       18  '18'

Parse error at or near `COME_FROM_LOOP' instruction at offset 256_0