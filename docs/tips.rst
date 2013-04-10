Tips
====

..
    >>> from pyquery import PyQuery as pq

Making links absolute
---------------------

You can make links absolute which can be usefull for screen scrapping::

    >>> d = pq(url=your_url, parser='html')
    >>> d('form').attr('action')
    '/form-submit'
    >>> d.make_links_absolute()
    [<html>]

Using different parsers
-----------------------

By default pyquery uses the lxml xml parser and then if it doesn't work goes on
to try the html parser from lxml.html. The xml parser can sometimes be
problematic when parsing xhtml pages because the parser will not raise an error
but give an unusable tree (on w3c.org for example).

You can also choose which parser to use explicitly::

   >>> pq('<html><body><p>toto</p></body></html>', parser='xml')
   [<html>]
   >>> pq('<html><body><p>toto</p></body></html>', parser='html')
   [<html>]
   >>> pq('<html><body><p>toto</p></body></html>', parser='html_fragments')
   [<p>]

The html and html_fragments parser are the ones from lxml.html.


