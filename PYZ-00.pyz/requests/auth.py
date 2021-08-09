# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\requests\auth.py
"""
requests.auth
~~~~~~~~~~~~~

This module contains the authentication handlers for Requests.
"""
import os, re, time, hashlib, threading, warnings
from base64 import b64encode
from .compat import urlparse, str, basestring
from .cookies import extract_cookies_to_jar
from ._internal_utils import to_native_string
from .utils import parse_dict_header
CONTENT_TYPE_FORM_URLENCODED = 'application/x-www-form-urlencoded'
CONTENT_TYPE_MULTI_PART = 'multipart/form-data'

def _basic_auth_str(username, password):
    """Returns a Basic Auth string."""
    if not isinstance(username, basestring):
        warnings.warn(("Non-string usernames will no longer be supported in Requests 3.0.0. Please convert the object you've passed in ({!r}) to a string or bytes object in the near future to avoid problems.".format(username)),
          category=DeprecationWarning)
        username = str(username)
    else:
        if not isinstance(password, basestring):
            warnings.warn(("Non-string passwords will no longer be supported in Requests 3.0.0. Please convert the object you've passed in ({!r}) to a string or bytes object in the near future to avoid problems.".format(password)),
              category=DeprecationWarning)
            password = str(password)
        if isinstance(username, str):
            username = username.encode('latin1')
        if isinstance(password, str):
            password = password.encode('latin1')
    authstr = 'Basic ' + to_native_string(b64encode((b':').join((username, password))).strip())
    return authstr


class AuthBase(object):
    __doc__ = 'Base class that all auth implementations derive from'

    def __call__(self, r):
        raise NotImplementedError('Auth hooks must be callable.')


class HTTPBasicAuth(AuthBase):
    __doc__ = 'Attaches HTTP Basic Authentication to the given Request object.'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __eq__(self, other):
        return all([
         self.username == getattr(other, 'username', None),
         self.password == getattr(other, 'password', None)])

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers['Authorization'] = _basic_auth_str(self.username, self.password)
        return r


class HTTPProxyAuth(HTTPBasicAuth):
    __doc__ = 'Attaches HTTP Proxy Authentication to a given Request object.'

    def __call__(self, r):
        r.headers['Proxy-Authorization'] = _basic_auth_str(self.username, self.password)
        return r


