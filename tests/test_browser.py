import unittest

from pyquery.pyquery import PyQuery
from .browser_base import TextExtractionMixin


class TestInnerText(unittest.TestCase, TextExtractionMixin):
    def _prepare_dom(self, html):
        super(TestInnerText, self)._prepare_dom(html)
        self.pq = PyQuery(self.last_html)

    def _simple_test(self, html, expected_sq, expected_nosq, **kwargs):
        self._prepare_dom(html)
        text_sq = self.pq.text(squash_space=True, **kwargs)
        text_nosq = self.pq.text(squash_space=False, **kwargs)
        self.assertEqual(text_sq, expected_sq)
        self.assertEqual(text_nosq, expected_nosq)
