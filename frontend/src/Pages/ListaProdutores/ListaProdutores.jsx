import React, { useEffect, useState } from "react";
import ProdutorCard from "../../components/ProdutorCard/ProdutorCard";
import { useNavigate } from "react-router";
import Footer from "../../components/footer/Footer";
import api from "../../services/api";

function ListaProdutores() {
  const [produtores, setProdutores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [cpf, setCpf] = useState("");
  let navigate = useNavigate();

  useEffect(() => {
    const fetchProdutores = async () => {
      const agronomoId = localStorage.getItem("agronomo_id");
      if (!agronomoId) {
        setError("ID do agrônomo não encontrado.");
        setLoading(false);
        return;
      }

      try {
        const response = await api.get("http://localhost:5000/produtores", {
          params: { agronomo_id: agronomoId },
        });

        console.log("Dados recebidos:", response.data);

        // Verifica se response.data é um array ou um objeto único
        if (Array.isArray(response.data)) {
          setProdutores(response.data);
        } else if (response.data && response.data.id) {
          setProdutores([response.data]); // Garante que mesmo um único objeto fique dentro de um array
        } else {
          console.error("Formato inesperado:", response.data);
          setProdutores([]);
        }
      } catch (error) {
        console.error(
          "Erro ao buscar produtores:",
          error.response?.data || error.message
        );
        setError("Erro ao carregar produtores.");
      } finally {
        setLoading(false);
      }
    };

    fetchProdutores();
  }, []);

  useEffect(() => {
    console.log("Estado atualizado:", produtores);
  }, [produtores]);

  const handleAddProdutor = async () => {
    const agronomoId = localStorage.getItem("agronomo_id");
    if (!agronomoId || !cpf) {
      alert("Por favor, informe um CPF válido.");
      return;
    }

    try {
      await api.post("http://localhost:5000/registro_analise", {
        agronomo_id: agronomoId,
        produtor_cpf: cpf,
      });
      alert("Produtor adicionado para análise com sucesso!");
      setShowModal(false);
      setCpf("");
    } catch (error) {
      console.error(
        "Erro ao adicionar produtor:",
        error.response?.data || error.message
      );
      alert("Erro ao adicionar produtor. Tente novamente.");
      console.log(agronomoId, cpf);
    }
  };

  if (loading) {
    return <p className="text-center mt-10">Carregando...</p>;
  }

  if (error && error !== "Erro ao carregar produtores.") {
    return <p className="text-center mt-10 text-red-500">{error}</p>;
  }

  return (
    <>
      <div className="max-w-3xl mx-auto p-4 mb-10">
        <h1 className="text-3xl font-bold text-bold-text mb-6 text-center mt-10">
          Seus produtores
        </h1>
        <div className="text-center mb-4">
          <button
            onClick={() => setShowModal(true)}
            className="bg-secondary text-white px-4 py-2 rounded"
          >
            Adicionar Produtor
          </button>
        </div>
        {produtores.length > 0 ? (
          <div className="space-y-4">
            {produtores.map((produtor) => (
              <ProdutorCard
                key={produtor.id}
                produtor={produtor}
                navigateToDetail={() => navigate("/telaAgronomo")}
              />
            ))}
          </div>
        ) : (
          <p className="text-center">
            Nenhum produtor encontrado. Cadastre um produtor para começar.
          </p>
        )}
      </div>

      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
          <div className="bg-white p-6 rounded shadow-lg w-96">
            <h2 className="text-xl font-bold mb-4">Adicionar Produtor</h2>
            <input
              type="text"
              placeholder="Digite o CPF do produtor"
              value={cpf}
              onChange={(e) => setCpf(e.target.value)}
              className="border p-2 w-full mb-4"
            />
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => setShowModal(false)}
                className="bg-gray-400 text-white px-4 py-2 rounded"
              >
                Cancelar
              </button>
              <button
                onClick={handleAddProdutor}
                className="bg-blue-500 text-white px-4 py-2 rounded"
              >
                Adicionar
              </button>
            </div>
          </div>
        </div>
      )}

      <Footer
        backgroundColor="primary"
        title="Voltar para a tela inicial"
        page="/"
      />
    </>
  );
}

export default ListaProdutores;
