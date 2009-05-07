#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt
from webob import Request, Response, exc
from lxml import etree
import unittest
import doctest
import os

import pyquery
from pyquery import PyQuery as pq
from ajax import PyQuery as pqa

dirname = os.path.dirname(os.path.abspath(pyquery.__file__))
docs = os.path.join(os.path.dirname(dirname), 'docs')
path_to_html_file = os.path.join(dirname, 'test.html')

def input_app(environ, start_response):
    resp = Response()
    req = Request(environ)
    if req.path_info == '/':
        resp.body = '<input name="youyou" type="text" value="" />'
    elif req.path_info == '/submit':
        resp.body = '<input type="submit" value="OK" />'
    else:
        resp.body = ''
    return resp(environ, start_response)

class TestReadme(doctest.DocFileCase):
    path = os.path.join(dirname, 'README.txt')

    def __init__(self, *args, **kwargs):
        parser = doctest.DocTestParser()
        doc = open(self.path).read()
        test = parser.get_doctest(doc, globals(), '', self.path, 0)
        doctest.DocFileCase.__init__(self, test, optionflags=doctest.ELLIPSIS)

    def setUp(self):
        test = self._dt_test
        test.globs.update(globals())

for filename in os.listdir(docs):
    if filename.endswith('.txt'):
        klass_name = 'Test%s' % filename.replace('.txt', '').title()
        path = os.path.join(docs, filename)
        exec '%s = type("%s", (TestReadme,), dict(path=path))' % (klass_name, klass_name)

class TestTests(doctest.DocFileCase):
    path = os.path.join(dirname, 'tests.txt')

    def __init__(self, *args, **kwargs):
        parser = doctest.DocTestParser()
        doc = open(self.path).read()
        test = parser.get_doctest(doc, globals(), '', self.path, 0)
        doctest.DocFileCase.__init__(self, test, optionflags=doctest.ELLIPSIS)

class TestSelector(unittest.TestCase):
    klass = pq
    html = """
           <html>
            <body>
              <div>node1</div>
              <div id="node2">node2</div>
              <div class="node3">node3</div>
            </body>
           </html>
           """

    html2 = """
           <html>
            <body>
              <div>node1</div>
            </body>
           </html>
           """

    html3 = """
           <html>
            <body>
              <div>node1</div>
              <div id="node2">node2</div>
              <div class="node3">node3</div>
            </body>
           </html>
           """

    html4 = """
           <html>
            <body>
              <form action="/">
                <input name="enabled" type="text" value="test"/>
                <input name="disabled" type="text" value="disabled" disabled="disabled"/>
                <input name="file" type="file" />
                <select name="select">
                  <option value="">Choose something</option>
                  <option value="one">One</option>
                  <option value="two" selected="selected">Two</option>
                  <option value="three">Three</option>
                </select>
                <input name="radio" type="radio" value="one"/>
                <input name="radio" type="radio" value="two" checked="checked"/>
                <input name="radio" type="radio" value="three"/>
                <input name="checkbox" type="checkbox" value="a"/>
                <input name="checkbox" type="checkbox" value="b" checked="checked"/>
                <input name="checkbox" type="checkbox" value="c"/>
                <input name="button" type="button" value="button" />
                <button>button</button>
              </form>
            </body>
           </html>
           """

    html5 = """
           <html>
            <body>
              <h1>Heading 1</h1>
              <h2>Heading 2</h2>
              <h3>Heading 3</h3>
              <h4>Heading 4</h4>
              <h5>Heading 5</h5>
              <h6>Heading 6</h6>
            </body>
           </html>
           """

    def test_selector_from_doc(self):
        doc = etree.fromstring(self.html)
        assert len(self.klass(doc)) == 1
        assert len(self.klass('div', doc)) == 3
        assert len(self.klass('div#node2', doc)) == 1

    def test_selector_from_html(self):
        assert len(self.klass(self.html)) == 1
        assert len(self.klass('div', self.html)) == 3
        assert len(self.klass('div#node2', self.html)) == 1

    def test_selector_from_obj(self):
        e = self.klass(self.html)
        assert len(e('div')) == 3
        assert len(e('div#node2')) == 1

    def test_selector_from_html_from_obj(self):
        e = self.klass(self.html)
        assert len(e('div', self.html2)) == 1
        assert len(e('div#node2', self.html2)) == 0

    def test_class(self):
        e = self.klass(self.html)
        assert isinstance(e, self.klass)
        n = e('div', self.html2)
        assert isinstance(n, self.klass)
        assert n._parent is e

    def test_pseudo_classes(self):
        e = self.klass(self.html)
        self.assertEqual(e('div:first').text(), 'node1')
        self.assertEqual(e('div:last').text(), 'node3')
        self.assertEqual(e('div:even').text(), 'node1 node3')
        self.assertEqual(e('div div:even').text(), None)
        self.assertEqual(e('body div:even').text(), 'node1 node3')
        self.assertEqual(e('div:gt(0)').text(), 'node2 node3')
        self.assertEqual(e('div:lt(1)').text(), 'node1')
        self.assertEqual(e('div:eq(2)').text(), 'node3')

        #test on the form
        e = self.klass(self.html4)
        assert len(e(':disabled')) == 1
        assert len(e('input:enabled')) == 9
        assert len(e(':selected')) == 1
        assert len(e(':checked')) == 2
        assert len(e(':file')) == 1
        assert len(e(':input')) == 12
        assert len(e(':button')) == 2
        assert len(e(':radio')) == 3
        assert len(e(':checkbox')) == 3

        #test on other elements
        e = self.klass(self.html5)
        assert len(e(":header")) == 6

