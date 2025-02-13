import React from "react";

import { ArrowRight } from "lucide-react";

const IncidentCard = ({ incident, navigateToDetail }) => {
  return (
    <div className="p-6 bg-white rounded-lg shadow-md mb-4">
      <p className="text-sm font-bold text-gray-700">ONG:</p>
      <p className="text-base text-gray-500 mb-4">{incident.name}</p>

      <p className="text-sm font-bold text-gray-700">CASO:</p>
      <p className="text-base text-gray-500 mb-4">{incident.title}</p>

      <p className="text-sm font-bold text-gray-700">Valor:</p>
      <p className="text-base text-gray-500 mb-4">
        {new Intl.NumberFormat("pt-BR", {
          style: "currency",
          currency: "BRL",
        }).format(incident.value)}
      </p>

      <button
        className="flex items-center justify-between text-red-500 font-bold text-base"
        onClick={() => navigateToDetail(incident)}
      >
        Ver mais detalhes
        <ArrowRight size={16} />
      </button>
    </div>
  );
};

export default IncidentCard;
