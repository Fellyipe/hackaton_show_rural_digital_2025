import PyPDF2

# Abrir o arquivo PDF
with open('C:/Users/Felipe/Downloads/RELATORIO DE FREQUENCIA DE DEFESAS.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    # Extrair texto de cada página
    for page in reader.pages:
        print(page.extract_text())


