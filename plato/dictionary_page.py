from collections import UserDict
import xml.etree.ElementTree as ET

class DictionaryEntry:
    _id_counter: int = 0

    def __init__(self, word: str, definition: str, inflections: list[str] = []):
        self._word = word
        self._definition = definition
        self._inflections = inflections
        self._id = self._id_counter
        self._id_counter += 1

    def __str__(self):
        return self._definition

    def __repr__(self):
        return f"'{self._definition}'"

    def generate(self):
        entry = ET.Element(
            "idx:entry",
            {
                "scriptable": "yes",
                "spell": "yes",
                "name": "Ελληνικά",
                "id": str(self._id),
            },
        )
        short = ET.Element("idx:short")
        link = ET.Element("a", {"id": str(self._id)})
        orth = ET.Element("idx:orth", {"value": self._word})
        title = ET.Element("b")
        title.text = self._word
        orth.append(title)
        short.append(link)
        short.append(orth)
        definition = ET.Element("p")
        definition.text = self._definition
        short.append(definition)
        entry.append(short)
        return entry


class DictionaryPage(UserDict[str, DictionaryEntry]):
    def __init__(self, initial: str):
        super().__init__()
        self._initial = initial.lower()

    def get_file_name(self):
        return self._initial + ".xhtml"

    def get_page_name(self):
        return self._initial

    def _html_root(self):
        root = ET.Element("html", {
            "xmlns:math": "http://exslt.org/math",
            "xmlns:svg": "http://www.w3.org/2000/svg",
            "xmlns:tl": "https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf",
            "xmlns:saxon": "http://saxon.sf.net/",
            "xmlns:xs": "http://www.w3.org/2001/XMLSchema",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:cx": "https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf",
            "xmlns:dc": "http://purl.org/dc/elements/1.1/",
            "xmlns:mbp": "https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf",
            "xmlns:mmc": "https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf",
            "xmlns:idx": "https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"
        })
        return root

    def _head(self):
        head = ET.Element("head")
        meta = ET.Element("meta", {
            "http-equiv": "Content-Type",
            "content": "text/html; charset=utf-8"
        })
        head.append(meta)
        return head

    def generate(self):
        print(f"Generating entries for page '{self._initial}'")
        html_root = self._html_root()
        body = ET.Element("body")
        frameset = ET.Element("mbp:frameset")
        for title, entry in self.items():
            print(f"{title}")
            frameset.append(entry.generate())
        body.append(frameset)
        html_root.append(self._head())
        html_root.append(body)
        print(ET.tostring(html_root))
        return html_root
