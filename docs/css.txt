CSS
---

.. Initialize tests

    >>> from pyquery import PyQuery
    >>> p = PyQuery('<p id="hello" class="hello"><a/></p>')('p')

You can play with css classes::

    >>> p.addClass("toto")
    [<p#hello.hello.toto>]
    >>> p.toggleClass("titi toto")
    [<p#hello.hello.titi>]
    >>> p.removeClass("titi")
    [<p#hello.hello>]

Or the css style::

    >>> p.css("font-size", "15px")
    [<p#hello.hello>]
    >>> p.attr("style")
    'font-size: 15px'
    >>> p.css({"font-size": "17px"})
    [<p#hello.hello>]
    >>> p.attr("style")
    'font-size: 17px'

Same thing the pythonic way ('_' characters are translated to '-')::

    >>> p.css.font_size = "16px"
    >>> p.attr.style
    'font-size: 16px'
    >>> p.css['font-size'] = "15px"
    >>> p.attr.style
    'font-size: 15px'
    >>> p.css(font_size="16px")
    [<p#hello.hello>]
    >>> p.attr.style
    'font-size: 16px'
    >>> p.css = {"font-size": "17px"}
    >>> p.attr.style
    'font-size: 17px'


