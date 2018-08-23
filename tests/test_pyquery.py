# -*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt
import os
import sys
import time
from lxml import etree
from pyquery.pyquery import PyQuery as pq, no_default
from pyquery.openers import HAS_REQUEST
from webtest import http
from webtest.debugapp import debug_app
from .compat import PY3k
from .compat import b
from .compat import text_type
from .compat import TestCase

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def not_py3k(func):
    if not PY3k:
        return func


dirname = os.path.dirname(os.path.abspath(__file__))
docs = os.path.join(os.path.dirname(dirname), 'docs')
path_to_html_file = os.path.join(dirname, 'test.html')
path_to_invalid_file = os.path.join(dirname, 'invalid.xml')


class TestUnicode(TestCase):

    def test_unicode(self):
        xml = pq(u"<html><p>é</p></html>")
        self.assertEqual(type(xml.html()), text_type)
        if PY3k:
            self.assertEqual(str(xml), '<html><p>é</p></html>')
            self.assertEqual(str(xml('p:contains("é")')), '<p>é</p>')
        else:
            self.assertEqual(text_type(xml),
                             u"<html><p>é</p></html>")
            self.assertEqual(str(xml), '<html><p>&#233;</p></html>')
            self.assertEqual(str(xml(u'p:contains("é")')),
                             '<p>&#233;</p>')
            self.assertEqual(text_type(xml(u'p:contains("é")')),
                             u'<p>é</p>')


class TestAttributeCase(TestCase):

    def test_xml_upper_element_name(self):
        xml = pq('<X>foo</X>', parser='xml')
        self.assertEqual(len(xml('X')), 1)
        self.assertEqual(len(xml('x')), 0)

    def test_html_upper_element_name(self):
        xml = pq('<X>foo</X>', parser='html')
        self.assertEqual(len(xml('X')), 1)
        self.assertEqual(len(xml('x')), 1)


