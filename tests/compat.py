# -*- coding: utf-8 -*-
import sys

PY3k = sys.version_info >= (3,)

try:
    unicode
except NameError:
    unicode = str

if PY3k:
    text_type = str

    def b(value):
        return value.encode('utf-8')
else:
    text_type = unicode

    def b(value):  # NOQA
        return str(value)

from unittest import TestCase  # NOQA
