# -*- coding: utf-8 -*-
from webob import Request
from webob import Response
from webob import exc
from .compat import b


def input_app(environ, start_response):
    resp = Response()
    req = Request(environ)
    if req.path_info == '/':
        resp.body = '<input name="youyou" type="text" value="" />'
    elif req.path_info == '/submit':
        resp.body = '<input type="submit" value="OK" />'
    elif req.path_info == '/html/':
        resp.body = '<html><p>Success</p></html>'
    else:
        resp.body = ''
    return resp(environ, start_response)


def application(environ, start_response):
    req = Request(environ)
    response = Response()
    if req.method == 'GET':
        response.body = b('<pre>Yeah !</pre>')
    else:
        response.body = b('<a href="/plop">Yeah !</a>')
    return response(environ, start_response)


def secure_application(environ, start_response):
    if 'REMOTE_USER' not in environ:
        return exc.HTTPUnauthorized('vomis')(environ, start_response)
    return application(environ, start_response)
