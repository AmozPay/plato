from ebooklib import epub
import pathlib

class Epub:
    def __init__(self, title: str = "The Republic", authors: list[str] = ["Plato"], language: str = "el"):
        self._title = title
        self._authors = authors
        self._language = language
        self._identifier = self._title.replace(" ", "-").lower()

    def generate(self):
        self._book = epub.EpubBook()
        self._book.set_identifier(self._identifier)
        for author in self._authors:
            self._book.add_author(author)
        self._book.set_title(self._title)
        self._book.set_language(self._language)
        self._chapters = self._generate_chapters()
        for chapter in self._chapters:
            self._book.add_item(chapter)
        self._generate_table_of_contents()
        self._style_nav()
        self._book.spine = ["nav", *self._chapters]

    def write(self, path: pathlib.Path = pathlib.Path("./")):
        filename = self._identifier + ".epub"
        filepath = pathlib.Path(path, filename)
        epub.write_epub(filepath, self._book, {})

    def _generate_chapters(self):
        c1= epub.EpubHtml(title="Chapter 1", file_name="chapter_1.xhtml", lang=self._language)
        c1.content = u"<html><body><p>Hello World!</p></body></html>"
        c2 = epub.EpubHtml(
            title="Chapter 2", file_name="chapter_2.xhtml", lang=self._language
        )
        c2.content = u"<html><body><p>My name is John Doe</p></body></html>"
        return [c1, c2]

    def _generate_table_of_contents(self):
        self._book.toc = tuple(epub.Link(chapter.file_name, chapter.title, chapter.get_id()) for chapter in self._chapters)
        self._book.add_item(epub.EpubNcx())
        self._book.add_item(epub.EpubNav())

    def _style_nav(self):
        style = """
@namespace epub "http://www.idpf.org/2007/ops";

body {
    font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
}

h2 {
     text-align: left;
     text-transform: uppercase;
     font-weight: 200;
}

ol {
        list-style-type: none;
}

ol > li:first-child {
        margin-top: 0.3em;
}


nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}


nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}

"""
        nav_css = epub.EpubItem(
            uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
        )
        self._book.add_item(nav_css)
