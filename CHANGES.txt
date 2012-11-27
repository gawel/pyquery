1.2.3
-----

Allow to pass this in .filter() callback

Add .contents() .items()

Add tox.ini

Bug fixes: fix #35 #55 #64 #66

1.2.2
-----

Fix cssselectpatch to match the newer implementation of cssselect. Fixes issue #62, #52 and #59 (Haoyu Bai)

Fix issue #37 (Caleb Burns)

1.2.1
-----

Allow to use a custom css translator.

Fix issue 44: case problem with xml documents

1.2
---

PyQuery now use `cssselect <http://pypi.python.org/pypi/cssselect>`_. See issue
43.

Fix issue 40: forward .html() extra arguments to ``lxml.etree.tostring``

1.1.1
-----

Minor release. Include test file so you can run tests from the tarball.


1.1
---

fix issues 30, 31, 32 - py3 improvements / webob 1.2+ support


1.0
---

fix issues 24

0.7
---

Python 3 compatible

Add __unicode__ method

Add root and encoding attribute

fix issues 19, 20, 22, 23 

0.6.1
------

Move README.txt at package root

Add CHANGES.txt and add it to long_description

0.6
----

Added PyQuery.outerHtml

Added PyQuery.fn

Added PyQuery.map

Change PyQuery.each behavior to reflect jQuery api


