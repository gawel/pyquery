Scraping
=========

..
  >>> from pyquery import PyQuery as pq

PyQuery is able to load an html document from a url::

  >>> pq(your_url)
  [<html>]

By default it uses python's urllib.

If `requests`_ is installed then it will use it. This allow you to use most of `requests`_ parameters::

  >>> pq(your_url, headers={'user-agent': 'pyquery'})
  [<html>]

  >>> pq(your_url, {'q': 'foo'}, method='post', verify=True)
  [<html>]


Timeout
-------

The default timeout is 60 seconds, you can change it by setting the timeout parameter which is forwarded to the underlying urllib or requests library.

Session
-------

When using the requests library you can instantiate a Session object which keeps state between http calls (for example - to keep cookies). You can set the session parameter to use this session object.

.. _requests: http://docs.python-requests.org/en/latest/
