Scraping
=========

..
  >>> from pyquery.ajax import PyQuery as pq

PyQuery is able to load an html document from a url::

  >>> pq(your_url)
  [<html>]

By default it uses python's urllib.

If `requests`_ is installed then it will use it. This allow you to use most of `requests`_ parameters::

  >>> pq(your_url, headers={'user-agent': 'pyquery'})
  [<html>]

  >>> pq(your_url, {'q': 'foo'}, method='post', verify=True)
  [<html>]

.. _requests: http://docs.python-requests.org/en/latest/
