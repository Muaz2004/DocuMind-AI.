import { BrowserRouter, Routes, Route } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import QueryPage from "./pages/QueryPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/query" element={<QueryPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
