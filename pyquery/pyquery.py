# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt
from .cssselectpatch import JQueryTranslator
from reprlib import recursive_repr
from urllib.parse import urlencode
from urllib.parse import urljoin
from .openers import url_opener
from .text import extract_text
from copy import deepcopy
from html import escape
from lxml import etree
import lxml.html
import inspect
import itertools
import types
import sys

if sys.version_info >= (3, 12, 0):
    from collections import OrderedDict
else:
    # backward compat. to be able to run doctest with 3.7+. see:
    # https://github.com/gawel/pyquery/issues/249
    # and:
    # https://github.com/python/cpython/blob/3.12/Lib/collections/__init__.py#L272
    from collections import OrderedDict as BaseOrderedDict

    class OrderedDict(BaseOrderedDict):
        @recursive_repr()
        def __repr__(self):
            'od.__repr__() <==> repr(od)'
            if not self:
                return '%s()' % (self.__class__.__name__,)
            return '%s(%r)' % (self.__class__.__name__, dict(self.items()))

basestring = (str, bytes)


def getargspec(func):
    args = inspect.signature(func).parameters.values()
    return [p.name for p in args
            if p.kind == p.POSITIONAL_OR_KEYWORD]


def with_camel_case_alias(func):
    """decorator for methods who required a camelcase alias"""
    _camel_case_aliases.add(func.__name__)
    return func


_camel_case_aliases = set()


def build_camel_case_aliases(PyQuery):
    """add camelcase aliases to PyQuery"""
    for alias in _camel_case_aliases:
        parts = list(alias.split('_'))
        name = parts[0] + ''.join([p.title() for p in parts[1:]])
        func = getattr(PyQuery, alias)
        f = types.FunctionType(func.__code__, func.__globals__,
                               name, func.__defaults__)
        f.__doc__ = (
            'Alias for :func:`~pyquery.pyquery.PyQuery.%s`') % func.__name__
        setattr(PyQuery, name, f.__get__(None, PyQuery))


def fromstring(context, parser=None, custom_parser=None):
    """use html parser if we don't have clean xml
    """
    if hasattr(context, 'read') and hasattr(context.read, '__call__'):
        meth = 'parse'
    else:
        meth = 'fromstring'
    if custom_parser is None:
        if parser is None:
            try:
                result = getattr(etree, meth)(context)
            except etree.XMLSyntaxError:
                if hasattr(context, 'seek'):
                    context.seek(0)
                result = getattr(lxml.html, meth)(context)
            if isinstance(result, etree._ElementTree):
                return [result.getroot()]
            else:
                return [result]
        elif parser == 'xml':
            custom_parser = getattr(etree, meth)
        elif parser == 'html':
            custom_parser = getattr(lxml.html, meth)
        elif parser == 'html5':
            from lxml.html import html5parser
            custom_parser = getattr(html5parser, meth)
        elif parser == 'soup':
            from lxml.html import soupparser
            custom_parser = getattr(soupparser, meth)
        elif parser == 'html_fragments':
            custom_parser = lxml.html.fragments_fromstring
        else:
            raise ValueError('No such parser: "%s"' % parser)

    result = custom_parser(context)
    if isinstance(result, list):
        return result
    elif isinstance(result, etree._ElementTree):
        return [result.getroot()]
    elif result is not None:
        return [result]
    else:
        return []


def callback(func, *args):
    return func(*args[:func.__code__.co_argcount])


class NoDefault(object):
    def __repr__(self):
        """clean representation in Sphinx"""
        return '<NoDefault>'


no_default = NoDefault()
del NoDefault


class FlexibleElement(object):
    """property to allow a flexible api"""
    def __init__(self, pget, pset=no_default, pdel=no_default):
        self.pget = pget
        self.pset = pset
        self.pdel = pdel

    def __get__(self, instance, klass):
        class _element(object):
            """real element to support set/get/del attr and item and js call
            style"""
            def __call__(prop, *args, **kwargs):
                return self.pget(instance, *args, **kwargs)
            __getattr__ = __getitem__ = __setattr__ = __setitem__ = __call__

            def __delitem__(prop, name):
                if self.pdel is not no_default:
                    return self.pdel(instance, name)
                else:
                    raise NotImplementedError()
            __delattr__ = __delitem__

            def __repr__(prop):
                return '<flexible_element %s>' % self.pget.__name__
        return _element()

    def __set__(self, instance, value):
        if self.pset is not no_default:
            self.pset(instance, value)
        else:
            raise NotImplementedError()


