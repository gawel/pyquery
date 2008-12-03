#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt

from lxml.cssselect import css_to_xpath
from lxml import etree
from copy import deepcopy

def selector_to_xpath(selector):
    '''JQuery selector to xpath.
    TODO: patch cssselect to add :first, :last, ...
    '''
    selector = selector.replace('[@', '[')
    return css_to_xpath(selector)


class PyQuery(list):
    '''See the pyquery module docstring.
    '''
    def __init__(self, *args, **kwargs):
        html = None
        elements = []
        if kwargs:
            # specific case to get the dom
            if 'filename' in kwargs:
                html = file(kwargs['filename']).read()
            elif 'url' in kwargs:
                from urllib2 import urlopen
                html = urlopen(kwargs['url']).read()
            else:
                raise ValueError('Invalid keyword arguments %s' % kwargs)
            elements = [etree.fromstring(html)]
        else:
            # get nodes

            # determine context and selector if any
            selector = context = None
            length = len(args)
            if len(args) == 1:
                context = args[0]
            elif len(args) == 2:
                selector, context = args

            # get context
            if isinstance(context, basestring):
                elements = [etree.fromstring(context)]
            elif isinstance(context, self.__class__):
                # copy
                elements = context[:]
            elif isinstance(context, list):
                elements = context
            elif isinstance(context, etree._Element):
                elements = [context]

            # select nodes
            if elements and selector is not None:
                xpath = selector_to_xpath(selector)
                results = [tag.xpath(xpath) for tag in elements]
                # Flatten the results
                elements = []
                for r in results:
                    elements.extend(r)

        list.__init__(self, elements)

    def __call__(self, *args):
        # just return a new instance
        length = len(args)
        if length == 0:
            raise ValueError('You must provide at least a selector')
        if len(args) == 1:
            args += (self,)
        return self.__class__(*args)

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
        for e in self:
            func(self.__class__([e]))
        return self

    @property
    def length(self):
        return len(self)

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

    def __setattr__(self, name, value):
        return self.attr(name, value)

    def __getattr__(self, name):
        return self.attr(name)

    def removeAttr(self, name):
        for tag in self:
            del tag.attrib[name]
        return self

    def __delattr__(self, name):
        self.removeAttr(name)

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
        value.append(self)
        return self

    def prepend(self, value):
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
        value.prepend(self)
        return self

    def after(self, value):
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
        value.after(self)
        return self

    def before(self, value):
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
        value.before(self)
        return self

    def clone(self):
        self[:] = [deepcopy(tag) for tag in self]
        return self

    def empty(self):
        for tag in self:
            tag.text = None
            tag[:] = []
        return self

    def remove(expr=None):
        if expr == None:
            for tag in self:
                parent = tag.getparent()
                parent.remove(tag)
        if expr != None:
            results = self.__class__(expr, self)
            results.remove()
        return self