class HTTPDigestAuth(AuthBase):
    __doc__ = 'Attaches HTTP Digest Authentication to the given Request object.'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._thread_local = threading.local()

    def init_per_thread_state(self):
        if not hasattr(self._thread_local, 'init'):
            self._thread_local.init = True
            self._thread_local.last_nonce = ''
            self._thread_local.nonce_count = 0
            self._thread_local.chal = {}
            self._thread_local.pos = None
            self._thread_local.num_401_calls = None

    def build_digest_header(self, method, url):
        """
        :rtype: str
        """
        realm = self._thread_local.chal['realm']
        nonce = self._thread_local.chal['nonce']
        qop = self._thread_local.chal.get('qop')
        algorithm = self._thread_local.chal.get('algorithm')
        opaque = self._thread_local.chal.get('opaque')
        hash_utf8 = None
        if algorithm is None:
            _algorithm = 'MD5'
        else:
            _algorithm = algorithm.upper()
        if _algorithm == 'MD5' or _algorithm == 'MD5-SESS':

            def md5_utf8(x):
                if isinstance(x, str):
                    x = x.encode('utf-8')
                return hashlib.md5(x).hexdigest()

            hash_utf8 = md5_utf8
        else:
            if _algorithm == 'SHA':

                def sha_utf8(x):
                    if isinstance(x, str):
                        x = x.encode('utf-8')
                    return hashlib.sha1(x).hexdigest()

                hash_utf8 = sha_utf8
            else:
                if _algorithm == 'SHA-256':

                    def sha256_utf8(x):
                        if isinstance(x, str):
                            x = x.encode('utf-8')
                        return hashlib.sha256(x).hexdigest()

                    hash_utf8 = sha256_utf8
                else:
                    if _algorithm == 'SHA-512':

                        def sha512_utf8(x):
                            if isinstance(x, str):
                                x = x.encode('utf-8')
                            return hashlib.sha512(x).hexdigest()

                        hash_utf8 = sha512_utf8
        KD = lambda s, d: hash_utf8('%s:%s' % (s, d))
        if hash_utf8 is None:
            return
        else:
            entdig = None
            p_parsed = urlparse(url)
            path = p_parsed.path or '/'
            if p_parsed.query:
                path += '?' + p_parsed.query
            A1 = '%s:%s:%s' % (self.username, realm, self.password)
            A2 = '%s:%s' % (method, path)
            HA1 = hash_utf8(A1)
            HA2 = hash_utf8(A2)
            if nonce == self._thread_local.last_nonce:
                self._thread_local.nonce_count += 1
            else:
                self._thread_local.nonce_count = 1
            ncvalue = '%08x' % self._thread_local.nonce_count
            s = str(self._thread_local.nonce_count).encode('utf-8')
            s += nonce.encode('utf-8')
            s += time.ctime().encode('utf-8')
            s += os.urandom(8)
            cnonce = hashlib.sha1(s).hexdigest()[:16]
            if _algorithm == 'MD5-SESS':
                HA1 = hash_utf8('%s:%s:%s' % (HA1, nonce, cnonce))
            if not qop:
                respdig = KD(HA1, '%s:%s' % (nonce, HA2))
            else:
                if qop == 'auth' or 'auth' in qop.split(','):
                    noncebit = '%s:%s:%s:%s:%s' % (
                     nonce, ncvalue, cnonce, 'auth', HA2)
                    respdig = KD(HA1, noncebit)
                else:
                    return
            self._thread_local.last_nonce = nonce
            base = 'username="%s", realm="%s", nonce="%s", uri="%s", response="%s"' % (
             self.username, realm, nonce, path, respdig)
            if opaque:
                base += ', opaque="%s"' % opaque
            if algorithm:
                base += ', algorithm="%s"' % algorithm
            if entdig:
                base += ', digest="%s"' % entdig
            if qop:
                base += ', qop="auth", nc=%s, cnonce="%s"' % (ncvalue, cnonce)
            return 'Digest %s' % base

    def handle_redirect(self, r, **kwargs):
        """Reset num_401_calls counter on redirects."""
        if r.is_redirect:
            self._thread_local.num_401_calls = 1

    def handle_401(self, r, **kwargs):
        """
        Takes the given response and tries digest-auth, if needed.

        :rtype: requests.Response
        """
        if not 400 <= r.status_code < 500:
            self._thread_local.num_401_calls = 1
            return r
        else:
            if self._thread_local.pos is not None:
                r.request.body.seek(self._thread_local.pos)
            s_auth = r.headers.get('www-authenticate', '')
            if 'digest' in s_auth.lower() and self._thread_local.num_401_calls < 2:
                self._thread_local.num_401_calls += 1
                pat = re.compile('digest ', flags=(re.IGNORECASE))
                self._thread_local.chal = parse_dict_header(pat.sub('', s_auth, count=1))
                r.content
                r.close()
                prep = r.request.copy()
                extract_cookies_to_jar(prep._cookies, r.request, r.raw)
                prep.prepare_cookies(prep._cookies)
                prep.headers['Authorization'] = self.build_digest_header(prep.method, prep.url)
                _r = (r.connection.send)(prep, **kwargs)
                _r.history.append(r)
                _r.request = prep
                return _r
            self._thread_local.num_401_calls = 1
            return r

    def __call__(self, r):
        self.init_per_thread_state()
        if self._thread_local.last_nonce:
            r.headers['Authorization'] = self.build_digest_header(r.method, r.url)
        try:
            self._thread_local.pos = r.body.tell()
        except AttributeError:
            self._thread_local.pos = None

        r.register_hook('response', self.handle_401)
        r.register_hook('response', self.handle_redirect)
        self._thread_local.num_401_calls = 1
        return r

    def __eq__(self, other):
        return all([
         self.username == getattr(other, 'username', None),
         self.password == getattr(other, 'password', None)])

    def __ne__(self, other):
        return not self == other