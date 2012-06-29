from lxml.etree import tostring
from lxml.html.soupparser import fromstring


class MarkdownConverter(object):
    def __init__(self, strip=None, keep=None):
        if strip is not None and keep is not None:
            raise ValueError('You may specify either tags to strip or tags to'
                    ' keep, but not both.')
        self.strip = strip
        self.keep = keep

    def convert(self, html):
        soup = fromstring(html)
        self.convert_tag(soup)
        return soup.text

    def convert_tag(self, node):
        text = node.text or ''

        # Convert the children first
        for el in node.findall('*'):
            self.convert_tag(el)

            convert_fn = getattr(self, 'convert_%s' % el.tag, None)
            tail = el.tail or ''
            el.tail = ''

            if convert_fn:
                text += convert_fn(el)
            else:
                text += el.text or ''

            text += tail

        node.clear()
        node.text = text

    def underline(self, text, pad_char):
        text = (text or '').rstrip()
        return '%s\n%s\n\n' % (text, pad_char * len(text)) if text else ''

    def convert_h1(self, el):
        return self.underline(el.text, '=')

    def convert_h2(self, el):
        return self.underline(el.text, '-')


def markdownify(html, strip=None, keep=None):
    converter = MarkdownConverter(strip, keep)
    return converter.convert(html)
