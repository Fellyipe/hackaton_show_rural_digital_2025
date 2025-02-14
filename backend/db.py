import sqlite3

DATABASE = "banco_de_dados.db"  # Nome do arquivo do banco SQLite

def init_db():
    """Cria as tabelas do banco de dados se não existirem."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS Agricultores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Agronomos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                crea TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Analises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agricultor_id INTEGER,
                agronomo_id INTEGER,
                parametro TEXT,
                valor TEXT,
                data DATE,
                classificacao TEXT,
                FOREIGN KEY (agricultor_id) REFERENCES Agricultores(id),
                FOREIGN KEY (agronomo_id) REFERENCES Agronomos(id)
            );
        ''')
        conn.commit()