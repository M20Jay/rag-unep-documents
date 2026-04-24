# Week 4 — RAG System on UNEP GEO-7 Documents
# Author: Martin James Ng'ang'a | github.com/M20Jay
# Build: v5 — Hugging Face PDF download

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/data &&     wget --no-check-certificate     -O /app/data/unep_geo7.pdf     "https://huggingface.co/datasets/MartinJayMLOps/unep-geo7/resolve/main/unep_geo7.pdf"

COPY src/ ./src/

EXPOSE 8002

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8002"]
