# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\setuptools-39.0.1-py3.6.egg\setuptools\ssl_support.py
import os, socket, atexit, re, functools
from setuptools.extern.six.moves import urllib, http_client, map, filter
from pkg_resources import ResolutionError, ExtractionError
try:
    import ssl
except ImportError:
    ssl = None

__all__ = [
 'VerifyingHTTPSHandler', 'find_ca_bundle', 'is_available', 'cert_paths',
 'opener_for']
cert_paths = '\n/etc/pki/tls/certs/ca-bundle.crt\n/etc/ssl/certs/ca-certificates.crt\n/usr/share/ssl/certs/ca-bundle.crt\n/usr/local/share/certs/ca-root.crt\n/etc/ssl/cert.pem\n/System/Library/OpenSSL/certs/cert.pem\n/usr/local/share/certs/ca-root-nss.crt\n/etc/ssl/ca-bundle.pem\n'.strip().split()
try:
    HTTPSHandler = urllib.request.HTTPSHandler
    HTTPSConnection = http_client.HTTPSConnection
except AttributeError:
    HTTPSHandler = HTTPSConnection = object

is_available = ssl is not None and object not in (HTTPSHandler, HTTPSConnection)
try:
    from ssl import CertificateError, match_hostname
except ImportError:
    try:
        from backports.ssl_match_hostname import CertificateError
        from backports.ssl_match_hostname import match_hostname
    except ImportError:
        CertificateError = None
        match_hostname = None

if not CertificateError:

    class CertificateError(ValueError):
        pass


if not match_hostname:

    def _dnsname_match(dn, hostname, max_wildcards=1):
        """Matching according to RFC 6125, section 6.4.3

        http://tools.ietf.org/html/rfc6125#section-6.4.3
        """
        pats = []
        if not dn:
            return False
        else:
            parts = dn.split('.')
            leftmost = parts[0]
            remainder = parts[1:]
            wildcards = leftmost.count('*')
            if wildcards > max_wildcards:
                raise CertificateError('too many wildcards in certificate DNS name: ' + repr(dn))
            if not wildcards:
                return dn.lower() == hostname.lower()
            if leftmost == '*':
                pats.append('[^.]+')
            else:
                if leftmost.startswith('xn--') or hostname.startswith('xn--'):
                    pats.append(re.escape(leftmost))
                else:
                    pats.append(re.escape(leftmost).replace('\\*', '[^.]*'))
            for frag in remainder:
                pats.append(re.escape(frag))

            pat = re.compile('\\A' + '\\.'.join(pats) + '\\Z', re.IGNORECASE)
            return pat.match(hostname)


    def match_hostname(cert, hostname):
        """Verify that *cert* (in decoded format as returned by
        SSLSocket.getpeercert()) matches the *hostname*.  RFC 2818 and RFC 6125
        rules are followed, but IP addresses are not accepted for *hostname*.

        CertificateError is raised on failure. On success, the function
        returns nothing.
        """
        if not cert:
            raise ValueError('empty or no certificate')
        else:
            dnsnames = []
            san = cert.get('subjectAltName', ())
            for key, value in san:
                if key == 'DNS':
                    if _dnsname_match(value, hostname):
                        return
                    dnsnames.append(value)

            if not dnsnames:
                for sub in cert.get('subject', ()):
                    for key, value in sub:
                        if key == 'commonName':
                            if _dnsname_match(value, hostname):
                                return
                            dnsnames.append(value)

            if len(dnsnames) > 1:
                raise CertificateError("hostname %r doesn't match either of %s" % (
                 hostname, ', '.join(map(repr, dnsnames))))
            else:
                if len(dnsnames) == 1:
                    raise CertificateError("hostname %r doesn't match %r" % (
                     hostname, dnsnames[0]))
                else:
                    raise CertificateError('no appropriate commonName or subjectAltName fields were found')


class VerifyingHTTPSHandler(HTTPSHandler):
    __doc__ = 'Simple verifying handler: no auth, subclasses, timeouts, etc.'

    def __init__(self, ca_bundle):
        self.ca_bundle = ca_bundle
        HTTPSHandler.__init__(self)

    def https_open(self, req):
        return self.do_open(lambda host, **kw: VerifyingHTTPSConn(host, (self.ca_bundle), **kw), req)


class VerifyingHTTPSConn(HTTPSConnection):
    __doc__ = 'Simple verifying connection: no auth, subclasses, timeouts, etc.'

    def __init__(self, host, ca_bundle, **kw):
        (HTTPSConnection.__init__)(self, host, **kw)
        self.ca_bundle = ca_bundle

    def connect(self):
        sock = socket.create_connection((
         self.host, self.port), getattr(self, 'source_address', None))
        if hasattr(self, '_tunnel'):
            if getattr(self, '_tunnel_host', None):
                self.sock = sock
                self._tunnel()
                actual_host = self._tunnel_host
            else:
                actual_host = self.host
        else:
            if hasattr(ssl, 'create_default_context'):
                ctx = ssl.create_default_context(cafile=(self.ca_bundle))
                self.sock = ctx.wrap_socket(sock, server_hostname=actual_host)
            else:
                self.sock = ssl.wrap_socket(sock,
                  cert_reqs=(ssl.CERT_REQUIRED), ca_certs=(self.ca_bundle))
        try:
            match_hostname(self.sock.getpeercert(), actual_host)
        except CertificateError:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            raise


def opener_for(ca_bundle=None):
    """Get a urlopen() replacement that uses ca_bundle for verification"""
    return urllib.request.build_opener(VerifyingHTTPSHandler(ca_bundle or find_ca_bundle())).open


def once(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(func, 'always_returns'):
            func.always_returns = func(*args, **kwargs)
        return func.always_returns

    return wrapper


@once
def get_win_certfile():
    try:
        import wincertstore
    except ImportError:
        return
    else:

        class CertFile(wincertstore.CertFile):

            def __init__(self):
                super(CertFile, self).__init__()
                atexit.register(self.close)

            def close(self):
                try:
                    super(CertFile, self).close()
                except OSError:
                    pass

        _wincerts = CertFile()
        _wincerts.addstore('CA')
        _wincerts.addstore('ROOT')
        return _wincerts.name


def find_ca_bundle():
    """Return an existing CA bundle path, or None"""
    extant_cert_paths = filter(os.path.isfile, cert_paths)
    return get_win_certfile() or next(extant_cert_paths, None) or _certifi_where()


def _certifi_where():
    try:
        return __import__('certifi').where()
    except (ImportError, ResolutionError, ExtractionError):
        pass