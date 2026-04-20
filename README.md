# RAG System on UNEP GEO-7 Documents
**Author:** Martin James Ng'ang'a | [github.com/M20Jay](https://github.com/M20Jay)  
**Status:** 🔨 In Progress — Week 4 of 15  
**Stack:** LaBSE · ChromaDB · FastAPI · pypdf · Docker · Render

---

## Overview

A Retrieval-Augmented Generation (RAG) system that allows users to ask natural language questions about UNEP's Global Environment Outlook 7 — a 1,244-page environmental assessment published by the United Nations Environment Programme.

The system retrieves relevant passages directly from the document rather than relying on a language model's general training knowledge.

---

## How It Works

```
INDEXING (once at startup):
1. Load UNEP GEO-7 PDF (1,244 pages)
2. Split text into 200-word chunks with 20-word overlap
3. Embed each chunk using LaBSE
4. Store embeddings and chunks in ChromaDB

QUERYING (every request):
1. User submits a question via POST /query
2. Question converted to embedding using LaBSE
3. ChromaDB retrieves 5 most similar chunks
4. Chunks returned with page references
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| LaBSE | Multilingual sentence embeddings — 109 languages |
| ChromaDB | Vector database for semantic similarity search |
| FastAPI | REST API |
| pypdf | PDF text extraction |
| Docker | Containerisation |
| Render | Deployment |

---

## How to Run Locally

```bash
git clone https://github.com/M20Jay/rag-unep-documents.git
cd rag-unep-documents

pip install -r requirements.txt

# Download UNEP GEO-7 PDF and place in data/ folder
# https://wedocs.unep.org/handle/20.500.11822/30797

uvicorn src.app:app --reload --port 8002
```

First startup indexes the full document — takes 5-10 minutes. Subsequent startups use the cached ChromaDB index.

---

## Progress

| Component | Status |
|-----------|--------|
| UNEP GEO-7 PDF loaded — 1,244 pages | ✅ Complete |
| Project structure and dependencies | ✅ Complete |
| Text chunking pipeline | ⏳ In Progress |
| LaBSE embeddings | ⏳ In Progress |
| ChromaDB vector storage | ⏳ In Progress |
| FastAPI /query endpoint | ⏳ In Progress |
| FastAPI /health endpoint | ⏳ In Progress |
| Docker containerisation | ⏳ Pending |
| Render deployment | ⏳ Pending |

---

*Part of a 15-week MLOps programme building production ML systems from scratch.*  
*Week 4 of 15 — Building in public. No shortcuts. 🇰🇪*