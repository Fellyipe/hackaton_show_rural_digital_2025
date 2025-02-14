import { List } from "@phosphor-icons/react";
import Sprout from "../../assets/sprout.png";
import Footer from "../../components/footer/Footer";

function TelaAgronomo() {
  return (
    <div>
      <main className="bg-primary w-full h-screen mt-40 rounded-t-2xl p-4">
        <div className="flex w-full justify-end items-end">
          <img className="-mt-32" src={Sprout} alt="sprout" />
        </div>
        <div>
          <span className="text-4xl text-emerald font-bold">
            Resultado da analise:
          </span>
        </div>
      </main>

      <Footer title="Voltar para produtores" page="/listaProdutores" />
    </div>
  );
}

export default TelaAgronomo;
