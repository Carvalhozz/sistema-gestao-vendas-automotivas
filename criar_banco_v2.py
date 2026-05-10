import sqlite3

conn = sqlite3.connect('vendas_loja.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cliente TEXT NOT NULL,
    telefone TEXT,
    modelo_carro TEXT NOT NULL,
    data_venda DATE NOT NULL,
    plataforma TEXT NOT NULL,
    preco REAL NOT NULL
)
''')

conn.commit()
conn.close()
print("Banco atualizado com sucesso!")