from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import csv
import PyPDF2
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

CSV_FOLDER = "csv_files"
ALLOWED_EXTENSIONS = {'pdf'}

# Certifique-se de que a pasta de CSV existe
os.makedirs(CSV_FOLDER, exist_ok=True)



def allowed_file(filename):
    """Verifica se o arquivo tem a extensão .pdf"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extrai o texto de um PDF usando PyPDF2"""
    extracted_text = []
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
    return "\n".join(extracted_text)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    """Recebe um PDF, extrai o texto e salva como CSV"""
    if 'pdf' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado!'}), 400

    pdf_file = request.files['pdf']

    if pdf_file.filename == '':
        return jsonify({'error': 'Nome do arquivo vazio!'}), 400

    if not allowed_file(pdf_file.filename):
        return jsonify({'error': 'Arquivo inválido. Apenas PDFs são permitidos.'}), 400

    filename = secure_filename(pdf_file.filename)
    temp_pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_file.save(temp_pdf_path)

    extracted_text = extract_text_from_pdf(temp_pdf_path)
    
    if not extracted_text:
        os.remove(temp_pdf_path)
        return jsonify({'error': 'Nenhum texto encontrado no PDF'}), 400

    csv_filename = f"{os.path.splitext(filename)[0]}.csv"
    csv_path = os.path.join(CSV_FOLDER, csv_filename)

    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for line in extracted_text.split("\n"):
            writer.writerow([line])

    os.remove(temp_pdf_path)

    process_csv(csv_path)

    return jsonify({'message': 'PDF processado com sucesso!', 'csv_file': csv_path}), 200

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

def process_csv(csv_path):
    """Processa o CSV gerado do PDF, segmenta os dados por parâmetros e aplica classify_value."""
    
    df = pd.read_csv(csv_path)

    # Suponha que a segmentação seja feita com base em uma coluna chamada 'Parametro'
    parametro_col = 'Parametro'  # Ajuste para a coluna correta
    valor_col = 'Valor'  # Ajuste para a coluna de valores

    if parametro_col not in df.columns or valor_col not in df.columns:
        raise ValueError(f"Colunas esperadas '{parametro_col}' e '{valor_col}' não encontradas no CSV!")

    # Itera sobre os diferentes parâmetros e valores
    resultados = {}
    for parametro, sub_df in df.groupby(parametro_col):
        sub_df['Classificacao'] = sub_df[valor_col].apply(classify_value)  # Aplica a classificação
        resultados[parametro] = sub_df

    # Salva cada conjunto de dados classificado em arquivos separados
    for parametro, data in resultados.items():
        output_path = f"{os.path.splitext(csv_path)[0]}_{parametro}.csv"
        data.to_csv(output_path, index=False)
        print(f"Arquivo salvo: {output_path}")

    return resultados  # Retorna um dicionário com os DataFrames segmentados

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
    produtor_id = request.args.get("agronomo_id")

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

    if not (agronomo_id and produtor_cpf):
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

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "banco_de_dados.db"

@app.route('/atualizar_analise', methods=['PUT'])
def atualizar_analise(analise_id):
    """Atualiza os dados de uma análise existente sem sobrescrever campos não enviados."""

    dados = request.json

    # Conectar ao banco de dados
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            # Verifica se a análise existe e obtém os valores atuais
            cursor.execute("""
                SELECT calculo_recomendado, cooperativa_recomendada, valor_cooperativa, sugestao 
                FROM Analises WHERE id = ?
            """, (analise_id,))
            analise = cursor.fetchone()

            if not analise:
                return jsonify({"erro": "Análise não encontrada"}), 404

            # Mantém os valores atuais caso não sejam enviados
            calculo_recomendado = dados.get("calculo_recomendado", analise[0])
            cooperativa_recomendada = dados.get("cooperativa_recomendada", analise[1])
            valor_cooperativa = dados.get("valor_cooperativa", analise[2])
            sugestao = dados.get("sugestao", analise[3])

            # Atualiza apenas os campos necessários
            cursor.execute("""
                UPDATE Analises 
                SET calculo_recomendado = ?, cooperativa_recomendada = ?, valor_cooperativa = ?, sugestao = ?
                WHERE id = ?
            """, (calculo_recomendado, cooperativa_recomendada, valor_cooperativa, sugestao, analise_id))

            conn.commit()

        return jsonify({"mensagem": "Análise atualizada com sucesso!"}), 200

    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro no banco de dados: {str(e)}"}), 500

@app.route('/resultados_analise', methods=['GET'])
def obter_resultados_analise():
    """Retorna todas as análises registradas para um determinado parâmetro indexado."""
    
    parametro_index = request.args.get("parametro_index", type=int)

    if parametro_index is None:
        return jsonify({"erro": "É necessário fornecer o índice do parâmetro."}), 400

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            # Obtém todas as análises para o parâmetro indexado
            cursor.execute("""
                SELECT id, agricultor_id, agronomo_id, parametro, valor, classificacao
                FROM Analises
                ORDER BY parametro
            """)
            todas_analises = cursor.fetchall()

            if not todas_analises:
                return jsonify({"erro": "Nenhuma análise encontrada."}), 404

            # Criar um dicionário agrupado por parâmetro
            analises_por_parametro = {}
            for analise in todas_analises:
                param = analise[3]  # Coluna 'parametro'
                if param not in analises_por_parametro:
                    analises_por_parametro[param] = []
                analises_por_parametro[param].append({
                    "id": analise[0],
                    "agricultor_id": analise[1],
                    "agronomo_id": analise[2],
                    "valor": analise[4],
                    "classificacao": analise[5]
                })

            # Obtém o nome do parâmetro correspondente ao índice solicitado
            parametros_disponiveis = list(analises_por_parametro.keys())

            if parametro_index < 0 or parametro_index >= len(parametros_disponiveis):
                return jsonify({"erro": "Índice de parâmetro inválido."}), 400

            parametro_escolhido = parametros_disponiveis[parametro_index]
            analises_filtradas = analises_por_parametro[parametro_escolhido]

            # Calcular a porcentagem de classificação
            total_analises = len(analises_filtradas)
            classificacao_contagem = {}

            for analise in analises_filtradas:
                classificacao = analise["classificacao"]
                classificacao_contagem[classificacao] = classificacao_contagem.get(classificacao, 0) + 1

            for analise in analises_filtradas:
                analise["percentual_classificacao"] = round(
                    (classificacao_contagem[analise["classificacao"]] / total_analises) * 100, 2
                )

            return jsonify({
                "parametro": parametro_escolhido,
                "analises": analises_filtradas
            }), 200

    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro no banco de dados: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

