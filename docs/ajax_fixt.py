# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from webtest import http
from doctest import SKIP
from tests.apps import input_app

PY3 = sys.version_info >= (3,)


def setup_test(test):
    for example in test.examples:
        # urlopen as moved in py3
        if PY3:
            example.options.setdefault(SKIP, 1)
    if not PY3:
        server = http.StopableWSGIServer.create(input_app)
        server.wait()
        path_to_html_file = os.path.join('tests', 'test.html')
        test.globs.update(
            input_app=input_app,
            server=server,
            your_url=server.application_url.rstrip('/') + '/html',
            path_to_html_file=path_to_html_file,
        )
setup_test.__test__ = False


def teardown_test(test):
    if 'server' in test.globs:
        test.globs['server'].shutdown()
teardown_test.__test__ = False
