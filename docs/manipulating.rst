Manipulating
------------

..
    >>> from pyquery import PyQuery as pq

You can also add content to the end of tags::

    >>> d = pq('<p class="hello" id="hello">you know Python rocks</p>')
    >>> d('p').append(' check out <a href="http://reddit.com/r/python"><span>reddit</span></a>')
    [<p#hello.hello>]
    >>> print(d)
    <p class="hello" id="hello">you know Python rocks check out <a href="http://reddit.com/r/python"><span>reddit</span></a></p>

Or to the beginning::

    >>> p = d('p')
    >>> p.prepend('check out <a href="http://reddit.com/r/python">reddit</a>')
    [<p#hello.hello>]
    >>> print(p.html())
    check out <a href="http://reddit.com/r/python">reddit</a>you know ...

Prepend or append an element into an other::

    >>> d = pq('<html><body><div id="test"><a href="http://python.org">python</a> !</div></body></html>')
    >>> p.prependTo(d('#test'))
    [<p#hello.hello>]
    >>> print(d('#test').html())
    <p class="hello" ...

Insert an element after another::

    >>> p.insertAfter(d('#test'))
    [<p#hello.hello>]
    >>> print(d('#test').html())
    <a href="http://python.org">python</a> !

Or before::

    >>> p.insertBefore(d('#test'))
    [<p#hello.hello>]
    >>> print(d('body').html())
    <p class="hello" id="hello">...

Doing something for each elements::

    >>> p.each(lambda i, e: pq(e).addClass('hello2'))
    [<p#hello.hello.hello2>]

Remove an element::

    >>> d = pq('<html><body><p id="id">Yeah!</p><p>python rocks !</p></div></html>')
    >>> d.remove('p#id')
    [<html>]
    >>> d('p#id')
    []

Remove what's inside the selection::

    >>> d('p').empty()
    [<p>]

And you can get back the modified html::

    >>> print(d)
    <html><body><p/></body></html>

You can generate html stuff::

    >>> from pyquery import PyQuery as pq
    >>> print(pq('<div>Yeah !</div>').addClass('myclass') + pq('<b>cool</b>'))
    <div class="myclass">Yeah !</div><b>cool</b>

Remove all namespaces::

    >>> d = pq('<foo xmlns="http://example.com/foo"></foo>')
    >>> d
    [<{http://example.com/foo}foo>]
    >>> d.remove_namespaces()
    [<foo>]

