import xml.sax

class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            self._pages.append((self._values['title'], self._values['text']))
            

# Object for handling xml
handler = WikiXmlHandler()

# Parsing object
parser = xml.sax.make_parser()
parser.setContentHandler(handler)



#import mwxml
#import glob


# paths = glob.glob('enwiki-20220201-pages-articles-multistream1.xml')

# def process_dump(dump, path):
#   for page in dump:
#     for revision in page:
#         yield page.id, revision.id, revision.timestamp, len(revision.text)

# def WikiReader():
#     for title, text in mwxml.map(process_dump, paths):
#         text_file = open("sample.txt", "wt")
#         n = text_file.write(text)
#         text_file.close()