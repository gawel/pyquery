#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt

import sys

try:
    import webob
except ImportError:
    from .pyquery import PyQuery
else:
    from .ajax import PyQuery

