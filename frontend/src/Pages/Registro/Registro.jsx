import { useState } from "react";
import Logo from "/logo.png";
import Footer from "../../components/footer/Footer.jsx";

function Registro() {
  const [formData, setFormData] = useState({
    email: "",
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

  const handleSubmit = (e) => {
    e.preventDefault();
    //TODO Implementar a lógica de registro
    
    console.log("Dados enviados:", formData);
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
        </div>
        <div>
          <input
            className="appearance-none border-none rounded w-full py-2 px-3 text-gray-700 mb-3 bg-white focus:outline-none"
            id="password"
            type="password"
            placeholder="Senha"
            value={formData.password}
            onChange={handleChange}
          />
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
            Registrar
          </button>
        </div>
      </form>
      <Footer title="Voltar para o Login" page="/login" />
    </div>
  );
}

export default Registro;
