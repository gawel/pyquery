# -*- coding:utf-8 -*-
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
        """Matches the first selected element::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><p class="first"></p><p></p></div>')
            >>> d('p:first')
            [<p.first>]

        ..
        """
        xpath.add_post_condition('position() = 1')
        return xpath

    def xpath_last_pseudo(self, xpath):
        """Matches the last selected element::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><p></p><p class="last"></p></div>')
            >>> d('p:last')
            [<p.last>]

        ..
        """
        xpath.add_post_condition('position() = last()')
        return xpath

    def xpath_even_pseudo(self, xpath):
        """Matches even elements, zero-indexed::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><p></p><p class="last"></p></div>')
            >>> d('p:even')
            [<p>]

        ..
        """
        # the first element is 1 in xpath and 0 in python and js
        xpath.add_post_condition('position() mod 2 = 1')
        return xpath

    def xpath_odd_pseudo(self, xpath):
        """Matches odd elements, zero-indexed::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><p></p><p class="last"></p></div>')
            >>> d('p:odd')
            [<p.last>]

        ..
        """
        xpath.add_post_condition('position() mod 2 = 0')
        return xpath

    def xpath_checked_pseudo(self, xpath):
        """Matches odd elements, zero-indexed::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input checked="checked"/></div>')
            >>> d('input:checked')
            [<input>]

        ..
        """
        xpath.add_condition("@checked and name(.) = 'input'")
        return xpath

    def xpath_selected_pseudo(self, xpath):
        """Matches all elements that are selected::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<select><option selected="selected"/></select>')
            >>> d('option:selected')
            [<option>]

        ..
        """
        xpath.add_condition("@selected and name(.) = 'option'")
        return xpath

    def xpath_disabled_pseudo(self, xpath):
        """Matches all elements that are disabled::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input disabled="disabled"/></div>')
            >>> d('input:disabled')
            [<input>]

        ..
        """
        xpath.add_condition("@disabled")
        return xpath

    def xpath_enabled_pseudo(self, xpath):
        """Matches all elements that are enabled::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input value="foo" /></div>')
            >>> d('input:enabled')
            [<input>]

        ..
        """
        xpath.add_condition("not(@disabled) and name(.) = 'input'")
        return xpath

    def xpath_file_pseudo(self, xpath):
        """Matches all input elements of type file::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input type="file"/></div>')
            >>> d('input:file')
            [<input>]

        ..
        """
        xpath.add_condition("@type = 'file' and name(.) = 'input'")
        return xpath

    def xpath_input_pseudo(self, xpath):
        """Matches all input elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery(('<div><input type="file"/>'
            ...              '<textarea></textarea></div>'))
            >>> d(':input')
            [<input>, <textarea>]

        ..
        """
        xpath.add_condition((
            "(name(.) = 'input' or name(.) = 'select') "
            "or (name(.) = 'textarea' or name(.) = 'button')"))
        return xpath

    def xpath_button_pseudo(self, xpath):
        """Matches all button input elements and the button element::

            >>> from pyquery import PyQuery
            >>> d = PyQuery(('<div><input type="button"/>'
            ...              '<button></button></div>'))
            >>> d(':button')
            [<input>, <button>]

        ..
        """
        xpath.add_condition((
            "(@type = 'button' and name(.) = 'input') "
            "or name(.) = 'button'"))
        return xpath

    def xpath_radio_pseudo(self, xpath):
        """Matches all radio input elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input type="radio"/></div>')
            >>> d('input:radio')
            [<input>]

        ..
        """
        xpath.add_condition("@type = 'radio' and name(.) = 'input'")
        return xpath

    def xpath_text_pseudo(self, xpath):
        """Matches all text input elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input type="text"/></div>')
            >>> d('input:text')
            [<input>]

        ..
        """
        xpath.add_condition("@type = 'text' and name(.) = 'input'")
        return xpath

    def xpath_checkbox_pseudo(self, xpath):
        """Matches all checkbox input elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input type="checkbox"/></div>')
            >>> d('input:checkbox')
            [<input>]

        ..
        """
        xpath.add_condition("@type = 'checkbox' and name(.) = 'input'")
        return xpath

    def xpath_password_pseudo(self, xpath):
        """Matches all password input elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input type="password"/></div>')
            >>> d('input:password')
            [<input>]

        ..
        """
        xpath.add_condition("@type = 'password' and name(.) = 'input'")
        return xpath

    def xpath_submit_pseudo(self, xpath):
        """Matches all submit input elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input type="submit"/></div>')
            >>> d('input:submit')
            [<input>]

        ..
        """
        xpath.add_condition("@type = 'submit' and name(.) = 'input'")
        return xpath

    def xpath_hidden_pseudo(self, xpath):
        """Matches all hidden input elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input type="hidden"/></div>')
            >>> d('input:hidden')
            [<input>]

        ..
        """
        xpath.add_condition("@type = 'hidden' and name(.) = 'input'")
        return xpath

    def xpath_image_pseudo(self, xpath):
        """Matches all image input elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input type="image"/></div>')
            >>> d('input:image')
            [<input>]

        ..
        """
        xpath.add_condition("@type = 'image' and name(.) = 'input'")
        return xpath

    def xpath_reset_pseudo(self, xpath):
        """Matches all reset input elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><input type="reset"/></div>')
            >>> d('input:reset')
            [<input>]

        ..
        """
        xpath.add_condition("@type = 'reset' and name(.) = 'input'")
        return xpath

    def xpath_header_pseudo(self, xpath):
        """Matches all header elelements (h1, ..., h6)::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><h1>title</h1></div>')
            >>> d(':header')
            [<h1>]

        ..
        """
        # this seems kind of brute-force, is there a better way?
        xpath.add_condition((
            "(name(.) = 'h1' or name(.) = 'h2' or name (.) = 'h3') "
            "or (name(.) = 'h4' or name (.) = 'h5' or name(.) = 'h6')"))
        return xpath

    def xpath_parent_pseudo(self, xpath):
        """Match all elements that contain other elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><h1><span>title</span></h1><h1/></div>')
            >>> d('h1:parent')
            [<h1>]

        ..
        """
        xpath.add_condition("count(child::*) > 0")
        return xpath

    def xpath_empty_pseudo(self, xpath):
        """Match all elements that do not contain other elements::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><h1><span>title</span></h1><h2/></div>')
            >>> d(':empty')
            [<h2>]

        ..
        """
        xpath.add_condition("not(node())")
        return xpath

    def xpath_eq_function(self, xpath, function):
        """Matches a single element by its index::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><h1 class="first"/><h1 class="last"/></div>')
            >>> d('h1:eq(0)')
            [<h1.first>]
            >>> d('h1:eq(1)')
            [<h1.last>]

        ..
        """
        if function.argument_types() != ['NUMBER']:
            raise ExpressionError(
                "Expected a single integer for :eq(), got %r" % (
                    function.arguments,))
        value = int(function.arguments[0].value)
        xpath.add_post_condition('position() = %s' % (value + 1))
        return xpath

    def xpath_gt_function(self, xpath, function):
        """Matches all elements with an index over the given one::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><h1 class="first"/><h1 class="last"/></div>')
            >>> d('h1:gt(0)')
            [<h1.last>]

        ..
        """
        if function.argument_types() != ['NUMBER']:
            raise ExpressionError(
                "Expected a single integer for :gt(), got %r" % (
                    function.arguments,))
        value = int(function.arguments[0].value)
        xpath.add_post_condition('position() > %s' % (value + 1))
        return xpath

    def xpath_lt_function(self, xpath, function):
        """Matches all elements with an index below the given one::

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><h1 class="first"/><h1 class="last"/></div>')
            >>> d('h1:lt(1)')
            [<h1.first>]

        ..
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

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div><h1/><h1 class="title">title</h1></div>')
            >>> d('h1:contains("title")')
            [<h1.title>]

        ..
        """
        if function.argument_types() not in (['STRING'], ['IDENT']):
            raise ExpressionError(
                "Expected a single string or ident for :contains(), got %r" % (
                    function.arguments,))

        value = self.xpath_literal(function.arguments[0].value)
        xpath.add_post_condition('contains(., %s)' % value)
        return xpath

    def xpath_has_function(self, xpath, function):
        """Matches elements which contain at least one element that matches
        the specified selector. https://api.jquery.com/has-selector/

            >>> from pyquery import PyQuery
            >>> d = PyQuery('<div class="foo"><div class="bar"></div></div>')
            >>> d('.foo:has(".baz")')
            []
            >>> d('.foo:has(".foo")')
            []
            >>> d('.foo:has(".bar")')
            [<div.foo>]
            >>> d('.foo:has(div)')
            [<div.foo>]

        ..
        """
        if function.argument_types() not in (['STRING'], ['IDENT']):
            raise ExpressionError(
                "Expected a single string or ident for :has(), got %r" % (
                    function.arguments,))
        value = self.css_to_xpath(
            function.arguments[0].value, prefix='descendant::',
        )
        xpath.add_post_condition(value)
        return xpath
