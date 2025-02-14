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

  const handleFileUpload = async (file) => {
    if (!file) {
      console.error("Nenhum arquivo selecionado.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("pdf", file);

      const response = await api.post("/upload_pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("Resposta do servidor:", response.data);
    } catch (e) {
      console.error("Erro no upload:", e);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({
      amostra,
      calculo,
      recomendacao,
      valorPorKg,
      recomendacaoAdicional,
    });
  };

  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="bg-primary w-full mt-40 rounded-t-2xl p-4 py-6 mb-14"
      >
        <div className="flex w-full justify-end">
          <img className="-mt-40 size-48" src={Ground} alt="sprout" />
        </div>

        <div className="px-6 gap-5 flex flex-col items-start w-full">
          <h2 className="text-3xl text-emerald font-bold">
            Análise de Potássio (K)
          </h2>

          <DragAndDropPDF onFileUpload={handleFileUpload} />

          <div>
            <p className="text-xl text-emerald">Valor encontrado na amostra:</p>
            <span className="text-3xl font-bold text-white-green">
              {amostra}% cmolc/dm³
            </span>
          </div>

          <div>
            <p className="text-xl text-emerald">Cálculo sugerido:</p>
            <span className="text-xl font-bold text-white-green">
              0.30 {">"} 0.40 =
              <input
                type="text"
                placeholder="Kg"
                className="bg-white text-black px-2 rounded-sm w-14 ml-2"
                value={calculo}
                onChange={(e) => setCalculo(e.target.value)}
              />
            </span>
          </div>

          <div className="flex flex-col gap-5">
            <p className="text-xl text-emerald">Recomendação de compra</p>
            <input
              placeholder="Nome da Cooperativa ou Empresa"
              type="text"
              className="bg-white rounded-xl h-12 w-80 p-4"
              value={recomendacao}
              onChange={(e) => setRecomendacao(e.target.value)}
            />
            <input
              placeholder="Valor por Kg"
              type="text"
              className="bg-white rounded-xl h-12 w-48 p-4"
              value={valorPorKg}
              onChange={(e) => setValorPorKg(e.target.value)}
            />
          </div>

          <div className="flex flex-col gap-5">
            <p className="text-xl text-emerald">Recomendações adicionais:</p>
            <textarea
              className="bg-white rounded-xl w-80 p-2"
              cols="30"
              rows="5"
              value={recomendacaoAdicional}
              onChange={(e) => setRecomendacaoAdicional(e.target.value)}
            ></textarea>
          </div>

          <button
            type="submit"
            className="bg-greenpeace text-white font-bold py-2 w-40 h-12 rounded hover:bg-emerald"
          >
            Salvar Análise
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
