import { BrowserRouter, Routes, Route } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import QueryPage from "./pages/QueryPage";
import Navbar from "./components/Navbar";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div style={{ maxWidth: 800, margin: "20px auto" }}>
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route path="/query" element={<QueryPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
