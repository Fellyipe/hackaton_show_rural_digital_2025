from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import sqlite3
from db import init_db
from refs import reference_intervals
import pandas as pd
import pdfplumber
import hashlib
from werkzeug.utils import secure_filename
from graph_utils import *


#df = pd.read_csv("dados.csv", delimiter=";", header=0, names=["latitude", "longitude"])
#compute_centroid(parse_src_file(df))

DATABASE = "banco_de_dados.db"  # Nome do arquivo do banco SQLite

app = Flask(__name__)
CORS(app)
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

def save_analysis(cpf, cref, data):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO Agricultores (cpf) VALUES (?)", (cpf,))
        cursor.execute("INSERT OR IGNORE INTO Agronomos (cref) VALUES (?)", (cref,))
        
        cursor.execute("SELECT id FROM Agricultores WHERE cpf = ?", (cpf,))
        agricultor_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM Agronomos WHERE cref = ?", (cref,))
        agronomo_id = cursor.fetchone()[0]
        
        for row in data:
            for param, value in row.items():
                if param != 'classification':
                    classification = classify_value(param, value)
                    cursor.execute(
                        "INSERT INTO Analises (agricultor_id, agronomo_id, parametro, valor, classificacao) VALUES (?, ?, ?, ?, ?)",
                        (agricultor_id, agronomo_id, param, value, classification)
                    )
        conn.commit()

def classify_value(parameter, value):
    """
    Classifica um valor para um determinado parâmetro com base nos intervalos definidos.
    Caso o valor seja inválido ou não informado, retorna None.
    """
    if value is None or value == "":
        return None  # Ignora parâmetros não informados

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
        min_val = interval.get('min')
        max_val = interval.get('max')

        # Se não há valor mínimo definido, compara apenas com o máximo.
        if min_val is None and val < max_val:
            return interval['class']
        # Se não há valor máximo definido, compara apenas com o mínimo.
        elif max_val is None and val > min_val:
            return interval['class']
        # Se ambos os valores estão definidos, verifica se o valor está no intervalo.
        elif min_val is not None and max_val is not None and min_val <= val <= max_val:
            return interval['class']

    return None  # Se não encontrou nenhuma classificação válida


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
 #   if 'pdf' not in request.files:
  #      return jsonify({'error': 'Nenhum arquivo enviado com o nome "pdf"'}), 400
    
    pdf_file = request.files['pdf']
    if pdf_file.filename == '' or not allowed_file(pdf_file.filename):
        return jsonify({'error': 'Arquivo inválido'}), 450
    
    pdf_file.seek(0, os.SEEK_END)
    file_size = pdf_file.tell()
    pdf_file.seek(0)
 #   if file_size > MAX_FILE_SIZE:
 #       return jsonify({'error': 'Arquivo excede 5MB'}), 500
    
    filename = secure_filename(pdf_file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_file.save(file_path)
    
    extracted_data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                header = table[0]
                for row in table[1:]:
                    extracted_data.append(dict(zip(header, row)))
    
    cpf = request.form.get('cpf')
    cref = request.form.get('cref')
 #   if not cpf or not cref:
  #      return jsonify({'error': 'CPF e cref são obrigatórios'}), 550
    
    save_analysis(cpf, cref, extracted_data)
    return jsonify({'message': 'PDF processado e salvo com sucesso!'})

@app.route('/analises', methods=['GET'])
def get_analises():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT A.cpf, AG.cref, AN.parametro, AN.valor, AN.classificacao FROM Analises AN "+
                        "JOIN Agricultores A ON AN.agricultor_id = A.id "+
                        "JOIN Agronomos AG ON AN.agronomo_id = AG.id")
        results = cursor.fetchall()
    
    return jsonify([{'cpf': row[0], 'cref': row[1], 'parametro': row[2], 'valor': row[3], 'classificacao': row[4]} for row in results])


def hash_senha(senha):
    """Criptografa a senha usando SHA-256."""
    return hashlib.sha256(senha.encode()).hexdigest()

