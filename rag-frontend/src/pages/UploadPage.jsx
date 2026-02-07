import React, { useState } from "react";
import { uploadPDF } from "../services/ragApi";

export default function UploadSection() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return setStatus("Select a file");
    setStatus("Uploading...");
    try {
      const res = await uploadPDF(file);
      console.log("Upload result:", res);
      setStatus(res.status || res.message || "Upload complete");
    } catch {
      setStatus("Error uploading file");
    }
  };

  return (
    <div className="upload-section">
      <h3>Upload PDF</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>
        {status === "Uploading..." ? status : "Upload"}
      </button>
      {status && <p className="upload-status">{status}</p>}
    </div>
  );
}