class TestSelector(TestCase):
    klass = pq
    html = """
           <html>
            <body>
              <div>node1</div>
              <div id="node2">node2</div>
              <div class="node3">node3</div>
            </body>
           </html>
           """

    html2 = """
           <html>
            <body>
              <div>node1</div>
            </body>
           </html>
           """

    html3 = """
           <html>
            <body>
              <div>node1</div>
              <div id="node2">node2</div>
              <div class="node3">node3</div>
            </body>
           </html>
           """

    html4 = """
           <html>
            <body>
              <form action="/">
                <input name="enabled" type="text" value="test"/>
                <b disabled>Not :disabled</b>
                <input name="disabled" type="text"
                       value="disabled" disabled="disabled"/>
                <fieldset>
                    <input name="fieldset-enabled">
                </fieldset>
                <fieldset disabled>
                    <legend>
                        <input name="legend-enabled">
                    </legend>
                    <input name="fieldset-disabled">
                    <legend>
                        <input name="legend-disabled">
                    </legend>
                    <select id="disabled-select">
                        <optgroup>
                            <option></option>
                        </optgroup>
                    </select>
                </fieldset>
                <select>
                    <optgroup id="disabled-optgroup" disabled>
                        <option id="disabled-from-optgroup"></option>
                        <option id="disabled-option" disabled></option>
                    </optgroup>
                </select>
                <input name="file" type="file" />
                <select name="select">
                  <option value="">Choose something</option>
                  <option value="one">One</option>
                  <option value="two" selected="selected">Two</option>
                  <option value="three">Three</option>
                </select>
                <input name="radio" type="radio" value="one"/>
                <input name="radio" type="radio"
                       value="two" checked="checked"/>
                <input name="radio" type="radio" value="three"/>
                <input name="checkbox" type="checkbox" value="a"/>
                <input name="checkbox" type="checkbox"
                       value="b" checked="checked"/>
                <input name="checkbox" type="checkbox" value="c"/>
                <input name="button" type="button" value="button" />
                <button>button</button>
              </form>
            </body>
           </html>
           """

    html5 = """
           <html>
            <body>
              <h1>Heading 1</h1>
              <h2>Heading 2</h2>
              <h3>Heading 3</h3>
              <h4>Heading 4</h4>
              <h5>Heading 5</h5>
              <h6>Heading 6</h6>
              <div></div>
            </body>
           </html>
           """

    def test_get_root(self):
        doc = pq(b('<?xml version="1.0" encoding="UTF-8"?><root><p/></root>'))
        self.assertEqual(isinstance(doc.root, etree._ElementTree), True)
        self.assertEqual(doc.encoding, 'UTF-8')

        child = doc.children().eq(0)
        self.assertNotEqual(child._parent, no_default)
        self.assertTrue(isinstance(child.root, etree._ElementTree))

    def test_selector_from_doc(self):
        doc = etree.fromstring(self.html)
        assert len(self.klass(doc)) == 1
        assert len(self.klass('div', doc)) == 3
        assert len(self.klass('div#node2', doc)) == 1

    def test_selector_from_html(self):
        assert len(self.klass(self.html)) == 1
        assert len(self.klass('div', self.html)) == 3
        assert len(self.klass('div#node2', self.html)) == 1

    def test_selector_from_obj(self):
        e = self.klass(self.html)
        assert len(e('div')) == 3
        assert len(e('div#node2')) == 1

    def test_selector_from_html_from_obj(self):
        e = self.klass(self.html)
        assert len(e('div', self.html2)) == 1
        assert len(e('div#node2', self.html2)) == 0

    def test_class(self):
        e = self.klass(self.html)
        assert isinstance(e, self.klass)
        n = e('div', self.html2)
        assert isinstance(n, self.klass)
        assert n._parent is e

    def test_pseudo_classes(self):
        e = self.klass(self.html)
        self.assertEqual(e('div:first').text(), 'node1')
        self.assertEqual(e('div:last').text(), 'node3')
        self.assertEqual(e('div:even').text(), 'node1 node3')
        self.assertEqual(e('div div:even').text(), '')
        self.assertEqual(e('body div:even').text(), 'node1 node3')
        self.assertEqual(e('div:gt(0)').text(), 'node2 node3')
        self.assertEqual(e('div:lt(1)').text(), 'node1')
        self.assertEqual(e('div:eq(2)').text(), 'node3')

        # test on the form
        e = self.klass(self.html4)
        disabled = e(':disabled')
        self.assertIn(e('[name="disabled"]')[0], disabled)
        self.assertIn(e('fieldset[disabled]')[0], disabled)
        self.assertIn(e('[name="legend-disabled"]')[0], disabled)
        self.assertIn(e('[name="fieldset-disabled"]')[0], disabled)
        self.assertIn(e('#disabled-optgroup')[0], disabled)
        self.assertIn(e('#disabled-from-optgroup')[0], disabled)
        self.assertIn(e('#disabled-option')[0], disabled)
        self.assertIn(e('#disabled-select')[0], disabled)

        assert len(disabled) == 8
        assert len(e('select:enabled')) == 2
        assert len(e('input:enabled')) == 11
        assert len(e(':selected')) == 1
        assert len(e(':checked')) == 2
        assert len(e(':file')) == 1
        assert len(e(':input')) == 18
        assert len(e(':button')) == 2
        assert len(e(':radio')) == 3
        assert len(e(':checkbox')) == 3

        # test on other elements
        e = self.klass(self.html5)
        assert len(e(":header")) == 6
        assert len(e(":parent")) == 2
        assert len(e(":empty")) == 1
        assert len(e(":contains('Heading')")) == 8

    def test_on_the_fly_dom_creation(self):
        e = self.klass(self.html)
        assert e('<p>Hello world</p>').text() == 'Hello world'
        assert e('').text() == ''


