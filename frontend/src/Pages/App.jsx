import React from "react";
import { useNavigate } from "react-router";
import logo from "/logo.png";

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
          className="bg-greenpeace hover:bg-emerald w-52 h-12 cursor-pointer rounded-md font-bold text-white text-xl"
        >
          Fazer Login
        </button>
      </div>
    </div>
  );
}

export default App;
