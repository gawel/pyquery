import os
import unittest
from threading import Thread
from time import sleep

from .browser_base import TextExtractionMixin

SELENIUM = 'MOZ_HEADLESS' in os.environ

try:
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
except ImportError:
    SELENIUM = False

if SELENIUM:
    from urllib.parse import urlunsplit
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from queue import Queue

    class BaseTestRequestHandler(BaseHTTPRequestHandler):
        _last_html = ''

        def _get_last_html(self):
            q = self.server.html_queue
            while not q.empty():
                self._last_html = q.get_nowait()
            return self._last_html

        def log_request(self, code='-', size='-'):
            pass

        def recv_from_testsuite(self, non_blocking=False):
            q = self.server.in_queue
            if non_blocking:
                return None if q.empty() else q.get_nowait()
            return q.get()

        def send_to_testsuite(self, value):
            self.server.out_queue.put(value)

    class HTMLSnippetSender(BaseTestRequestHandler):
        last_html = b''

        def get_last_html(self):
            while True:
                value = self.recv_from_testsuite(non_blocking=True)
                if value is None:
                    break
                self.last_html = value
            return self.last_html

        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(self.get_last_html().encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

    class BaseBrowserTest(unittest.TestCase):
        LOCAL_IP = '127.0.0.1'
        PORT = 28546
        # descendant of BaseBrowserTestRequestHandler
        REQUEST_HANDLER_CLASS = None

        @classmethod
        def setUpClass(cls):
            cls.to_server_queue = Queue()
            cls.from_server_queue = Queue()
            cls.server = HTTPServer((cls.LOCAL_IP, cls.PORT),
                                    cls.REQUEST_HANDLER_CLASS)
            cls.server.in_queue = cls.to_server_queue
            cls.server.out_queue = cls.from_server_queue
            cls.server_thread = Thread(target=cls.server.serve_forever)
            cls.server_thread.daemon = True
            cls.server_thread.start()
            options = Options()
            options.add_argument('-headless')
            cls.driver = webdriver.Firefox(options=options)
            sleep(1)

        @classmethod
        def tearDownClass(cls):
            cls.driver.quit()
            cls.server.shutdown()
            cls.server.server_close()

        def send_to_server(self, value):
            self.to_server_queue.put(value)

        def recv_from_server(self, non_blocking=False):
            q = self.from_server_queue
            if non_blocking:
                return None if q.empty() else q.get_nowait()
            return q.get()

        def open_url(self, path):
            self.driver.get(urlunsplit(
                ('http', '{}:{}'.format(
                    self.LOCAL_IP, self.PORT), path, '', '')))

    class TestInnerText(BaseBrowserTest, TextExtractionMixin):
        REQUEST_HANDLER_CLASS = HTMLSnippetSender

        def _simple_test(self, html, expected_sq, expected_nosq, **kwargs):
            self.send_to_server(html)
            self.open_url('/')

            selenium_text = self.driver.find_element_by_tag_name('body').text
            self.assertEqual(selenium_text, expected_sq)

            #  inner_text = self.driver.execute_script(
            #    'return document.body.innerText')
            #  text_content = self.driver.execute_script(
            #    'return document.body.textContent')