class TestTraversal(TestCase):
    klass = pq
    html = """
           <html>
            <body>
              <div id="node1"><span>node1</span></div>
              <div id="node2" class="node3">
                        <span>node2</span><span> booyah</span></div>
            </body>
           </html>
           """

    def test_filter(self):
        assert len(self.klass('div', self.html).filter('.node3')) == 1
        assert len(self.klass('div', self.html).filter('#node2')) == 1
        assert len(self.klass('div', self.html).filter(lambda i: i == 0)) == 1

        d = pq('<p>Hello <b>warming</b> world</p>')
        self.assertEqual(d('strong').filter(lambda el: True), [])

    def test_not(self):
        assert len(self.klass('div', self.html).not_('.node3')) == 1

    def test_is(self):
        assert self.klass('div', self.html).is_('.node3')
        assert not self.klass('div', self.html).is_('.foobazbar')

    def test_find(self):
        assert len(self.klass('#node1', self.html).find('span')) == 1
        assert len(self.klass('#node2', self.html).find('span')) == 2
        assert len(self.klass('div', self.html).find('span')) == 3

    def test_each(self):
        doc = self.klass(self.html)
        doc('span').each(lambda: doc(this).wrap("<em></em>"))  # NOQA
        assert len(doc('em')) == 3

    def test_map(self):
        def ids_minus_one(i, elem):
            return int(self.klass(elem).attr('id')[-1]) - 1
        assert self.klass('div', self.html).map(ids_minus_one) == [0, 1]

        d = pq('<p>Hello <b>warming</b> world</p>')
        self.assertEqual(d('strong').map(lambda i, el: pq(this).text()), [])  # NOQA

    def test_end(self):
        assert len(self.klass('div', self.html).find('span').end()) == 2
        assert len(self.klass('#node2', self.html).find('span').end()) == 1

    def test_closest(self):
        assert len(self.klass('#node1 span', self.html).closest('body')) == 1
        assert self.klass('#node2',
                          self.html).closest('.node3').attr('id') == 'node2'
        assert self.klass('.node3', self.html).closest('form') == []


class TestOpener(TestCase):

    def test_open_filename(self):
        doc = pq(filename=path_to_html_file)
        self.assertEqual(len(doc('p#test').text()), 14)

    def test_invalid_filename(self):
        doc = pq(filename=path_to_invalid_file)
        self.assertEqual(len(doc('p#test').text()), 14)

    def test_custom_opener(self):
        def opener(url):
            return '<html><body><div class="node"></div>'

        doc = pq(url='http://example.com', opener=opener)
        assert len(doc('.node')) == 1, doc


class TestConstruction(TestCase):

    def test_typeerror_on_invalid_value(self):
        self.assertRaises(TypeError, pq, object())


class TestComment(TestCase):

    def test_comment(self):
        doc = pq('<div><!-- foo --> bar</div>')
        self.assertEqual(doc.text(), 'bar')


class TestCallback(TestCase):
    html = """
        <ol>
            <li>Coffee</li>
            <li>Tea</li>
            <li>Milk</li>
        </ol>
    """

    def test_S_this_inside_callback(self):
        S = pq(self.html)
        self.assertEqual(S('li').map(lambda i, el: S(this).html()),  # NOQA
                                     ['Coffee', 'Tea', 'Milk'])

    def test_parameterless_callback(self):
        S = pq(self.html)
        self.assertEqual(S('li').map(lambda: S(this).html()),  # NOQA
                                     ['Coffee', 'Tea', 'Milk'])


