import Sprout from "../../assets/sprout.png";
import Footer from "../../components/footer/Footer";

function TelaAgronomo() {
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

          <div>
            <p className="text-2xl text-white-green">Potassio(K)</p>
            <spam className="text-4xl text-red">Baixo</spam>
          </div>
          <div>
            <p className="text-2xl text-white-green">Quantidade sugerida</p>
            <spam className="text-4xl font-bold text-white-green">50Kg</spam>
          </div>
          <div>
            <p className="text-2xl text-white-green">
              Recomendação de compra do agronomo:
            </p>
            <spam className="text-2xl text-white-green">
              Copavel: R$2.400,00
            </spam>
          </div>
          <div>
            <p className="text-2xl text-white-green">
              Recomendação do agronomo:
            </p>
            <spam className="text-2xl text-white-green">
              lorem ipsum dolor sit amet escruz te vier no madare to su lorem
              ipsum dolor sit amet escruz te vier no madare to su
            </spam>
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

export default TelaAgronomo;
