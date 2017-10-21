# -*- coding: utf-8 -*-
import sys

PY3k = sys.version_info >= (3,)

if PY3k:
    from urllib.request import urlopen
    from urllib.parse import urlencode
    from urllib.error import HTTPError
    basestring = (str, bytes)
else:
    from urllib2 import urlopen  # NOQA
    from urllib import urlencode  # NOQA
    from urllib2 import HTTPError

try:
    import requests
    HAS_REQUEST = True
except ImportError:
    HAS_REQUEST = False


allowed_args = (
    'auth', 'data', 'headers', 'verify',
    'cert', 'config', 'hooks', 'proxies', 'cookies'
)


def _query(url, method, kwargs):
    data = None
    if 'data' in kwargs:
        data = kwargs.pop('data')
    if type(data) in (dict, list, tuple):
        data = urlencode(data)

    if isinstance(method, basestring) and \
       method.lower() == 'get' and data:
        if '?' not in url:
            url += '?'
        elif url[-1] not in ('?', '&'):
            url += '&'
        url += data
        data = None

    if data and PY3k:
        data = data.encode('utf-8')
    return url, data


def _requests(url, kwargs):
    encoding = kwargs.get('encoding')
    method = kwargs.get('method', 'get').lower()
    meth = getattr(requests, str(method))
    if method == 'get':
        url, data = _query(url, method, kwargs)
    kw = {}
    for k in allowed_args:
        if k in kwargs:
            kw[k] = kwargs[k]
    resp = meth(url=url, **kw)
    if not (200 <= resp.status_code < 300):
        raise HTTPError(resp.url, resp.status_code,
                        resp.reason, resp.headers, None)
    if encoding:
        resp.encoding = encoding
    html = resp.text
    return html


def _urllib(url, kwargs):
    method = kwargs.get('method')
    url, data = _query(url, method, kwargs)
    return urlopen(url, data)


def url_opener(url, kwargs):
    if HAS_REQUEST:
        return _requests(url, kwargs)
    return _urllib(url, kwargs)
