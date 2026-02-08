# views.py
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings

from rag_app.services.rag_engine import async_index, retrieve_top_chunks, organize_answer

# ---------------- UPLOAD PDF ----------------
@csrf_exempt
def upload_pdf(request):
    if request.method == "POST" and request.FILES.get("pdf"):
        pdf_file = request.FILES["pdf"]

       
        relative_path = default_storage.save(f"uploads/{pdf_file.name}", pdf_file)

      
        absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        print("📄 PDF saved at:", absolute_path)

        async_index(absolute_path)

        return JsonResponse({
            "status": "PDF uploaded",
            "path": absolute_path
        })

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

            top_chunks = retrieve_top_chunks(question)
            answer = organize_answer(top_chunks)

            return JsonResponse({
                "question": question,
                "answer": answer,
                "sources": top_chunks
            })

        except Exception as e:
            return JsonResponse({
                "error": "Index not ready",
                "details": str(e)
            }, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
