import React from 'react';
import { useNavigate } from 'react-router';

function App() {
 let navigate = useNavigate();

    return (
      <div className="w-full flex flex-col h-screen items-center justify-center">
        <div className="flex flex-col items-center justify-between h-1/4">
          <h1 className="text-5xl">Bem Vindo</h1>
          <button
            onClick={() => navigate("/analisePotassio")}
            className="bg-primary w-40 h-10 rounded-md text-white"
          >
            Entrar
          </button>
        </div>
      </div>
    );
}

export default App;