from io import StringIO

import pytest
from lxml import etree

from pyquery import PyQuery
from pyquery.pyquery import fromstring


@pytest.mark.parametrize('markup', ['', ' \t\n'])
@pytest.mark.parametrize('parser,error', [
    (None, etree.XMLSyntaxError),
    ('xml', etree.XMLSyntaxError),
    ('html', etree.ParserError),
])
def test_empty_file_rejected(tmp_path, markup, parser, error):
    filename = tmp_path / 'file.txt'
    filename.write_text(markup)
    with pytest.raises(error):
        PyQuery(filename=str(filename), parser=parser)


@pytest.mark.parametrize('markup', ['text', '<p>text<br>', '<p>text</p>'])
def test_nonempty_file_still_parsed(tmp_path, markup):
    filename = tmp_path / 'file.txt'
    filename.write_text(markup)
    assert PyQuery(filename=str(filename)).text() == 'text'


@pytest.mark.parametrize('markup', ['', ' \t\n', b'', b' \t\n'])
def test_empty_literal_returns_empty_selection(markup):
    doc = PyQuery(markup)
    assert not doc
    assert not doc.find('div')


def test_custom_parser_empty_tree_rejected():
    with pytest.raises(etree.ParserError):
        fromstring('ignored', custom_parser=lambda _: etree.ElementTree())


@pytest.mark.parametrize('result', [None, [], etree.Element('p'),
                                  etree.ElementTree(etree.Element('p'))])
def test_custom_parser_result_preserved(result):
    if isinstance(result, etree._ElementTree):
        expected = [result.getroot()]
    else:
        expected = [] if result is None or isinstance(result, list) else [result]
    assert fromstring('ignored', custom_parser=lambda _: result) == expected


@pytest.mark.parametrize('parser', [None, 'xml', 'html'])
@pytest.mark.parametrize('source', ['filename', 'url'])
def test_file_closed_after_parse_error(monkeypatch, parser, source):
    stream = StringIO('')
    if source == 'filename':
        monkeypatch.setattr('pyquery.pyquery.open', lambda *a, **kw: stream,
                            raising=False)
        kwargs = {'filename': 'file.txt'}
    else:
        kwargs = {'url': 'http://example.com', 'opener': lambda url: stream}
    with pytest.raises(etree.LxmlError):
        PyQuery(parser=parser, **kwargs)
    assert stream.closed