@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    """Registra um novo usuário como agricultor ou agrônomo."""
    dados = request.json  # Obtém os dados do corpo da requisição
    nome = dados.get("nome")
    senha = dados.get("senha")
    cpf = dados.get("cpf")
    cref = dados.get("cref")  # Opcional, pode ser None

    if not nome or not senha or not cpf:
        return jsonify({"erro": "Nome, senha e CPF são obrigatórios"}), 400

    senha_hash = hash_senha(senha)
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            if cref:
                cursor.execute(
                    "INSERT INTO Agronomos (nome, senha, cpf, cref) VALUES (?, ?, ?, ?)", 
                    (nome, senha_hash, cpf, cref)
                )
                return jsonify({"mensagem": "Agrônomo registrado com sucesso!"}), 201
            else:
                cursor.execute(
                    "INSERT INTO Agricultores (nome, senha, cpf) VALUES (?, ?, ?)", 
                    (nome, senha_hash, cpf)
                )
                return jsonify({"mensagem": "Agricultor registrado com sucesso!"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"erro": "CPF ou cref já cadastrado"}), 400

@app.route('/login', methods=['GET'])
def login_usuario():
    """Realiza o login e retorna o tipo de usuário (Agricultor ou Agrônomo)."""
    cpf = request.args.get("cpf")
    senha = request.args.get("senha")

    if not cpf or not senha:
        return jsonify({"erro": "CPF e senha são obrigatórios"}), 400

    senha_hash = hash_senha(senha)

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Verifica primeiro na tabela Agricultores
        cursor.execute("SELECT id, nome FROM Agricultores WHERE cpf = ? AND senha = ?", (cpf, senha_hash))
        agricultor = cursor.fetchone()

        if agricultor:
            return jsonify({"tipo": "agricultor", "id": agricultor[0], "nome": agricultor[1]}), 200

        # Se não encontrou, verifica na tabela Agrônomos
        cursor.execute("SELECT id, nome FROM Agronomos WHERE cpf = ? AND senha = ?", (cpf, senha_hash))
        agronomo = cursor.fetchone()

        if agronomo:
            return jsonify({"tipo": "agronomo", "id": agronomo[0], "nome": agronomo[1]}), 200

        return jsonify({"erro": "CPF ou senha incorretos"}), 400

@app.route('/produtores', methods=['GET'])
def produtores():
    produtor_id = request.args.get("id")

    if not produtor_id:
        return jsonify({"erro": "ID do produtor é obrigatório"}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Verifica se o ID pertence a um agricultor
        cursor.execute("SELECT id, nome FROM Agricultores WHERE id = ?", (produtor_id,))
        agricultor = cursor.fetchone()

        if not agricultor:
            return jsonify({"erro": "Agricultor não encontrado"}), 404

        # Busca todas as análises associadas ao agricultor
        cursor.execute("""
            SELECT id, agronomo_id, parametro, valor, data, classificacao 
            FROM Analises 
            WHERE agricultor_id = ?
        """, (produtor_id,))
        
        analises = cursor.fetchall()

        # Formata os resultados
        analises_formatadas = [
            {
                "id": row[0],
                "agronomo_id": row[1],
                "parametro": row[2],
                "valor": row[3],
                "data": row[4],
                "classificacao": row[5],
            }
            for row in analises
        ]

        return jsonify({
            "id": agricultor[0],
            "nome": agricultor[1],
            "analises": analises_formatadas
        }), 200

@app.route('/registro_analise', methods=['POST'])
def registrar_analise():
    """Registra uma nova análise associando um agrônomo a um agricultor pelo CPF."""
    dados = request.json
    
    agronomo_id = dados.get("agronomo_id")
    produtor_cpf = dados.get("produtor_cpf")
    parametro = dados.get("parametro")
    valor = dados.get("valor")
    classificacao = dados.get("classificacao")

    if not (agronomo_id and produtor_cpf and parametro and valor and classificacao):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Busca o ID do agricultor pelo CPF
        cursor.execute("SELECT id FROM Agricultores WHERE cpf = ?", (produtor_cpf,))
        agricultor = cursor.fetchone()

        if not agricultor:
            return jsonify({"erro": "Agricultor não encontrado"}), 404

        agricultor_id = agricultor[0]
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formata a data e hora

        # Insere a nova análise sem precisar da data na requisição
        cursor.execute("""
            INSERT INTO Analises (agricultor_id, agronomo_id, parametro, valor, data, classificacao)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (agricultor_id, agronomo_id, parametro, valor, data_atual, classificacao))

        conn.commit()

        return jsonify({"mensagem": "Análise registrada com sucesso!", "data": data_atual}), 201

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

