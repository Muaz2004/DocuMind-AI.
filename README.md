 Documind AI

Documind AI is a fully local RAG (Retrieval-Augmented Generation) system that lets users upload PDFs and ask questions based on their content.

No OpenAI. No paid APIs. Everything runs locally.

 What It Does

Upload multiple PDF files

Extract and chunk text

Create local embeddings

Store vectors in FAISS (append mode, no overwrite)

Ask questions and retrieve relevant answers from PDFs

 How It Works (Simple)

User uploads a PDF

PDF → text → chunks

Chunks → embeddings (local model)

Embeddings saved in FAISS (vector_db/)

User asks a question

Question is embedded

FAISS finds top-K similar chunks

Chunks are returned as the answer

🛠 Tech Stack

Django

FAISS

SentenceTransformers (all-MiniLM-L6-v2)

PyPDF2

Local filesystem storage

📁 Key Folders
media/uploads/     # Uploaded PDFs
vector_db/         # FAISS index + chunks
rag_engine.py      # RAG logic
views.py           # API endpoints

🔌 API
Upload PDF
POST /api/upload/

Ask Question
POST /api/query/

 Notes

PDFs are appended, not overwritten

Vector DB is created automatically

Works fully offline after setup
