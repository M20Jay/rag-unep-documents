# RAG System on UNEP GEO-7 Documents
**Author:** Martin James Ng'ang'a | [github.com/M20Jay](https://github.com/M20Jay)  
**Status:** 🔨 In Progress — Week 4 of 15  
**Stack:** LaBSE · ChromaDB · FastAPI · pypdf · Docker · Render

---

## What This Is

A Retrieval-Augmented Generation (RAG) system built on UNEP's Global Environment Outlook 7 — the United Nations Environment Programme's flagship assessment of the state of the global environment.

Instead of asking a general language model about environmental topics and receiving approximate answers, this system retrieves the exact passages from UNEP's own 1,244-page published research to answer questions about biodiversity loss, climate change, pollution, and land degradation.

> *"I built a RAG system on UNEP's own documents. You can ask it questions about UNEP's findings on biodiversity loss, pollution, or climate change and it retrieves the precise passages from your own published research to answer. That is not a toy. That is a prototype of exactly the kind of tool a Chief Digital Office should be building to make institutional knowledge accessible at scale."*

---

## Why UNEP Documents Specifically

UNEP publishes some of the most complex, multilingual, domain-specific documents in the world. The GEO-7 assessment covers all six UNEP strategic themes and is published in the six official UN languages. This makes it a genuinely challenging and meaningful test case for a multilingual retrieval system — not a toy dataset.

The choice of LaBSE (Language-agnostic BERT Sentence Embeddings) is deliberate. LaBSE supports 109 languages including all six UN official languages, enabling cross-lingual retrieval without translation. A query in French retrieves relevant passages from the English document natively.

---

## Live API

> **Deployment pending — will be live by end of week.**

### Health Check
```bash
curl https://rag-unep-documents.onrender.com/health
```

### Ask a Question
```bash
curl -X POST "https://rag-unep-documents.onrender.com/query" \
-H "Content-Type: application/json" \
-d '{
  "question": "What does UNEP say about biodiversity loss in Africa?",
  "n_results": 3
}'
```

### Example Response
```json
{
  "question": "What does UNEP say about biodiversity loss in Africa?",
  "answer": "...retrieved passages from UNEP GEO-7...",
  "sources": [
    "UNEP GEO-7 — Page 312",
    "UNEP GEO-7 — Page 318",
    "UNEP GEO-7 — Page 445"
  ]
}
```

---

## How It Works

### The RAG Architecture

```
INDEXING (done once at startup):
1. Load UNEP GEO-7 PDF (1,244 pages)
2. Extract text page by page
3. Split into 200-word chunks with 20-word overlap
4. Convert each chunk to a vector embedding using LaBSE
5. Store embeddings + chunks in ChromaDB

QUERYING (every request):
1. User sends a question via POST /query
2. Question converted to embedding using LaBSE
3. ChromaDB finds 5 most semantically similar chunks
4. Retrieved chunks returned with page references
5. Response is grounded in UNEP's actual documents
```

### Why LaBSE

LaBSE was developed by Google and supports 109 languages. For a UNEP system this matters because UNEP documents are published in English, French, Spanish, Arabic, Russian, and Chinese. LaBSE embeds queries and documents in a shared multilingual semantic space — cross-lingual retrieval works natively without translation.

### Why ChromaDB

ChromaDB is a vector database designed specifically for similarity search. Unlike PostgreSQL which searches by exact match, ChromaDB finds documents by semantic meaning. A query about "water contamination" retrieves chunks about "river pollution" because their vector embeddings are mathematically close — even though the exact words differ.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| LaBSE | Multilingual sentence embeddings — 109 languages |
| ChromaDB | Vector database for semantic similarity search |
| FastAPI | REST API for live document querying |
| pypdf | PDF text extraction from UNEP GEO-7 |
| Docker | Containerisation |
| Render | Cloud deployment |

---

## Document

**UNEP Global Environment Outlook 7 (GEO-7)**  
Published: 2022  
Pages: 1,244  
Coverage: Climate change · Biodiversity · Pollution · Land degradation · Freshwater · Oceans  
Source: [wedocs.unep.org](https://wedocs.unep.org)

---

## How to Run Locally

```bash
# Clone the repo
git clone https://github.com/M20Jay/rag-unep-documents.git
cd rag-unep-documents

# Install dependencies
pip install -r requirements.txt

# Add the UNEP GEO-7 PDF to data/ folder
# Download from: https://wedocs.unep.org/handle/20.500.11822/30797

# Run the API
uvicorn src.app:app --reload --port 8002

# The system indexes the document on first startup
# Takes 5-10 minutes for 1,244 pages
# Subsequent startups use the cached ChromaDB index
```

---

## Connection to UNEP's Mission

This system is a direct prototype of a tool UNEP's Chief Digital Office could build to make UNEP's institutional knowledge accessible at scale. Staff, partners, and member states could query 50 years of UNEP research in natural language — in any of the six official UN languages — and receive answers grounded in UNEP's own published documents.

---

## Progress

| Component | Status |
|-----------|--------|
| UNEP GEO-7 PDF — 1,244 pages loaded | ✅ Complete |
| Project structure and dependencies | ✅ Complete |
| Text chunking pipeline | ⏳ In Progress |
| LaBSE multilingual embeddings | ⏳ In Progress |
| ChromaDB vector storage | ⏳ In Progress |
| FastAPI /query endpoint | ⏳ In Progress |
| FastAPI /health endpoint | ⏳ In Progress |
| Docker containerisation | ⏳ Pending |
| Render deployment | ⏳ Pending |

---

*Part of a 15-week MLOps programme building production ML systems from scratch.*  
*Week 4 of 15 — Building in public. No shortcuts. 🇰🇪*