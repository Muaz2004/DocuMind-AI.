const API_BASE = "http://127.0.0.1:8000/api";

export const uploadPDF = async (file) => {
  try {
    const formData = new FormData();
    formData.append("pdf", file);
    console.log("Uploading file:", file.name);

    const res = await fetch(`${API_BASE}/upload/`, {  // match view name
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    console.log("Upload response:", data);
    return data;
  } catch (err) {
    console.error("Upload error:", err);
    return { status: "Upload failed" };
  }
};

export const queryRAG = async (question) => {
  try {
    console.log("FRONTEND QUESTION SENT:", question);
    const res = await fetch(`${API_BASE}/query/`, {  // match view name
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    console.log("Query response:", data);
    return data;
  } catch (err) {
    console.error("Query error:", err);
    return { answer: "Query failed", sources: [] };
  }
};
