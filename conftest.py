import os
import pytest
from webtest import http
from webtest.debugapp import debug_app
from urllib.request import urlopen


@pytest.fixture
def readme_fixt():
    server = http.StopableWSGIServer.create(debug_app)
    server.wait()
    path_to_html_file = os.path.join('tests', 'test.html')
    yield (
        urlopen,
        server.application_url,
        path_to_html_file,
    )
    server.shutdown()
