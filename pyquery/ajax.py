# -*- coding: utf-8 -*-
from .pyquery import PyQuery as Base
from .pyquery import no_default

from webob import Request, Response

try:
    from restkit.contrib.wsgi_proxy import HostProxy
except ImportError:
    HostProxy = no_default # NOQA


class PyQuery(Base):

    def __init__(self, *args, **kwargs):
        if 'response' in kwargs:
            self.response = kwargs.pop('response')
        else:
            self.response = Response()
        if 'app' in kwargs:
            self.app = kwargs.pop('app')
            if len(args) == 0:
                args = [[]]
        else:
            self.app = no_default
        Base.__init__(self, *args, **kwargs)
        if self._parent is not no_default:
            self.app = self._parent.app

    def _wsgi_get(self, path_info, **kwargs):
        if path_info.startswith('/'):
            if 'app' in kwargs:
                app = kwargs.pop('app')
            elif self.app is not no_default:
                app = self.app
            else:
                raise ValueError('There is no app available')
        else:
            if HostProxy is not no_default:
                app = HostProxy(path_info)
                path_info = '/'
            else:
                raise ImportError('restkit is not installed')

        environ = kwargs.pop('environ').copy()
        environ.update(kwargs)

        # unsuported (came from Deliverance)
        for key in ['HTTP_ACCEPT_ENCODING', 'HTTP_IF_MATCH',
                    'HTTP_IF_UNMODIFIED_SINCE', 'HTTP_RANGE', 'HTTP_IF_RANGE']:
            if key in environ:
                del environ[key]

        req = Request.blank(path_info)
        req.environ.update(environ)
        resp = req.get_response(app)
        status = resp.status.split()
        ctype = resp.content_type.split(';')[0]
        if status[0] not in '45' and ctype == 'text/html':
            body = resp.body
        else:
            body = []
        result = self.__class__(body,
                                parent=self._parent,
                                app=self.app,  # always return self.app
                                response=resp)
        return result

    def get(self, path_info, **kwargs):
        """GET a path from wsgi app or url
        """
        environ = kwargs.setdefault('environ', {})
        environ['REQUEST_METHOD'] = 'GET'
        environ['CONTENT_LENGTH'] = '0'
        return self._wsgi_get(path_info, **kwargs)

    def post(self, path_info, **kwargs):
        """POST a path from wsgi app or url
        """
        environ = kwargs.setdefault('environ', {})
        environ['REQUEST_METHOD'] = 'POST'
        return self._wsgi_get(path_info, **kwargs)
