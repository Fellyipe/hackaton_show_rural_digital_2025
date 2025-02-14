import React from "react";
import Footer from "../../components/footer/Footer.jsx";
import Ground from "../../assets/ground.png";

function AddAnalise() {
  return (
    <div>
      <main className="bg-primary w-full h-screen mt-40 rounded-t-2xl p-4">
        <div className="flex w-full justify-end items-end">
          <img className="-mt-32" src={Ground} alt="sprout" />
        </div>
        <div className="space-y-5 flex-col items-center justify-center w-full">
          <span className="text-3xl text-emerald font-bold">
            Analise de Potassio(K)
          </span>

          <div>{/* Adicionar aqui arrasta e solta do PDF */}</div>

          <div>
            <p className="text-2xl text-white-green">
              Valor encontrado na amostra:
            </p>
            <span className="text-4xl font-bold text-white-green">
              {/* Variavel de amostra */}0.38% cmolc/dm3
            </span>
          </div>
          <div>
            <p className="text-2xl text-white-green">
              Recomendação de compra
            </p>
            <div>
              {/* Adicionar aqui dois inputs um com o nome da cooperativa  */}
            </div>


          </div>
          <div>
            <p className="text-2xl text-white-green">
              Recomendação do agronomo:
            </p>
            <span className="text-2xl text-white-green">
              lorem ipsum dolor sit amet escruz te vier no madare to su lorem
              ipsum dolor sit amet escruz te vier no madare to su
            </span>
          </div>
          <button
            onClick={() => {}}
            className="bg-secondary cursor-pointer text-white font-bold py-2 w-40 h-12 rounded hover:bg-emerald"
          >
            Nova Analise
          </button>
        </div>
      </main>

      <Footer title="Voltar para produtores" page="/listaProdutores" />
    </div>
  );
}

export default AddAnalise;
