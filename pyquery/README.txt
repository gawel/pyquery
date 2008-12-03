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

You can use the PyQuery class to load an xml document from a string, from a
file or from an url::

    >>> from pyquery import PyQuery
    >>> d = PyQuery(html="<html></html>")
    >>> d = PyQuery(url='http://w3c.org/')
    >>> d = PyQuery(filename="pyquery/test.html")

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

And you can get back the modified html::

    >>> print d #doctest: +ELLIPSIS
    <html>
    ...style="font-size: 17px"...
    </html>

For more documentation about the API use the jquery website http://jquery.com/

You can run the doctests that you just read by running the test function or by
running "$ python pyquery.py" in the pyquery source folder.

The reference I'm using for the API now is ... the color cheat sheet
http://colorcharge.com/wp-content/uploads/2007/12/jquery12_colorcharge.png

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

