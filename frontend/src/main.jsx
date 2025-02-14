import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { BrowserRouter, Route, Routes } from "react-router";

// Importação de telas
import App from "./Pages/App.jsx";
import TelaProdutor from "./Pages/TelaProdutor/TelaProdutor.jsx";
import Login from "./Pages/Login/Login";
import ListaProdutores from "./Pages/ListaProdutores/ListaProdutores.jsx";
import Registro from "./Pages/Registro/Registro.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Registro />} />
        <Route path="/listaProdutores" element={<ListaProdutores />} />
        <Route path="/telaProdutor" element={<TelaProdutor />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
