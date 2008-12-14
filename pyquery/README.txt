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

.. contents::

Usage
-----

You can use the PyQuery class to load an xml document from a string, a lxml
document, from a file or from an url::

    >>> from pyquery import PyQuery
    >>> from lxml import etree
    >>> d = PyQuery("<html></html>")
    >>> d = PyQuery(etree.fromstring("<html></html>"))
    >>> d = PyQuery(url='http://google.com/')
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

You can use some of the pseudo classes that are available in jQuery but that
are not standard in css such as :first :last :even :odd :eq :lt :gt::

    >>> d('p:first')


Attributes
----------

You can play with the attributes with the jquery API::

    >>> p.attr("id")
    'hello'
    >>> p.attr("id", "plop")
    [<p#plop.hello>]
    >>> p.attr("id", "hello")
    [<p#hello.hello>]


Or in a more pythonic way::

    >>> p.attr.id = "plop"
    >>> p.attr.id
    'plop'
    >>> p.attr["id"] = "ola"
    >>> p.attr["id"]
    'ola'
    >>> p.attr(id='hello', class_='hello2')
    [<p#hello.hello2>]
    >>> p.attr.class_
    'hello2'
    >>> p.attr.class_ = 'hello'

CSS
---

You can also play with css classes::

    >>> p.addClass("toto")
    [<p#hello.toto.hello>]
    >>> p.toggleClass("titi toto")
    [<p#hello.titi.hello>]
    >>> p.removeClass("titi")
    [<p#hello.hello>]

Or the css style::

    >>> p.css("font-size", "15px")
    [<p#hello.hello>]
    >>> p.attr("style")
    'font-size: 15px'
    >>> p.css({"font-size": "17px"})
    [<p#hello.hello>]
    >>> p.attr("style")
    'font-size: 17px'

Same thing the pythonic way ('_' characters are translated to '-')::

    >>> p.css.font_size = "16px"
    >>> p.attr.style
    'font-size: 16px'
    >>> p.css['font-size'] = "15px"
    >>> p.attr.style
    'font-size: 15px'
    >>> p.css(font_size="16px")
    [<p#hello.hello>]
    >>> p.attr.style
    'font-size: 16px'
    >>> p.css = {"font-size": "17px"}
    >>> p.attr.style
    'font-size: 17px'

Traversing
----------

Some jQuery traversal methods are supported.  For instance, you can filter the selection list
using a string selector::

    >>> d('p').filter('.hello')
    [<p#hello.hello>]

Filtering can also be done using a function::

    >>> d('p').filter(lambda i: i == 1)
    [<p#test>]

Filtering functions can refer to the current element as 'this', like in jQuery::

    >>> d('p').filter(lambda i: PyQuery(this).text() == 'you know Python rocks')
    [<p#hello.hello>]

The opposite of filter is `not_` - it returns the items that don't match the selector::

    >>> d('p').not_('.hello')
    [<p#test>]

You can map a callable onto a PyQuery and get a mutated result. The result can
contain any items, not just elements::

    >>> d('p').map(lambda i, e: PyQuery(e).text())
    ['you know Python rocks', 'hello python !']

Like the filter method, map callbacks can reference the current item as this::

    >>> d('p').map(lambda i, e: len(PyQuery(this).text()))
    [21, 14]

The map callback can also return a list, which will extend the resulting
PyQuery::

    >>> d('p').map(lambda i, e: PyQuery(this).text().split())
    ['you', 'know', 'Python', 'rocks', 'hello', 'python', '!']

It is possible to select a single element with eq::

    >>> d('p').eq(0)
    [<p#hello.hello>]

The `is_` method lets you query if any current elements match the selector::

    >>> d('p').eq(0).is_('.hello')
    True
    >>> d('p').eq(1).is_('.hello')
    False

hasClass allows for checking for the presence of a class by name::

    >>> d('p').eq(0).hasClass('hello')
    True
    >>> d('p').eq(1).hasClass('hello')
    False

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

Manipulating
------------

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

Remove an element::

    >>> d.remove('p#id')
    [<html>]
    >>> d('p#id')
    []

Replace an element by another::

    >>> p.replaceWith('<p>testing</p>')
    [<p#hello.hello2.hello>]
    >>> d('p')
    [<p>, <p#test>]

Or the other way around::

    >>> d('<h1>arya stark</h1>').replaceAll('p')
    [<h1>]
    >>> d('p')
    []
    >>> d('h1')
    [<h1>, <h1>]

Remove what's inside the selection::

    >>> d('h1').empty()
    [<h1>, <h1>]

And you can get back the modified html::

    >>> print d
    <html>
    <body>
    <h1/><h1/></body>
    </html>

You can generate html stuff::

    >>> from pyquery import PyQuery as pq
    >>> print pq('<div>Yeah !</div>').addClass('myclass') + pq('<b>cool</b>')
    <div class="myclass">Yeah !</div><b>cool</b>


AJAX
----

.. fake imports

    >>> from ajax import PyQuery as pq

You can query some wsgi app if `WebOb`_ is installed (it's not a pyquery
dependencie). IN this example the test app returns a simple input at `/` and a
submit button at `/submit`::

    >>> d = pq('<form></form>', app=input_app)
    >>> d.append(d.get('/'))
    [<form>]
    >>> print d
    <form><input name="youyou" type="text" value=""/></form>

The app is also available in new nodes::

    >>> d.get('/').app is d.app is d('form').app
    True

You can also request another path::

    >>> d.append(d.get('/submit'))
    [<form>]
    >>> print d
    <form><input name="youyou" type="text" value=""/><input type="submit" value="OK"/></form>

If `Paste`_ is installed, you are able to get url directly with a `Proxy`_ app::

    >>> a = d.get('https://bitbucket.org/olauzanne/pyquery/')
    >>> a
    [<html>]

You can retrieve the app response::

    >>> print a.response.status
    301 Moved Permanently

The response attribute is a `WebOb`_ `Response`_

.. _webob: http://pythonpaste.org/webob/
.. _response: http://pythonpaste.org/webob/#response
.. _paste: http://pythonpaste.org/
.. _proxy: http://pythonpaste.org/modules/proxy.html#paste.proxy.Proxy

Testing
-------

If you want to run the tests that you can see above you should do::

    $ hg clone https://bitbucket.org/olauzanne/pyquery/
    $ cd pyquery
    $ python bootstrap.py
    $ bin/buildout
    $ bin/test

If you don't already have lxml installed use this line::

    $ STATIC_DEPS=true bin/buildout

Other documentations
--------------------

For more documentation about the API use the jquery website http://docs.jquery.com/

The reference I'm now using for the API is ... the color cheat sheet
http://colorcharge.com/wp-content/uploads/2007/12/jquery12_colorcharge.png

TODO
----

- SELECTORS: it works fine but missing all the :xxx (:first, :last, ...) can be
  done by patching lxml.cssselect
- ATTRIBUTES: done
- CSS: done
- HTML: done
- MANIPULATING: did all but the "wrap" methods
- TRAVERSING: did a few
- EVENTS: nothing to do with server side might be used later for automatic ajax
- CORE UI EFFECTS: did hide and show the rest doesn't really makes sense on
  server side
- AJAX: some with wsgi app
