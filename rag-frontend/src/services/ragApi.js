
const BASE_URL = "http://127.0.0.1:8000";


export async function uploadPDF(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/upload_pdf`, {
    method: "POST",
    body: formData,
  });

  return response.json();
}


export async function queryRAG(question) {
  const response = await fetch(`${BASE_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  return response.json();
}