class TestHook(TestCase):
    html = """
        <ol>
            <li>Coffee</li>
            <li>Tea</li>
            <li>Milk</li>
        </ol>
    """

    def test_fn(self):
        "Example from `PyQuery.Fn` docs."
        fn = lambda: this.map(lambda i, el: pq(this).outerHtml())  # NOQA
        pq.fn.listOuterHtml = fn
        S = pq(self.html)
        self.assertEqual(S('li').listOuterHtml(),
                         ['<li>Coffee</li>', '<li>Tea</li>', '<li>Milk</li>'])

    def test_fn_with_kwargs(self):
        "fn() with keyword arguments."
        pq.fn.test = lambda p=1: pq(this).eq(p)  # NOQA
        S = pq(self.html)
        self.assertEqual(S('li').test(0).text(), 'Coffee')
        self.assertEqual(S('li').test().text(), 'Tea')
        self.assertEqual(S('li').test(p=2).text(), 'Milk')


class TestManipulating(TestCase):
    html = '''
    <div class="portlet">
      <a href="/toto">Test<img src ="myimage" />My link text</a>
      <a href="/toto2"><img src ="myimage2" />My link text 2</a>
    </div>
    '''

    html2 = '''
        <input name="spam" value="Spam">
        <input name="eggs" value="Eggs">
        <input type="checkbox" value="Bacon">
        <input type="radio" value="Ham">
    '''

    html2_newline = '''
        <input id="newline-text" type="text" name="order" value="S
pam">
        <input id="newline-radio" type="radio" name="order" value="S
pam">
    '''

    html3 = '''
        <textarea id="textarea-single">Spam</textarea>
        <textarea id="textarea-multi">Spam
<b>Eggs</b>
Bacon</textarea>
    '''

    html4 = '''
        <select id="first">
            <option value="spam">Spam</option>
            <option value="eggs">Eggs</option>
        </select>
        <select id="second">
            <option value="spam">Spam</option>
            <option value="eggs" selected>Eggs</option>
            <option value="bacon">Bacon</option>
        </select>
        <select id="third">
        </select>
        <select id="fourth">
            <option value="spam">Spam</option>
            <option value="spam">Eggs</option>
            <option value="spam">Bacon</option>
        </select>
    '''

    html6 = '''
        <select id="first" multiple>
            <option value="spam" selected>Spam</option>
            <option value="eggs" selected>Eggs</option>
            <option value="bacon">Bacon</option>
        </select>
        <select id="second" multiple>
            <option value="spam">Spam</option>
            <option value="eggs">Eggs</option>
            <option value="bacon">Bacon</option>
        </select>
        <select id="third" multiple>
            <option value="spam">Spam</option>
            <option value="spam">Eggs</option>
            <option value="spam">Bacon</option>
        </select>
    '''

    html5 = '''
        <div>
            <input id="first" value="spam">
            <input id="second" value="eggs">
            <textarea id="third">bacon</textarea>
        </div>
    '''

    def test_attr_empty_string(self):
        d = pq('<div>')
        d.attr('value', '')
        self.assertEqual(d.outer_html(), '<div value=""></div>')
        self.assertEqual(d.outer_html(method="xml"), '<div value=""/>')

    def test_remove(self):
        d = pq(self.html)
        d('img').remove()
        val = d('a:first').html()
        assert val == 'Test My link text', repr(val)
        val = d('a:last').html()
        assert val == ' My link text 2', repr(val)

    def test_class(self):
        d = pq('<div></div>')
        d.removeClass('xx')
        assert 'class' not in str(d), str(d)

    def test_val_for_inputs(self):
        d = pq(self.html2)
        self.assertIsNone(d('input[name="none"]').val())
        self.assertEqual(d('input[name="spam"]').val(), 'Spam')
        self.assertEqual(d('input[name="eggs"]').val(), 'Eggs')
        self.assertEqual(d('input:checkbox').val(), 'Bacon')
        self.assertEqual(d('input:radio').val(), 'Ham')
        d('input[name="spam"]').val('42')
        d('input[name="eggs"]').val('43')
        d('input:checkbox').val('44')
        d('input:radio').val('45')
        self.assertEqual(d('input[name="spam"]').val(), '42')
        self.assertEqual(d('input[name="eggs"]').val(), '43')
        self.assertEqual(d('input:checkbox').val(), '44')
        self.assertEqual(d('input:radio').val(), '45')

    def test_val_for_inputs_with_newline(self):
        d = pq(self.html2_newline)
        self.assertEqual(d('#newline-text').val(), 'Spam')
        self.assertEqual(d('#newline-radio').val(), 'S\npam')

    def test_val_for_textarea(self):
        d = pq(self.html3)
        self.assertEqual(d('#textarea-single').val(), 'Spam')
        self.assertEqual(d('#textarea-single').text(), 'Spam')
        d('#textarea-single').val('42')
        self.assertEqual(d('#textarea-single').val(), '42')
        # Note: jQuery still returns 'Spam' here.
        self.assertEqual(d('#textarea-single').text(), '42')

        multi_expected = '''Spam\n<b>Eggs</b>\nBacon'''
        self.assertEqual(d('#textarea-multi').val(), multi_expected)
        self.assertEqual(d('#textarea-multi').text(), multi_expected)
        multi_new = '''Bacon\n<b>Eggs</b>\nSpam'''
        d('#textarea-multi').val(multi_new)
        self.assertEqual(d('#textarea-multi').val(), multi_new)
        self.assertEqual(d('#textarea-multi').text(), multi_new)

    def test_val_for_select(self):
        d = pq(self.html4)
        self.assertEqual(d('#first').val(), 'spam')
        self.assertEqual(d('#second').val(), 'eggs')
        self.assertIsNone(d('#third').val())
        d('#first').val('eggs')
        d('#second').val('bacon')
        d('#third').val('eggs')  # Selecting non-existing option.
        self.assertEqual(d('#first').val(), 'eggs')
        self.assertEqual(d('#second').val(), 'bacon')
        self.assertIsNone(d('#third').val())
        d('#first').val('bacon')  # Selecting non-existing option.
        self.assertEqual(d('#first').val(), 'spam')
        # Value set based on option order, not value order
        d('#second').val(['bacon', 'eggs'])
        self.assertEqual(d('#second').val(), 'eggs')
        d('#fourth').val(['spam'])
        self.assertEqual(d('#fourth').val(), 'spam')
        # Sets first option with matching value
        self.assertEqual(d('#fourth option[selected]').length, 1)
        self.assertEqual(d('#fourth option[selected]').text(), 'Spam')

    def test_val_for_select_multiple(self):
        d = pq(self.html6)
        self.assertEqual(d('#first').val(), ['spam', 'eggs'])
        # Selecting non-existing option.
        d('#first').val(['eggs', 'sausage', 'bacon'])
        self.assertEqual(d('#first').val(), ['eggs', 'bacon'])
        self.assertEqual(d('#second').val(), [])
        d('#second').val('eggs')
        self.assertEqual(d('#second').val(), ['eggs'])
        d('#second').val(['not spam', 'not eggs'])
        self.assertEqual(d('#second').val(), [])
        d('#third').val(['spam'])
        self.assertEqual(d('#third').val(), ['spam', 'spam', 'spam'])

    def test_val_for_input_and_textarea_given_array_value(self):
        d = pq('<input type="text">')
        d('input').val(['spam', 'eggs'])
        self.assertEqual(d('input').val(), 'spam,eggs')
        d = pq('<textarea></textarea>')
        d('textarea').val(['spam', 'eggs'])
        self.assertEqual(d('textarea').val(), 'spam,eggs')

    def test_val_for_multiple_elements(self):
        d = pq(self.html5)
        # "Get" returns *first* value.
        self.assertEqual(d('div > *').val(), 'spam')
        # "Set" updates *every* value.
        d('div > *').val('42')
        self.assertEqual(d('#first').val(), '42')
        self.assertEqual(d('#second').val(), '42')
        self.assertEqual(d('#third').val(), '42')

    def test_val_checkbox_no_value_attribute(self):
        d = pq('<input type="checkbox">')
        self.assertEqual(d.val(), 'on')
        d = pq('<input type="checkbox" value="">')
        self.assertEqual(d.val(), '')

    def test_val_radio_no_value_attribute(self):
        d = pq('<input type="radio">')
        self.assertEqual(d.val(), 'on')

    def test_val_value_is_empty_string(self):
        d = pq('<input value="">')
        self.assertEqual(d.val(), '')

    def test_val_input_has_no_value_attr(self):
        d = pq('<input>')
        self.assertEqual(d.val(), '')

    def test_html_replacement(self):
        html = '<div>Not Me<span>Replace Me</span>Not Me</div>'
        replacement = 'New <em>Contents</em> New'
        expected = html.replace('Replace Me', replacement)

        d = pq(html)
        d.find('span').html(replacement)

        new_html = d.outerHtml()
        self.assertEqual(new_html, expected)
        self.assertIn(replacement, new_html)


