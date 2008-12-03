#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt

'''pyquery: a jquery-like library
====================================

pyquery allows you to make jquery queries on xml documents.
The API is as much as possible the similar to jquery. PyQuery use lxml for fast
xml and html manipulation.

This is not (or at least not yet) a library to produce or interact with
javascript code. I just liked the jquery API and I missed it in python so I
told myself 'Hey let's make jquery in python'. This is the result.

It can be used for many purposes, one idea that I might try in the future is to
use it for templating with pure http templates that you modify using pyquery.

You can use the PyQuery class to load an xml document from a string, from a
file or from an url.

    >>> d = PyQuery(html='<html></html>')
    >>> d = PyQuery(url='http://w3c.org/')
    >>> d = PyQuery(filename='test.html')

Now d is like the $ in jquery.

    >>> d('#hello')
    [<p#hello.hello>]
    >>> p = d('#hello')
    >>> p.html()
    'Hello world !'
    >>> p.html('you know <a href="http://python.org/">Python</a> rocks')
    [<p#hello.hello>]
    >>> p.html()
    'you know <a href="http://python.org/">Python</a> rocks'
    >>> p.text()
    'you know Python rocks'

You can play with the attributes

    >>> p.attr('id')
    'hello'
    >>> p.attr('id', 'plop')
    [<p#plop.hello>]
    >>> p.attr('id', 'hello')
    [<p#hello.hello>]

And the class

    >>> p.addClass('toto')
    [<p#hello.toto.hello>]
    >>> p.toggleClass('titi toto')
    [<p#hello.titi.hello>]
    >>> p.removeClass('titi')
    [<p#hello.hello>]

Or the style

    >>> p.css('font-size', '15px')
    [<p#hello.hello>]
    >>> p.attr('style')
    'font-size: 15px'
    >>> p.css({'font-size': '17px'})
    [<p#hello.hello>]
    >>> p.attr('style')
    'font-size: 17px'

You can also add content to the end of tags

    >>> d('p').append('check out <a href="http://reddit.com/r/python"><span>reddit</span></a>')
    [<p#hello.hello>, <p#test>]
    >>> print d
    <html>
    ...
    <p class="hello" id="hello" style="font-size: 17px">you know <a href="http://python.org/">Python</a> rockscheck out <a href="http://reddit.com/r/python"><span>reddit</span></a></p><p id="test">
    hello <a href="http://python.org">python</a> !
    check out <a href="http://python.org/">Python</a> rockscheck out <a href="http://reddit.com/r/python"><span>reddit</span></a></p>
    ...


Or to the beginning

    >>> p.prepend('check out <a href="http://reddit.com/r/python">reddit</a>')
    [<p#hello.hello>]
    >>> p.html()
    'check out <a href="http://reddit.com/r/python">reddit</a>you know ...'

Prepend or append an element into an other

    >>> p.prependTo(d('#test'))
    [<p#hello.hello>]
    >>> d('#test').html()
    '<p class="hello" ...</p>...hello...python...'


And you can get back the modified html

    >>> print d
    <html>
    ...style="font-size: 17px"...
    </html>

For more documentation about the API use the jquery website http://jquery.com/

You can run the doctests that you just read by running the test function or by
running '$ python pyquery.py' in the pyquery source folder.

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
'''

from lxml.cssselect import css_to_xpath
from lxml import etree
from copy import deepcopy

def selector_to_xpath(selector):
    '''JQuery selector to xpath.
    TODO: patch cssselect to add :first, :last, ...
    '''
    selector = selector.replace('[@', '[')
    return css_to_xpath(selector)


class PyQuery(object):
    '''See the pyquery module docstring.
    '''
    def __init__(self, html=None, filename=None, url=None):
        if html:
            pass
        elif filename:
            html = file(filename).read()
        elif url:
            from urllib2 import urlopen
            html = urlopen(url).read()
        self.root = etree.fromstring(html)

    def __call__(self, selector='', context=None):
        if context == None:
            context = PyQueryResults([self.root])
        if not selector:
            return context
        results = PyQueryResults()
        xpath = selector_to_xpath(selector)
        results = [tag.xpath(xpath) for tag in context]

        # Flatten the results
        result = []
        for r in results:
            result.extend(r)
        return PyQueryResults(result)

    def __str__(self):
        return etree.tostring(self.root)


