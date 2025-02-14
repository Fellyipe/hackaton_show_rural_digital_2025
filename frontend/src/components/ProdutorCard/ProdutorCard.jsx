import React from "react";

import { ArrowRight } from "@phosphor-icons/react";

const ProdutorCard = ({ produtor, navigateToDetail }) => {
  return (
    <div className="p-6 bg-primary rounded-lg shadow-md mb-4">
      <div className="flex justify-between">
        <div>
          <p className="text-sm font-bold text-white-green">Nome:</p>
          <p className="text-base text-white-green mb-4">{produtor.name}</p>
        </div>

        <div>
          <p className="text-sm font-bold text-white-green">Cooperativa:</p>
          <p className="text-base text-white-green mb-4">
            {produtor.cooperativa}
          </p>
        </div>
      </div>

      <button
        className="flex items-center justify-between w-full text-emerald font-bold text-base border-t-2 border-emerald"
        onClick={() => navigateToDetail()}
      >
        Ver mais detalhes
        <ArrowRight size={16} />
      </button>
    </div>
  );
};

export default ProdutorCard;
