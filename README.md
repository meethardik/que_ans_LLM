# que_ans_LLM — Retrieval-Augmented Q&A with LLMs ✅

A compact Python project that implements a simple RAG (Retrieval-Augmented Generation) pipeline:
- chunk PDF documents, generate embeddings (SentenceTransformers), store them in a persistent Chroma vector store, retrieve relevant chunks for a query, and generate an answer using OpenAI LLM (or via Azure Key Vault secret retrieval).
- Built with LangChain utilities, sentence-transformers, chromadb and OpenAI SDK.

---

## Table of contents
- **Quick overview**
- **Features**
- **Requirements & setup**
- **Configuration (.env and Key Vault)**
- **How it works (architecture)**
- **Usage / Examples**
- **Common tasks & troubleshooting**
- **Project structure**
- **Contributing & License**

---

## Quick overview ✨
This repository provides a small RAG pipeline:
- `summarizer.py` loads and splits PDFs into chunks.
- `EmbeddingManager.py` builds embeddings using SentenceTransformer (default: `all-MiniLM-L6-v2`).
- `VectorStore.py` persists embeddings in Chroma (`data/vector_store`).
- `RetrieverPipeline.py` finds top-k relevant chunks for a query and scores them.
- `RagUsingLLM.py` contacts an LLM to generate a final response using retrieved context.

---

## Features ✅
- PDF loading & chunking (PyMuPDF via LangChain community loader)
- Sentence-transformer embeddings (local model by default)
- Persistent vector database (Chroma)
- Retrieval + re-ranking (cosine similarity)
- LLM answer generation with OpenAI (supports retrieving key from Azure Key Vault)

---

## Requirements & setup 🔧

Prerequisites:
- Python 3.10+ recommended
- Git
- (Optional) GPU + proper PyTorch build for faster embedding generation

Install:
```bash
# create & activate venv (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
```

Notes:
- Many heavy ML libs (torch, transformers, sentence-transformers) are listed in `requirements.txt`. On some machines you may want to install the appropriate `torch` wheel for your CUDA/CPU configuration.

---

## Configuration (.env & Azure Key Vault) 🔐

Local development:
- Create a `.env` in repo root with (example):
```env
ENVIRONMENT=development
OPENAI_API_KEY=sk-xxxx...   # required if not using Key Vault
Model=gpt-4o                # or a model you want to use
```

Azure Key Vault option:
- The project can fetch the OpenAI key from Azure Key Vault by setting:
```env
KeyVault_Name=your-keyvault-name
secret_name=your-openai-secret
AZURE_TENANT_ID=...
AZURE_CLIENT_ID=...
AZURE_CLIENT_SECRET=...
```
The code uses `Infrastructure/configuration.py:GetConfiguration` to fetch the secret. If both Key Vault and `OPENAI_API_KEY` are not available, `RagUsingLLM.generate_response_using_llm()` will raise an error.

Environment variables summary:
- `OPENAI_API_KEY` — fallback API key (OpenAI)
- `KeyVault_Name`, `secret_name` — use Azure Key Vault for secret retrieval
- `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` — Key Vault credentials
- `Model` — the model name used for LLM requests
- `ENVIRONMENT=development` — loads `.env`

On Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="sk-..."
$env:Model="gpt-4o"
```

---

## How it works (high-level) 🧭
1. Load PDFs from `data/pdf` using `summarizer.load_pdf()`.
2. Split into chunks using `genreate_pdf_chunks(...)` (langchain text splitter).
3. Create embeddings for chunks with `EmbeddingManager`.
4. Initialize `VectorStore` (Chroma) and `add_documents()` to persist docs & embeddings.
5. Query flow:
   - `RetrieverPipeline.retrieve(query, top_k)` returns top chunks with similarity scores.
   - `RagUsingLLM` composes the context and calls the LLM (OpenAI client) to produce final answer.

---

## Example usage (copy-paste) 💡
Place this in `example_run.py` at project root or run interactively:

```python
from Services.summarizer import load_pdf, genreate_pdf_chunks
from Services.EmbeddingManager import EmbeddingManager
from Services.VectorStore import VectorStore
from Services.RetrieverPipeline import RetrieverPipeline
from Services.RagUsingLLM import RagUsingLLM

# 1. Load & chunk PDFs
pdf_docs = load_pdf()  # loads all PDFs in data/pdf
chunks = genreate_pdf_chunks(pdf_docs)

# 2. Build embeddings
emb_mgr = EmbeddingManager(model_name="all-MiniLM-L6-v2")
texts = [c['text'] for c in chunks]
embeddings = emb_mgr.generate_embeddings(texts)

# 3. Create vector store and persist
vs = VectorStore(collection_name="pdf_documents", persist_directory="data/vector_store", documents=chunks, embeddings=embeddings)
vs.add_documents()

# 4. Create retriever & RAG instance
retriever = RetrieverPipeline(vector_store=vs, embeddings=emb_mgr)
rag = RagUsingLLM(query="What professional skills are needed for Integration Architect?", retriever_object=retriever, top_k=3)

# 5. Generate response
result = rag.generate_response_using_llm()
print(result)
# For OpenAI response access (if using OpenAI API response object)
# print(result.choices[0].message.content)
```

---

## Common tasks & troubleshooting ⚠️

- No OpenAI key error:
  - Ensure `OPENAI_API_KEY` is set or Key Vault variables are valid.
  - For development set `ENVIRONMENT=development` + `.env`.

- Embedding model load failure:
  - Check `sentence-transformers` and `torch` installation.
  - Use CPU-compatible torch wheel if GPU not present.

- Chroma persistence issues:
  - Vector store defaults to `data/vector_store`. Make sure the process has filesystem permissions.
  - Remove `data/vector_store` to reset store (be careful — permanent).

- PDF loading:
  - PDFs must be placed under `data/pdf` and readable. PyMuPDF (`PyMuPDF`) is used.

- Model selection:
  - Set `Model` env var to any available model name you want the OpenAI client to use.

---

## File structure & what each file does 📁
- `Services/`
  - `summarizer.py` — load PDFs & split them into chunks
  - `EmbeddingManager.py` — load sentence-transformer model & create embeddings
  - `VectorStore.py` — Chroma client and add/query documents
  - `RetrieverPipeline.py` — retrieval + re-ranking logic
  - `RagUsingLLM.py` — orchestrates retrieval + LLM prompt
  - `summarizer.py` — chunking logic (text splitter)
- `Infrastructure/`
  - `configuration.py` — helper to fetch secrets from Azure Key Vault
- `Models/schema.py` — Pydantic models used for typed outputs
- `Data/` — store PDFs & Chroma DB (`data/vector_store`, `chroma.sqlite3`)
- `requirements.txt` — pinned dependencies

---

## Testing & development tips 🧪
- Use a small subset of PDFs while developing to iterate quickly.
- Use `ENVIRONMENT=development` + `.env` to avoid Key Vault during local dev.
- Keep an eye on memory usage when embedding large numbers of chunks — batch if needed.

---

## Contributing & License 🤝
- Contributions welcome — create issues or PRs.
- Add tests and keep style consistent with existing files.
- License: MIT (update if you prefer a different license).

---

## Final notes 💬
- This project is intentionally modular: swap the embedding model, LLM provider, or vector DB with minimal changes.
- If you want, I can add:
  - a CLI or small FastAPI server to expose a query endpoint,
  - tests and CI config,
  - a script to re-index `data/pdf` automatically.

---

If you want, I can now:
- generate an `example_run.py` file and a `.env.example`, or
- add a small FastAPI endpoint that exposes the RAG query functionality.

Which one would you prefer next?