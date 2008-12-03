#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt
import unittest
import doctest
from lxml import etree
import os

from pyquery import PyQuery as pq

dirname = os.path.dirname(__file__)
path_to_html_file = os.path.join(dirname, 'test.html')


class DocTest(doctest.DocFileCase):

    path = os.path.join(dirname, 'README.txt')

    def __init__(self, *args, **kwargs):
        parser = doctest.DocTestParser()
        doc = open(self.path).read()
        test = parser.get_doctest(doc, globals(), '', self.path, 0)
        doctest.DocFileCase.__init__(self, test, optionflags=doctest.ELLIPSIS)

    def setUp(self):
        test = self._dt_test
        test.globs.update(globals())

class TestSelector(unittest.TestCase):

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
    def test_selector_from_doc(self):
        doc = etree.fromstring(self.html)
        assert len(pq(doc)) == 1
        assert len(pq('div', doc)) == 3
        assert len(pq('div#node2', doc)) == 1

    def test_selector_from_html(self):
        assert len(pq(self.html)) == 1
        assert len(pq('div', self.html)) == 3
        assert len(pq('div#node2', self.html)) == 1

    def test_selector_from_obj(self):
        e = pq(self.html)
        assert len(e('div')) == 3
        assert len(e('div#node2')) == 1

    def test_selector_from_html_from_obj(self):
        e = pq(self.html)
        assert len(e('div', self.html2)) == 1
        assert len(e('div#node2', self.html2)) == 0


def main():
    doctest.testfile('README.txt', globs=globals(),
                     optionflags=doctest.ELLIPSIS)
    fails, total = doctest.testfile('README.txt', optionflags=doctest.ELLIPSIS)
    if fails == 0:
        print 'OK'

if __name__ == '__main__':
    main()
