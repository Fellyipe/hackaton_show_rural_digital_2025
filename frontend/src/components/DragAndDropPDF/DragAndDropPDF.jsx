import { useState } from "react";
import { CloudArrowUp, FilePdf } from "@phosphor-icons/react";

function DragAndDropPDF({ onFileUpload }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  const handleFile = (selectedFile) => {
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setError("");
      if (onFileUpload) onFileUpload(selectedFile);
    } else {
      setError("Apenas arquivos PDF são permitidos.");
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0];
    handleFile(droppedFile);
  };

  return (
    <div
      className="bg-white border-2 border- border-dashed border-gray-300 p-6 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-green-500 transition"
      onDrop={handleDrop}
      onDragOver={(event) => event.preventDefault()}
      onClick={() => document.getElementById("pdfInput").click()}
    >
      <input
        id="pdfInput"
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={(e) => handleFile(e.target.files[0])}
      />
      {file ? (
        <div className="flex items-center gap-2">
          <FilePdf size={24} className="text-red-500" />
          <span className="text-gray-700">{file.name}</span>
        </div>
      ) : (
        <>
          <CloudArrowUp size={40} className="text-gray-400" />
          <p className="text-gray-600 mt-2">Arraste e solte um PDF aqui</p>
          <p className="text-sm text-gray-500">ou clique para selecionar</p>
        </>
      )}
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
}

export default DragAndDropPDF;
