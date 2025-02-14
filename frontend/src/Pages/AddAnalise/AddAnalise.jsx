import { useState } from "react";
import Footer from "../../components/footer/Footer.jsx";
import Ground from "../../assets/ground.png";
import DragAndDropPDF from "../../components/DragAndDropPDF/DragAndDropPDF.jsx";
import api from "../../services/api.js";

function AddAnalise() {
  const [file, setFile] = useState(null);
  const [amostra, setAmostra] = useState(0.38);
  const [calculo, setCalculo] = useState("");
  const [recomendacao, setRecomendacao] = useState("");
  const [valorPorKg, setValorPorKg] = useState("");
  const [recomendacaoAdicional, setRecomendacaoAdicional] = useState("");
  const analiseId = 1;

  const handleFileUpload = async (file) => {
    try {
      const formData = new FormData();
      formData.append("pdf", file); // "pdf" deve ser o nome calculo_recomandadoesperado pelo backend
      formData.append("analiseId", analiseId);
      const response = await api.post("/upload_pdf", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("Resposta do servidor:", response);
    } catch (e) {
      console.error("Erro no upload:", e);
    }
  };

  const handleUpdateAnalise = async () => {
    const dados = {};
    if (calculo) dados.calculo_recomendado = calculo;
    if (recomendacao) dados.cooperativa_recomendada = recomendacao;
    if (valorPorKg) dados.valor_cooperativa = valorPorKg;
    if (recomendacaoAdicional) dados.sugestao = recomendacaoAdicional;
    dados.analise_id = analiseId;
    try {
      const response = await api.put(`/atualizar_analise`, dados);
      alert("Análise atualizada com sucesso!", response);
    } catch (error) {
      console.error("Erro ao atualizar análise:", error);
      alert("Erro ao atualizar análise. Verifique os dados e tente novamente.");
    }
  };

  return (
    <>
      <form className="bg-primary w-full mt-40 rounded-t-2xl p-4 py-6 mb-14">
        <div className="flex w-full justify-end items-end">
          <img className="-mt-40 size-48" src={Ground} alt="sprout" />
        </div>
        <div className="px-6 gap-5 flex flex-col items-start justify-center w-full">
          <span className="text-3xl text-emerald font-bold">
            Analise de Potassio(K)
          </span>

          <div>
            <DragAndDropPDF onFileUpload={handleFileUpload} />
          </div>
          <div>
            <p className="text-xl text-emerald">Valor encontrado na amostra:</p>
            <span className="text-3xl font-bold text-white-green">
              {amostra}% cmolc/dm3
            </span>
          </div>

          <div>
            <p className="text-xl text-emerald">Calculo sugerido:</p>
            <span className="text-xl font-bold text-white-green">
              0.30 {">"} 0.40 ={" "}
              <input
                type="text"
                placeholder="Kg"
                className="bg-white text-black px-2 rounded-sm w-14"
                onChange={(e) => setCalculo(e.target.value)}
              />
            </span>
          </div>

          <div className="flex flex-col gap-5">
            <p className="text-xl text-emerald">Recomendação de compra</p>
            <div className="flex flex-col gap-3">
              <input
                placeholder="Nome da Cooperativa ou Empresa"
                type="text"
                className="bg-white rounded-xl h-12 w-80 p-4"
                onChange={(e) => setRecomendacao(e.target.value)}
              />
              <input
                placeholder="Valor por Kg"
                type="text"
                className="bg-white rounded-xl h-12 w-48 p-4"
                onChange={(e) => setValorPorKg(e.target.value)}
              />
            </div>
          </div>
          <div className="flex flex-col gap-5">
            <p className="text-xl text-emerald">Recomendação adicional:</p>
            <div>
              <textarea
                className="bg-white rounded-xl w-80"
                name="recomendacoes"
                id="recomendacoes"
                cols="30"
                rows="5"
                onChange={(e) => setRecomendacaoAdicional(e.target.value)}
              ></textarea>
            </div>
          </div>
          <button
            type="button"
            onClick={handleUpdateAnalise}
            className="bg-greenpeace cursor-pointer text-white font-bold py-2 w-40 h-12 rounded hover:bg-emerald"
          >
            Atualizar Análise
          </button>
        </div>
      </form>

      <Footer
        title="Voltar para produtores"
        page="/listaProdutores"
        backgroundColor="primary"
      />
    </>
  );
}

export default AddAnalise;
