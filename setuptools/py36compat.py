# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\py36compat.py
import sys
from distutils.errors import DistutilsOptionError
from distutils.util import strtobool
from distutils.debug import DEBUG

class Distribution_parse_config_files:
    __doc__ = '\n    Mix-in providing forward-compatibility for functionality to be\n    included by default on Python 3.7.\n\n    Do not edit the code in this class except to update functionality\n    as implemented in distutils.\n    '

    def parse_config_files(self, filenames=None):
        from configparser import ConfigParser
        if sys.prefix != sys.base_prefix:
            ignore_options = ['install-base', 'install-platbase', 'install-lib',
             'install-platlib', 'install-purelib', 'install-headers',
             'install-scripts', 'install-data', 'prefix', 'exec-prefix',
             'home', 'user', 'root']
        else:
            ignore_options = []
        ignore_options = frozenset(ignore_options)
        if filenames is None:
            filenames = self.find_config_files()
        if DEBUG:
            self.announce('Distribution.parse_config_files():')
        parser = ConfigParser(interpolation=None)
        for filename in filenames:
            if DEBUG:
                self.announce('  reading %s' % filename)
            parser.read(filename)
            for section in parser.sections():
                options = parser.options(section)
                opt_dict = self.get_option_dict(section)
                for opt in options:
                    if opt != '__name__' and opt not in ignore_options:
                        val = parser.get(section, opt)
                        opt = opt.replace('-', '_')
                        opt_dict[opt] = (filename, val)

            parser.__init__()

        if 'global' in self.command_options:
            for opt, (src, val) in self.command_options['global'].items():
                alias = self.negative_opt.get(opt)
                try:
                    if alias:
                        setattr(self, alias, not strtobool(val))
                    else:
                        if opt in ('verbose', 'dry_run'):
                            setattr(self, opt, strtobool(val))
                        else:
                            setattr(self, opt, val)
                except ValueError as msg:
                    raise DistutilsOptionError(msg)


if sys.version_info < (3, ):

    class Distribution_parse_config_files:
        pass