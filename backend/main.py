from flask import Flask, request, jsonify
import os
from db import init_db
from refs import reference_intervals
import pandas as pd
import pdfplumber
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

def allowed_file(filename):
    """Verifica se o arquivo possui uma extensão válida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_tables_from_pdf(file_path):
    """Extrai tabelas do PDF e retorna uma lista de tabelas em formato JSON com classificação."""
    tables = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                header = table[0]           # Primeiro elemento é o cabeçalho
                data_rows = table[1:]       # O restante são os dados
                classified_data = []        # Lista para armazenar os dados classificados

                # Converte cada linha de dados para dicionário utilizando o cabeçalho
                for row in data_rows:
                    row_dict = dict(zip(header, row))
                    # Para cada parâmetro definido, aplica a classificação se o valor existir
                    for parameter in reference_intervals:
                        value = row_dict.get(parameter)
                        if value is not None:
                            row_dict[f"{parameter}_classification"] = classify_value(parameter, value)
                    classified_data.append(row_dict)

                tables.append(classified_data)
    return tables if tables else None

# Definindo os intervalos de referência para os parâmetros.
# Você pode ajustar e adicionar os intervalos para os demais parâmetros.


def classify_value(parameter, value):
    """
    Classifica um valor para um determinado parâmetro com base nos intervalos definidos.
    Caso o valor seja inválido, retorna None.
    """
    try:
        # Caso o valor venha como string e use vírgula para decimal, substituímos por ponto.
        if isinstance(value, str):
            value = value.replace(',', '.')
        val = float(value)
    except (ValueError, TypeError):
        return None

    intervals = reference_intervals.get(parameter)
    if not intervals:
        return None

    for interval in intervals:
        min_val = interval['min']
        max_val = interval['max']
        # Se não há valor mínimo definido, compara apenas com o máximo.
        if min_val is None:
            if val < max_val:
                return interval['class']
        # Se não há valor máximo definido, compara apenas com o mínimo.
        elif max_val is None:
            if val > min_val:
                return interval['class']
        else:
            if min_val <= val <= max_val:
                return interval['class']
    return None

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    # Verifica se o arquivo foi enviado com a chave 'pdf'
    if 'pdf' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado com o nome "pdf"'}), 400

    pdf_file = request.files['pdf']

    if pdf_file.filename == '':
        return jsonify({'error': 'Nome do arquivo vazio'}), 400

    if not allowed_file(pdf_file.filename):
        return jsonify({'error': 'Formato de arquivo inválido. Apenas PDFs são permitidos.'}), 400

    # Verifica o tamanho do arquivo
    pdf_file.seek(0, os.SEEK_END)
    file_size = pdf_file.tell()
    pdf_file.seek(0)
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'O arquivo excede o tamanho máximo permitido (5MB)'}), 400

    # Garante um nome seguro e salva o arquivo
    filename = secure_filename(pdf_file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_file.save(file_path)

    # Extrai as tabelas do PDF
    extracted_tables = extract_tables_from_pdf(file_path)

    if extracted_tables:
        classified_tables = []
        # Itera sobre cada tabela extraída
        for table in extracted_tables:
            classified_data = []
            for row in table:
                # Exemplo de classificação para pH
                ph_value = row.get("pH")
                row["pH_classification"] = classify_value('pH', ph_value)
                
                # Exemplo de classificação para Al³+ (ajuste o nome da coluna conforme seu PDF)
                al_value = row.get("Al³+")
                row["Al³+_classification"] = classify_value('Al³+', al_value)

                # Você pode adicionar a classificação para outros parâmetros aqui...
                
                classified_data.append(row)
            classified_tables.append(classified_data)
        return jsonify({
            'message': 'PDF processado com sucesso!',
            'tables': classified_tables
        })
    else:
        return jsonify({'message': 'PDF recebido, mas nenhuma tabela foi encontrada.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
