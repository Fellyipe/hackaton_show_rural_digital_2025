import React from 'react';
import { useNavigate } from 'react-router';

function App() {
 let navigate = useNavigate();

    return (
      <div className="w-full flex flex-col h-screen items-center justify-center">
        <div className="flex flex-col items-center justify-between h-1/4">
          <h1 className="text-3xl">Bem Vindo ao nosso app</h1>
          <div className="flex flex-col items-center gap-5">
            <button
              onClick={() => navigate("/analisePotassio")}
              className="bg-primary w-52 h-12 rounded-md font-bold text-white text-xl"
            >
              Sou Agronomo
            </button>
            <button
              onClick={() => navigate("/analisePotassio")}
              className="bg-secondary w-52 h-12 rounded-md font-bold text-white text-xl"
            >
              Sou Produtor
            </button>
          </div>
        </div>
      </div>
    );
}

export default App;