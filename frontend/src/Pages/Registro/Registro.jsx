import { useState } from "react";
import Logo from "/logo.png";
import Footer from "../../components/footer/Footer.jsx";
import { Eye, EyeSlash } from "@phosphor-icons/react";
import api from "../../services/api.js";

function Registro() {
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    cpf: "",
    produtor: false,
    agronomo: false,
    cref: "",
  });

  const handleChange = (e) => {
    const { id, type, checked, value } = e.target;

    setFormData((prev) => {
      if (type === "checkbox") {
        return {
          ...prev,
          produtor: id === "produtor" ? checked : false,
          agronomo: id === "agronomo" ? checked : false,
          cref: id === "agronomo" && checked ? prev.cref : "",
        };
      }
      return { ...prev, [id]: value };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/registrar", {
        nome: formData.email,
        cpf: formData.cpf,
        senha: formData.password,
        crea: formData.agronomo ? formData.cref : null,
      });

      if (response.data.tipo) {
        alert(`Login bem-sucedido! Tipo: ${response.data.tipo}`);
        // Redirecionar ou salvar os dados do usuário no estado global
      } else {
        alert("CPF ou senha incorretos.");
      }
    } catch (error) {
      console.error("Erro ao fazer login", error);
      alert("Erro ao tentar logar. Verifique suas credenciais.");
    }
  };

  return (
    <div className="flex flex-col items-center h-screen gap-5 p-8 bg-white-green">
      <div className="mt-10">
        <img src={Logo} alt="logotipo" />
      </div>
      <form onSubmit={handleSubmit} className="flex flex-col gap-5 w-full">
        <div>
          <input
            className="appearance-none border-none rounded w-full py-2 px-3 text-gray-700 bg-white focus:outline-none"
            id="email"
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
          />
          <input
            className="appearance-none border-none rounded w-full py-2 mt-5 px-3 text-gray-700 bg-white focus:outline-none"
            id="cpf"
            type="text"
            placeholder="CPF"
            value={formData.cpf}
            onChange={handleChange}
          />
        </div>

        <div className="flex items-center justify-center bg-white rounded px-2">
          <input
            className="appearance-none border-none rounded w-full py-2 px-1 text-gray-700 bg-white focus:outline-none"
            id="password"
            type={showPassword ? "text" : "password"}
            placeholder="Senha"
            value={formData.password}
            onChange={handleChange}
          />
          <button
            type="button"
            className="ml-2"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? <EyeSlash size={24} /> : <Eye size={24} />}
          </button>
        </div>

        <button
          type="submit"
          className="bg-green-500 text-white py-2 px-4 rounded"
        >
          Entrar
        </button>
      </form>
      <Footer />
    </div>
  );
}

export default Registro;
