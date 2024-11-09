from zipfile import ZipFile, ZIP_DEFLATED
from collections import UserDict
import os
import pathlib
import xml.etree.ElementTree as ET

from plato.epub import Epub
from plato.metadata import DictionaryMetadata
from plato.dictionary_page import DictionaryPage, DictionaryEntry


class Dictionary(UserDict[str, DictionaryPage]):
    def __init__(
            self,
            name: str,
            author: str,
            path: pathlib.Path = pathlib.Path("./"),
            input_lang: str = "el",
            output_lang: str = "el"
        ):
        super().__init__()
        self._path = path
        self._input_lang = input_lang
        self._output_lang = output_lang
        self._current_page: str = None
        self._name = name
        self._author = author

    def _create_initial_epub(self):
        epub = Epub(
            title=self._name,
            authors=[self._author],
            language=self._input_lang
        )
        for page in self.values():
            element = page.generate()
            content = ET.tostring(element, encoding='utf-8')
            epub.add_chapter(page.get_page_name(), page.get_file_name(), content)

        epub.generate()
        filename = epub.write(self._path)
        return filename

    def _zip_folder(self, folder_path, zip_filename):
        with ZipFile(zip_filename, 'w', ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Use arcname to make the folder structure within the zip
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname=arcname)

    def _edit_metadata(self, epub_zip: pathlib.Path):
        dirname = str(epub_zip).replace(".zip", "")
        with ZipFile(epub_zip, 'r') as z:
            z.extractall(dirname)
        content_filename = pathlib.Path(dirname, "EPUB", "content.opf")
        default_namespace = "http://www.idpf.org/2007/opf"
        ET.register_namespace("", default_namespace)
        tree = ET.parse(content_filename)
        root = tree.getroot()
        metadata = root.find(f"{{{default_namespace}}}metadata")
        metadata.append(DictionaryMetadata("el", "el").to_xml())
        tree.write(content_filename, xml_declaration=True, encoding='utf-8')
        self._zip_folder(dirname, dirname + ".2.epub")

    def new_page(self, initial: str):
        initial = initial.lower()
        self._current_page = initial
        self.setdefault(initial, DictionaryPage(initial))


    def add_entry(self, word: str, definition: str, inflections: list[str] = []):
        self[self._current_page][word] = DictionaryEntry(word, definition, inflections)

    def generate(self):
        filename = self._create_initial_epub()
        self._edit_metadata(filename)
