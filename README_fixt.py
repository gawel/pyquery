# -*- coding: utf-8 -*-
import os
from webtest import http
from webtest.debugapp import debug_app

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen


def setup_test(test):
    server = http.StopableWSGIServer.create(debug_app)
    server.wait()
    path_to_html_file = os.path.join('tests', 'test.html')
    test.globs.update(
        urlopen=urlopen,
        server=server,
        your_url=server.application_url,
        path_to_html_file=path_to_html_file,
    )
setup_test.__test__ = False


def teardown_test(test):
    test.globs['server'].shutdown()
teardown_test.__test__ = False
