import { useState } from "react";
import { queryRAG } from "../services/ragApi";
import ResultList from "../components/ResultList";

function QueryPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [chunks, setChunks] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question) return;

    setLoading(true);
    try {
      const res = await queryRAG(question);
      console.log("Query response:", res);

      setAnswer(res.answer || "No answer found");
      setChunks(res.chunks || []);
    } catch (err) {
      console.error("Query error:", err);
      setAnswer("Error fetching answer");
      setChunks([]);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: 20, maxWidth: 700, margin: "auto", display: "flex", flexDirection: "column", gap: 15 }}>
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
        disabled={loading}
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
        {loading ? "Fetching..." : "Ask"}
      </button>

      {answer && (
        <div style={{ marginTop: 20 }}>
          <h3>Answer:</h3>
          <p>{answer}</p>
        </div>
      )}

      {chunks.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <h4>Source Chunks:</h4>
          <ResultList results={chunks} />
        </div>
      )}
    </div>
  );
}

export default QueryPage;
