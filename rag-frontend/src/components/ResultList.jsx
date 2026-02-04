import React from "react";

function ResultList({ results }) {
  return (
    <div>
      {results.map((chunk, i) => (
        <div key={i} style={{ marginBottom: 10, padding: 10, border: "1px solid #ddd", borderRadius: 5 }}>
          <strong>Chunk {i + 1}</strong>
          <p>{chunk}</p>
        </div>
      ))}
    </div>
  );
}

export default ResultList;
