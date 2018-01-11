import re
import sys


PY3k = sys.version_info >= (3,)

try:
    unicode
except NameError:
    unicode = str


if PY3k:
    def is_string(s):
        return isinstance(s, str)
else:
    def is_string(s):
        return isinstance(s, (unicode, str))


# https://developer.mozilla.org/en-US/docs/Web/HTML/Inline_elements#Elements
INLINE_TAGS = {
    'a', 'abbr', 'acronym', 'b', 'bdo', 'big', 'br', 'button', 'cite',
    'code', 'dfn', 'em', 'i', 'img', 'input', 'kbd', 'label', 'map',
    'object', 'q', 'samp', 'script', 'select', 'small', 'span', 'strong',
    'sub', 'sup', 'textarea', 'time', 'tt', 'var'
}

SEPARATORS = {'br'}


# Definition of whitespace in HTML:
# https://www.w3.org/TR/html4/struct/text.html#h-9.1
WHITESPACE_RE = re.compile(u'[\x20\x09\x0C\u200B\x0A\x0D]+')


def squash_html_whitespace(text):
    # use raw extract_text for preformatted content (like <pre> content or set
    # by CSS rules)
    # apply this function on top of
    return WHITESPACE_RE.sub(' ', text)


def _squash_artifical_nl(parts):
    output, last_nl = [], False
    for x in parts:
        if x is not None:
            output.append(x)
            last_nl = False
        elif not last_nl:
            output.append(None)
            last_nl = True
    return output


def _strip_artifical_nl(parts):
    if not parts:
        return parts
    for start_idx, pt in enumerate(parts):
        if is_string(pt):
            # 0, 1, 2, index of first string [start_idx:...
            break
    iterator = enumerate(parts[:start_idx - 1 if start_idx > 0 else None:-1])
    for end_idx, pt in iterator:
        if is_string(pt):  # 0=None, 1=-1, 2=-2, index of last string
            break
    return parts[start_idx:-end_idx if end_idx > 0 else None]


def _merge_original_parts(parts):
    output, orp_buf = [], []

    def flush():
        if orp_buf:
            item = squash_html_whitespace(''.join(orp_buf)).strip()
            if item:
                output.append(item)
            orp_buf[:] = []

    for x in parts:
        if not is_string(x):
            flush()
            output.append(x)
        else:
            orp_buf.append(x)
    flush()
    return output


def extract_text_array(dom, squash_artifical_nl=True, strip_artifical_nl=True):
    if callable(dom.tag):
        return ''
    r = []
    if dom.tag in SEPARATORS:
        r.append(True)  # equivalent of '\n' used to designate separators
    elif dom.tag not in INLINE_TAGS:
        # equivalent of '\n' used to designate artifically inserted newlines
        r.append(None)
    if dom.text is not None:
        r.append(dom.text)
    for child in dom.getchildren():
        r.extend(extract_text_array(child, squash_artifical_nl=False,
                                    strip_artifical_nl=False))
        if child.tail is not None:
            r.append(child.tail)
    if dom.tag not in INLINE_TAGS and dom.tag not in SEPARATORS:
        # equivalent of '\n' used to designate artifically inserted newlines
        r.append(None)
    if squash_artifical_nl:
        r = _squash_artifical_nl(r)
    if strip_artifical_nl:
        r = _strip_artifical_nl(r)
    return r


def extract_text(dom, block_symbol='\n', sep_symbol='\n', squash_space=True):
    a = extract_text_array(dom, squash_artifical_nl=squash_space)
    if squash_space:
        a = _strip_artifical_nl(_squash_artifical_nl(_merge_original_parts(a)))
    result = ''.join(
        block_symbol if x is None else (
            sep_symbol if x is True else x
        )
        for x in a
    )
    if squash_space:
        result = result.strip()
    return result
