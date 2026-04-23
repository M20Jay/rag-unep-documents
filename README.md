# Week 4 — RAG System on UNEP GEO-7 Documents

**Author:** Martin James Ng'ang'a | [github.com/M20Jay](https://github.com/M20Jay)  
**Status:** 🔨 Week 4 In Progress  
**Stack:** LaBSE · ChromaDB · FastAPI · pypdf · Docker · Render

---

## Business Problem

UNEP's Global Environment Outlook 7 is a 1,244-page environmental assessment covering biodiversity, climate change, pollution, and land degradation across every region of the world. Finding specific information requires reading hundreds of pages manually.

This RAG system lets policymakers, researchers, and analysts ask natural language questions and get answers sourced directly from the document — with exact page references — in under one second.

Built on LaBSE, a Google multilingual model supporting 109 languages, the system accepts questions in any language and retrieves relevant passages from the English document natively. A question in Swahili retrieves the same passages as the same question in English.

---

## How It Works

INDEXING (once at startup):
1. Load UNEP GEO-7 PDF — 1,244 pages
2. Split text into 200-word chunks with 20-word overlap
3. Embed each chunk using LaBSE — 109 languages
4. Store 4,329 embeddings in ChromaDB

QUERYING (every request):
1. User submits a question via POST /query
2. Question converted to embedding using LaBSE
3. ChromaDB finds most semantically similar chunks
4. Retrieved chunks returned with exact page references

---

## Example

Request:
curl -X POST http://localhost:8002/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main drivers of ecosystem degradation?", "n_results": 3}'

Response:
{
  "question": "What are the main drivers of ecosystem degradation?",
  "answer": "Ecosystem degradation and biological vulnerability. Unsustainable exploitation and use of natural resources. Climate change vulnerability and extreme events...",
  "sources": ["UNEP GEO-7 — Page 358", "UNEP GEO-7 — Page 231", "UNEP GEO-7 — Page 1060"]
}

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

git clone https://github.com/M20Jay/rag-unep-documents.git
cd rag-unep-documents
pip install -r requirements.txt
uvicorn src.app:app --reload --port 8002

First startup indexes the full document — takes 5-10 minutes.
Subsequent startups use the cached ChromaDB index — ready in 30 seconds.

---

## Progress

| Component | Status |
|-----------|--------|
| UNEP GEO-7 PDF loaded — 1,244 pages | ✅ Complete |
| Project structure and dependencies | ✅ Complete |
| Text chunking — 4,329 chunks created | ✅ Complete |
| LaBSE embeddings | ✅ Complete |
| ChromaDB vector storage | ✅ Complete |
| FastAPI /query endpoint | ✅ Complete |
| FastAPI /health endpoint | ✅ Complete |
| Docker containerisation | ⏳ Pending |
| Render deployment | ⏳ Pending |

---

*Part of a 15-week MLOps programme building production ML systems from scratch.*  
*Week 4 of 15 — Building in public. No shortcuts. 🇰🇪*