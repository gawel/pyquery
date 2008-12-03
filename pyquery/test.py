#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt

def test():
    import doctest
    fails, total = doctest.testfile('README.txt', optionflags=doctest.ELLIPSIS)
    if fails == 0:
        print 'OK'

if __name__ == '__main__':
    test()
