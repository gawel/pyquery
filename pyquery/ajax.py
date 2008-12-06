# -*- coding: utf-8 -*-
from webob import Request, Response
from pyquery import PyQuery as Base
from pyquery import no_default

try:
    from paste.proxy import Proxy
except ImportError:
    Proxy = no_default

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
            if Proxy is not no_default:
                app = Proxy(path_info)
                path_info = '/'
            else:
                raise ImportError('Paste is not installed')

        if 'environ' in kwargs:
            environ = kwargs.pop('environ').copy()
        else:
            environ = {}
        if path_info:
            kwargs['PATH_INFO'] = path_info
        environ.update(kwargs)

        # unsuported (came from Deliverance)
        for key in ['HTTP_ACCEPT_ENCODING', 'HTTP_IF_MATCH', 'HTTP_IF_UNMODIFIED_SINCE',
                    'HTTP_RANGE', 'HTTP_IF_RANGE']:
            if key in environ:
                del environ[key]

        req = Request(environ)
        resp = req.get_response(app)
        status = resp.status.split()
        ctype = resp.content_type.split(';')[0]
        if status[0] not in '45' and ctype == 'text/html':
            body = resp.body
        else:
            body = []
        result = self.__class__(body,
                                parent=self._parent,
                                app=self.app, # always return self.app
                                response=resp)
        return result

    def get(self, path_info, **kwargs):
        """GET a path from wsgi app or url
        """
        kwargs['REQUEST_METHOD'] = 'GET'
        return self._wsgi_get(path_info, **kwargs)

    def post(self, path_info, **kwargs):
        """POST a path from wsgi app or url
        """
        kwargs['REQUEST_METHOD'] = 'POST'
        return self._wsgi_get(path_info, **kwargs)
