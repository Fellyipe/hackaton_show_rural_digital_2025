import { useState } from "react";
import Logo from "/logo.png";
import Footer from "../../components/footer/Footer.jsx";
import api from "../../services/api.js";
import { useNavigate } from "react-router";
import { Eye, EyeSlash } from "@phosphor-icons/react";

function Registro() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);

  function validateCPF(cpf) {
    cpf = cpf.replace(/\D/g, "");
    return cpf.length === 11;
  }
  function validatePassword(password) {
    return password.length >= 8;
  }
  
  const [formData, setFormData] = useState({
    email: "",
    cpf: "",
    password: "",
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
    setError(null);

    if (!validateCPF(formData.cpf)) {
      setError("CPF inválido");
      return;
    }
    if (!validatePassword(formData.password)) {
      setError("Senha deve ter no mínimo 8 caracteres");
      return;
    }

    try {
      const response = await api.post("/registrar", {
        nome: formData.email,
        senha: formData.password, // Corrigido
        cpf: formData.cpf,
        produtor: formData.produtor,
        agronomo: formData.agronomo,
        cref: formData.agronomo ? formData.cref : null, // Só envia se for agrônomo
      });

      alert("Registro bem-sucedido!");
      navigate("/Login");
    } catch (error) {
      console.error("Erro ao registrar", error);
      alert("Erro ao tentar registrar. Verifique os dados.");
    }
  };

  return (
    <div className="flex flex-col items-center h-screen gap-5 p-8 bg-white-green">
      <div className="mt-10">
        <img src={Logo} alt="logotipo" />
      </div>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-5 w-full md:w-96"
      >
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
            className="appearance-none  mt-5 border-none rounded w-full py-2 px-3 text-gray-700 bg-white focus:outline-none"
            id="cpf"
            type="text"
            placeholder="CPF"
            value={formData.cpf}
            onChange={handleChange}
            autoComplete="off"
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
            className="cursor-pointer  flex items-center text-gray-500 hover:text-gray-700"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? <EyeSlash size={20} /> : <Eye size={20} />}
          </button>
        </div>

        <div className="flex justify-between p-6">
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="produtor"
              className="appearance-none size-5 border-2 border-gray-500 rounded-md checked:bg-emerald checked:border-transparent"
              checked={formData.produtor}
              onChange={handleChange}
            />
            <span>Sou Produtor</span>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="agronomo"
              className="appearance-none size-5 border-2 border-gray-500 rounded-md checked:bg-emerald checked:border-transparent"
              checked={formData.agronomo}
              onChange={handleChange}
            />
            <span>Sou Agrônomo</span>
          </div>
        </div>

        {formData.agronomo && (
          <div>
            <input
              className="appearance-none border-none rounded w-full py-2 px-3 text-gray-700 bg-white focus:outline-none"
              id="cref"
              type="text"
              placeholder="CREF do Agrônomo"
              value={formData.cref}
              onChange={handleChange}
            />
          </div>
        )}

        <div>
          <button
            className="bg-greenpeace cursor-pointer text-white font-bold py-2 w-full rounded hover:bg-emerald"
            type="submit"
            >
            Cadastrar
          </button>
        </div>
            {error && <p className="text-red-500">{error}</p>}
      </form>
      <Footer
        backgroundColor="primary"
        title="Voltar para o Login"
        page="/login"
      />
    </div>
  );
}

export default Registro;
