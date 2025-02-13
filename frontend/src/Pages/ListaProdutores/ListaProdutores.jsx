import React from "react";
import IncidentCard from "./IncidentCard";

const incidentes = [
  { id: 1, name: "ONG A", title: "Ajuda para cães", value: 120.5 },
  { id: 2, name: "ONG B", title: "Resgate de gatos", value: 250.0 },
  { id: 3, name: "ONG C", title: "Abrigo para animais", value: 320.75 },
];

function ListaProdutores() {
  const navigateToDetail = (incident) => {
    console.log("Navegando para detalhes:", incident);
  };

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">
        Lista de Incidentes
      </h1>
      <div className="space-y-4">
        {incidentes.map((incident) => (
          <IncidentCard
            key={incident.id}
            incident={incident}
            navigateToDetail={navigateToDetail}
          />
        ))}
      </div>
    </div>
  );
}

export default ListaProdutores;
