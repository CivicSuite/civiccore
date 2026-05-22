from pathlib import Path
from civiccore.ingest.parsers.base import BaseParser, ParseResult
from civiccore.ingest.parsers.csv_parser import CsvParser
from civiccore.ingest.parsers.docx import DocxParser
from civiccore.ingest.parsers.email import EmailParser
from civiccore.ingest.parsers.html import HtmlParser
from civiccore.ingest.parsers.pdf import PdfParser
from civiccore.ingest.parsers.text import TextParser
from civiccore.ingest.parsers.xlsx import XlsxParser

_PARSERS: list[BaseParser] = [PdfParser(), DocxParser(), XlsxParser(), CsvParser(), EmailParser(), HtmlParser(), TextParser()]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"}

def detect_parser(file_path: Path) -> BaseParser | None:
    for parser in _PARSERS:
        if parser.can_parse(file_path):
            return parser
    return None

def is_image_file(file_path: Path) -> bool:
    return file_path.suffix.lower() in IMAGE_EXTENSIONS

__all__ = ["detect_parser", "is_image_file", "ParseResult", "BaseParser"]
