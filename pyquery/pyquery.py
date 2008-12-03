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
