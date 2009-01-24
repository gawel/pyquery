# -*- coding: utf-8 -*-
try:
    from deliverance.pyref import PyReference
    from deliverance import rules
    from ajax import PyQuery as pq
except ImportError:
    pass
else:
    class PyQuery(rules.AbstractAction):
        """Python function"""
        name = 'py'
        def __init__(self, source_location, pyref):
            self.source_location = source_location
            self.pyref = pyref

        def apply(self, content_doc, theme_doc, resource_fetcher, log):
            self.pyref(pq([content_doc]), pq([theme_doc]), resource_fetcher, log)

        @classmethod
        def from_xml(cls, el, source_location):
            """Parses and instantiates the class from an element"""
            pyref = PyReference.parse_xml(
                el, source_location=source_location,
                default_function='transform')
            return cls(source_location, pyref)

    rules._actions['pyquery'] = PyQuery

    def deliverance_proxy():
        import deliverance.proxycommand
        deliverance.proxycommand.main()
