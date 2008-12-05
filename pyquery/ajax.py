# -*- coding: utf-8 -*-
from webob import Request
from pyquery import PyQuery as Base
from pyquery import NoDefault

class PyQuery(Base):

    def __init__(self, *args, **kwargs):
        if 'app' in kwargs:
            self.app = kwargs.pop('app')
        else:
            self.app = NoDefault
        Base.__init__(self, *args, **kwargs)
        if self._parent is not NoDefault:
            self.app = self._parent.app

    def _wsgi_get(self, path_info, **kwargs):
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
        resp = req.get_response(self.app)
        status = resp.status.split()[0]
        ctype = resp.content_type.split(';')[0]
        if status == '200' and ctype == 'text/html':
            result = self.__class__(resp.body,
                                   parent=self._parent,
                                   app=self.app)
        else:
            result = self.__class__([],
                                    parent=self._parent,
                                    app=self.app)
        return result

    def get(self, path_info, **kwargs):
        kwargs['REQUEST_METHOD'] = 'GET'
        return self._wsgi_get(path_info, **kwargs)

    def post(self, path_info, **kwargs):
        kwargs['REQUEST_METHOD'] = 'POST'
        return self._wsgi_get(path_info, **kwargs)

