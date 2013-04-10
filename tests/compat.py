# -*- coding: utf-8 -*-
import sys

PY3k = sys.version_info >= (3,)

if PY3k:
    text_type = str

    def u(value, encoding):
        return str(value)

    def b(value):
        return value.encode('utf-8')
else:
    text_type = unicode

    def u(value, encoding):  # NOQA
        return unicode(value, encoding)

    def b(value):  # NOQA
        return str(value)

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase  # NOQA
