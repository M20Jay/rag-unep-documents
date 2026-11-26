# loader: read a PDF and keep only pages that have real text
from pypdf import PdfReader


def keep_useful_pages(texts, min_chars=50):
    pages = []
    for page_num, text in enumerate(texts, start=1):
        if text and len(text.strip()) >= min_chars:
            pages.append({"page": page_num, "text": text})
    return pages


def load_pdf_pages(pdf_path, min_chars=50):
    reader = PdfReader(pdf_path)
    texts = [page.extract_text() for page in reader.pages]
    return keep_useful_pages(texts, min_chars)
