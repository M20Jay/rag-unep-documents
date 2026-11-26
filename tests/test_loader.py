from src.ingestion.loader import keep_useful_pages


def test_skips_empty_and_tiny_pages():
    texts = ["x " * 40, "", None, "short", "y " * 40]
    pages = keep_useful_pages(texts, min_chars=50)
    assert [p["page"] for p in pages] == [1, 5]
