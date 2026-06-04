# Week 4 — RAG System on UNEP GEO-7 Documents
**Martin James Ng'ang'a · MLOps Engineer · Nairobi, Kenya 🇰🇪**
`github.com/M20Jay` · Week 4 of 15

---

## Overview

Semantic search system across a 1,244-page UNEP Global Environment Outlook (GEO-7) document. LaBSE multilingual embeddings support 109 languages — a question in Swahili retrieves the same passages as the same question in English. Returns exact page references in under one second.

**The core problem:** Finding specific information in a 1,244-page environmental assessment requires reading hundreds of pages manually. This RAG system fixes that.

---

## Final Results

| Metric | Result |
|--------|--------|
| Document | UNEP GEO-7 — 1,244 pages |
| Chunks indexed | 4,329 chunks (200 words, 20-word overlap) |
| Embedding model | LaBSE — 109 languages |
| Vector database | ChromaDB |
| First startup | 5-10 minutes (indexes full document) |
| Subsequent startups | ~30 seconds (uses cached index) |
| Repository | https://github.com/M20Jay/rag-unep-documents |

---

## 7-Day Build Plan

| Day | Task | Status |
|-----|------|--------|
| Day 1 | PDF loading + text extraction | ✅ |
| Day 2 | Text chunking — 4,329 chunks | ✅ |
| Day 3 | LaBSE embeddings + ChromaDB storage | ✅ |
| Day 4 | FastAPI /query + /health endpoints | ✅ |
| Day 5 | Idempotent indexing — skip on restart | ✅ |
| Day 6 | Docker containerisation | ✅ |
| Day 7 | README + HuggingFace dataset hosting | ✅ |

---

## Project Structure

```
rag-unep-documents/
├── data/
│   └── geo7_report.pdf         1,244-page UNEP document (HuggingFace hosted)
├── src/
│   ├── app.py                  FastAPI app — /query + /health
│   ├── indexer.py              PDF loading, chunking, embedding, ChromaDB storage
│   └── retriever.py            Semantic search — query → chunks → response
├── chroma_db/                  ChromaDB persistent storage (gitignored)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Architecture

```
INDEXING (runs once at first startup):
PDF (1,244 pages)
    ↓
pypdf → extract text page by page
    ↓
Split into 4,329 chunks
  - chunk size: 200 words
  - overlap: 20 words (preserves context at boundaries)
    ↓
LaBSE → convert each chunk to 768-dimensional vector embedding
    ↓
ChromaDB → store all 4,329 embeddings with page references
    ↓
chroma_db/ folder persists to disk

QUERYING (every request):
User submits question (any of 109 languages)
    ↓
LaBSE → convert question to same 768-dimensional vector space
    ↓
ChromaDB → cosine similarity search → top N most similar chunks
    ↓
Return chunks with exact page references
```

---

## Key Concepts

### What is RAG

```
RAG = Retrieval Augmented Generation

Traditional keyword search:
"water contamination" → misses "river pollution" even though same meaning

RAG semantic search:
"water contamination" → finds "river pollution" because vectors are similar
                      → finds "aquifer depletion" because context is related
                      → finds passages in Swahili about "uchafuzi wa maji"

How: text is converted to numbers (vectors) that capture MEANING not words
     similar meaning = similar vectors = similar position in vector space
```

### Text Chunking Strategy

```python
from pypdf import PdfReader

def load_and_chunk_pdf(pdf_path: str, chunk_size: int = 200, overlap: int = 20):
    reader = PdfReader(pdf_path)
    chunks = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue

        words = text.split()

        # Sliding window chunking
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            if len(chunk_words) < 20:  # skip tiny chunks
                continue
            chunk_text = ' '.join(chunk_words)
            chunks.append({
                'text': chunk_text,
                'page': page_num,
                'source': f'UNEP GEO-7 — Page {page_num}'
            })

    return chunks
# Result: 4,329 chunks from 1,244 pages
```

### LaBSE Embeddings

```python
from sentence_transformers import SentenceTransformer

# LaBSE — Language-agnostic BERT Sentence Embeddings
# Google model — 109 languages — 1.88GB
model = SentenceTransformer('sentence-transformers/LaBSE')

# Embed chunks — each chunk becomes a 768-dimensional vector
texts = [chunk['text'] for chunk in chunks]
embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)
# Takes 5-10 minutes for 4,329 chunks on first run

# Key property: same meaning = similar vector regardless of language
# "water pollution" ≈ "uchafuzi wa maji" ≈ "contaminación del agua"
```

### ChromaDB Vector Storage

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="unep_geo7",
    metadata={"hnsw:space": "cosine"}  # cosine similarity
)

# Store embeddings with metadata
collection.add(
    ids=[str(i) for i in range(len(chunks))],
    embeddings=embeddings.tolist(),
    documents=[chunk['text'] for chunk in chunks],
    metadatas=[{'source': chunk['source'], 'page': chunk['page']} for chunk in chunks]
)
```

### Idempotent Indexing

```python
def index_if_needed(collection, chunks, model):
    # Check if already indexed
    existing_count = collection.count()

    if existing_count >= len(chunks):
        print(f"Already indexed {existing_count} chunks — skipping")
        return  # idempotent — safe to call multiple times

    print(f"Indexing {len(chunks)} chunks...")
    # ... embed and store
    print("Indexing complete")

# Idempotency means:
# First startup:  indexes 4,329 chunks → stores to chroma_db/
# Second startup: finds 4,329 chunks → skips → ready in 30s
# Third startup:  finds 4,329 chunks → skips → ready in 30s
# Running multiple times = same result as running once
```

