import sqlite3

DB_PATH = "oficina.db"


def conectar_banco():
    """Conecta ao banco de dados e retorna a conexão."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Retorna dicts ao invés de tuplas
    return conn


def criar_tabelas():
    """Cria as tabelas se não existirem."""
    conn = conectar_banco()
    cursor = conn.cursor()

    # Tabela de veículos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS veiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT NOT NULL UNIQUE,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        ano INTEGER NOT NULL,
        proprietario TEXT NOT NULL,
        data_cadastro TEXT NOT NULL
    )
    """)

    # Tabela de serviços
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        veiculo_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        data_entrada TEXT NOT NULL,
        valor REAL NOT NULL,
        concluido INTEGER DEFAULT 0,
        FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_tabelas()
    print("✅ Tabelas criadas com sucesso!")
