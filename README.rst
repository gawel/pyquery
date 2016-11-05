pyquery: a jquery-like library for python
=========================================

.. image:: https://travis-ci.org/gawel/pyquery.svg
   :alt: Build Status
   :target: https://travis-ci.org/gawel/pyquery

pyquery allows you to make jquery queries on xml documents.
The API is as much as possible the similar to jquery. pyquery uses lxml for fast
xml and html manipulation.

This is not (or at least not yet) a library to produce or interact with
javascript code. I just liked the jquery API and I missed it in python so I
told myself "Hey let's make jquery in python". This is the result.

The `project`_ is being actively developed on a git repository on Github. I
have the policy of giving push access to anyone who wants it and then to review
what he does. So if you want to contribute just email me.

Please report bugs on the `github
<https://github.com/gawel/pyquery/issues>`_ issue
tracker.

.. _deliverance: http://www.gawel.org/weblog/en/2008/12/skinning-with-pyquery-and-deliverance
.. _project: https://github.com/gawel/pyquery/

Install
=======

- Linux ~ Python 2.x
        sudo apt-get update

        sudo apt-get install libxml2-dev libxslt1-dev python-dev python-pip

        pip install pyquery

- Linux ~ Python 3.x
        sudo apt-get update

        sudo apt-get install libxml2-dev libxslt1-dev python3-lxml python3-dev python-pip3

        pip3 install pyquery

- Mac ~ Python 2.x
        sudo easy_install pip

        pip install pyquery

- Mac ~ Python 3.x
        sudo easy_install pip3

        pip3 install pyquery

http://docs.python-guide.org/en/latest/starting/install/win

- Win
        python ez_setup.py

        python get-pip.py

        pip install pyquery

Quickstart
==========

You can use the PyQuery class to load an xml document from a string, a lxml
document, from a file or from an url::

    >>> from pyquery import PyQuery as pq
    >>> from lxml import etree
    >>> import urllib
    >>> d = pq("<html></html>")
    >>> d = pq(etree.fromstring("<html></html>"))
    >>> d = pq(url=your_url)
    >>> d = pq(url=your_url,
    ...        opener=lambda url, **kw: urlopen(url).read())
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

