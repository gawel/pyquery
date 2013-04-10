=============================================
:mod:`pyquery.ajax` -- PyQuery AJAX extension
=============================================

.. automodule:: pyquery.ajax


.. fake imports

    >>> from pyquery.ajax import PyQuery as pq

You can query some wsgi app if `WebOb`_ is installed (it's not a pyquery
dependencie). IN this example the test app returns a simple input at `/` and a
submit button at `/submit`::

    >>> d = pq('<form></form>', app=input_app)
    >>> d.append(d.get('/'))
    [<form>]
    >>> print(d)
    <form><input name="youyou" type="text" value=""/></form>

The app is also available in new nodes::

    >>> d.get('/').app is d.app is d('form').app
    True

You can also request another path::

    >>> d.append(d.get('/submit'))
    [<form>]
    >>> print(d)
    <form><input name="youyou" type="text" value=""/><input type="submit" value="OK"/></form>

If `restkit`_ is installed, you are able to get url directly with a `HostProxy`_ app::

    >>> a = d.get(your_url)
    >>> a
    [<html>]

You can retrieve the app response::

    >>> print(a.response.status)
    200 OK

The response attribute is a `WebOb`_ `Response`_

.. _webob: http://pythonpaste.org/webob/
.. _response: http://pythonpaste.org/webob/#response
.. _restkit: http://benoitc.github.com/restkit/
.. _hostproxy: http://benoitc.github.com/restkit/wsgi_proxy.html

Api
---

.. autoclass:: PyQuery
   :members:

