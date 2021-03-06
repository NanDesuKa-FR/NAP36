# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\pycountry\__init__.py
"""pycountry"""
import os.path, pycountry.db
try:
    from pkg_resources import resource_filename
except ImportError:

    def resource_filename(package_or_requirement, resource_name):
        return os.path.join(os.path.dirname(__file__), resource_name)


LOCALES_DIR = resource_filename('pycountry', 'locales')
DATABASE_DIR = resource_filename('pycountry', 'databases')

class ExistingCountries(pycountry.db.Database):
    __doc__ = 'Provides access to an ISO 3166 database (Countries).'
    data_class_name = 'Country'
    root_key = '3166-1'


class HistoricCountries(pycountry.db.Database):
    __doc__ = 'Provides access to an ISO 3166-3 database\n    (Countries that have been removed from the standard).'
    data_class_name = 'Country'
    root_key = '3166-3'


class Scripts(pycountry.db.Database):
    __doc__ = 'Provides access to an ISO 15924 database (Scripts).'
    data_class_name = 'Script'
    root_key = '15924'


class Currencies(pycountry.db.Database):
    __doc__ = 'Provides access to an ISO 4217 database (Currencies).'
    data_class_name = 'Currency'
    root_key = '4217'


class Languages(pycountry.db.Database):
    __doc__ = 'Provides access to an ISO 639-1/2T/3 database (Languages).'
    no_index = [
     'status', 'scope', 'type', 'inverted_name', 'common_name']
    data_class_name = 'Language'
    root_key = '639-3'


class Subdivision(pycountry.db.Data):

    def __init__(self, **kw):
        if 'parent' in kw:
            kw['parent_code'] = kw['parent']
        else:
            kw['parent_code'] = None
        (super(Subdivision, self).__init__)(**kw)
        self.country_code = self.code.split('-')[0]
        if self.parent_code is not None:
            self.parent_code = '%s-%s' % (self.country_code, self.parent_code)

    @property
    def country(self):
        return countries.get(alpha_2=(self.country_code))

    @property
    def parent(self):
        if not self.parent_code:
            return
        else:
            return subdivisions.get(code=(self.parent_code))


class Subdivisions(pycountry.db.Database):
    data_class_base = Subdivision
    data_class_name = 'Subdivision'
    no_index = ['name', 'parent_code', 'parent', 'type']
    root_key = '3166-2'

    def _load(self, *args, **kw):
        (super(Subdivisions, self)._load)(*args, **kw)
        self.indices['country_code'] = {}
        for subdivision in self:
            divs = self.indices['country_code'].setdefault(subdivision.country_code, set())
            divs.add(subdivision)

    def get(self, **kw):
        default = kw.setdefault('default', None)
        subdivisions = (super(Subdivisions, self).get)(**kw)
        if subdivisions is default:
            if 'country_code' in kw:
                if countries.get(alpha_2=(kw['country_code'])) is not None:
                    return []
        return subdivisions


countries = ExistingCountries(os.path.join(DATABASE_DIR, 'iso3166-1.json'))
historic_countries = HistoricCountries(os.path.join(DATABASE_DIR, 'iso3166-3.json'))
scripts = Scripts(os.path.join(DATABASE_DIR, 'iso15924.json'))
currencies = Currencies(os.path.join(DATABASE_DIR, 'iso4217.json'))
languages = Languages(os.path.join(DATABASE_DIR, 'iso639-3.json'))
subdivisions = Subdivisions(os.path.join(DATABASE_DIR, 'iso3166-2.json'))