#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt
from lxml.cssselect import Pseudo, XPathExpr, XPathExprOr, Function, css_to_xpath
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
        """Matches all elements that are disabled.
        """
        xpath.add_condition("not(@disabled) and name(.) = 'input'")
        return xpath

    def _xpath_file(self, xpath):
        """Matches all input elements of type file.
        """
        xpath.add_condition("@type = 'file' and name(.) = 'input'")
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

    def __str__(self):
        prefix = self.prefix or ''
        for item in self.items:
            item.prefix = prefix
        return ' | '.join([str(i) for i in self.items])

cssselect.XPathExprOr = AdvancedXPathExprOr

def selector_to_xpath(selector):
    """JQuery selector to xpath.
    """
    selector = selector.replace('[@', '[')
    return css_to_xpath(selector)
