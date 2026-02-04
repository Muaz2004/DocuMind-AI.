import { useState } from "react";
import { uploadPDF } from "../services/ragApi";

function UploadPage() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setStatus("Please select a PDF first");
      return;
    }

    setStatus("Uploading...");
    try {
      const res = await uploadPDF(file);
      setStatus(res.message || "Done");
    } catch (err) {
      console.error(err);
      setStatus("Upload failed");
    }
  };

  return (
    <div style={{ padding: 20, display: "flex", flexDirection: "column", gap: 15 }}>
      <h2>Upload Document</h2>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
        style={{ padding: 8 }}
      />

      <button
        onClick={handleUpload}
        style={{
          padding: "10px 15px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          cursor: "pointer",
          borderRadius: 5,
          width: 150
        }}
      >
        Upload & Index
      </button>

      {status && <p style={{ fontWeight: "bold" }}>{status}</p>}
    </div>
  );
}

export default UploadPage;
