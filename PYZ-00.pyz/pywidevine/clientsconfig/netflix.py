# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\pywidevine\clientsconfig\netflix.py
import configparser, os, sys
Config = configparser.ConfigParser(interpolation=None)
netflix_cfg = './netflix.cfg'
if not os.path.isfile(netflix_cfg):
    cfgfile = open(netflix_cfg, 'w')
    print('Configuration file not found, generating it...')
    email = None
    while not email:
        email = input('email: ')

    password = None
    while not password:
        password = input('Password: ')

    esn = None
    esn = input('ESN, press ENTER for not change default value: ')
    if esn == '':
        esn = 'NFCDCH-02-DMT46QNHH01MNAHJF9415XFCF9X5YJ'
    esn_manifest = None
    esn_manifest = input('ESN for manifest, press ENTER for not change default value: ')
    if esn_manifest == '':
        esn_manifest = 'NFUWA-001-DMT46QNHH01MNAHJF9415XFCF9X5YJ'
    manifest_url = None
    manifest_url = input('Manifest URL, press ENTER for not change default value: ')
    if manifest_url == '':
        manifest_url = 'https://www.netflix.com/api/msl/cadmium/manifest'
    license_url = None
    license_url = input('License URL, press ENTER for not change default value: ')
    if license_url == '':
        license_url = 'https://www.netflix.com/api/msl/cadmium/license'
    Config.add_section('config')
    Config.set('config', 'email', email)
    Config.set('config', 'password', password)
    Config.set('config', 'esn', esn)
    Config.set('config', 'esn_manifest', esn_manifest)
    Config.set('config', 'manifest_url', manifest_url)
    Config.set('config', 'license_url', license_url)
    Config.write(cfgfile)
    cfgfile.close()
    print('\nThe program will close to save the configuration, then start it again.\n')
    sys.exit(0)
Config.read(netflix_cfg)
try:
    email = Config.get('config', 'email')
    password = Config.get('config', 'password')
    esn = Config.get('config', 'esn')
    esn_manifest = Config.get('config', 'esn_manifest')
    manifest_url = Config.get('config', 'manifest_url')
    license_url = Config.get('config', 'license_url')
except Exception:
    os.remove(netflix_cfg)
    cfgfile = open(netflix_cfg, 'w')
    print('Configuration file not found, generating it...')
    email = input('email: ')
    while not email:
        email = input('email: ')

    password = input('Password: ')
    while not password:
        password = input('Password: ')

    esn = None
    esn = input('ESN, press ENTER for not change default value: ')
    if esn == '':
        esn = 'NFCDCH-02-DMT46QNHH01MNAHJF9415XFCF9X5YJ'
    esn_manifest = None
    esn_manifest = input('ESN for manifest, press ENTER for not change default value: ')
    if esn_manifest == '':
        esn_manifest = 'NFUWA-001-DMT46QNHH01MNAHJF9415XFCF9X5YJ'
    manifest_url = None
    manifest_url = input('Manifest URL, press ENTER for not change default value: ')
    if manifest_url == '':
        manifest_url = 'https://www.netflix.com/api/msl/cadmium/manifest'
    license_url = None
    license_url = input('License URL, press ENTER for not change default value: ')
    if license_url == '':
        license_url = 'https://www.netflix.com/api/msl/cadmium/license'
    Config.add_section('config')
    Config.set('config', 'email', email)
    Config.set('config', 'password', password)
    Config.set('config', 'esn', esn)
    Config.set('config', 'esn_manifest', esn_manifest)
    Config.set('config', 'manifest_url', manifest_url)
    Config.set('config', 'license_url', license_url)
    Config.write(cfgfile)
    cfgfile.close()
    print('\nThe program will close to save the configuration, then start it again.\n')
    sys.exit(0)

if email == '' or password == '' or esn == '' or esn_manifest == '' or manifest_url == '' or license_url == '':
    os.remove(netflix_cfg)
    cfgfile = open(netflix_cfg, 'w')
    print('Configuration file not found, generating it...')
    email = input('email: ')
    while not email:
        email = input('email: ')

    password = input('Password: ')
    while not password:
        password = input('Password: ')

    esn = None
    esn = input('ESN, press ENTER for not change default value: ')
    if esn == '':
        esn = 'NFCDCH-02-DMT46QNHH01MNAHJF9415XFCF9X5YJ'
    esn_manifest = None
    esn_manifest = input('ESN for manifest, press ENTER for not change default value: ')
    if esn_manifest == '':
        esn_manifest = 'NFUWA-001-DMT46QNHH01MNAHJF9415XFCF9X5YJ'
    manifest_url = None
    manifest_url = input('Manifest URL, press ENTER for not change default value: ')
    if manifest_url == '':
        manifest_url = 'https://www.netflix.com/api/msl/cadmium/manifest'
    license_url = None
    license_url = input('License URL, press ENTER for not change default value: ')
    if license_url == '':
        license_url = 'https://www.netflix.com/api/msl/cadmium/license'
    Config.add_section('config')
    Config.set('config', 'email', email)
    Config.set('config', 'password', password)
    Config.set('config', 'esn', esn)
    Config.set('config', 'esn_manifest', esn_manifest)
    Config.set('config', 'manifest_url', manifest_url)
    Config.set('config', 'license_url', license_url)
    Config.write(cfgfile)
    cfgfile.close()
    print('\nThe program will close to save the configuration, then start it again.\n')
    sys.exit(0)
config = {'username':email, 
 'password':password, 
 'esn':esn, 
 'esn_manifest':esn_manifest, 
 'manifest':manifest_url, 
 'license':license_url}

class NetflixConfig(object):

    def configNetflix():
        return (
         config['username'], config['password'], config['esn'], config['esn_manifest'], config['manifest'], config['license'])