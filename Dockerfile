# Week 4 — RAG System on UNEP GEO-7 Documents
# Author: Martin James Ng'ang'a | github.com/M20Jay

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/

EXPOSE 8002

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8002"]