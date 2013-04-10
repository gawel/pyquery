# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from webtest import http
from tests.apps import input_app


def setup_test(test):
    server = http.StopableWSGIServer.create(input_app)
    server.wait()
    test.globs.update(
        server=server,
        your_url=server.application_url.rstrip('/') + '/html',
    )
setup_test.__test__ = False


def teardown_test(test):
    test.globs['server'].shutdown()
teardown_test.__test__ = False
