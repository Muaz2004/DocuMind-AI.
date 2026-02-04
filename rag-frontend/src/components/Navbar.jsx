// src/components/Navbar.jsx
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav style={{
      padding: "10px 20px",
      backgroundColor: "#4CAF50",
      color: "white",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    }}>
      <h1 style={{ margin: 0, fontSize: 20 }}>RAG App</h1>
      <div>
        <Link to="/" style={{ color: "white", marginRight: 15, textDecoration: "none" }}>Upload</Link>
        <Link to="/query" style={{ color: "white", textDecoration: "none" }}>Query</Link>
      </div>
    </nav>
  );
}

export default Navbar;
