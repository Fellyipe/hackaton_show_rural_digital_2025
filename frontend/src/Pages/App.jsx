import React from "react";
import { useNavigate } from "react-router";
import logo from "../../public/logo.svg";

function App() {
  let navigate = useNavigate();

  return (
    <div className="w-full flex flex-col h-screen items-center justify-center gap-6 bg-white-green">
      <h1 className="text-3xl font-bold text-bold-text">
        Bem Vindo ao nosso App
      </h1>
      <div>
        <img src={logo} alt="logotipo" />
      </div>

      <div className="flex flex-col items-center gap-5">
        <button
          onClick={() => navigate("/Login")}
          className="bg-primary w-52 h-12 rounded-md font-bold text-white text-xl"
        >
          Fazer Login
        </button>
      </div>
    </div>
  );
}

export default App;
