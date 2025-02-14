import React from "react";
import Footer from "../../components/footer/Footer.jsx";
import Ground from "../../assets/ground.png";
import DragAndDropPDF from "../../components/DragAndDropPDF/DragAndDropPDF.jsx";

function AddAnalise() {
  function handleFileUpload(file) {
    console.log("Arquivo recebido:", file);
  }
  
  return (
    <div>
      <main className="bg-primary w-full h-screen mt-40 rounded-t-2xl p-4">
        <div className="flex w-full justify-end items-end">
          <img className="-mt-40 size-48" src={Ground} alt="sprout" />
        </div>
        <div className="gap-5 flex flex-col items-center justify-center w-full">
          <span className="text-3xl text-emerald font-bold">
            Analise de Potassio(K)
          </span>

          <div>
            <DragAndDropPDF onFileUpload={handleFileUpload} />
          </div>
          <div>
            <p className="text-xl text-emerald">Valor encontrado na amostra:</p>
            <span className="text-3xl font-bold text-white-green">
              {/* Variavel de amostra */}0.38% cmolc/dm3
            </span>
          </div>

          <div>
            <p className="text-xl text-emerald">Calculo sugerido:</p>
            <span className="text-xl font-bold text-white-green">
              {/* Variavel de calculo */}0.30 {">"} 0.40 ={" "}
              <input type="text" className="bg-white rounded-sm w-14" />
            </span>
          </div>

          <div className="flex flex-col gap-5">
            <p className="text-xl text-emerald">Recomendação de compra</p>
            <div className="flex flex-col gap-5">
              <input
                placeholder="Nome da Cooperativa ou Empresa"
                type="text"
                className="bg-white rounded-xl h-12 w-80 p-4"
              />
              <input
                placeholder="Valor por Kg"
                type="text"
                className="bg-white rounded-xl h-12 w-48 p-4"
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
      </main>

      <Footer title="Voltar para produtores" page="/listaProdutores" />
    </div>
  );
}

export default AddAnalise;
