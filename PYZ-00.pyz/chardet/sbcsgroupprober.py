# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\chardet\sbcsgroupprober.py
from .charsetgroupprober import CharSetGroupProber
from .sbcharsetprober import SingleByteCharSetProber
from .langcyrillicmodel import Win1251CyrillicModel, Koi8rModel, Latin5CyrillicModel, MacCyrillicModel, Ibm866Model, Ibm855Model
from .langgreekmodel import Latin7GreekModel, Win1253GreekModel
from .langbulgarianmodel import Latin5BulgarianModel, Win1251BulgarianModel
from .langthaimodel import TIS620ThaiModel
from .langhebrewmodel import Win1255HebrewModel
from .hebrewprober import HebrewProber
from .langturkishmodel import Latin5TurkishModel

class SBCSGroupProber(CharSetGroupProber):

    def __init__(self):
        super(SBCSGroupProber, self).__init__()
        self.probers = [
         SingleByteCharSetProber(Win1251CyrillicModel),
         SingleByteCharSetProber(Koi8rModel),
         SingleByteCharSetProber(Latin5CyrillicModel),
         SingleByteCharSetProber(MacCyrillicModel),
         SingleByteCharSetProber(Ibm866Model),
         SingleByteCharSetProber(Ibm855Model),
         SingleByteCharSetProber(Latin7GreekModel),
         SingleByteCharSetProber(Win1253GreekModel),
         SingleByteCharSetProber(Latin5BulgarianModel),
         SingleByteCharSetProber(Win1251BulgarianModel),
         SingleByteCharSetProber(TIS620ThaiModel),
         SingleByteCharSetProber(Latin5TurkishModel)]
        hebrew_prober = HebrewProber()
        logical_hebrew_prober = SingleByteCharSetProber(Win1255HebrewModel, False, hebrew_prober)
        visual_hebrew_prober = SingleByteCharSetProber(Win1255HebrewModel, True, hebrew_prober)
        hebrew_prober.set_model_probers(logical_hebrew_prober, visual_hebrew_prober)
        self.probers.extend([hebrew_prober, logical_hebrew_prober,
         visual_hebrew_prober])
        self.reset()