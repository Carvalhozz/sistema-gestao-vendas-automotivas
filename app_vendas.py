import customtkinter as ctk
import sqlite3
import pandas as pd
from datetime import datetime
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- CONFIGURAÇÃO DO BANCO ---
def configurar_banco():
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

configurar_banco()

# --- FUNÇÕES DE LÓGICA ---

def abrir_dashboard():
    # 1. Busca os dados
    conn = sqlite3.connect('vendas_loja.db')
    df = pd.read_sql_query("SELECT plataforma, SUM(preco) as total FROM vendas GROUP BY plataforma", conn)
    conn.close()

    if df.empty:
        messagebox.showwarning("Aviso", "Sem dados para gerar gráfico!")
        return

    # 2. Criar a nova janela para o gráfico
    janela_dash = ctk.CTkToplevel(app)
    janela_dash.title("Dashboard de Faturamento")
    janela_dash.geometry("600x500")
    janela_dash.after(200, lambda: janela_dash.focus_force()) # Traz para frente

    # 3. Criar o gráfico com Matplotlib
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    df.plot(kind='bar', x='plataforma', y='total', ax=ax, color='#1f77b4', edgecolor='black')
    ax.set_title("Faturamento Total por Plataforma")
    ax.set_ylabel("Valor em R$")
    ax.set_xlabel("Origem")
    plt.tight_layout()

    # 4. Colocar o gráfico dentro da janela do CustomTkinter
    canvas = FigureCanvasTkAgg(fig, master=janela_dash)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20, padx=20, fill="both", expand=True)

def salvar_dados():
    try:
        nome = entry_nome.get()
        tel = entry_tel.get()
        carro = combo_carro.get()
        data = entry_data.get() or datetime.now().strftime("%Y-%m-%d")
        origem = combo_origem.get()
        
        texto_preco = entry_preco.get().replace(',', '.')
        if not nome or not texto_preco:
            messagebox.showwarning("Erro", "Nome e Preço são obrigatórios!")
            return
        
        preco = float(texto_preco)

        conn = sqlite3.connect('vendas_loja.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vendas (nome_cliente, telefone, modelo_carro, data_venda, plataforma, preco)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, tel, carro, data, origem, preco))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", f"Venda salva!")
        limpar_campos()
    except:
        messagebox.showerror("Erro", "Verifique o valor do preço.")

def exportar_excel():
    try:
        conn = sqlite3.connect('vendas_loja.db')
        df = pd.read_sql_query("SELECT * FROM vendas", conn)
        conn.close()
        caminho = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if caminho:
            df.to_excel(caminho, index=False)
            messagebox.showinfo("Sucesso", "Excel gerado!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def limpar_campos():
    entry_nome.delete(0, 'end')
    entry_tel.delete(0, 'end')
    entry_preco.delete(0, 'end')

# --- INTERFACE ---
app = ctk.CTk()
app.title("Gestão de Vendas v3.0")
app.geometry("450x700")

ctk.CTkLabel(app, text="SISTEMA DE VENDAS", font=("Arial", 22, "bold")).pack(pady=20)

entry_nome = ctk.CTkEntry(app, placeholder_text="Nome do Cliente", width=350)
entry_nome.pack(pady=10)

entry_tel = ctk.CTkEntry(app, placeholder_text="Telefone", width=350)
entry_tel.pack(pady=10)

combo_carro = ctk.CTkComboBox(app, values=["Argo", "Polo", "HB20", "Onix", "Corolla", "Outro"], width=350)
combo_carro.pack(pady=10)

entry_preco = ctk.CTkEntry(app, placeholder_text="Preço (Ex: 50000)", width=350)
entry_preco.pack(pady=10)

entry_data = ctk.CTkEntry(app, placeholder_text="Data (AAAA-MM-DD)", width=350)
entry_data.pack(pady=10)

combo_origem = ctk.CTkComboBox(app, values=["Instagram", "OLX", "Facebook", "Loja Física"], width=350)
combo_origem.pack(pady=10)

btn_salvar = ctk.CTkButton(app, text="SALVAR VENDA", command=salvar_dados, fg_color="blue", width=250)
btn_salvar.pack(pady=20)

# Novos botões de saída
btn_dash = ctk.CTkButton(app, text="📊 VER DASHBOARD", command=abrir_dashboard, fg_color="#555555", width=250)
btn_dash.pack(pady=5)

btn_excel = ctk.CTkButton(app, text="📁 EXPORTAR EXCEL", command=exportar_excel, fg_color="green", width=250)
btn_excel.pack(pady=5)

app.mainloop()