# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\requests\__init__.py
"""
Requests HTTP Library
~~~~~~~~~~~~~~~~~~~~~

Requests is an HTTP library, written in Python, for human beings. Basic GET
usage:

   >>> import requests
   >>> r = requests.get('https://www.python.org')
   >>> r.status_code
   200
   >>> 'Python is a programming language' in r.content
   True

... or POST:

   >>> payload = dict(key1='value1', key2='value2')
   >>> r = requests.post('https://httpbin.org/post', data=payload)
   >>> print(r.text)
   {
     ...
     "form": {
       "key2": "value2",
       "key1": "value1"
     },
     ...
   }

The other HTTP methods are supported - see `requests.api`. Full documentation
is at <http://python-requests.org>.

:copyright: (c) 2017 by Kenneth Reitz.
:license: Apache 2.0, see LICENSE for more details.
"""
import urllib3, chardet, warnings
from .exceptions import RequestsDependencyWarning

def check_compatibility(urllib3_version, chardet_version):
    urllib3_version = urllib3_version.split('.')
    if not urllib3_version != ['dev']:
        raise AssertionError
    else:
        if len(urllib3_version) == 2:
            urllib3_version.append('0')
        else:
            major, minor, patch = urllib3_version
            major, minor, patch = int(major), int(minor), int(patch)
            assert major == 1
            assert minor >= 21
            assert minor <= 24
            major, minor, patch = chardet_version.split('.')[:3]
            major, minor, patch = int(major), int(minor), int(patch)
            assert major == 3
            assert minor < 1
        assert patch >= 2


def _check_cryptography(cryptography_version):
    try:
        cryptography_version = list(map(int, cryptography_version.split('.')))
    except ValueError:
        return
    else:
        if cryptography_version < [1, 3, 4]:
            warning = 'Old version of cryptography ({}) may cause slowdown.'.format(cryptography_version)
            warnings.warn(warning, RequestsDependencyWarning)


try:
    check_compatibility(urllib3.__version__, chardet.__version__)
except (AssertionError, ValueError):
    warnings.warn("urllib3 ({}) or chardet ({}) doesn't match a supported version!".format(urllib3.__version__, chardet.__version__), RequestsDependencyWarning)

try:
    from urllib3.contrib import pyopenssl
    pyopenssl.inject_into_urllib3()
    from cryptography import __version__ as cryptography_version
    _check_cryptography(cryptography_version)
except ImportError:
    pass

from urllib3.exceptions import DependencyWarning
warnings.simplefilter('ignore', DependencyWarning)
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __build__, __author__, __author_email__, __license__
from .__version__ import __copyright__, __cake__
from . import utils
from . import packages
from .models import Request, Response, PreparedRequest
from .api import request, get, head, post, patch, put, delete, options
from .sessions import session, Session
from .status_codes import codes
from .exceptions import RequestException, Timeout, URLRequired, TooManyRedirects, HTTPError, ConnectionError, FileModeWarning, ConnectTimeout, ReadTimeout
import logging
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())
warnings.simplefilter('default', FileModeWarning, append=True)