from src.chunking.chunker import split_into_chunks

def test_chunks_overlap_by_one_word():
    chunks = split_into_chunks("a b c d e f g h i j", chunk_size=4, overlap=1)
    assert chunks == ["a b c d", "d e f g", "g h i j", "j"]

def test_empty_text_gives_no_chunks():
    assert split_into_chunks("") == []