class PyQueryResults(list):
    '''Class returned when calling an instance of PyQuery.

    See the pyquery module docstring for more details.
    '''
    def __repr__(self):
        r = []
        for el in self:
            c = el.get('class')
            c = c and '.' + '.'.join(c.split(' ')) or ''
            id = el.get('id')
            id = id and '#' + id or ''
            r.append('<%s%s%s>' % (el.tag, id, c))
        return '[' + (', '.join(r)) + ']'

    ##############
    # Attributes #
    ##############
    def attr(self, name, value=None):
        if not self:
            return None
        if value == None:
            return self[0].get(name)
        elif value == '':
            return self.removeAttr(name)
        elif type(name) == dict:
            for tag in self:
                for key, value in name.items():
                    tag.set(key, value)
        else:
            for tag in self:
                tag.set(name, value)
        return self

    def removeAttr(self, name):
        for tag in self:
            del tag.attrib[name]
        return self

    #######
    # CSS #
    #######
    def height(self, value=None):
        return self.attr('height', value)

    def width(self, value=None):
        return self.attr('width', value)

    def addClass(self, value):
        for tag in self:
            values = value.split(' ')
            classes = set((tag.get('class') or '').split())
            classes = classes.union(values)
            classes.difference_update([''])
            tag.set('class', ' '.join(classes))
        return self

    def removeClass(self, value):
        for tag in self:
            values = value.split(' ')
            classes = set((tag.get('class') or '').split())
            classes.difference_update(values)
            classes.difference_update([''])
            tag.set('class', ' '.join(classes))
        return self

    def toggleClass(self, value):
        for tag in self:
            values = set(value.split(' '))
            classes = set((tag.get('class') or '').split())
            values_to_add = values.difference(classes)
            classes.difference_update(values)
            classes = classes.union(values_to_add)
            classes.difference_update([''])
            tag.set('class', ' '.join(classes))
        return self

    def css(self, attr, value=None):
        if type(attr) == dict:
            for tag in self:
                stripped_keys = [key.strip() for key in attr.keys()]
                current = [el.strip()
                           for el in (tag.get('style') or '').split(';')
                           if el.strip()
                           and not el.split(':')[0].strip() in stripped_keys]
                for key, value in attr.items():
                    current.append('%s: %s' % (key, value))
                tag.set('style', '; '.join(current))
        else:
            for tag in self:
                current = [el.strip()
                           for el in (tag.get('style') or '').split(';')
                           if el.strip()
                              and not el.split(':')[0].strip() == attr.strip()]
                current.append('%s: %s' % (attr, value))
                tag.set('style', '; '.join(current))
        return self

    ###################
    # CORE UI EFFECTS #
    ###################
    def hide(self):
        return self.css('display', 'none')

    def show(self):
        return self.css('display', 'block')

    ########
    # HTML #
    ########
    def val(self, value=None):
        return self.attr('value', value)

    def html(self, value=None):
        if value == None:
            if not self:
                return None
            tag = self[0]
            children = tag.getchildren()
            if not children:
                return tag.text
            html = tag.text or ''
            html += ''.join(map(etree.tostring, children))
            return html

        for tag in self:
            for child in tag.getchildren():
                tag.remove(child)
            root = etree.fromstring('<root>' + value + '</root>')
            children = root.getchildren()
            if children:
                tag.extend(children)
            tag.text = root.text
            tag.tail = root.tail
        return self

    def text(self, value=None):
        def get_text(tag):
            text = []
            if tag.text:
                text.append(tag.text)
            for child in tag.getchildren():
                text.extend(get_text(child))
            if tag.tail:
                text.append(tag.tail)
            return text

        if value == None:
            if not self:
                return None
            return ' '.join([''.join(get_text(tag)).strip() for tag in self])

        for tag in self:
            for child in tag.getchildren():
                tag.remove(child)
            tag.text = value
        return self

    ################
    # Manipulating #
    ################

    def append(self, value):
        is_pyquery_results = isinstance(value, PyQueryResults)
        is_string = isinstance(value, basestring)
        assert is_string or is_pyquery_results
        if is_string:
            root = etree.fromstring('<root>' + value + '</root>')
        elif is_pyquery_results:
            root = value
        if hasattr(root, 'text') and isinstance(root.text, basestring):
            root_text = root.text
        else:
            root_text = ''
        for i, tag in enumerate(self):
            if len(tag) > 0: # if the tag has children
                last_child = tag[-1]
                if not last_child.tail:
                    last_child.tail = ''
                last_child.tail += root_text
            else:
                if not tag.text:
                    tag.text = ''
                tag.text += root_text
            if i > 0:
                root = deepcopy(list(root))
            tag.extend(root)
            root = tag[-len(root):]

        return self

    def appendTo(self, value):
        value.append(self)
        return self

    def prepend(self, value):
        is_pyquery_results = isinstance(value, PyQueryResults)
        if isinstance(value, basestring):
            root = etree.fromstring('<root>' + value + '</root>')
        elif is_pyquery_results:
            root = value
        if hasattr(root, 'text') and isinstance(root.text, basestring):
            root_text = root.text
        else:
            root_text = ''
        for i, tag in enumerate(self):
            if not tag.text:
                tag.text = ''
            if len(root) > 0:
                root[-1].tail = tag.text
                tag.text = root_text
            else:
                tag.text = root_text + tag.text
            if i > 0:
                root = deepcopy(list(root))
            tag[:0] = root
            root = tag[:len(root)]

        return self

    def prependTo(self, value):
        value.prepend(self)
        return self

def test():
    import doctest
    print '%s fails out of %s' % doctest.testmod(optionflags=doctest.ELLIPSIS)

if __name__ == '__main__':
    test()
