Attributes
----------

..
    >>> from pyquery import PyQuery as pq

Using attribute to select specific tag
In attribute selectors, the value should be a valid CSS identifier or quoted as string::

    >>> d = pq("<option value='1'><option value='2'>")
    >>> d('option[value="1"]')
    [<option>]


You can play with the attributes with the jquery API::

    >>> p = pq('<p id="hello" class="hello"></p>')('p')
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


XML namespaces
~~~~~~~~~~~~~~

Parse namespaced documents as XML and pass a prefix-to-URI mapping through
``namespaces``. CSS selectors use ``prefix|name`` for namespaced elements and
attributes::

    >>> xml = '''<feed xmlns="urn:feed" xmlns:meta="urn:meta">
    ...   <entry meta:id="first"/>
    ... </feed>'''
    >>> d = pq(xml, parser='xml',
    ...        namespaces={'f': 'urn:feed', 'm': 'urn:meta'})
    >>> entry = d('f|entry[m|id="first"]')
    >>> len(entry)
    1

The prefixes in this mapping are selector aliases: they do not need to match
the prefixes in the source XML. A default XML namespace also needs an alias
when selecting its elements this way.

``attr()`` uses lxml's expanded names, ``{namespace-uri}local-name``, rather
than CSS selector syntax. Unprefixed XML attributes have no namespace::

    >>> entry.attr('{urn:meta}id')
    'first'
    >>> _ = entry.attr('{urn:meta}id', 'second')
    >>> entry.attr('{urn:meta}id')
    'second'
    >>> _ = entry.attr('id', 'plain')
    >>> entry.attr('id')
    'plain'
    >>> _ = entry.remove_attr('{urn:meta}id')
    >>> entry.attr('{urn:meta}id') is None
    True
