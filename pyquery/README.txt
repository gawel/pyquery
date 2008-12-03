pyquery: a jquery-like library
====================================

pyquery allows you to make jquery queries on xml documents.
The API is as much as possible the similar to jquery. PyQuery use lxml for fast
xml and html manipulation.

This is not (or at least not yet) a library to produce or interact with
javascript code. I just liked the jquery API and I missed it in python so I
told myself "Hey let's make jquery in python". This is the result.

It can be used for many purposes, one idea that I might try in the future is to
use it for templating with pure http templates that you modify using pyquery.

You can use the PyQuery class to load an xml document from a string, a lxml
document, from a file or from an url::

    >>> from pyquery import PyQuery
    >>> from lxml import etree
    >>> d = PyQuery("<html></html>")
    >>> d = PyQuery(etree.fromstring("<html></html>"))
    >>> d = PyQuery(url='http://w3c.org/')
    >>> d = PyQuery(filename=path_to_html_file)

Now d is like the $ in jquery::

    >>> d("#hello")
    [<p#hello.hello>]
    >>> p = d("#hello")
    >>> p.html()
    'Hello world !'
    >>> p.html("you know <a href='http://python.org/'>Python</a> rocks")
    [<p#hello.hello>]
    >>> p.html()
    'you know <a href="http://python.org/">Python</a> rocks'
    >>> p.text()
    'you know Python rocks'

You can play with the attributes::

    >>> p.attr("id")
    'hello'
    >>> p.attr("id", "plop")
    [<p#plop.hello>]
    >>> p.attr("id", "hello")
    [<p#hello.hello>]

Or the pythonic way::    

    >>> p.id
    'hello'
    >>> p.id = "plop"
    >>> p.id
    'plop'
    >>> p.id = "hello"

And the class::

    >>> p.addClass("toto")
    [<p#hello.toto.hello>]
    >>> p.toggleClass("titi toto")
    [<p#hello.titi.hello>]
    >>> p.removeClass("titi")
    [<p#hello.hello>]

Or the style::

    >>> p.css("font-size", "15px")
    [<p#hello.hello>]
    >>> p.attr("style")
    'font-size: 15px'
    >>> p.css({"font-size": "17px"})
    [<p#hello.hello>]
    >>> p.attr("style")
    'font-size: 17px'

You can also add content to the end of tags::

    >>> d('p').append('check out <a href="http://reddit.com/r/python"><span>reddit</span></a>')
    [<p#hello.hello>, <p#test>]
    >>> print d
    <html>
    ...
    <p class="hello" id="hello" style="font-size: 17px">you know <a href="http://python.org/">Python</a> rockscheck out <a href="http://reddit.com/r/python"><span>reddit</span></a></p><p id="test">
    hello <a href="http://python.org">python</a> !
    check out <a href="http://python.org/">Python</a> rockscheck out <a href="http://reddit.com/r/python"><span>reddit</span></a></p>
    ...

Or to the beginning::

    >>> p.prepend('check out <a href="http://reddit.com/r/python">reddit</a>')
    [<p#hello.hello>]
    >>> p.html()
    'check out <a href="http://reddit.com/r/python">reddit</a>you know ...'

Prepend or append an element into an other::

    >>> p.prependTo(d('#test'))
    [<p#hello.hello>]
    >>> d('#test').html()
    '<p class="hello" ...</p>...hello...python...'

Insert an element after another::

    >>> p.insertAfter(d('#test'))
    [<p#hello.hello>]
    >>> d('#test').html()
    '<a href="http://python.org">python</a> !...'

Or before::

    >>> p.insertBefore(d('#test'))
    [<p#hello.hello>]
    >>> d('body').html()
    '\n<p class="hello" id="hello" style="font-size: 17px">...'


Doing something for each elements::

    >>> p.each(lambda e: e.addClass('hello2'))
    [<p#hello.hello2.hello>]

And you can get back the modified html::

    >>> print d
    <html>
    ...style="font-size: 17px"...
    </html>

You can generate html stuff::

    >>> from pyquery import PyQuery as pq
    >>> print pq('<div>Yeah !</div>').addClass('myclass') + pq('<b>cool</b>')
    <div class="myclass">Yeah !</div><b>cool</b>

For more documentation about the API use the jquery website http://jquery.com/

You can run the doctests that you just read by running the test function or by
running "$ python pyquery.py" in the pyquery source folder.

The reference I'm using for the API now is ... the color cheat sheet
http://colorcharge.com/wp-content/uploads/2007/12/jquery12_colorcharge.png

To run the tests go into the pyquery folder and do::

    $ python test.py

- SELECTORS: it works fine but missing all the :xxx (:first, :last, ...) can be
  done by patching lxml.cssselect
- ATTRIBUTES: done
- CSS: done
- HTML: done
- MANIPULATING: TODO (this is the priority very useful)
- TRAVERSING: TODO (may prove troublesome)
- EVENTS: nothing to do with server side might be used later for automatic ajax
- CORE UI EFFECTS: did hide and show the rest doesn't really makes sense on
  server side
- AJAX: don't make sense on server side
