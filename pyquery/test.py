#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt
import doctest
import os

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

def test_docs():
    doctest.testfile('README.txt', globs=globals(),
                     optionflags=doctest.ELLIPSIS)
    fails, total = doctest.testfile('README.txt', optionflags=doctest.ELLIPSIS)
    if fails == 0:
        print 'OK'

if __name__ == '__main__':
    test_docs()
