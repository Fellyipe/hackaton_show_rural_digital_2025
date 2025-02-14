import React, { useEffect, useState } from "react";
import ProdutorCard from "../../components/ProdutorCard/ProdutorCard";
import { useNavigate } from "react-router";
import Footer from "../../components/footer/Footer";
import api from "../../services/api"; //

function ListaProdutores() {
  const [produtores, setProdutores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
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
        setProdutores(response.data);
      } catch (error) {
        console.error("Erro ao buscar produtores:", error);
        setError("Erro ao carregar produtores.");
      } finally {
        setLoading(false);
      }
    };

    fetchProdutores();
  }, []);

  const navigateToDetail = () => {
    navigate("/telaAgronomo");
  };

  if (loading) {
    return <p className="text-center mt-10">Carregando...</p>;
  }

  if (error) {
    return <p className="text-center mt-10 text-red-500">{error}</p>;
  }

  return (
    <>
      <div className="max-w-3xl mx-auto p-4 mb-10">
        <h1 className="text-3xl font-bold text-bold-text mb-6 text-center mt-10">
          Seus produtores
        </h1>
        <div className="space-y-4">
          {produtores.length > 0 ? (
            produtores.map((produtor) => (
              <ProdutorCard
                key={produtor.id}
                produtor={produtor}
                navigateToDetail={navigateToDetail}
              />
            ))
          ) : (
            <p className="text-center">Nenhum produtor encontrado.</p>
          )}
        </div>
      </div>
      <Footer
        backgroundColor="primary"
        title="Voltar para a tela inicial"
        page="/"
      />
    </>
  );
}

export default ListaProdutores;
