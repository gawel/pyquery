
class TextExtractionMixin():
    def _prepare_dom(self, html):
        self.last_html = '<html><body>' + html + '</body></html>'

    def _simple_test(self, html, expected_sq, expected_nosq, **kwargs):
        raise NotImplementedError

    def test_inline_tags(self):
        self._simple_test(
            'Phas<em>ell</em>us<i> eget </i>sem <b>facilisis</b> justo',
            'Phasellus eget sem facilisis justo',
            'Phasellus eget sem facilisis justo',
        )
        self._simple_test(
            'Phasellus <span> eget </span> sem <b>facilisis\n</b> justo',
            'Phasellus eget sem facilisis justo',
            'Phasellus  eget  sem facilisis\n justo',
        )
        self._simple_test(
            ('Phasellus   <span>\n  eget\n           '
             'sem\n\tfacilisis</span>   justo'),
            'Phasellus eget sem facilisis justo',
            'Phasellus   \n  eget\n           sem\n\tfacilisis   justo'
        )

    def test_block_tags(self):
        self._simple_test(
            'Phas<p>ell</p>us<div> eget </div>sem <h1>facilisis</h1> justo',
            'Phas\nell\nus\neget\nsem\nfacilisis\njusto',
            'Phas\nell\nus\n eget \nsem \nfacilisis\n justo',
        )
        self._simple_test(
            '<p>In sagittis</p> <p>rutrum</p><p>condimentum</p>',
            'In sagittis\nrutrum\ncondimentum',
            'In sagittis\n \nrutrum\n\ncondimentum',
        )
        self._simple_test(
            'In <p>\nultricies</p>\n erat et <p>\n\n\nmaximus\n\n</p> mollis',
            'In\nultricies\nerat et\nmaximus\nmollis',
            'In \n\nultricies\n\n erat et \n\n\n\nmaximus\n\n\n mollis',
        )
        self._simple_test(
            ('Integer <div><div>\n  <div>quis commodo</div></div> '
             '</div> libero'),
            'Integer\nquis commodo\nlibero',
            'Integer \n\n\n  \nquis commodo\n\n \n libero',
        )
        self._simple_test(
            'Heading<ul><li>one</li><li>two</li><li>three</li></ul>',
            'Heading\none\ntwo\nthree',
            'Heading\n\none\n\ntwo\n\nthree',
        )

    def test_separators(self):
        self._simple_test(
            'Some words<br>test. Another word<br><br> <br> test.',
            'Some words\ntest. Another word\n\n\ntest.',
            'Some words\ntest. Another word\n\n \n test.',
        )
        self._simple_test(
            'Inline <span>  splitted by\nbr<br>tag</span> test',
            'Inline splitted by br\ntag test',
            'Inline   splitted by\nbr\ntag test',
        )
        self._simple_test(
            'Some words<hr>test. Another word<hr><hr> <hr> test.',
            'Some words\ntest. Another word\ntest.',
            'Some words\n\ntest. Another word\n\n\n\n \n\n test.',
        )

    def test_strip(self):
        self._simple_test(
            ' text\n',
            'text',
            ' text\n',
        )

    def test_ul_li(self):
        self._simple_test(
            '<ul> <li>  </li> </ul>',
            '',
            ' \n  \n '
        )
