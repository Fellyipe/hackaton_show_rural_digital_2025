import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { BrowserRouter, Route, Routes } from "react-router";

// Importação de telas
import App from "./Pages/App.jsx";
import TelaProdutor from "./Pages/TelaProdutor/TelaProdutor.jsx";
import Login from "./Pages/Login/Login";
import ListaProdutores from "./Pages/ListaProdutores/ListaProdutores.jsx";
import Cadastro from "./Pages/Cadastro/Cadastro.jsx";
import TelaAgronomo from "./Pages/TelaAgronomo/TelaAgronomo.jsx";
import AddAnalise from "./Pages/AddAnalise/AddAnalise.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro" element={<Cadastro />} />
        <Route path="/listaProdutores" element={<ListaProdutores />} />
        <Route path="/telaProdutor" element={<TelaProdutor />} />
        <Route path="/telaAgronomo" element={<TelaAgronomo />} />
        <Route path="/addAnalise" element={<AddAnalise />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
