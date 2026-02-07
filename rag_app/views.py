# views.py
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from rag_app.services.rag_engine import async_index, retrieve_top_chunks, organize_answer

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------- UPLOAD PDF ----------------
@csrf_exempt
def upload_pdf(request):
    if request.method == "POST" and request.FILES.get("pdf"):
        pdf_file = request.FILES["pdf"]
        saved_path = default_storage.save(f"uploads/{pdf_file.name}", pdf_file)

        # Start indexing in background
        async_index(saved_path)

        return JsonResponse({"status": "PDF uploaded. Indexing started (append mode)."})
    return JsonResponse({"error": "No PDF uploaded"}, status=400)

# ---------------- QUERY ----------------
@csrf_exempt
def query_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "").strip()
            if not question:
                return JsonResponse({"error": "Question required"}, status=400)

            # Retrieve top chunks
            try:
                top_chunks = retrieve_top_chunks(question)
            except Exception as e:
                return JsonResponse({"error": "Index not ready. Upload PDF first.", "details": str(e)}, status=400)

            answer = organize_answer(top_chunks)

            return JsonResponse({
                "question": question,
                "answer": answer,
                "sources": top_chunks
            })
        except Exception as e:
            return JsonResponse({"error": "Invalid request", "details": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
