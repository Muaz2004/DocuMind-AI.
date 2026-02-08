# rag_engine.py
import os
import pickle
from threading import Thread
import PyPDF2
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent 
VECTOR_DIR = BASE_DIR / "vector_db"
INDEX_PATH = VECTOR_DIR / "faiss.index"
CHUNKS_PATH = VECTOR_DIR / "chunks.pkl"
CHUNK_SIZE = 500
OVERLAP = 100
TOP_K = 3

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def index_document(pdf_path):
    print(f"📄 Indexing PDF: {pdf_path}")

    # Load PDF
    text = load_pdf_text(pdf_path)
    new_chunks = chunk_text(text)
    print(f"🧩 Chunks created: {len(new_chunks)}")

    # Create embeddings
    new_embeddings = embedding_model.encode(new_chunks, batch_size=32).astype("float32")

    # Ensure vector directory exists
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Vector DB folder: {VECTOR_DIR.resolve()}")

    # Load or create index
    if INDEX_PATH.exists() and CHUNKS_PATH.exists():
        print("➕ Existing index found. Appending data...")
        index = faiss.read_index(str(INDEX_PATH))
        with open(CHUNKS_PATH, "rb") as f:
            all_chunks = pickle.load(f)
    else:
        print("🆕 No index found. Creating new one...")
        dim = new_embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        all_chunks = []

    # Append new embeddings and chunks
    index.add(new_embeddings)
    all_chunks.extend(new_chunks)

    # Save index and chunks
    faiss.write_index(index, str(INDEX_PATH))
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"✅ Index saved. Total chunks: {len(all_chunks)}")

def async_index(pdf_path):
    Thread(target=index_document, args=(pdf_path,)).start()

# RETRIEVAL 
def load_index():
    if not INDEX_PATH.exists() or not CHUNKS_PATH.exists():
        raise Exception("Index not ready. Upload PDF first.")
    index = faiss.read_index(str(INDEX_PATH))
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def retrieve_top_chunks(query, top_k=TOP_K):
    index, chunks = load_index()
    query_embedding = embedding_model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)
    results = [chunks[i] for i in indices[0] if i < len(chunks)]
    return results

#  ANSWER ORGANIZER 
def organize_answer(chunks):
    return "\n\n".join(chunks) if chunks else "No relevant content found."
