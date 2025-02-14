from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import csv
import PyPDF2
import pdfplumber
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
    """Extrai os dados do PDF usando pdfplumber."""
    extracted_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                extracted_text.extend(table)  # Adiciona todas as linhas da tabela extraída
    return extracted_text

def process_pdf(file_path):
    """Processa o PDF e calcula a média das variáveis"""
    extracted_data = extract_text_from_pdf(file_path)
    data = []

    for row in extracted_data:
        if len(row) >= 5 and row[0].startswith("L"):  # Exemplo: L01 0,13 1,1 0,87 1,36 4,95
            try:
                k = float(row[1].replace(",", "."))
                ca = float(row[2].replace(",", "."))
                mg = float(row[3].replace(",", "."))
                data.append({"K": k, "Ca": ca, "Mg": mg})
            except ValueError:
                continue

    if not data:
        return None

    avg_k = sum(d["K"] for d in data) / len(data)
    avg_ca = sum(d["Ca"] for d in data) / len(data)
    avg_mg = sum(d["Mg"] for d in data) / len(data)

    return {"K": avg_k, "Ca": avg_ca, "Mg": avg_mg}

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    """Recebe um PDF, extrai os dados e insere no banco"""
    if "pdf" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado!"}), 400

    pdf_file = request.files["pdf"]

    if pdf_file.filename == "":
        return jsonify({"error": "Nome do arquivo vazio!"}), 400

    if not allowed_file(pdf_file.filename):
        return jsonify({"error": "Arquivo inválido. Apenas PDFs são permitidos."}), 400

    filename = secure_filename(pdf_file.filename)
    temp_pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_file.save(temp_pdf_path)

    averages = process_pdf(temp_pdf_path)
    
    if not averages:
        os.remove(temp_pdf_path)
        return jsonify({"error": "Nenhum dado válido encontrado no PDF"}), 400

    analiseId = request.form.get("analiseId")  

    if not analiseId:
        return jsonify({"error": "O campo 'analiseId' é obrigatório!"}), 400

    save_analysis(analiseId, averages)
    os.remove(temp_pdf_path)

    return jsonify({"message": "PDF processado com sucesso!", "data": averages}), 200

# Definindo os intervalos de referência para os parâmetros.
# Você pode ajustar e adicionar os intervalos para os demais parâmetros.

def save_analysis(analiseId, averages):
    """Salva as médias no banco de dados vinculando ao analiseId"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        data_atual = datetime.today().date()

        for param, value in averages.items():
            classificacao = classify_value(param, value)

            # Verificando os tipos e valores
            print(f"Param: {param} ({type(param)})")
            print(f"Value: {value} ({type(value)})")
            print(f"Classificacao: {classificacao} ({type(classificacao)})")
            print(f"AnaliseID: {analiseId} ({type(analiseId)})")

            # Certificando-se de que são strings onde necessário
            param = str(param)
            value = str(value)
            id = analiseId
            classificacao = str(classificacao)

            # Atualiza a análise existente com os novos valores
            cursor.execute(
                """UPDATE Analises 
                   SET parametro = ?, valor = ?, data = ?, classificacao = ? 
                   WHERE id = ?""",
                (param, value, data_atual, classificacao, analiseId)
            )

            # Se a análise não existir, insere uma nova
            if cursor.rowcount == 0:
                cursor.execute(
                    """INSERT INTO Analises ( parametro, valor, data, classificacao) 
                       VALUES (?, ?, ?, ?)""",
                    ( param, value, data_atual, classificacao)
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

@app.route('/atualizar_analise', methods=['PUT'])
def atualizar_analise():
    """Atualiza os dados de uma análise existente sem sobrescrever campos não enviados."""
    dados = request.json
    print("Dados recebidos:", dados)
    analiseId = dados.get("analise_id")
    if not analiseId:
        return jsonify({"erro": "O ID da análise deve ser fornecido."}), 400

    # Conectar ao banco de dados
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            # Verifica se a análise existe e obtém os valores atuais
            cursor.execute("""
                SELECT calculo_recomendado, cooperativa_recomendada, valor_cooperativa, sugestao 
                FROM Analises WHERE id = ?
            """, (analiseId,))
            analise = cursor.fetchone()

            if not analise:
                return jsonify({"erro": "Análise não encontrada"}), 404

            # Mantém os valores atuais caso não sejam enviados
            calculo_recomendado = dados.get("calculo_recomendado", analise[0])
            cooperativa_recomendada = dados.get("cooperativa_recomendada", analise[1])
            valor_cooperativa = dados.get("valor_cooperativa", analise[2])
            sugestao = dados.get("sugestao", analise[3])
            agronomo_id = dados.get("agronomo_id")
            agricultor_id = dados.get("produtorId")

            # Atualiza apenas os campos necessários
            cursor.execute("""
                UPDATE Analises 
                SET agricultor_id = ?, agricultor_id = ?, calculo_recomendado = ?, cooperativa_recomendada = ?, valor_cooperativa = ?, sugestao = ?
                WHERE id = ?
            """, (agricultor_id, agronomo_id, calculo_recomendado, cooperativa_recomendada, valor_cooperativa, sugestao, analiseId))

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