class PyQuery(list):
    """The main class
    """

    _translator_class = JQueryTranslator

    def __init__(self, *args, **kwargs):
        html = None
        elements = []
        self._base_url = None
        self.parser = kwargs.pop('parser', None)

        if 'parent' in kwargs:
            self._parent = kwargs.pop('parent')
        else:
            self._parent = no_default

        if 'css_translator' in kwargs:
            self._translator = kwargs.pop('css_translator')
        elif self.parser in ('xml',):
            self._translator = self._translator_class(xhtml=True)
        elif self._parent is not no_default:
            self._translator = self._parent._translator
        else:
            self._translator = self._translator_class(xhtml=False)

        self.namespaces = kwargs.pop('namespaces', None)

        if kwargs:
            # specific case to get the dom
            if 'filename' in kwargs:
                html = open(kwargs['filename'],
                            encoding=kwargs.get('encoding'))
            elif 'url' in kwargs:
                url = kwargs.pop('url')
                if 'opener' in kwargs:
                    opener = kwargs.pop('opener')
                    html = opener(url, **kwargs)
                else:
                    html = url_opener(url, kwargs)
                if not self.parser:
                    self.parser = 'html'
                self._base_url = url
            else:
                raise ValueError('Invalid keyword arguments %s' % kwargs)

            elements = fromstring(html, self.parser)
            # close open descriptor if possible
            if hasattr(html, 'close'):
                try:
                    html.close()
                except Exception:
                    pass

        else:
            # get nodes

            # determine context and selector if any
            selector = context = no_default
            length = len(args)
            if length == 1:
                context = args[0]
            elif length == 2:
                selector, context = args
            else:
                raise ValueError(
                    "You can't do that. Please, provide arguments")

            # get context
            if isinstance(context, basestring):
                try:
                    elements = fromstring(context, self.parser)
                except Exception:
                    raise
            elif isinstance(context, self.__class__):
                # copy
                elements = context[:]
            elif isinstance(context, list):
                elements = context
            elif isinstance(context, etree._Element):
                elements = [context]
            else:
                raise TypeError(context)

            # select nodes
            if elements and selector is not no_default:
                xpath = self._css_to_xpath(selector)
                results = []
                for tag in elements:
                    results.extend(
                        tag.xpath(xpath, namespaces=self.namespaces))
                elements = results

        list.__init__(self, elements)

    def _css_to_xpath(self, selector, prefix='descendant-or-self::'):
        selector = selector.replace('[@', '[')
        return self._translator.css_to_xpath(selector, prefix)

    def _copy(self, *args, **kwargs):
        kwargs.setdefault('namespaces', self.namespaces)
        return self.__class__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """return a new PyQuery instance
        """
        length = len(args)
        if length == 0:
            raise ValueError('You must provide at least a selector')
        if args[0] == '':
            return self._copy([])
        if (len(args) == 1 and
                isinstance(args[0], str) and
                not args[0].startswith('<')):
            args += (self,)
        result = self._copy(*args, parent=self, **kwargs)
        return result

    # keep original list api prefixed with _
    _append = list.append
    _extend = list.extend

    # improve pythonic api
    def __add__(self, other):
        assert isinstance(other, self.__class__)
        return self._copy(self[:] + other[:])

    def extend(self, other):
        """Extend with another PyQuery object"""
        assert isinstance(other, self.__class__)
        self._extend(other[:])
        return self

    def items(self, selector=None):
        """Iter over elements. Return PyQuery objects:

            >>> d = PyQuery('<div><span>foo</span><span>bar</span></div>')
            >>> [i.text() for i in d.items('span')]
            ['foo', 'bar']
            >>> [i.text() for i in d('span').items()]
            ['foo', 'bar']
            >>> list(d.items('a')) == list(d('a').items())
            True
        """
        if selector:
            elems = self(selector) or []
        else:
            elems = self
        for elem in elems:
            yield self._copy(elem, parent=self)

    def xhtml_to_html(self):
        """Remove xhtml namespace:

            >>> doc = PyQuery(
            ...         '<html xmlns="http://www.w3.org/1999/xhtml"></html>')
            >>> doc
            [<{http://www.w3.org/1999/xhtml}html>]
            >>> doc.xhtml_to_html()
            [<html>]
        """
        try:
            root = self[0].getroottree()
        except IndexError:
            pass
        else:
            lxml.html.xhtml_to_html(root)
        return self

    def remove_namespaces(self):
        """Remove all namespaces:

            >>> doc = PyQuery('<foo xmlns="http://example.com/foo"></foo>')
            >>> doc
            [<{http://example.com/foo}foo>]
            >>> doc.remove_namespaces()
            [<foo>]
        """
        try:
            root = self[0].getroottree()
        except IndexError:
            pass
        else:
            for el in root.iter('{*}*'):
                if el.tag.startswith('{'):
                    el.tag = el.tag.split('}', 1)[1]
        return self

    def __str__(self):
        """xml representation of current nodes::

            >>> xml = PyQuery(
            ...   '<script><![[CDATA[ ]></script>', parser='html_fragments')
            >>> print(str(xml))
            <script>&lt;![[CDATA[ ]&gt;</script>

        """
        return ''.join([etree.tostring(e, encoding=str) for e in self])

    def __unicode__(self):
        """xml representation of current nodes"""
        return u''.join([etree.tostring(e, encoding=str)
                         for e in self])

    def __html__(self):
        """html representation of current nodes::

            >>> html = PyQuery(
            ...   '<script><![[CDATA[ ]></script>', parser='html_fragments')
            >>> print(html.__html__())
            <script><![[CDATA[ ]></script>

        """
        return u''.join([lxml.html.tostring(e, encoding=str)
                         for e in self])

    def __repr__(self):
        r = []
        try:
            for el in self:
                c = el.get('class')
                c = c and '.' + '.'.join(c.split(' ')) or ''
                id = el.get('id')
                id = id and '#' + id or ''
                r.append('<%s%s%s>' % (el.tag, id, c))
            return '[' + (', '.join(r)) + ']'
        except AttributeError:
            return list.__repr__(self)

    @property
    def root(self):
        """return the xml root element
        """
        if self._parent is not no_default:
            return self._parent[0].getroottree()
        return self[0].getroottree()

    @property
    def encoding(self):
        """return the xml encoding of the root element
        """
        root = self.root
        if root is not None:
            return self.root.docinfo.encoding

    ##############
    # Traversing #
    ##############

    def _filter_only(self, selector, elements, reverse=False, unique=False):
        """Filters the selection set only, as opposed to also including
           descendants.
        """
        if selector is None:
            results = elements
        else:
            xpath = self._css_to_xpath(selector, 'self::')
            results = []
            for tag in elements:
                results.extend(tag.xpath(xpath, namespaces=self.namespaces))
        if reverse:
            results.reverse()
        if unique:
            result_list = results
            results = []
            for item in result_list:
                if item not in results:
                    results.append(item)
        return self._copy(results, parent=self)

    def parent(self, selector=None):
        return self._filter_only(
            selector,
            [e.getparent() for e in self if e.getparent() is not None],
            unique=True)

    def prev(self, selector=None):
        return self._filter_only(
            selector,
            [e.getprevious() for e in self if e.getprevious() is not None])

    def next(self, selector=None):
        return self._filter_only(
            selector,
            [e.getnext() for e in self if e.getnext() is not None])

    def _traverse(self, method):
        for e in self:
            current = getattr(e, method)()
            while current is not None:
                yield current
                current = getattr(current, method)()

    def _traverse_parent_topdown(self):
        for e in self:
            this_list = []
            current = e.getparent()
            while current is not None:
                this_list.append(current)
                current = current.getparent()
            this_list.reverse()
            for j in this_list:
                yield j

    def _next_all(self):
        return [e for e in self._traverse('getnext')]

    @with_camel_case_alias
    def next_all(self, selector=None):
        """
        >>> h = '<span><p class="hello">Hi</p><p>Bye</p><img scr=""/></span>'
        >>> d = PyQuery(h)
        >>> d('p:last').next_all()
        [<img>]
        >>> d('p:last').nextAll()
        [<img>]
        """
        return self._filter_only(selector, self._next_all())

    @with_camel_case_alias
    def next_until(self, selector, filter_=None):
        """
        >>> h = '''
        ... <h2>Greeting 1</h2>
        ... <p>Hello!</p><p>World!</p>
        ... <h2>Greeting 2</h2><p>Bye!</p>
        ... '''
        >>> d = PyQuery(h)
        >>> d('h2:first').nextUntil('h2')
        [<p>, <p>]
        """
        return self._filter_only(
            filter_, [
                e
                for q in itertools.takewhile(
                    lambda q: not q.is_(selector), self.next_all().items())
                for e in q
            ]
        )

    def _prev_all(self):
        return [e for e in self._traverse('getprevious')]

    @with_camel_case_alias
    def prev_all(self, selector=None):
        """
        >>> h = '<span><p class="hello">Hi</p><p>Bye</p><img scr=""/></span>'
        >>> d = PyQuery(h)
        >>> d('p:last').prev_all()
        [<p.hello>]
        >>> d('p:last').prevAll()
        [<p.hello>]
        """
        return self._filter_only(selector, self._prev_all(), reverse=True)

    def siblings(self, selector=None):
        """
         >>> h = '<span><p class="hello">Hi</p><p>Bye</p><img scr=""/></span>'
         >>> d = PyQuery(h)
         >>> d('.hello').siblings()
         [<p>, <img>]
         >>> d('.hello').siblings('img')
         [<img>]

        """
        return self._filter_only(selector, self._prev_all() + self._next_all())

    def parents(self, selector=None):
        """
        >>> d = PyQuery('<span><p class="hello">Hi</p><p>Bye</p></span>')
        >>> d('p').parents()
        [<span>]
        >>> d('.hello').parents('span')
        [<span>]
        >>> d('.hello').parents('p')
        []
        """
        return self._filter_only(
            selector,
            [e for e in self._traverse_parent_topdown()],
            unique=True
        )

    def children(self, selector=None):
        """Filter elements that are direct children of self using optional
        selector:

            >>> d = PyQuery('<span><p class="hello">Hi</p><p>Bye</p></span>')
            >>> d
            [<span>]
            >>> d.children()
            [<p.hello>, <p>]
            >>> d.children('.hello')
            [<p.hello>]
        """
        elements = [child for tag in self for child in tag.getchildren()]
        return self._filter_only(selector, elements)

    def closest(self, selector=None):
        """
        >>> d = PyQuery(
        ...  '<div class="hello"><p>This is a '
        ...  '<strong class="hello">test</strong></p></div>')
        >>> d('strong').closest('div')
        [<div.hello>]
        >>> d('strong').closest('.hello')
        [<strong.hello>]
        >>> d('strong').closest('form')
        []
        """
        result = []
        for current in self:
            while (current is not None and
                    not self._copy(current).is_(selector)):
                current = current.getparent()
            if current is not None:
                result.append(current)
        return self._copy(result, parent=self)

    def contents(self):
        """
        Return contents (with text nodes):

            >>> d = PyQuery('hello <b>bold</b>')
            >>> d.contents()  # doctest: +ELLIPSIS
            ['hello ', <Element b at ...>]
        """
        results = []
        for elem in self:
            results.extend(elem.xpath('child::text()|child::*',
                           namespaces=self.namespaces))
        return self._copy(results, parent=self)

    def filter(self, selector):
        """Filter elements in self using selector (string or function):

            >>> d = PyQuery('<p class="hello">Hi</p><p>Bye</p>')
            >>> d('p')
            [<p.hello>, <p>]
            >>> d('p').filter('.hello')
            [<p.hello>]
            >>> d('p').filter(lambda i: i == 1)
            [<p>]
            >>> d('p').filter(lambda i: PyQuery(this).text() == 'Hi')
            [<p.hello>]
            >>> d('p').filter(lambda i, this: PyQuery(this).text() == 'Hi')
            [<p.hello>]
        """
        if not hasattr(selector, '__call__'):
            return self._filter_only(selector, self)
        else:
            elements = []
            args = getargspec(callback)
            try:
                for i, this in enumerate(self):
                    if len(args) == 1:
                        selector.__globals__['this'] = this
                    if callback(selector, i, this):
                        elements.append(this)
            finally:
                f_globals = selector.__globals__
                if 'this' in f_globals:
                    del f_globals['this']
            return self._copy(elements, parent=self)

    def not_(self, selector):
        """Return elements that don't match the given selector:

            >>> d = PyQuery('<p class="hello">Hi</p><p>Bye</p><div></div>')
            >>> d('p').not_('.hello')
            [<p>]
        """
        exclude = set(self._copy(selector, self))
        return self._copy([e for e in self if e not in exclude],
                          parent=self)

    def is_(self, selector):
        """Returns True if selector matches at least one current element, else
        False:

            >>> d = PyQuery('<p class="hello"><span>Hi</span></p><p>Bye</p>')
            >>> d('p').eq(0).is_('.hello')
            True

            >>> d('p').eq(0).is_('span')
            False

            >>> d('p').eq(1).is_('.hello')
            False

        ..
        """
        return bool(self._filter_only(selector, self))

    def find(self, selector):
        """Find elements using selector traversing down from self:

            >>> m = '<p><span><em>Whoah!</em></span></p><p><em> there</em></p>'
            >>> d = PyQuery(m)
            >>> d('p').find('em')
            [<em>, <em>]
            >>> d('p').eq(1).find('em')
            [<em>]
        """
        xpath = self._css_to_xpath(selector)
        results = [child.xpath(xpath, namespaces=self.namespaces)
                   for tag in self
                   for child in tag.getchildren()]
        # Flatten the results
        elements = []
        for r in results:
            elements.extend(r)
        return self._copy(elements, parent=self)

    def eq(self, index):
        """Return PyQuery of only the element with the provided index::

            >>> d = PyQuery('<p class="hello">Hi</p><p>Bye</p><div></div>')
            >>> d('p').eq(0)
            [<p.hello>]
            >>> d('p').eq(1)
            [<p>]
            >>> d('p').eq(2)
            []

        ..
        """
        # Slicing will return empty list when index=-1
        # we should handle out of bound by ourselves
        try:
            items = self[index]
        except IndexError:
            items = []
        return self._copy(items, parent=self)

    def each(self, func):
        """apply func on each nodes
        """
        try:
            for i, element in enumerate(self):
                func.__globals__['this'] = element
                if callback(func, i, element) is False:
                    break
        finally:
            f_globals = func.__globals__
            if 'this' in f_globals:
                del f_globals['this']
        return self

    def map(self, func):
        """Returns a new PyQuery after transforming current items with func.

        func should take two arguments - 'index' and 'element'.  Elements can
        also be referred to as 'this' inside of func::

            >>> d = PyQuery('<p class="hello">Hi there</p><p>Bye</p><br />')
            >>> d('p').map(lambda i, e: PyQuery(e).text())
            ['Hi there', 'Bye']

            >>> d('p').map(lambda i, e: len(PyQuery(this).text()))
            [8, 3]

            >>> d('p').map(lambda i, e: PyQuery(this).text().split())
            ['Hi', 'there', 'Bye']

        """
        items = []
        try:
            for i, element in enumerate(self):
                func.__globals__['this'] = element
                result = callback(func, i, element)
                if result is not None:
                    if not isinstance(result, list):
                        items.append(result)
                    else:
                        items.extend(result)
        finally:
            f_globals = func.__globals__
            if 'this' in f_globals:
                del f_globals['this']
        return self._copy(items, parent=self)

    @property
    def length(self):
        return len(self)

    def size(self):
        return len(self)

    def end(self):
        """Break out of a level of traversal and return to the parent level.

            >>> m = '<p><span><em>Whoah!</em></span></p><p><em> there</em></p>'
            >>> d = PyQuery(m)
            >>> d('p').eq(1).find('em').end().end()
            [<p>, <p>]
        """
        return self._parent

    ##############
    # Attributes #
    ##############
    def attr(self, *args, **kwargs):
        """Attributes manipulation
        """

        mapping = {'class_': 'class', 'for_': 'for'}

        attr = value = no_default
        length = len(args)
        if length == 1:
            attr = args[0]
            attr = mapping.get(attr, attr)
        elif length == 2:
            attr, value = args
            attr = mapping.get(attr, attr)
        elif kwargs:
            attr = {}
            for k, v in kwargs.items():
                attr[mapping.get(k, k)] = v
        else:
            raise ValueError('Invalid arguments %s %s' % (args, kwargs))

        if not self:
            return None
        elif isinstance(attr, dict):
            for tag in self:
                for key, value in attr.items():
                    tag.set(key, value)
        elif value is no_default:
            return self[0].get(attr)
        elif value is None:
            return self.remove_attr(attr)
        else:
            for tag in self:
                tag.set(attr, value)
        return self

    @with_camel_case_alias
    def remove_attr(self, name):
        """Remove an attribute::

            >>> d = PyQuery('<div id="myid"></div>')
            >>> d.remove_attr('id')
            [<div>]
            >>> d.removeAttr('id')
            [<div>]

        ..
        """
        for tag in self:
            try:
                del tag.attrib[name]
            except KeyError:
                pass
        return self

    attr = FlexibleElement(pget=attr, pdel=remove_attr)

    #######
    # CSS #
    #######
    def height(self, value=no_default):
        """set/get height of element
        """
        return self.attr('height', value)

    def width(self, value=no_default):
        """set/get width of element
        """
        return self.attr('width', value)

    @with_camel_case_alias
    def has_class(self, name):
        """Return True if element has class::

            >>> d = PyQuery('<div class="myclass"></div>')
            >>> d.has_class('myclass')
            True
            >>> d.hasClass('myclass')
            True

        ..
        """
        return self.is_('.%s' % name)

    @with_camel_case_alias
    def add_class(self, value):
        """Add a css class to elements::

            >>> d = PyQuery('<div></div>')
            >>> d.add_class('myclass')
            [<div.myclass>]
            >>> d.addClass('myclass')
            [<div.myclass>]

        ..
        """
        for tag in self:
            values = value.split(' ')
            classes = (tag.get('class') or '').split()
            classes += [v for v in values if v not in classes]
            tag.set('class', ' '.join(classes))
        return self

    @with_camel_case_alias
    def remove_class(self, value):
        """Remove a css class to elements::

            >>> d = PyQuery('<div class="myclass"></div>')
            >>> d.remove_class('myclass')
            [<div>]
            >>> d.removeClass('myclass')
            [<div>]

        ..
        """
        for tag in self:
            values = value.split(' ')
            classes = set((tag.get('class') or '').split())
            classes.difference_update(values)
            classes.difference_update([''])
            classes = ' '.join(classes)
            if classes.strip():
                tag.set('class', classes)
            elif tag.get('class'):
                tag.set('class', classes)
        return self

    @with_camel_case_alias
    def toggle_class(self, value):
        """Toggle a css class to elements

            >>> d = PyQuery('<div></div>')
            >>> d.toggle_class('myclass')
            [<div.myclass>]
            >>> d.toggleClass('myclass')
            [<div>]

        """
        for tag in self:
            values = value.split(' ')
            classes = (tag.get('class') or '').split()
            values_to_add = [v for v in values if v not in classes]
            values_to_del = [v for v in values if v in classes]
            classes = [v for v in classes if v not in values_to_del]
            classes += values_to_add
            tag.set('class', ' '.join(classes))
        return self

    def css(self, *args, **kwargs):
        """css attributes manipulation
        """

        attr = value = no_default
        length = len(args)
        if length == 1:
            attr = args[0]
        elif length == 2:
            attr, value = args
        elif kwargs:
            attr = kwargs
        else:
            raise ValueError('Invalid arguments %s %s' % (args, kwargs))

        if isinstance(attr, dict):
            for tag in self:
                stripped_keys = [key.strip().replace('_', '-')
                                 for key in attr.keys()]
                current = [el.strip()
                           for el in (tag.get('style') or '').split(';')
                           if el.strip()
                           and el.split(':')[0].strip() not in stripped_keys]
                for key, value in attr.items():
                    key = key.replace('_', '-')
                    current.append('%s: %s' % (key, value))
                tag.set('style', '; '.join(current))
        elif isinstance(value, basestring):
            attr = attr.replace('_', '-')
            for tag in self:
                current = [
                    el.strip()
                    for el in (tag.get('style') or '').split(';')
                    if (el.strip() and
                        not el.split(':')[0].strip() == attr.strip())]
                current.append('%s: %s' % (attr, value))
                tag.set('style', '; '.join(current))
        return self

    css = FlexibleElement(pget=css, pset=css)

    ###################
    # CORE UI EFFECTS #
    ###################
    def hide(self):
        """Add display:none to elements style:

            >>> print(PyQuery('<div style="display:none;"/>').hide())
            <div style="display: none"/>

        """
        return self.css('display', 'none')

    def show(self):
        """Add display:block to elements style:

            >>> print(PyQuery('<div />').show())
            <div style="display: block"/>

        """
        return self.css('display', 'block')

    ########
    # HTML #
    ########
    def val(self, value=no_default):
        """Set the attribute value::

            >>> d = PyQuery('<input />')
            >>> d.val('Youhou')
            [<input>]

        Get the attribute value::

            >>> d.val()
            'Youhou'

        Set the selected values for a `select` element with the `multiple`
        attribute::

            >>> d = PyQuery('''
            ...             <select multiple>
            ...                 <option value="you"><option value="hou">
            ...             </select>
            ...             ''')
            >>> d.val(['you', 'hou'])
            [<select>]

        Get the selected values for a `select` element with the `multiple`
        attribute::

            >>> d.val()
            ['you', 'hou']

        """
        def _get_value(tag):
            # <textarea>
            if tag.tag == 'textarea':
                return self._copy(tag).html()
            # <select>
            elif tag.tag == 'select':
                if 'multiple' in tag.attrib:
                    # Only extract value if selected
                    selected = self._copy(tag)('option[selected]')
                    # Rebuild list to avoid serialization error
                    return list(selected.map(
                        lambda _, o: self._copy(o).attr('value')
                    ))
                selected_option = self._copy(tag)('option[selected]:last')
                if selected_option:
                    return selected_option.attr('value')
                else:
                    return self._copy(tag)('option').attr('value')
            # <input type="checkbox"> or <input type="radio">
            elif self.is_(':checkbox,:radio'):
                val = self._copy(tag).attr('value')
                if val is None:
                    return 'on'
                else:
                    return val
            # <input>
            elif tag.tag == 'input':
                val = self._copy(tag).attr('value')
                return val.replace('\n', '') if val else ''
            # everything else.
            return self._copy(tag).attr('value') or ''

        def _set_value(pq, value):
            for tag in pq:
                # <select>
                if tag.tag == 'select':
                    if not isinstance(value, list):
                        value = [value]

                    def _make_option_selected(_, elem):
                        pq = self._copy(elem)
                        if pq.attr('value') in value:
                            pq.attr('selected', 'selected')
                            if 'multiple' not in tag.attrib:
                                del value[:]  # Ensure it toggles first match
                        else:
                            pq.removeAttr('selected')

                    self._copy(tag)('option').each(_make_option_selected)
                    continue
                # Stringify array
                if isinstance(value, list):
                    value = ','.join(value)
                # <textarea>
                if tag.tag == 'textarea':
                    self._copy(tag).text(value)
                    continue
                # <input> and everything else.
                self._copy(tag).attr('value', value)

        if value is no_default:
            if len(self):
                return _get_value(self[0])
        else:
            _set_value(self, value)
            return self

    def html(self, value=no_default, **kwargs):
        """Get or set the html representation of sub nodes.

        Get the text value::

            >>> d = PyQuery('<div><span>toto</span></div>')
            >>> print(d.html())
            <span>toto</span>

        Extra args are passed to ``lxml.etree.tostring``::

            >>> d = PyQuery('<div><span></span></div>')
            >>> print(d.html())
            <span/>
            >>> print(d.html(method='html'))
            <span></span>

        Set the text value::

            >>> d.html('<span>Youhou !</span>')
            [<div>]
            >>> print(d)
            <div><span>Youhou !</span></div>
        """
        if value is no_default:
            if not self:
                return None
            tag = self[0]
            children = tag.getchildren()
            html = escape(tag.text or '', quote=False)
            if not children:
                return html
            if 'encoding' not in kwargs:
                kwargs['encoding'] = str
            html += u''.join([etree.tostring(e, **kwargs)
                              for e in children])
            return html
        else:
            if isinstance(value, self.__class__):
                new_html = str(value)
            elif isinstance(value, basestring):
                new_html = value
            elif not value:
                new_html = ''
            else:
                raise ValueError(type(value))

            for tag in self:
                for child in tag.getchildren():
                    tag.remove(child)
                root = fromstring(
                    u'<root>' + new_html + u'</root>',
                    self.parser)[0]
                children = root.getchildren()
                if children:
                    tag.extend(children)
                tag.text = root.text
        return self

    @with_camel_case_alias
    def outer_html(self, method="html"):
        """Get the html representation of the first selected element::

            >>> d = PyQuery('<div><span class="red">toto</span> rocks</div>')
            >>> print(d('span'))
            <span class="red">toto</span> rocks
            >>> print(d('span').outer_html())
            <span class="red">toto</span>
            >>> print(d('span').outerHtml())
            <span class="red">toto</span>

            >>> S = PyQuery('<p>Only <b>me</b> & myself</p>')
            >>> print(S('b').outer_html())
            <b>me</b>

        ..
        """

        if not self:
            return None
        e0 = self[0]
        if e0.tail:
            e0 = deepcopy(e0)
            e0.tail = ''
        return etree.tostring(e0, encoding=str, method=method)

    def text(self, value=no_default, **kwargs):
        """Get or set the text representation of sub nodes.

        Get the text value::

            >>> doc = PyQuery('<div><span>toto</span><span>tata</span></div>')
            >>> print(doc.text())
            tototata
            >>> doc = PyQuery('''<div><span>toto</span>
            ...               <span>tata</span></div>''')
            >>> print(doc.text())
            toto tata

        Get the text value, without squashing newlines::

            >>> doc = PyQuery('''<div><span>toto</span>
            ...               <span>tata</span></div>''')
            >>> print(doc.text(squash_space=False))
            toto
            tata

        Set the text value::

            >>> doc.text('Youhou !')
            [<div>]
            >>> print(doc)
            <div>Youhou !</div>

        """

        if value is no_default:
            if not self:
                return ''
            return ' '.join(
                self._copy(tag).html() if tag.tag == 'textarea' else
                extract_text(tag, **kwargs) for tag in self
            )

        for tag in self:
            for child in tag.getchildren():
                tag.remove(child)
            tag.text = value
        return self

    ################
    # Manipulating #
    ################

    def _get_root(self, value):
        if isinstance(value, basestring):
            root = fromstring(u'<root>' + value + u'</root>',
                              self.parser)[0]
        elif isinstance(value, etree._Element):
            root = self._copy(value)
        elif isinstance(value, PyQuery):
            root = value
        else:
            raise TypeError(
                'Value must be string, PyQuery or Element. Got %r' % value)
        if hasattr(root, 'text') and isinstance(root.text, basestring):
            root_text = root.text
        else:
            root_text = ''
        return root, root_text

    def append(self, value):
        """append value to each nodes
        """
        root, root_text = self._get_root(value)
        for i, tag in enumerate(self):
            if len(tag) > 0:  # if the tag has children
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
        return self

    @with_camel_case_alias
    def append_to(self, value):
        """append nodes to value
        """
        value.append(self)
        return self

    def prepend(self, value):
        """prepend value to nodes
        """
        root, root_text = self._get_root(value)
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

    @with_camel_case_alias
    def prepend_to(self, value):
        """prepend nodes to value
        """
        value.prepend(self)
        return self

    def after(self, value):
        """add value after nodes
        """
        root, root_text = self._get_root(value)
        for i, tag in enumerate(self):
            if not tag.tail:
                tag.tail = ''
            tag.tail += root_text
            if i > 0:
                root = deepcopy(list(root))
            parent = tag.getparent()
            index = parent.index(tag) + 1
            parent[index:index] = root
            root = parent[index:len(root)]
        return self

    @with_camel_case_alias
    def insert_after(self, value):
        """insert nodes after value
        """
        value.after(self)
        return self

    def before(self, value):
        """insert value before nodes
        """
        root, root_text = self._get_root(value)
        for i, tag in enumerate(self):
            previous = tag.getprevious()
            if previous is not None:
                if not previous.tail:
                    previous.tail = ''
                previous.tail += root_text
            else:
                parent = tag.getparent()
                if not parent.text:
                    parent.text = ''
                parent.text += root_text
            if i > 0:
                root = deepcopy(list(root))
            parent = tag.getparent()
            index = parent.index(tag)
            parent[index:index] = root
            root = parent[index:len(root)]
        return self

    @with_camel_case_alias
    def insert_before(self, value):
        """insert nodes before value
        """
        value.before(self)
        return self

    def wrap(self, value):
        """A string of HTML that will be created on the fly and wrapped around
        each target:

            >>> d = PyQuery('<span>youhou</span>')
            >>> d.wrap('<div></div>')
            [<div>]
            >>> print(d)
            <div><span>youhou</span></div>

        """
        assert isinstance(value, basestring)
        value = fromstring(value)[0]
        nodes = []
        for tag in self:
            wrapper = deepcopy(value)
            # FIXME: using iterchildren is probably not optimal
            if not wrapper.getchildren():
                wrapper.append(deepcopy(tag))
            else:
                childs = [c for c in wrapper.iterchildren()]
                child = childs[-1]
                child.append(deepcopy(tag))
            nodes.append(wrapper)

            parent = tag.getparent()
            if parent is not None:
                for t in parent.iterchildren():
                    if t is tag:
                        t.addnext(wrapper)
                        parent.remove(t)
                        break
        self[:] = nodes
        return self

    @with_camel_case_alias
    def wrap_all(self, value):
        """Wrap all the elements in the matched set into a single wrapper
        element::

            >>> d = PyQuery('<div><span>Hey</span><span>you !</span></div>')
            >>> print(d('span').wrap_all('<div id="wrapper"></div>'))
            <div id="wrapper"><span>Hey</span><span>you !</span></div>

            >>> d = PyQuery('<div><span>Hey</span><span>you !</span></div>')
            >>> print(d('span').wrapAll('<div id="wrapper"></div>'))
            <div id="wrapper"><span>Hey</span><span>you !</span></div>

        ..
        """
        if not self:
            return self

        assert isinstance(value, basestring)
        value = fromstring(value)[0]
        wrapper = deepcopy(value)
        if not wrapper.getchildren():
            child = wrapper
        else:
            childs = [c for c in wrapper.iterchildren()]
            child = childs[-1]

        replace_childs = True
        parent = self[0].getparent()
        if parent is None:
            parent = no_default

        # add nodes to wrapper and check parent
        for tag in self:
            child.append(deepcopy(tag))
            if tag.getparent() is not parent:
                replace_childs = False

        # replace nodes i parent if possible
        if parent is not no_default and replace_childs:
            childs = [c for c in parent.iterchildren()]
            if len(childs) == len(self):
                for tag in self:
                    parent.remove(tag)
                parent.append(wrapper)

        self[:] = [wrapper]
        return self

    @with_camel_case_alias
    def replace_with(self, value):
        """replace nodes by value:

            >>> doc = PyQuery("<html><div /></html>")
            >>> node = PyQuery("<span />")
            >>> child = doc.find('div')
            >>> child.replace_with(node)
            [<div>]
            >>> print(doc)
            <html><span/></html>

        """
        if isinstance(value, PyQuery):
            value = str(value)
        if hasattr(value, '__call__'):
            for i, element in enumerate(self):
                self._copy(element).before(
                    value(i, element) + (element.tail or ''))
                parent = element.getparent()
                parent.remove(element)
        else:
            for tag in self:
                self._copy(tag).before(value + (tag.tail or ''))
                parent = tag.getparent()
                parent.remove(tag)
        return self

    @with_camel_case_alias
    def replace_all(self, expr):
        """replace nodes by expr
        """
        if self._parent is no_default:
            raise ValueError(
                'replaceAll can only be used with an object with parent')
        self._parent(expr).replace_with(self)
        return self

    def clone(self):
        """return a copy of nodes
        """
        return PyQuery([deepcopy(tag) for tag in self])

    def empty(self):
        """remove nodes content
        """
        for tag in self:
            tag.text = None
            tag[:] = []
        return self

    def remove(self, expr=no_default):
        """Remove nodes:

             >>> h = (
             ... '<div>Maybe <em>she</em> does <strong>NOT</strong> know</div>'
             ... )
             >>> d = PyQuery(h)
             >>> d('strong').remove()
             [<strong>]
             >>> print(d)
             <div>Maybe <em>she</em> does  know</div>
        """
        if expr is no_default:
            for tag in self:
                parent = tag.getparent()
                if parent is not None:
                    if tag.tail:
                        prev = tag.getprevious()
                        if prev is None:
                            if not parent.text:
                                parent.text = ''
                            parent.text += tag.tail
                        else:
                            if not prev.tail:
                                prev.tail = ''
                            prev.tail += tag.tail
                    parent.remove(tag)
        else:
            results = self._copy(expr, self)
            results.remove()
        return self

    class Fn(object):
        """Hook for defining custom function (like the jQuery.fn):

        .. sourcecode:: python

         >>> fn = lambda: this.map(lambda i, el: PyQuery(this).outerHtml())
         >>> PyQuery.fn.listOuterHtml = fn
         >>> S = PyQuery(
         ...   '<ol>   <li>Coffee</li>   <li>Tea</li>   <li>Milk</li>   </ol>')
         >>> S('li').listOuterHtml()
         ['<li>Coffee</li>', '<li>Tea</li>', '<li>Milk</li>']

        """
        def __setattr__(self, name, func):
            def fn(self, *args, **kwargs):
                func.__globals__['this'] = self
                return func(*args, **kwargs)
            fn.__name__ = name
            setattr(PyQuery, name, fn)
    fn = Fn()

    ########
    # AJAX #
    ########

    @with_camel_case_alias
    def serialize_array(self):
        """Serialize form elements as an array of dictionaries, whose structure
        mirrors that produced by the jQuery API. Notably, it does not handle
        the deprecated `keygen` form element.

            >>> d = PyQuery('<form><input name="order" value="spam"></form>')
            >>> d.serialize_array() == [{'name': 'order', 'value': 'spam'}]
            True
            >>> d.serializeArray() == [{'name': 'order', 'value': 'spam'}]
            True
        """
        return list(map(
            lambda p: {'name': p[0], 'value': p[1]},
            self.serialize_pairs()
        ))

    def serialize(self):
        """Serialize form elements as a URL-encoded string.

            >>> h = (
            ... '<form><input name="order" value="spam">'
            ... '<input name="order2" value="baked beans"></form>'
            ... )
            >>> d = PyQuery(h)
            >>> d.serialize()
            'order=spam&order2=baked%20beans'
        """
        return urlencode(self.serialize_pairs()).replace('+', '%20')

    #####################################################
    # Additional methods that are not in the jQuery API #
    #####################################################

    @with_camel_case_alias
    def serialize_pairs(self):
        """Serialize form elements as an array of 2-tuples conventional for
        typical URL-parsing operations in Python.

            >>> d = PyQuery('<form><input name="order" value="spam"></form>')
            >>> d.serialize_pairs()
            [('order', 'spam')]
            >>> d.serializePairs()
            [('order', 'spam')]
        """
        # https://github.com/jquery/jquery/blob
        # /2d4f53416e5f74fa98e0c1d66b6f3c285a12f0ce/src/serialize.js#L14
        _submitter_types = ['submit', 'button', 'image', 'reset', 'file']

        controls = self._copy([])
        # Expand list of form controls
        for el in self.items():
            if el[0].tag == 'form':
                form_id = el.attr('id')
                if form_id:
                    # Include inputs outside of their form owner
                    root = self._copy(el.root.getroot())
                    controls.extend(root(
                        '#%s :not([form]):input, [form="%s"]:input'
                        % (form_id, form_id)))
                else:
                    controls.extend(el(':not([form]):input'))
            elif el[0].tag == 'fieldset':
                controls.extend(el(':input'))
            else:
                controls.extend(el)
        # Filter controls
        selector = '[name]:enabled:not(button)'  # Not serializing image button
        selector += ''.join(map(
            lambda s: ':not([type="%s"])' % s,
            _submitter_types))
        controls = controls.filter(selector)

        def _filter_out_unchecked(_, el):
            el = controls._copy(el)
            return not el.is_(':checkbox:not(:checked)') and \
                not el.is_(':radio:not(:checked)')
        controls = controls.filter(_filter_out_unchecked)

        # jQuery serializes inputs with the datalist element as an ancestor
        # contrary to WHATWG spec as of August 2018
        #
        # xpath = 'self::*[not(ancestor::datalist)]'
        # results = []
        # for tag in controls:
        #     results.extend(tag.xpath(xpath, namespaces=controls.namespaces))
        # controls = controls._copy(results)

        # Serialize values
        ret = []
        for field in controls:
            val = self._copy(field).val() or ''
            if isinstance(val, list):
                ret.extend(map(
                    lambda v: (field.attrib['name'], v.replace('\n', '\r\n')),
                    val
                ))
            else:
                ret.append((field.attrib['name'], val.replace('\n', '\r\n')))
        return ret

    @with_camel_case_alias
    def serialize_dict(self):
        """Serialize form elements as an ordered dictionary. Multiple values
        corresponding to the same input name are concatenated into one list.

            >>> d = PyQuery('''<form>
            ...             <input name="order" value="spam">
            ...             <input name="order" value="eggs">
            ...             <input name="order2" value="ham">
            ...             </form>''')
            >>> d.serialize_dict()
            OrderedDict({'order': ['spam', 'eggs'], 'order2': 'ham'})
            >>> d.serializeDict()
            OrderedDict({'order': ['spam', 'eggs'], 'order2': 'ham'})
        """
        ret = OrderedDict()
        for name, val in self.serialize_pairs():
            if name not in ret:
                ret[name] = val
            elif not isinstance(ret[name], list):
                ret[name] = [ret[name], val]
            else:
                ret[name].append(val)
        return ret

    @property
    def base_url(self):
        """Return the url of current html document or None if not available.
        """
        if self._base_url is not None:
            return self._base_url
        if self._parent is not no_default:
            return self._parent.base_url

    def make_links_absolute(self, base_url=None):
        """Make all links absolute.
        """
        if base_url is None:
            base_url = self.base_url
            if base_url is None:
                raise ValueError((
                    'You need a base URL to make your links'
                    'absolute. It can be provided by the base_url parameter.'))

        def repl(attr):
            def rep(i, e):
                attr_value = self(e).attr(attr)
                # when label hasn't such attr, pass
                if attr_value is None:
                    return None

                # skip specific "protocol" schemas
                if any(attr_value.startswith(schema)
                       for schema in ('tel:', 'callto:', 'sms:')):
                    return None

                return self(e).attr(attr,
                                    urljoin(base_url, attr_value.strip()))
            return rep

        self('a').each(repl('href'))
        self('link').each(repl('href'))
        self('script').each(repl('src'))
        self('img').each(repl('src'))
        self('iframe').each(repl('src'))
        self('form').each(repl('action'))

        return self


build_camel_case_aliases(PyQuery)
