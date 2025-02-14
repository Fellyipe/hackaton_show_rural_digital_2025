import { useEffect, useState } from "react";
import Sprout from "../../assets/sprout.png";
import Footer from "../../components/footer/Footer";
import { useNavigate } from "react-router";
import api from "../../services/api"; // Ajuste conforme sua configuração de api

function TelaAgronomo() {
  let navigate = useNavigate();

  // Definindo os estados para armazenar os dados
  const [resultado, setResultado] = useState({
    parametro: "",
    analises: [], // Lista de análises
  });

  useEffect(() => {
    const fetchAnalise = async () => {
      const agronomoId = localStorage.getItem("agronomo_id");
      const produtorId = localStorage.getItem("produtor_id");

      try {
        const response = await api.get(
          "http://localhost:5000/resultados_analise",
          {
            params: {
              parametro_index: 0,
              agronomo_id: agronomoId,
              produtor_id: produtorId,
            },
          }
        );

        // Atualizando o estado com os dados recebidos
        setResultado({
          parametro: response.data.parametro,
          analises: response.data.analises || [],
        });
        console.log(resultado);
      } catch (error) {
        console.error("Erro ao buscar os dados da análise", error);
      }
    };

    fetchAnalise();
  }, []);

  return (
    <div>
      <main className="bg-primary w-full h-screen mt-40 rounded-t-2xl p-4">
        <div className="flex w-full justify-end items-end">
          <img className="-mt-32" src={Sprout} alt="sprout" />
        </div>
        <div className="space-y-5 flex-col items-center justify-center w-full">
          <span className="text-4xl text-emerald font-bold">
            Resultado da analise:
          </span>

          {/* Exibindo o parâmetro */}
          <div>
            <p className="text-2xl text-white-green">Parametro</p>
            <span className="text-4xl text-red">
              {resultado.parametro || "Carregando..."}
            </span>
          </div>

          {/* Exibindo as análises */}
          {resultado.analises.length > 0 ? (
            resultado.analises.map((analise) => (
              <div key={analise.id} className="space-y-2">
                <div>
                  <p className="text-2xl text-white-green">
                    {`nivel de ${resultado.parametro} do solo`}
                  </p>
                  <span className="text-4xl text-red">
                    {`${analise.valor} ${analise.classificacao}` ||
                      "Carregando..."}
                  </span>
                </div>
                <div>
                  <p className="text-2xl text-white-green">
                    Quantidade sugerida
                  </p>
                  <span className="text-4xl text-red">
                    {analise.calculo_recomendado || "Carregando..."}
                  </span>
                </div>
                <div>
                  <p className="text-2xl text-white-green">
                    Recomendação do agronomo
                  </p>
                  <span className="text-4xl text-red">
                    {`${analise.cooperativa_recomendada} ${analise.valor_cooperativa}` ||
                      "Carregando..."}
                  </span>
                </div>
                <div>
                  <p className="text-2xl text-white-green">
                    Recomendações finais
                  </p>
                  <span className="text-4xl text-red">
                    {analise.sugestao || "Carregando..."}
                  </span>
                </div>
              </div>
            ))
          ) : (
            <p className="text-xl text-white-green">
              Sem análises disponíveis.
            </p>
          )}

          <button
            onClick={() => navigate("/addAnalise")}
            className="bg-secondary cursor-pointer text-white font-bold py-2 w-40 h-12 rounded hover:bg-emerald"
          >
            Nova Analise
          </button>
        </div>
      </main>

      <Footer
        backgroundColor="primary"
        title="Voltar para produtores"
        page="/listaProdutores"
      />
    </div>
  );
}

export default TelaAgronomo;
