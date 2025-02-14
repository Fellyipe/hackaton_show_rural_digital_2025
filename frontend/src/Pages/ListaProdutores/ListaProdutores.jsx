import React from "react";
import ProdutorCard from "../../components/ProdutorCard/ProdutorCard";

import Footer from "../../components/footer/Footer";

const produtores = [
  { id: 1, name: "José", cooperativa: "Cebrapa" },
  { id: 2, name: "Monica", cooperativa: "Cebrapa" },
  { id: 3, name: "Ademar", cooperativa: "Cebrapa" },
  { id: 4, name: "José", cooperativa: "Cebrapa" },
  { id: 5, name: "Monica", cooperativa: "Cebrapa" },
  { id: 6, name: "Ademar", cooperativa: "Cebrapa" },
  { id: 7, name: "José", cooperativa: "Cebrapa" },
  { id: 8, name: "Monica", cooperativa: "Cebrapa" },
  { id: 9, name: "Ademar", cooperativa: "Cebrapa" },
];

function ListaProdutores() {
  const navigateToDetail = (produtor) => {
    console.log("Navegando para detalhes:", produtor);
  };

  return (
    <>
      <div className="max-w-3xl mx-auto p-4 mb-10">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">
          Lista de produtores
        </h1>
        <div className="space-y-4">
          {produtores.map((produtor) => (
            <ProdutorCard
              key={produtor.id}
              produtor={produtor}
              navigateToDetail={navigateToDetail}
            />
          ))}
        </div>
      </div>
      <Footer title="Voltar para a tela inicial" page="/Login" />
    </>
  );
}

export default ListaProdutores;