class TestTraversal(unittest.TestCase):
    klass = pq
    html = """
           <html>
            <body>
              <div id="node1"><span>node1</span></div>
              <div id="node2" class="node3"><span>node2</span><span> booyah</span></div>
            </body>
           </html>
           """

    def test_filter(self):
        assert len(self.klass('div', self.html).filter('.node3')) == 1
        assert len(self.klass('div', self.html).filter('#node2')) == 1
        assert len(self.klass('div', self.html).filter(lambda i: i == 0)) == 1

    def test_not(self):
        assert len(self.klass('div', self.html).not_('.node3')) == 1

    def test_is(self):
        assert self.klass('div', self.html).is_('.node3')
        assert not self.klass('div', self.html).is_('.foobazbar')

    def test_find(self):
        assert len(self.klass('#node1', self.html).find('span')) == 1
        assert len(self.klass('#node2', self.html).find('span')) == 2
        assert len(self.klass('div', self.html).find('span')) == 3

    def test_map(self):
        def ids_minus_one(i, elem):
            return int(self.klass(elem).attr('id')[-1]) - 1
        assert self.klass('div', self.html).map(ids_minus_one) == [0, 1]

    def test_end(self):
        assert len(self.klass('div', self.html).find('span').end()) == 2
        assert len(self.klass('#node2', self.html).find('span').end()) == 1

def application(environ, start_response):
    req = Request(environ)
    response = Response()
    if req.method == 'GET':
        response.body = '<pre>Yeah !</pre>'
    else:
        response.body = '<a href="/plop">Yeah !</a>'
    return response(environ, start_response)

def secure_application(environ, start_response):
    if 'REMOTE_USER' not in environ:
        return exc.HTTPUnauthorized('vomis')(environ, start_response)
    return application(environ, start_response)

class TestAjaxSelector(TestSelector):
    klass = pqa

    def test_proxy(self):
        e = self.klass([])
        val = e.get('http://pyquery.org/')
        assert len(val('div.document')) == 1, (val.response, val)

    def test_get(self):
        e = self.klass(app=application)
        val = e.get('/')
        assert len(val('pre')) == 1, val

    def test_secure_get(self):
        e = self.klass(app=secure_application)
        val = e.get('/', environ=dict(REMOTE_USER='gawii'))
        assert len(val('pre')) == 1, val
        val = e.get('/', REMOTE_USER='gawii')
        assert len(val('pre')) == 1, val

    def test_secure_get_not_authorized(self):
        e = self.klass(app=secure_application)
        val = e.get('/')
        assert len(val('pre')) == 0, val

    def test_post(self):
        e = self.klass(app=application)
        val = e.post('/')
        assert len(val('a')) == 1, val

    def test_subquery(self):
        e = self.klass(app=application)
        n = e('div')
        val = n.post('/')
        assert len(val('a')) == 1, val

if __name__ == '__main__':
    fails, total = unittest.main()
    if fails == 0:
        print 'OK'
