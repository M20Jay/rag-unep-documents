# chunker: split text into overlapping pieces of words
def split_into_chunks(text: str, chunk_size: int = 200, overlap: int = 20):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks
