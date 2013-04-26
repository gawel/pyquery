#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt
from __future__ import unicode_literals
from cssselect import xpath as cssselect_xpath
from cssselect.xpath import ExpressionError

XPathExprOrig = cssselect_xpath.XPathExpr


class XPathExpr(XPathExprOrig):

    def __init__(self, path='', element='*', condition='', star_prefix=False):
        self.path = path
        self.element = element
        self.condition = condition
        self.post_condition = None

    def add_post_condition(self, post_condition):
        if self.post_condition:
            self.post_condition = '%s and (%s)' % (self.post_condition,
                                                   post_condition)
        else:
            self.post_condition = post_condition

    def __str__(self):
        path = XPathExprOrig.__str__(self)
        if self.post_condition:
            path = '%s[%s]' % (path, self.post_condition)
        return path

    def join(self, combiner, other):
        res = XPathExprOrig.join(self, combiner, other)
        self.post_condition = other.post_condition
        return res


# keep cssselect < 0.8 compat for now


class JQueryTranslator(cssselect_xpath.HTMLTranslator):
    """This class is used to implement the css pseudo classes
    (:first, :last, ...) that are not defined in the css standard,
    but are defined in the jquery API.
    """

    xpathexpr_cls = XPathExpr

    def xpath_first_pseudo(self, xpath):
        """Matches the first selected element.
        """
        xpath.add_post_condition('position() = 1')
        return xpath

    def xpath_last_pseudo(self, xpath):
        """Matches the last selected element.
        """
        xpath.add_post_condition('position() = last()')
        return xpath

    def xpath_even_pseudo(self, xpath):
        """Matches even elements, zero-indexed.
        """
        # the first element is 1 in xpath and 0 in python and js
        xpath.add_post_condition('position() mod 2 = 1')
        return xpath

    def xpath_odd_pseudo(self, xpath):
        """Matches odd elements, zero-indexed.
        """
        xpath.add_post_condition('position() mod 2 = 0')
        return xpath

    def xpath_checked_pseudo(self, xpath):
        """Matches odd elements, zero-indexed.
        """
        xpath.add_condition("@checked and name(.) = 'input'")
        return xpath

    def xpath_selected_pseudo(self, xpath):
        """Matches all elements that are selected.
        """
        xpath.add_condition("@selected and name(.) = 'option'")
        return xpath

    def xpath_disabled_pseudo(self, xpath):
        """Matches all elements that are disabled.
        """
        xpath.add_condition("@disabled")
        return xpath

    def xpath_enabled_pseudo(self, xpath):
        """Matches all elements that are enabled.
        """
        xpath.add_condition("not(@disabled) and name(.) = 'input'")
        return xpath

    def xpath_file_pseudo(self, xpath):
        """Matches all input elements of type file.
        """
        xpath.add_condition("@type = 'file' and name(.) = 'input'")
        return xpath

    def xpath_input_pseudo(self, xpath):
        """Matches all input elements.
        """
        xpath.add_condition((
            "(name(.) = 'input' or name(.) = 'select') "
            "or (name(.) = 'textarea' or name(.) = 'button')"))
        return xpath

    def xpath_button_pseudo(self, xpath):
        """Matches all button input elements and the button element.
        """
        xpath.add_condition((
            "(@type = 'button' and name(.) = 'input') "
            "or name(.) = 'button'"))
        return xpath

    def xpath_radio_pseudo(self, xpath):
        """Matches all radio input elements.
        """
        xpath.add_condition("@type = 'radio' and name(.) = 'input'")
        return xpath

    def xpath_text_pseudo(self, xpath):
        """Matches all text input elements.
        """
        xpath.add_condition("@type = 'text' and name(.) = 'input'")
        return xpath

    def xpath_checkbox_pseudo(self, xpath):
        """Matches all checkbox input elements.
        """
        xpath.add_condition("@type = 'checkbox' and name(.) = 'input'")
        return xpath

    def xpath_password_pseudo(self, xpath):
        """Matches all password input elements.
        """
        xpath.add_condition("@type = 'password' and name(.) = 'input'")
        return xpath

    def xpath_submit_pseudo(self, xpath):
        """Matches all submit input elements.
        """
        xpath.add_condition("@type = 'submit' and name(.) = 'input'")
        return xpath

    def xpath_image_pseudo(self, xpath):
        """Matches all image input elements.
        """
        xpath.add_condition("@type = 'image' and name(.) = 'input'")
        return xpath

    def xpath_reset_pseudo(self, xpath):
        """Matches all reset input elements.
        """
        xpath.add_condition("@type = 'reset' and name(.) = 'input'")
        return xpath

    def xpath_header_pseudo(self, xpath):
        """Matches all header elelements (h1, ..., h6)
        """
        # this seems kind of brute-force, is there a better way?
        xpath.add_condition((
            "(name(.) = 'h1' or name(.) = 'h2' or name (.) = 'h3') "
            "or (name(.) = 'h4' or name (.) = 'h5' or name(.) = 'h6')"))
        return xpath

    def xpath_parent_pseudo(self, xpath):
        """Match all elements that contain other elements
        """
        xpath.add_condition("count(child::*) > 0")
        return xpath

    def xpath_empty_pseudo(self, xpath):
        """Match all elements that do not contain other elements
        """
        xpath.add_condition("count(child::*) = 0")
        return xpath

    def xpath_eq_function(self, xpath, function):
        """Matches a single element by its index.
        """
        if function.argument_types() != ['NUMBER']:
            raise ExpressionError(
                "Expected a single integer for :eq(), got %r" % (
                    function.arguments,))
        value = int(function.arguments[0].value)
        xpath.add_post_condition('position() = %s' % (value + 1))
        return xpath

    def xpath_gt_function(self, xpath, function):
        """Matches all elements with an index over the given one.
        """
        if function.argument_types() != ['NUMBER']:
            raise ExpressionError(
                "Expected a single integer for :gt(), got %r" % (
                    function.arguments,))
        value = int(function.arguments[0].value)
        xpath.add_post_condition('position() > %s' % (value + 1))
        return xpath

    def xpath_lt_function(self, xpath, function):
        """Matches all elements with an index below the given one.
        """
        if function.argument_types() != ['NUMBER']:
            raise ExpressionError(
                "Expected a single integer for :gt(), got %r" % (
                    function.arguments,))

        value = int(function.arguments[0].value)
        xpath.add_post_condition('position() < %s' % (value + 1))
        return xpath

    def xpath_contains_function(self, xpath, function):
        """Matches all elements that contain the given text
        """
        if function.argument_types() != ['STRING']:
            raise ExpressionError(
                "Expected a single string for :contains(), got %r" % (
                    function.arguments,))

        value = self.xpath_literal(function.arguments[0].value)
        xpath.add_post_condition("contains(text(), %s)" % value)
        return xpath
