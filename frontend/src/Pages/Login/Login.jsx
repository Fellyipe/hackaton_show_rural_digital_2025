import { useState } from "react";
import { useNavigate } from "react-router";
import { Eye, EyeSlash } from "@phosphor-icons/react";
import Logo from "/public/logo.png";
import Footer from "../../components/footer/Footer.jsx";

import api from "../../services/api.js";

function Login() {
  const [cpf, setCpf] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();
    setError(null); // Reseta o erro antes da requisição

    try {
      const response = await api.get("http://localhost:5000/login", {
        params: {
          cpf,
          senha: password,
        },
      });

      console.log("Login bem-sucedido:", response.data);

      // Redireciona o usuário após o login bem-sucedido
      navigate("/listaProdutores");
    } catch (error) {
      console.error("Erro no login:", error);
      setError(error.response?.data?.erro || "Erro ao realizar login");
    }
  }

  return (
    <div className="flex flex-col items-center h-screen gap-5 p-8 bg-white-green">
      <div className="mt-10">
        <img src={Logo} alt="logotipo" />
      </div>
      <form onSubmit={handleSubmit} className="flex flex-col gap-5 w-full">
        <div>
          <input
            className="appearance-none border-none rounded w-full py-2 px-3 text-gray-700 bg-white focus:outline-none"
            id="cpf"
            type="text"
            placeholder="Cpf"
            value={cpf}
            onChange={(e) => setCpf(e.target.value)}
          />
        </div>
        <div className="flex items-center justify-center bg-white rounded px-2">
          <input
            className="appearance-none border-none rounded w-full py-2 px-1 text-gray-700 bg-white focus:outline-none"
            id="password"
            type={showPassword ? "text" : "password"}
            placeholder="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            type="button"
            className="cursor-pointer  flex items-center text-gray-500 hover:text-gray-700"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? <EyeSlash size={20} /> : <Eye size={20} />}
          </button>
        </div>
        {error && <p className="text-red-500">{error}</p>}
        <div>
          <button
            className="bg-greenpeace cursor-pointer text-white font-bold py-2 w-full rounded hover:bg-emerald"
            type="submit"
          >
            Entrar
          </button>
        </div>
      </form>
      <Footer
        backgroundColor="primary"
        title="Não tem uma conta? Cadastre-se"
        page="/registro"
      />
    </div>
  );
}

export default Login;