### Semantic Query

```python
def query(question: str, n_results: int = 3):
    # Embed the question in the same vector space as the chunks
    question_embedding = model.encode([question])

    # Find most similar chunks by cosine similarity
    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=n_results
    )

    return {
        "question": question,
        "answer": " ".join(results['documents'][0]),
        "sources": results['metadatas'][0]
    }
```

### FastAPI Endpoints

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    n_results: int = 3

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "chunks_indexed": collection.count()  # 4,329 when ready
    }

@app.post("/query")
def query_endpoint(request: QueryRequest):
    return query(request.question, request.n_results)
```

---

## Example Usage

```bash
# Health check — confirms 4,329 chunks indexed
curl -s http://localhost:8002/health | python3 -m json.tool
# {
#   "status": "healthy",
#   "chunks_indexed": 4329
# }

# Query in English
curl -s -X POST http://localhost:8002/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main drivers of ecosystem degradation?", "n_results": 3}' \
  | python3 -m json.tool
# {
#   "question": "What are the main drivers of ecosystem degradation?",
#   "answer": "primarily driven by land-use change, pollution and climate change...",
#   "sources": ["UNEP GEO-7 — Page 324", "UNEP GEO-7 — Page 158", "UNEP GEO-7 — Page 54"]
# }

# Query in Swahili — same results
curl -s -X POST http://localhost:8002/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Ni nini kinachosababisha uharibifu wa mfumo wa ikolojia?", "n_results": 3}' \
  | python3 -m json.tool
```

---

## CLI Reference

### Run Locally

```bash
# Clone and install
git clone https://github.com/M20Jay/rag-unep-documents.git
cd rag-unep-documents
pip install -r requirements.txt

# Start API — first run takes 5-10 minutes to index
uvicorn src.app:app --reload --port 8002

# Subsequent runs — 30 seconds (cached index)
uvicorn src.app:app --reload --port 8002
```

### Docker Commands

```bash
# Build and start
docker compose up --build -d

# Check logs — watch indexing progress
docker compose logs api -f

# Check indexing complete
curl -s http://localhost:8002/health | python3 -m json.tool
# chunks_indexed: 4329 = ready

# Stop
docker compose down

# Note: chroma_db/ volume persists index across restarts
```

### Check Index Status

```python
# Verify ChromaDB has all chunks
python3 -c "
import chromadb
client = chromadb.PersistentClient(path='./chroma_db')
collection = client.get_collection('unep_geo7')
print(f'Chunks indexed: {collection.count()}')
# Should print: Chunks indexed: 4329
"
```

---

## Debugging Reference

### Common Errors and Fixes

| Error | Fix |
|-------|-----|
| `OOM / killed` during indexing | LaBSE needs 1GB+ RAM. Reduce `batch_size` to 8 in `model.encode()` |
| `chunks_indexed: 0` after restart | ChromaDB volume not mounted — check `docker-compose.yml` volumes |
| `Collection not found` | First run didn't complete — delete `chroma_db/` and restart |
| `Render 512MB OOM` | LaBSE (1.88GB) exceeds Render free tier — use AWS EC2 with 1GB+ RAM |
| `Slow queries` | Normal — first query loads model into memory. Subsequent queries fast |
| `Wrong language results` | LaBSE is multilingual — this is expected behaviour, not a bug |

### Debugging Order

```
1. Check health endpoint: curl http://localhost:8002/health
2. Confirm chunks_indexed: 4329 — if 0, indexing failed
3. Check logs: docker compose logs api --tail=100
4. Check ChromaDB folder exists: ls -lh chroma_db/
5. Check RAM available: free -h — LaBSE needs 1GB+
```

---

## Why Render Failed — Engineering Decision

```
LaBSE model size:     1.88GB
Render free tier RAM: 512MB
Result:               OOM crash at startup

Decision: do NOT swap LaBSE for a smaller model just to get a live URL

Why: smaller models (e.g. all-MiniLM-L6-v2) lose multilingual capability
     The 109-language support is the core value proposition
     A system that works in English only defeats the purpose

The architecture is correct. The deployment environment was wrong.
AWS EC2 t3.small (2GB RAM) runs LaBSE correctly.
Week 10 will deploy this to production on AWS.

This is what separates junior from senior:
knowing when NOT to compromise your architecture.
```

---

## Key Learnings from Week 4

- **Semantic search vs keyword search** — vectors capture meaning, not words — "water contamination" finds "river pollution"
- **Chunking overlap matters** — 20-word overlap preserves context at chunk boundaries — without overlap you lose sentences split across chunks
- **Idempotency is critical** — index once, use forever — never re-index on every restart
- **LaBSE is language-agnostic** — same vector space for 109 languages — multilingual by design not by translation
- **ChromaDB persistence** — use `PersistentClient` not in-memory client — data survives restarts
- **Don't compromise architecture for deployment** — the correct decision was to keep LaBSE and wait for proper infrastructure

---

*Week 4 of 15 · RAG Document Search System · Built in Nairobi, Kenya 🇰🇪*
*Repository: https://github.com/M20Jay/rag-unep-documents · Full production system: Week 12*