class TestAjax(TestCase):

    html = '''
    <div id="div">
    <input form="dispersed" name="order" value="spam">
    </div>
    <form id="dispersed">
    <div><input name="order" value="eggs"></div>
    <input form="dispersed" name="order" value="ham">
    <input form="other-form" name="order" value="nothing">
    <input form="" name="order" value="nothing">
    </form>
    <form id="other-form">
    <input form="dispersed" name="order" value="tomato">
    </form>
    <form class="no-id">
    <input form="dispersed" name="order" value="baked beans">
    <input name="spam" value="Spam">
    </form>
    '''

    html2 = '''
    <form id="first">
    <input name="order" value="spam">
    <fieldset>
    <input name="fieldset" value="eggs">
    <input id="input" name="fieldset" value="ham">
    </fieldset>
    </form>
    <form id="datalist">
    <datalist><div><input name="datalist" value="eggs"></div></datalist>
    <input type="checkbox" name="checkbox" checked>
    <input type="radio" name="radio" checked>
    </form>
    '''

    html3 = '''
    <form>
    <input name="order" value="spam">
    <input id="noname" value="sausage">
    <fieldset disabled>
    <input name="order" value="sausage">
    </fieldset>
    <input name="disabled" value="ham" disabled>
    <input type="submit" name="submit" value="Submit">
    <input type="button" name="button" value="">
    <input type="image" name="image" value="">
    <input type="reset" name="reset" value="Reset">
    <input type="file" name="file" value="">
    <button type="submit" name="submit" value="submit"></button>
    <input type="checkbox" name="spam">
    <input type="radio" name="eggs">
    </form>
    '''

    html4 = '''
    <form>
    <input name="spam" value="Spam/
spam">
    <select name="order" multiple>
    <option value="baked
beans" selected>
    <option value="tomato" selected>
    <option value="spam">
    </select>
    <textarea name="multiline">multiple
lines
of text</textarea>
    </form>
    '''

    def test_serialize_pairs_form_id(self):
        d = pq(self.html)
        self.assertEqual(d('#div').serialize_pairs(), [])
        self.assertEqual(d('#dispersed').serialize_pairs(), [
            ('order', 'spam'), ('order', 'eggs'), ('order', 'ham'),
            ('order', 'tomato'), ('order', 'baked beans'),
        ])
        self.assertEqual(d('.no-id').serialize_pairs(), [
            ('spam', 'Spam'),
        ])

    def test_serialize_pairs_form_controls(self):
        d = pq(self.html2)
        self.assertEqual(d('fieldset').serialize_pairs(), [
            ('fieldset', 'eggs'), ('fieldset', 'ham'),
        ])
        self.assertEqual(d('#input, fieldset, #first').serialize_pairs(), [
            ('order', 'spam'), ('fieldset', 'eggs'), ('fieldset', 'ham'),
            ('fieldset', 'eggs'), ('fieldset', 'ham'), ('fieldset', 'ham'),
        ])
        self.assertEqual(d('#datalist').serialize_pairs(), [
            ('datalist', 'eggs'), ('checkbox', 'on'), ('radio', 'on'),
        ])

    def test_serialize_pairs_filter_controls(self):
        d = pq(self.html3)
        self.assertEqual(d('form').serialize_pairs(), [
            ('order', 'spam')
        ])

    def test_serialize_pairs_form_values(self):
        d = pq(self.html4)
        self.assertEqual(d('form').serialize_pairs(), [
            ('spam', 'Spam/spam'), ('order', 'baked\r\nbeans'),
            ('order', 'tomato'), ('multiline', 'multiple\r\nlines\r\nof text'),
        ])

    def test_serialize_array(self):
        d = pq(self.html4)
        self.assertEqual(d('form').serialize_array(), [
            {'name': 'spam', 'value': 'Spam/spam'},
            {'name': 'order', 'value': 'baked\r\nbeans'},
            {'name': 'order', 'value': 'tomato'},
            {'name': 'multiline', 'value': 'multiple\r\nlines\r\nof text'},
        ])

    def test_serialize(self):
        d = pq(self.html4)
        self.assertEqual(
            d('form').serialize(),
            'spam=Spam%2Fspam&order=baked%0D%0Abeans&order=tomato&'
            'multiline=multiple%0D%0Alines%0D%0Aof%20text'
        )

    def test_serialize_dict(self):
        d = pq(self.html4)
        self.assertEqual(d('form').serialize_dict(), {
            'spam': 'Spam/spam',
            'order': ['baked\r\nbeans', 'tomato'],
            'multiline': 'multiple\r\nlines\r\nof text',
        })


