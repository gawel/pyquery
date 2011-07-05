#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt
from lxml.cssselect import Pseudo, XPathExpr, XPathExprOr, Function, css_to_xpath, Element
from lxml import cssselect

class JQueryPseudo(Pseudo):
    """This class is used to implement the css pseudo classes
    (:first, :last, ...) that are not defined in the css standard,
    but are defined in the jquery API.
    """
    def _xpath_first(self, xpath):
        """Matches the first selected element.
        """
        xpath.add_post_condition('position() = 1')
        return xpath

    def _xpath_last(self, xpath):
        """Matches the last selected element.
        """
        xpath.add_post_condition('position() = last()')
        return xpath

    def _xpath_even(self, xpath):
        """Matches even elements, zero-indexed.
        """
        # the first element is 1 in xpath and 0 in python and js
        xpath.add_post_condition('position() mod 2 = 1')
        return xpath

    def _xpath_odd(self, xpath):
        """Matches odd elements, zero-indexed.
        """
        xpath.add_post_condition('position() mod 2 = 0')
        return xpath

    def _xpath_checked(self, xpath):
        """Matches odd elements, zero-indexed.
        """
        xpath.add_condition("@checked and name(.) = 'input'")
        return xpath

    def _xpath_selected(self, xpath):
        """Matches all elements that are selected.
        """
        xpath.add_condition("@selected and name(.) = 'option'")
        return xpath

    def _xpath_disabled(self, xpath):
        """Matches all elements that are disabled.
        """
        xpath.add_condition("@disabled")
        return xpath

    def _xpath_enabled(self, xpath):
        """Matches all elements that are enabled.
        """
        xpath.add_condition("not(@disabled) and name(.) = 'input'")
        return xpath

    def _xpath_file(self, xpath):
        """Matches all input elements of type file.
        """
        xpath.add_condition("@type = 'file' and name(.) = 'input'")
        return xpath

    def _xpath_input(self, xpath):
        """Matches all input elements.
        """
        xpath.add_condition("(name(.) = 'input' or name(.) = 'select') "
        + "or (name(.) = 'textarea' or name(.) = 'button')")
        return xpath

    def _xpath_button(self, xpath):
        """Matches all button input elements and the button element.
        """
        xpath.add_condition("(@type = 'button' and name(.) = 'input') "
            + "or name(.) = 'button'")
        return xpath

    def _xpath_radio(self, xpath):
        """Matches all radio input elements.
        """
        xpath.add_condition("@type = 'radio' and name(.) = 'input'")
        return xpath

    def _xpath_text(self, xpath):
        """Matches all text input elements.
        """
        xpath.add_condition("@type = 'text' and name(.) = 'input'")
        return xpath

    def _xpath_checkbox(self, xpath):
        """Matches all checkbox input elements.
        """
        xpath.add_condition("@type = 'checkbox' and name(.) = 'input'")
        return xpath

    def _xpath_password(self, xpath):
        """Matches all password input elements.
        """
        xpath.add_condition("@type = 'password' and name(.) = 'input'")
        return xpath

    def _xpath_submit(self, xpath):
        """Matches all submit input elements.
        """
        xpath.add_condition("@type = 'submit' and name(.) = 'input'")
        return xpath

    def _xpath_image(self, xpath):
        """Matches all image input elements.
        """
        xpath.add_condition("@type = 'image' and name(.) = 'input'")
        return xpath

    def _xpath_reset(self, xpath):
        """Matches all reset input elements.
        """
        xpath.add_condition("@type = 'reset' and name(.) = 'input'")
        return xpath

    def _xpath_header(self, xpath):
        """Matches all header elelements (h1, ..., h6)
        """
        # this seems kind of brute-force, is there a better way?
        xpath.add_condition("(name(.) = 'h1' or name(.) = 'h2' or name (.) = 'h3') "
        + "or (name(.) = 'h4' or name (.) = 'h5' or name(.) = 'h6')")
        return xpath

    def _xpath_parent(self, xpath):
        """Match all elements that contain other elements
        """
        xpath.add_condition("count(child::*) > 0")
        return xpath

    def _xpath_empty(self, xpath):
        """Match all elements that do not contain other elements
        """
        xpath.add_condition("count(child::*) = 0")
        return xpath

cssselect.Pseudo = JQueryPseudo

class JQueryFunction(Function):
    """Represents selector:name(expr) that are present in JQuery but not in the
    css standard.
    """
    def _xpath_eq(self, xpath, expr):
        """Matches a single element by its index.
        """
        xpath.add_post_condition('position() = %s' % int(expr+1))
        return xpath

    def _xpath_gt(self, xpath, expr):
        """Matches all elements with an index over the given one.
        """
        xpath.add_post_condition('position() > %s' % int(expr+1))
        return xpath

    def _xpath_lt(self, xpath, expr):
        """Matches all elements with an index below the given one.
        """
        xpath.add_post_condition('position() < %s' % int(expr+1))
        return xpath

    def _xpath_contains(self, xpath, expr):
        """Matches all elements that contain the given text
        """
        xpath.add_post_condition("contains(text(), '%s')" % str(expr))
        return xpath

cssselect.Function = JQueryFunction

class AdvancedXPathExpr(XPathExpr):
    def __init__(self, prefix=None, path=None, element='*', condition=None,
                 post_condition=None, star_prefix=False):
        self.prefix = prefix
        self.path = path
        self.element = element
        self.condition = condition
        self.post_condition = post_condition
        self.star_prefix = star_prefix

    def add_post_condition(self, post_condition):
        if self.post_condition:
            self.post_condition = '%s and (%s)' % (self.post_condition,
                                                   post_condition)
        else:
            self.post_condition = post_condition

    def __str__(self):
        path = XPathExpr.__str__(self)
        if self.post_condition:
            path = '(%s)[%s]' % (path, self.post_condition)
        return path

    def join(self, combiner, other):
        XPathExpr.join(self, combiner, other)
        self.post_condition = other.post_condition

cssselect.XPathExpr = AdvancedXPathExpr

class AdvancedXPathExprOr(XPathExprOr):
    def __init__(self, items, prefix=None):
        self.prefix = prefix = prefix or ''
        self.items = items
        self.prefix_prepended = False

    def __str__(self):
        if not self.prefix_prepended:
            # We cannot prepend the prefix at __init__ since it's legal to
            # modify it after construction. And because __str__ can be called
            # multiple times we have to take care not to prepend it twice.
            prefix = self.prefix or ''
            for item in self.items:
                item.prefix = prefix+(item.prefix or '')
            self.prefix_prepended = True
        return ' | '.join([str(i) for i in self.items])

cssselect.XPathExprOr = AdvancedXPathExprOr

class JQueryElement(Element):
    """
    Represents namespace|element
    """
    
    def xpath(self):
        if self.namespace == '*':
            el = self.element
        else:
            # FIXME: Should we lowercase here?
            el = '%s:%s' % (self.namespace, self.element)
        return AdvancedXPathExpr(element=el)
        
cssselect.Element = JQueryElement

def selector_to_xpath(selector, prefix='descendant-or-self::'):
    """JQuery selector to xpath.
    """
    selector = selector.replace('[@', '[')
    return css_to_xpath(selector, prefix)
