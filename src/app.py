# ── RAG System on UNEP GEO-7 Documents ──────────────────────────
# Author: Martin James Ng'ang'a | github.com/M20Jay
# Week 4 — RAG System
# Stack: LaBSE · ChromaDB · FastAPI · pypdf

import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# ── FastAPI App ──────────────────────────────────────────────────
app = FastAPI(
    title="UNEP GEO-7 RAG API",
    description="""
    Retrieval-Augmented Generation system on UNEP's
    Global Environment Outlook 7 document.
    Built by Martin James Ng'ang'a — MLOps Engineer
    github.com/M20Jay
    """,
    version="1.0.0"
)

# ── Load Embedding Model ─────────────────────────────────────────
print("⏳ Loading LaBSE embedding model...")
embedding_model = SentenceTransformer('LaBSE')
print("✅ LaBSE model loaded")

# ── ChromaDB Setup ───────────────────────────────────────────────
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(
    name="unep_geo7",
    metadata={"description": "UNEP GEO-7 document chunks"}
)

# ── Helper: Split text into chunks ──────────────────────────────
def split_into_chunks(text: str, chunk_size: int = 200, overlap: int = 20):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ── Index the PDF ────────────────────────────────────────────────
def index_document(pdf_path: str):
    if collection.count() > 0:
        print(f"✅ Already indexed — {collection.count()} chunks")
        return

    print(f"⏳ Reading PDF: {pdf_path}")
    reader = PdfReader(pdf_path)
    print(f"✅ PDF loaded — {len(reader.pages)} pages")

    all_chunks = []
    chunk_ids = []
    chunk_metadata = []

    print("⏳ Splitting into chunks...")
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text or len(text.strip()) < 50:
            continue
        chunks = split_into_chunks(text)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            chunk_ids.append(f"page_{page_num}_chunk_{i}")
            chunk_metadata.append({
                "page": page_num + 1,
                "source": "UNEP_GEO7"
            })

    print(f"✅ {len(all_chunks)} chunks created")

    print("⏳ Embedding chunks with LaBSE...")
    batch_size = 100
    all_embeddings = []
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        embeddings = embedding_model.encode(batch).tolist()
        all_embeddings.extend(embeddings)
        print(f"   {min(i + batch_size, len(all_chunks))}/{len(all_chunks)}")

    print("⏳ Storing in ChromaDB...")
    collection.add(
        documents=all_chunks,
        embeddings=all_embeddings,
        ids=chunk_ids,
        metadatas=chunk_metadata
    )
    print(f"✅ Indexed {collection.count()} chunks")

# ── Run indexing on startup ──────────────────────────────────────
PDF_PATH = "data/unep_geo7.pdf"
index_document(PDF_PATH)

# ── Request/Response Models ──────────────────────────────────────
class QueryRequest(BaseModel):
    question: str
    n_results: int = 5

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list

# ── Query Endpoint ───────────────────────────────────────────────
@app.post("/query", response_model=QueryResponse)
def query_document(request: QueryRequest):
    question_embedding = embedding_model.encode(
        request.question
    ).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=request.n_results
    )

    retrieved_chunks = results['documents'][0]
    metadatas = results['metadatas'][0]
    answer = "\n\n---\n\n".join(retrieved_chunks)
    sources = [f"UNEP GEO-7 — Page {m['page']}" for m in metadatas]

    return QueryResponse(
        question=request.question,
        answer=answer,
        sources=sources
    )

# ── Health Endpoint ──────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "status": "ok",
        "chunks_indexed": collection.count(),
        "embedding_model": "LaBSE",
        "document": "UNEP GEO-7"
    }