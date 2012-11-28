Testing
-------

If you want to run the tests that you can see above you should do::

    $ git clone git://github.com/gawel/pyquery.git
    $ cd pyquery
    $ python bootstrap.py
    $ bin/buildout install tox
    $ bin/tox

You can build the Sphinx documentation by doing::

    $ cd docs
    $ make html
