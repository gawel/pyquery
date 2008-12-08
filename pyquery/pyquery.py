#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt
from lxml.cssselect import css_to_xpath
from lxml import etree
from copy import deepcopy

def selector_to_xpath(selector):
    """JQuery selector to xpath.
    TODO: patch cssselect to add :first, :last, ...
    """
    selector = selector.replace('[@', '[')
    return css_to_xpath(selector)

def fromstring(context):
    """use html parser if we don't have clean xml
    """
    try:
        return etree.fromstring(context)
    except etree.XMLSyntaxError:
        return etree.fromstring(context, etree.HTMLParser())

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
                return '<flexible_element %s>' % self.pget.func_name
        return _element()
    def __set__(self, instance, value):
        if self.pset is not no_default:
            self.pset(instance, value)
        else:
            raise NotImplementedError()

class PyQuery(list):
    """The main class
    """
    def __init__(self, *args, **kwargs):
        html = None
        elements = []

        if 'parent' in kwargs:
            self._parent = kwargs.pop('parent')
        else:
            self._parent = no_default

        if kwargs:
            # specific case to get the dom
            if 'filename' in kwargs:
                html = file(kwargs['filename']).read()
            elif 'url' in kwargs:
                from urllib2 import urlopen
                html = urlopen(kwargs['url']).read()
            else:
                raise ValueError('Invalid keyword arguments %s' % kwargs)
            elements = [fromstring(html)]
        else:
            # get nodes

            # determine context and selector if any
            selector = context = no_default
            length = len(args)
            if len(args) == 1:
                context = args[0]
            elif len(args) == 2:
                selector, context = args
            else:
                raise ValueError("You can't do that." +\
                        " Please, provide arguments")

            # get context
            if isinstance(context, basestring):
                try:
                    elements = [fromstring(context)]
                except Exception, e:
                    raise ValueError('%r, %s' % (e, context))
            elif isinstance(context, self.__class__):
                # copy
                elements = context[:]
            elif isinstance(context, list):
                elements = context
            elif isinstance(context, etree._Element):
                elements = [context]

            # select nodes
            if elements and selector is not no_default:
                xpath = selector_to_xpath(selector)
                results = [tag.xpath(xpath) for tag in elements]
                # Flatten the results
                elements = []
                for r in results:
                    elements.extend(r)

        list.__init__(self, elements)

    def __call__(self, *args):
        """return a new PyQuery instance
        """
        length = len(args)
        if length == 0:
            raise ValueError('You must provide at least a selector')
        if len(args) == 1 and not args[0].startswith('<'):
            args += (self,)
        result = self.__class__(*args, **dict(parent=self))
        return result

    # keep original list api prefixed with _
    _append = list.append
    _extend = list.extend

    # improve pythonic api
    def __add__(self, other):
        assert isinstance(other, self.__class__)
        return self.__class__(self[:] + other[:])

    def extend(self, other):
        assert isinstance(other, self.__class__)
        self._extend(other[:])

    def __str__(self):
        """html representation of current nodes
        """
        return ''.join([etree.tostring(e) for e in self])

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
    # Traversing #
    ##############

    def each(self, func):
        """apply func on each nodes
        """
        for e in self:
            func(self.__class__([e]))
        return self

    @property
    def length(self):
        return len(self)

    def size(self):
        return len(self)

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
        elif value is None or value == '':
            return self.removeAttr(attr)
        else:
            for tag in self:
                tag.set(attr, value)
        return self

    def removeAttr(self, name):
        """remove an attribute
        """
        for tag in self:
            del tag.attrib[name]
        return self

    attr = FlexibleElement(pget=attr, pdel=removeAttr)

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

    def addClass(self, value):
        """add a css class to elements
        """
        for tag in self:
            values = value.split(' ')
            classes = set((tag.get('class') or '').split())
            classes = classes.union(values)
            classes.difference_update([''])
            tag.set('class', ' '.join(classes))
        return self

    def removeClass(self, value):
        """remove a css class to elements
        """
        for tag in self:
            values = value.split(' ')
            classes = set((tag.get('class') or '').split())
            classes.difference_update(values)
            classes.difference_update([''])
            tag.set('class', ' '.join(classes))
        return self

    def toggleClass(self, value):
        """toggle a css class to elements
        """
        for tag in self:
            values = set(value.split(' '))
            classes = set((tag.get('class') or '').split())
            values_to_add = values.difference(classes)
            classes.difference_update(values)
            classes = classes.union(values_to_add)
            classes.difference_update([''])
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
                           and not el.split(':')[0].strip() in stripped_keys]
                for key, value in attr.items():
                    key = key.replace('_', '-')
                    current.append('%s: %s' % (key, value))
                tag.set('style', '; '.join(current))
        elif isinstance(value, basestring):
            attr = attr.replace('_', '-')
            for tag in self:
                current = [el.strip()
                           for el in (tag.get('style') or '').split(';')
                           if el.strip()
                              and not el.split(':')[0].strip() == attr.strip()]
                current.append('%s: %s' % (attr, value))
                tag.set('style', '; '.join(current))
        return self

    css = FlexibleElement(pget=css, pset=css)

    ###################
    # CORE UI EFFECTS #
    ###################
    def hide(self):
        """add display:none to elements style
        """
        return self.css('display', 'none')

    def show(self):
        """add display:block to elements style
        """
        return self.css('display', 'block')

    ########
    # HTML #
    ########
    def val(self, value=no_default):
        """return the value attribute
        """
        return self.attr('value', value)

    def html(self, value=no_default):
        """return the html representation of sub nodes
        """
        if value is no_default:
            if not self:
                return None
            tag = self[0]
            children = tag.getchildren()
            if not children:
                return tag.text
            html = tag.text or ''
            html += ''.join(map(etree.tostring, children))
            return html
        else:
            if isinstance(value, self.__class__):
                new_html = str(value)
            elif isinstance(value, basestring):
                new_html = value

            for tag in self:
                for child in tag.getchildren():
                    tag.remove(child)
                root = etree.fromstring('<root>' + new_html + '</root>')
                children = root.getchildren()
                if children:
                    tag.extend(children)
                tag.text = root.text
                tag.tail = root.tail
        return self

    def text(self, value=no_default):
        """return the text representation of sub nodes
        """
        def get_text(tag, no_tail=False):
            text = []
            if tag.text:
                text.append(tag.text)
            for child in tag.getchildren():
                text.extend(get_text(child))
            if not no_tail and tag.tail:
                text.append(tag.tail)
            return text

        if value is no_default:
            if not self:
                return None
            return ' '.join([''.join(get_text(tag, no_tail=True)).strip()
                             for tag in self])

        for tag in self:
            for child in tag.getchildren():
                tag.remove(child)
            tag.text = value
        return self

    ################
    # Manipulating #
    ################

    def _get_root(self, value):
        is_pyquery_results = isinstance(value, self.__class__)
        is_string = isinstance(value, basestring)
        assert is_string or is_pyquery_results, value
        if is_string:
            root = etree.fromstring('<root>' + value + '</root>')
        elif is_pyquery_results:
            root = value
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

    def prependTo(self, value):
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

    def insertAfter(self, value):
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
            if previous != None:
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

    def insertBefore(self, value):
        """insert nodes before value
        """
        value.before(self)
        return self

    def replaceWith(self, value):
        """replace nodes by value
        """
        self.before(value)
        for tag in self:
            parent = tag.getparent()
            parent.remove(tag)
        return self

    def replaceAll(self, expr):
        """replace nodes by expr
        """
        if self._parent is no_default:
            raise ValueError(
                    'replaceAll can only be used with an object with parent')
        self._parent(expr).replaceWith(self)
        return self

    def clone(self):
        """return a copy of nodes
        """
        self[:] = [deepcopy(tag) for tag in self]
        return self

    def empty(self):
        """remove nodes content
        """
        for tag in self:
            tag.text = None
            tag[:] = []
        return self

    def remove(self, expr=no_default):
        """remove nodes
        """
        if expr is no_default:
            for tag in self:
                parent = tag.getparent()
                parent.remove(tag)
        else:
            results = self.__class__(expr, self)
            results.remove()
        return self
