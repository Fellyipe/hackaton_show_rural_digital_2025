import { useState } from "react";
import Footer from "../../components/footer/Footer.jsx";
import Ground from "../../assets/ground.png";
import DragAndDropPDF from "../../components/DragAndDropPDF/DragAndDropPDF.jsx";
import api from "../../services/api.js";

function AddAnalise() {
  const [file, setFile] = useState(null);
  const [amostra, setAmostra] = useState(0.38);
  const [calculo, setCalculo] = useState(null);
  const [recomendacao, setRecomendacao] = useState(null);
  const [valorPorKg, setValorPorKg] = useState(null);
  const [recomendacaoAdicional, setRecomendacaoAdicional] = useState(null);

  const handleFileUpload = async (file) => {
    //console.log("Arquivo recebido:", file);
    try {
      const response = await api.post("/upload_pdf", file, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Resposta do servidor:", response);
    } catch (e) {
      alert(e);
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
            <p className="text-xl text-emerald">Recomendação adicionais:</p>
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
            onClick={() => {}}
            className="bg-greenpeace cursor-pointer text-white font-bold py-2 w-40 h-12 rounded hover:bg-emerald"
          >
            Salvar Analise
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
