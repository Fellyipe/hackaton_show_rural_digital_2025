import { List } from "@phosphor-icons/react";

import Footer from "../../components/footer/Footer";

function AnalisePotassio() {
  return (
    <div>
      <header className="bg-white-green w-full flex flex-col p-4">
        <button>
          <List size={42} />
        </button>
        <h1 className="text-center text-3xl">Analise de Potassio</h1>
      </header>
      <main className="bg-primary w-full h-screen rounded-t-2xl p-4">
        <div></div>
        <div>aaa</div>
      </main>

      <Footer title="Voltar para a tela inicial" page="/" />
    </div>
  );
}

export default AnalisePotassio;
