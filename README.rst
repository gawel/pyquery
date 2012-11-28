pyquery: a jquery-like library for python
=========================================

pyquery allows you to make jquery queries on xml documents.
The API is as much as possible the similar to jquery. pyquery uses lxml for fast
xml and html manipulation.

This is not (or at least not yet) a library to produce or interact with
javascript code. I just liked the jquery API and I missed it in python so I
told myself "Hey let's make jquery in python". This is the result.

It can be used for many purposes, one idea that I might try in the future is to
use it for templating with pure http templates that you modify using pyquery.
I can also be used for web scrapping or for theming applications with
`Deliverance`_.

The `project`_ is being actively developped on a mercurial repository on
Github. I have the policy of giving push access to anyone who wants it
and then to review what he does. So if you want to contribute just email me.

Please report bugs on the `github
<https://github.com/gawel/pyquery/issues>`_ issue
tracker.

.. _deliverance: http://www.gawel.org/weblog/en/2008/12/skinning-with-pyquery-and-deliverance
.. _project: https://github.com/gawel/pyquery/

Quickstart
==========

You can use the PyQuery class to load an xml document from a string, a lxml
document, from a file or from an url::

    >>> from pyquery import PyQuery as pq
    >>> from lxml import etree
    >>> import urllib
    >>> d = pq("<html></html>")
    >>> d = pq(etree.fromstring("<html></html>"))
    >>> d = pq(url='http://google.com/')
    >>> # d = pq(url='http://google.com/', opener=lambda url: urllib.urlopen(url).read())
    >>> d = pq(filename=path_to_html_file)

Now d is like the $ in jquery::

    >>> d("#hello")
    [<p#hello.hello>]
    >>> p = d("#hello")
    >>> print(p.html())
    Hello world !
    >>> p.html("you know <a href='http://python.org/'>Python</a> rocks")
    [<p#hello.hello>]
    >>> print(p.html())
    you know <a href="http://python.org/">Python</a> rocks
    >>> print(p.text())
    you know Python rocks

You can use some of the pseudo classes that are available in jQuery but that
are not standard in css such as :first :last :even :odd :eq :lt :gt :checked
:selected :file::

    >>> d('p:first')
    [<p#hello.hello>]

