Traversing
----------

..
    >>> from pyquery import PyQuery as pq

Some jQuery traversal methods are supported.  Here are a few examples.

You can filter the selection list using a string selector::

    >>> d = pq('<p id="hello" class="hello"><a/></p><p id="test"><a/></p>')
    >>> d('p').filter('.hello')
    [<p#hello.hello>]

It is possible to select a single element with eq::

    >>> d('p').eq(0)
    [<p#hello.hello>]

You can find nested elements::

    >>> d('p').find('a')
    [<a>, <a>]
    >>> d('p').eq(1).find('a')
    [<a>]

Breaking out of a level of traversal is also supported using end::

    >>> d('p').find('a').end()
    [<p#hello.hello>, <p#test>]
    >>> d('p').eq(0).end()
    [<p#hello.hello>, <p#test>]
    >>> d('p').filter(lambda i: i == 1).end()
    [<p#hello.hello>, <p#test>]


If you want to select a dotted id you need to escape the dot::

    >>> d = pq('<p id="hello.you"><a/></p><p id="test"><a/></p>')
    >>> d('#hello\.you')
    [<p#hello.you>]