class TestMakeLinks(TestCase):

    html = '''
    <html>
    <div>
    <a href="/path_info">with href</a>
    <a>without href</a>
    </div>
    </html>
    '''

    def test_make_link(self):
        d = pq(self.html, parser='xml')
        d.make_links_absolute(base_url='http://example.com')
        self.assertTrue(len(d('a[href]')), 1)
        self.assertEqual(d('a[href]').attr('href'),
                         'http://example.com/path_info')


class TestHTMLParser(TestCase):
    xml = "<div>I'm valid XML</div>"
    html = '''<div class="portlet">
      <a href="/toto">TestimageMy link text</a>
      <a href="/toto2">imageMy link text 2</a>
      Behind you, a three-headed HTML&dash;Entity!
    </div>'''

    def test_parser_persistance(self):
        d = pq(self.xml, parser='xml')
        self.assertRaises(etree.XMLSyntaxError, lambda: d.after(self.html))
        d = pq(self.xml, parser='html')
        d.after(self.html)  # this should not fail

    def test_replaceWith(self):
        expected = '''<div class="portlet">
      <a href="/toto">TestimageMy link text</a>
      <a href="/toto2">imageMy link text 2</a>
      Behind you, a three-headed HTML&amp;dash;Entity!
    </div>'''
        d = pq(self.html)
        d('img').replace_with('image')
        val = d.__html__()
        assert val == expected, (repr(val), repr(expected))

    def test_replaceWith_with_function(self):
        expected = '''<div class="portlet">
      TestimageMy link text
      imageMy link text 2
      Behind you, a three-headed HTML&amp;dash;Entity!
    </div>'''
        d = pq(self.html)
        d('a').replace_with(lambda i, e: pq(e).html())
        val = d.__html__()
        assert val == expected, (repr(val), repr(expected))


