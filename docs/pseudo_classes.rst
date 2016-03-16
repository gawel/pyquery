=========================
Using pseudo classes
=========================


:button
==================

Matches all button input elements and the button element::

        >>> from pyquery import PyQuery
        >>> d = PyQuery(('<div><input type="button"/>'
        ...          '<button></button></div>'))
        >>> d(':button')
        [<input>, <button>]



:checkbox
==================

Matches all checkbox input elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input type="checkbox"/></div>')
        >>> d('input:checkbox')
        [<input>]



:checked
==================

Matches odd elements, zero-indexed::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input checked="checked"/></div>')
        >>> d('input:checked')
        [<input>]



:child
==================

right is an immediate child of left

:contains()
==================

Matches all elements that contain the given text

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><h1/><h1 class="title">title</h1></div>')
        >>> d('h1:contains("title")')
        [<h1.title>]



:descendant
==================

right is a child, grand-child or further descendant of left

:disabled
==================

Matches all elements that are disabled::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input disabled="disabled"/></div>')
        >>> d('input:disabled')
        [<input>]



:empty
==================

Match all elements that do not contain other elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><h1><span>title</span></h1><h2/></div>')
        >>> d(':empty')
        [<h2>]



:enabled
==================

Matches all elements that are enabled::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input value="foo" /></div>')
        >>> d('input:enabled')
        [<input>]



:eq()
==================

Matches a single element by its index::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><h1 class="first"/><h1 class="last"/></div>')
        >>> d('h1:eq(0)')
        [<h1.first>]
        >>> d('h1:eq(1)')
        [<h1.last>]



:even
==================

Matches even elements, zero-indexed::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><p></p><p class="last"></p></div>')
        >>> d('p:even')
        [<p>]



:file
==================

Matches all input elements of type file::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input type="file"/></div>')
        >>> d('input:file')
        [<input>]



:first
==================

Matches the first selected element::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><p class="first"></p><p></p></div>')
        >>> d('p:first')
        [<p.first>]



:gt()
==================

Matches all elements with an index over the given one::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><h1 class="first"/><h1 class="last"/></div>')
        >>> d('h1:gt(0)')
        [<h1.last>]



:has()
==================
Matches elements which contain at least one element that matches the
specified selector. https://api.jquery.com/has-selector/

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




:header
==================

Matches all header elelements (h1, ..., h6)::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><h1>title</h1></div>')
        >>> d(':header')
        [<h1>]



:hidden
==================

Matches all hidden input elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input type="hidden"/></div>')
        >>> d('input:hidden')
        [<input>]



:image
==================

Matches all image input elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input type="image"/></div>')
        >>> d('input:image')
        [<input>]



:input
==================

Matches all input elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery(('<div><input type="file"/>'
        ...          '<textarea></textarea></div>'))
        >>> d(':input')
        [<input>, <textarea>]



:last
==================

Matches the last selected element::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><p></p><p class="last"></p></div>')
        >>> d('p:last')
        [<p.last>]



:lt()
==================

Matches all elements with an index below the given one::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><h1 class="first"/><h1 class="last"/></div>')
        >>> d('h1:lt(1)')
        [<h1.first>]



:odd
==================

Matches odd elements, zero-indexed::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><p></p><p class="last"></p></div>')
        >>> d('p:odd')
        [<p.last>]



:parent
==================

Match all elements that contain other elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><h1><span>title</span></h1><h1/></div>')
        >>> d('h1:parent')
        [<h1>]



:password
==================

Matches all password input elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input type="password"/></div>')
        >>> d('input:password')
        [<input>]



:radio
==================

Matches all radio input elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input type="radio"/></div>')
        >>> d('input:radio')
        [<input>]



:reset
==================

Matches all reset input elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input type="reset"/></div>')
        >>> d('input:reset')
        [<input>]



:selected
==================

Matches all elements that are selected::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<select><option selected="selected"/></select>')
        >>> d('option:selected')
        [<option>]



:submit
==================

Matches all submit input elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input type="submit"/></div>')
        >>> d('input:submit')
        [<input>]



:text
==================

Matches all text input elements::

        >>> from pyquery import PyQuery
        >>> d = PyQuery('<div><input type="text"/></div>')
        >>> d('input:text')
        [<input>]


