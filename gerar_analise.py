import sqlite3
import pandas as pd

# 1. Conectar ao banco e ler os dados
conn = sqlite3.connect('vendas_loja.db')
df = pd.read_sql_query("SELECT * FROM vendas", conn)
conn.close()

print("\n--- VISÃO GERAL DOS DADOS ---")
print(df.head()) # Mostra as primeiras linhas

# 2. Análise de Marketing (Qual plataforma vende mais?)
print("\n--- VENDAS POR PLATAFORMA ---")
analise_plataforma = df['plataforma'].value_counts()
print(analise_plataforma)

# 3. Análise de Estoque (Qual modelo sai mais?)
print("\n--- MODELOS MAIS VENDIDOS ---")
analise_modelo = df['modelo_carro'].value_counts()
print(analise_modelo)

# 4. Exportar para Excel (Para mostrar que você sabe integrar ferramentas)
df.to_excel('relatorio_vendas.xlsx', index=False)
print("\nSucesso! Arquivo 'relatorio_vendas.xlsx' gerado.")