class TestXMLNamespace(TestCase):
    xml = '''<?xml version="1.0" encoding="UTF-8" ?>
    <foo xmlns:bar="http://example.com/bar">
    <bar:blah>What</bar:blah>
    <idiot>123</idiot>
    <baz xmlns="http://example.com/baz" a="b">
          <subbaz/>
    </baz>
    </foo>'''

    xhtml = '''
    <html xmlns="http://www.w3.org/1999/xhtml">
    <body>
    <div>What</div>
    </body>
    </html>'''

    namespaces = {'bar': 'http://example.com/bar',
                  'baz': 'http://example.com/baz'}

    def test_selector(self):
        expected = 'What'
        d = pq(b(self.xml), parser='xml')
        val = d('bar|blah',
                namespaces=self.namespaces).text()
        self.assertEqual(repr(val), repr(expected))

    def test_selector_with_xml(self):
        expected = 'What'
        d = pq('bar|blah', b(self.xml), parser='xml',
               namespaces=self.namespaces)
        val = d.text()
        self.assertEqual(repr(val), repr(expected))

    def test_selector_html(self):
        expected = 'What'
        d = pq('blah', self.xml.split('?>', 1)[1], parser='html')
        val = d.text()
        self.assertEqual(repr(val), repr(expected))

    def test_xhtml_namespace(self):
        expected = 'What'
        d = pq(b(self.xhtml), parser='xml')
        d.xhtml_to_html()
        val = d('div').text()
        self.assertEqual(repr(val), repr(expected))

    def test_xhtml_namespace_html_parser(self):
        expected = 'What'
        d = pq(self.xhtml, parser='html')
        d.xhtml_to_html()
        val = d('div').text()
        self.assertEqual(repr(val), repr(expected))

    def test_remove_namespaces(self):
        expected = 'What'
        d = pq(b(self.xml), parser='xml').remove_namespaces()
        val = d('blah').text()
        self.assertEqual(repr(val), repr(expected))

    def test_persistent_namespaces(self):
        d = pq(b(self.xml), parser='xml', namespaces=self.namespaces)
        val = d('bar|blah').text()
        self.assertEqual(repr(val), repr('What'))

    def test_namespace_traversal(self):
        d = pq(b(self.xml), parser='xml', namespaces=self.namespaces)
        val = d('baz|subbaz').closest('baz|baz').attr('a')
        self.assertEqual(repr(val), repr('b'))


