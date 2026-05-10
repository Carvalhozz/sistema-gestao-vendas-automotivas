import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 1. Carrega os dados
conn = sqlite3.connect('vendas_loja.db')
df = pd.read_sql_query("SELECT * FROM vendas", conn)
conn.close()

# Converte data e cria coluna de Mês/Ano
df['data_venda'] = pd.to_datetime(df['data_venda'])
df['mes_ano'] = df['data_venda'].dt.strftime('%m/%Y')

# FILTRO: Ver apenas o mês atual
mes_atual = datetime.now().strftime('%m/%Y')
df_filtrado = df[df['mes_ano'] == mes_atual]

if df_filtrado.empty:
    print(f"Sem vendas cadastradas em {mes_atual}")
else:
    # Análise de Faturamento por Plataforma
    faturamento = df_filtrado.groupby('plataforma')['preco'].sum()

    # Gráfico
    plt.figure(figsize=(10, 6))
    faturamento.plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title(f'Distribuição de Faturamento por Origem ({mes_atual})')
    plt.ylabel('')
    
    print(f"Total Faturado em {mes_atual}: R$ {faturamento.sum():,.2f}")
    plt.show()