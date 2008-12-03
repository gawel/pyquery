#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt
import doctest
import os

dirname = os.path.dirname(__file__)
path_to_html_file = open(os.path.join(dirname, 'test.html'))

def test_docs():
    doctest.testfile('README.txt', globs=globals(),
                     optionflags=doctest.ELLIPSIS)
    fails, total = doctest.testfile('README.txt', optionflags=doctest.ELLIPSIS)
    if fails == 0:
        print 'OK'

if __name__ == '__main__':
    test_docs()