class TestWebScrapping(TestCase):

    def setUp(self):
        self.s = http.StopableWSGIServer.create(debug_app)
        self.s.wait()
        self.application_url = self.s.application_url.rstrip('/')

    def test_get(self):
        d = pq(self.application_url, {'q': 'foo'},
               method='get')
        print(d)
        self.assertIn('REQUEST_METHOD: GET', d('p').text())
        self.assertIn('q=foo', d('p').text())

    def test_post(self):
        d = pq(self.application_url, {'q': 'foo'},
               method='post')
        self.assertIn('REQUEST_METHOD: POST', d('p').text())
        self.assertIn('q=foo', d('p').text())

    def test_session(self):
        if HAS_REQUEST:
            import requests
            session = requests.Session()
            session.headers.update({'X-FOO': 'bar'})
            d = pq(self.application_url, {'q': 'foo'},
                   method='get', session=session)
            self.assertIn('HTTP_X_FOO: bar', d('p').text())
        else:
            self.skipTest('no requests library')

    def tearDown(self):
        self.s.shutdown()


class TestWebScrappingEncoding(TestCase):

    def test_get(self):
        d = pq(u'http://ru.wikipedia.org/wiki/Заглавная_страница',
               method='get')
        print(d)
        self.assertEqual(d('#pt-login').text(), u'Войти')


class TestWebScrappingTimeouts(TestCase):

    def setUp(self):
        def app(environ, start_response):
            start_response('200 OK', [('Content-Type', 'text/plain')])
            time.sleep(2)
            return [b'foobar\n']
        self.s = http.StopableWSGIServer.create(app)
        self.s.wait()
        self.application_url = self.s.application_url.rstrip('/')

    def test_get(self):
        pq(self.application_url)
        with self.assertRaises(Exception):
            pq(self.application_url, timeout=1)

    def tearDown(self):
        self.s.shutdown()
