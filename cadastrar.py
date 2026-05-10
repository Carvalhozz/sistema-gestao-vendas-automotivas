import sqlite3
from datetime import datetime

def salvar_venda(nome, telefone, modelo, data, plataforma):
    conn = sqlite3.connect('vendas_loja.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vendas (nome_cliente, telefone, modelo_carro, data_venda, plataforma)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, telefone, modelo, data, plataforma))
    conn.commit()
    conn.close()
    print("\nVenda cadastrada com sucesso!")

# Interface simples no terminal
print("--- SISTEMA DE CADASTRO DE VENDAS ---")
nome = input("Nome do Cliente: ")
tel = input("Telefone: ")
carro = input("Modelo do Carro: ")
data = input("Data (AAAA-MM-DD) ou enter para hoje: ") or datetime.now().strftime("%Y-%m-%d")
origem = input("Plataforma (OLX, Instagram, Facebook, Loja): ")

salvar_venda(nome, tel, carro, data, origem)