# Week 4 — RAG System on UNEP GEO-7 Documents

**Author:** Martin James Ng'ang'a | [github.com/M20Jay](https://github.com/M20Jay)  
**Status:** ✅ Week 4 Complete — Local API confirmed working — AWS deployment in progress  
**Stack:** LaBSE · ChromaDB · FastAPI · pypdf · Docker · Render
## The Problem

1,244 pages. One question.

A policymaker preparing for a briefing on biodiversity loss doesn't have time to read UNEP's entire GEO-7 assessment — they need the three paragraphs that actually answer their question, with the page number to back it up in the room.

Most document search tools give you a keyword match. This one gives you an answer — sourced, page-referenced, in under a second — because a paraphrase without a citation is not something a policymaker can defend in a meeting.

**The harder problem underneath it:** UNEP operates across regions where English isn't the working language, but nearly every document search tool is built as if it is. A Swahili-speaking analyst using a keyword search tool built for English gets a materially worse experience than an English-speaking one — not because the information isn't there, but because the *tool* can't reach it in their language.

This system is built on **LaBSE**, a multilingual model trained across 109 languages, so a question asked in Swahili retrieves the *same* passages as the same question asked in English — no translation layer, no quality drop, native retrieval either way.



## Where This Fits

Answering a question about a policy document isn't the end goal — it's an input into decisions that require citation, not just an answer:

- **Policy briefing and decision support** — a policymaker preparing for a meeting needs a sourced, page-referenced answer they can defend, not a paraphrase they can't trace back to the original document.
- **Multilingual institutional access** — UNEP and similar bodies operate across regions where English isn't the working language. Native multilingual retrieval means a Swahili-speaking analyst gets the same access as an English-speaking one, without a separate translation step that introduces error or delay.
- **Research and citation workflows** — researchers building on GEO-7 findings need exact page references to cite correctly, not a summary that has to be manually re-verified against the source.
- **Institutional knowledge base integration** — a single 1,244-page document is one instance of a much larger pattern: any organization with dense, authoritative documents (regulatory filings, technical standards, legal texts) has the same retrieval problem.
- **Feedback loop** — which questions get asked most, and which retrieved passages get flagged as unhelpful, is the real signal that should refine retrieval quality over time.

This is currently a standalone query system — the natural next integration is embedding it into an institution's existing knowledge management or policy-support tooling, rather than requiring users to access it as a separate destination.


---

## Architecture

INDEXING (once at startup):
1. Load PDF — 1,244 pages
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
  "answer": "primarily driven by land-use change, pollution and climate change. effect of climate warming on land ecosystems as carbon sinks. global plant and animal extinctions.",
  "sources": ["UNEP GEO-7 — Page 324", "UNEP GEO-7 — Page 158", "UNEP GEO-7 — Page 54"]
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
| AWS | Cloud deployment — in progress |

---

## How to Run Locally

git clone https://github.com/M20Jay/rag-unep-documents.git
cd rag-unep-documents
pip install -r requirements.txt
uvicorn src.app:app --reload --port 8002

First startup indexes the full document — takes 5-10 minutes.
Subsequent startups use the cached ChromaDB index — ready in 30 seconds.

---

## Deployment Note

LaBSE is a 1.88GB multilingual model. Render's free tier provides 512MB RAM — insufficient to load LaBSE at runtime. The architecture is correct and intentional. AWS deployment is in progress — LaBSE runs correctly on instances with 1GB+ RAM.

---

## Progress

| Component | Status |
|-----------|--------|
| PDF loaded — 1,244 pages | ✅ Complete |
| Project structure and dependencies | ✅ Complete |
| Text chunking — 4,329 chunks created | ✅ Complete |
| LaBSE embeddings | ✅ Complete |
| ChromaDB vector storage | ✅ Complete |
| FastAPI /query endpoint | ✅ Complete |
| FastAPI /health endpoint | ✅ Complete |
| Docker containerisation | ✅ Complete |
| Hugging Face dataset — 153MB PDF hosted | ✅ Complete |
| Render deployment | ❌ Insufficient RAM — LaBSE requires 1GB+ |
| AWS deployment | ⏳ In progress |

---

*Part of a 15-week MLOps programme building production ML systems from scratch.*  
*Week 4 of 15 — Building in public. No shortcuts. 🇰🇪*