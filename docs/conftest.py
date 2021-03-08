import os
import sys
import pytest
from webtest import http
from webtest.debugapp import debug_app


@pytest.fixture
def scrap_url():
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from tests.apps import input_app
    server = http.StopableWSGIServer.create(input_app)
    server.wait()
    yield server.application_url.rstrip('/') + '/html'
    server.shutdown()


@pytest.fixture
def tips_url():
    server = http.StopableWSGIServer.create(debug_app)
    server.wait()
    yield server.application_url.rstrip('/') + '/form.html'
    server.shutdown()
