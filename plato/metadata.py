import xml.etree.ElementTree as ET

class DictionaryMetadata:
    def __init__(self, input_lang: str, output_lang: str):
        self._input_lang = input_lang
        self._output_lang = output_lang

    def _create_element_with_text(self, tag, text):
        element = ET.Element(tag)
        element.text = text
        return element

    def to_xml(self):
        root = ET.Element("x-metadata")
        for element in [
          self._create_element_with_text("DictionaryInLanguage", self._input_lang),
          self._create_element_with_text("DictionaryOutLanguage", self._output_lang),
          self._create_element_with_text("DefaultLookupIndex", "Ελληνικά")
        ]:
            root.append(element)
        return root
