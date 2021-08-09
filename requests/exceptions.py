# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: lib\site-packages\requests\exceptions.py
"""
requests.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Requests' exceptions.
"""
from urllib3.exceptions import HTTPError as BaseHTTPError

class RequestException(IOError):
    __doc__ = 'There was an ambiguous exception that occurred while handling your\n    request.\n    '

    def __init__(self, *args, **kwargs):
        response = kwargs.pop('response', None)
        self.response = response
        self.request = kwargs.pop('request', None)
        if response is not None:
            if not self.request:
                if hasattr(response, 'request'):
                    self.request = self.response.request
        (super(RequestException, self).__init__)(*args, **kwargs)


class HTTPError(RequestException):
    __doc__ = 'An HTTP error occurred.'


class ConnectionError(RequestException):
    __doc__ = 'A Connection error occurred.'


class ProxyError(ConnectionError):
    __doc__ = 'A proxy error occurred.'


class SSLError(ConnectionError):
    __doc__ = 'An SSL error occurred.'


class Timeout(RequestException):
    __doc__ = 'The request timed out.\n\n    Catching this error will catch both\n    :exc:`~requests.exceptions.ConnectTimeout` and\n    :exc:`~requests.exceptions.ReadTimeout` errors.\n    '


class ConnectTimeout(ConnectionError, Timeout):
    __doc__ = 'The request timed out while trying to connect to the remote server.\n\n    Requests that produced this error are safe to retry.\n    '


class ReadTimeout(Timeout):
    __doc__ = 'The server did not send any data in the allotted amount of time.'


class URLRequired(RequestException):
    __doc__ = 'A valid URL is required to make a request.'


class TooManyRedirects(RequestException):
    __doc__ = 'Too many redirects.'


class MissingSchema(RequestException, ValueError):
    __doc__ = 'The URL schema (e.g. http or https) is missing.'


class InvalidSchema(RequestException, ValueError):
    __doc__ = 'See defaults.py for valid schemas.'


class InvalidURL(RequestException, ValueError):
    __doc__ = 'The URL provided was somehow invalid.'


class InvalidHeader(RequestException, ValueError):
    __doc__ = 'The header value provided was somehow invalid.'


class InvalidProxyURL(InvalidURL):
    __doc__ = 'The proxy URL provided is invalid.'


class ChunkedEncodingError(RequestException):
    __doc__ = 'The server declared chunked encoding but sent an invalid chunk.'


class ContentDecodingError(RequestException, BaseHTTPError):
    __doc__ = 'Failed to decode response content'


class StreamConsumedError(RequestException, TypeError):
    __doc__ = 'The content for this response was already consumed'


class RetryError(RequestException):
    __doc__ = 'Custom retries logic failed'


class UnrewindableBodyError(RequestException):
    __doc__ = 'Requests encountered an error when trying to rewind a body'


class RequestsWarning(Warning):
    __doc__ = 'Base warning for Requests.'


class FileModeWarning(RequestsWarning, DeprecationWarning):
    __doc__ = 'A file was opened in text mode, but Requests determined its binary length.'


class RequestsDependencyWarning(RequestsWarning):
    __doc__ = "An imported dependency doesn't match the expected version range."