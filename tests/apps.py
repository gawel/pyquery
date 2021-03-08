# -*- coding: utf-8 -*-
from webob import Request
from webob import Response
from webob import exc


def input_app(environ, start_response):
    resp = Response()
    req = Request(environ)
    if req.path_info == '/':
        resp.text = '<input name="youyou" type="text" value="" />'
    elif req.path_info == '/submit':
        resp.text = '<input type="submit" value="OK" />'
    elif req.path_info.startswith('/html'):
        resp.text = '<html><p>Success</p></html>'
    else:
        resp.text = '<html></html>'
    return resp(environ, start_response)


def application(environ, start_response):
    req = Request(environ)
    response = Response()
    if req.method == 'GET':
        response.text = '<pre>Yeah !</pre>'
    else:
        response.text = '<a href="/plop">Yeah !</a>'
    return response(environ, start_response)


def secure_application(environ, start_response):
    if 'REMOTE_USER' not in environ:
        return exc.HTTPUnauthorized('vomis')(environ, start_response)
    return application(environ, start_response)
