import os
import pickle
import PyPDF2
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# CONFIG

PDF_PATH = "test_docs/sample.pdf"

VECTOR_DIR = "vector_db"
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(VECTOR_DIR, "chunks.pkl")

CHUNK_SIZE = 500
OVERLAP = 100
TOP_K = 3



# LOAD PDF

def load_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text



# CHUNK TEXT
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks



# EMBEDDING MODEL
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")



# INDEX DOCUMENT (PERSISTENT)

def index_document(pdf_path):
    print("Loading PDF...")
    text = load_pdf_text(pdf_path)

    print("Chunking text...")
    chunks = chunk_text(text)
    print(f"Total chunks: {len(chunks)}")

    model = load_embedding_model()
    print("Creating embeddings...")
    embeddings = model.encode(chunks).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs(VECTOR_DIR, exist_ok=True)

    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print("FAISS index and chunks saved to disk.")


# LOAD INDEX

def load_index():
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks



# RETRIEVAL

def retrieve(query, top_k=3):
    model = load_embedding_model()
    index, chunks = load_index()

    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    return [chunks[i] for i in indices[0]]



# MAIN (TEST)

if __name__ == "__main__":

    if not os.path.exists(INDEX_PATH):
        index_document(PDF_PATH)

    print("\n--- QUERY TEST ---\n")

    question = "What does the company do?"
    results = retrieve(question, TOP_K)

    for i, chunk in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(chunk)
