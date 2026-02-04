import { useState } from "react";
import { queryRAG } from "../services/ragApi";
import ResultList from "../components/ResultList";

function QueryPage() {
  const [question, setQuestion] = useState("");
  const [results, setResults] = useState([]);

  const handleAsk = async () => {
    if (!question) return;

    const res = await queryRAG(question);
    setResults(res.results || []);
  };

  return (
    <div style={{ padding: 20, display: "flex", flexDirection: "column", gap: 15 }}>
      <h2>Ask a Question</h2>

      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Type your question here..."
        style={{ padding: 8, width: "100%", borderRadius: 5, border: "1px solid #ccc" }}
      />

      <button
        onClick={handleAsk}
        style={{
          padding: "10px 15px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          cursor: "pointer",
          borderRadius: 5,
          width: 100
        }}
      >
        Ask
      </button>

      <ResultList results={results} />
    </div>
  );
}

export default QueryPage;
