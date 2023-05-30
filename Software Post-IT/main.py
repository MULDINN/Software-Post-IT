import tkinter as tk
import sqlite3
from tkinter import messagebox

def adicionar_postit():
    titulo = titulo_entry.get()
    descricao = descricao_entry.get('1.0', 'end-1c')
    dia = dia_spinbox.get()
    mes = mes_spinbox.get()
    ano = ano_spinbox.get()

    if not titulo or not descricao or not dia or not mes or not ano:
        messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")
        return

    # Conectar ao banco de dados
    conn = sqlite3.connect('postits.db')
    cursor = conn.cursor()

    # Criar tabela se ainda não existir
    cursor.execute('''CREATE TABLE IF NOT EXISTS postits
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, descricao TEXT, prazo TEXT)''')

    # Inserir dados do post-it na tabela
    prazo = f"{dia}/{mes}/{ano}"
    cursor.execute("INSERT INTO postits (titulo, descricao, prazo) VALUES (?, ?, ?)", (titulo, descricao, prazo))
    conn.commit()

    # Recuperar o ID do post-it inserido
    postit_id = cursor.lastrowid

    # Fechar a conexão com o banco de dados
    conn.close()

    postit_frame = tk.LabelFrame(canvas_frame, bg='white', padx=10, pady=10, relief='solid', bd=1)
    postit_frame.pack(pady=10)

    titulo_label = tk.Label(postit_frame, text=titulo, font=('Arial', 14, 'bold'), fg='black', bg='white')
    titulo_label.pack(anchor='w')

    descricao_label = tk.Label(postit_frame, text=descricao, font=('Arial', 12), fg='black', bg='white', wraplength=300)
    descricao_label.pack(anchor='w')

    prazo_label = tk.Label(postit_frame, text="Prazo:", font=('Arial', 12, 'bold'), fg='black', bg='white')
    prazo_label.pack(anchor='w')

    data_frame = tk.Frame(postit_frame, bg='white')
    data_frame.pack(anchor='w')

    dia_label = tk.Label(data_frame, text=dia, font=('Arial', 12), fg='black', bg='white')
    dia_label.grid(row=0, column=0, padx=5)

    mes_label = tk.Label(data_frame, text=mes, font=('Arial', 12), fg='black', bg='white')
    mes_label.grid(row=0, column=1, padx=5)

    ano_label = tk.Label(data_frame, text=ano, font=('Arial', 12), fg='black', bg='white')
    ano_label.grid(row=0, column=2, padx=5)

    # Botão "X" para fechar o post-it
    close_button = tk.Button(postit_frame, text="X", font=('Arial', 12), fg='black', bg='white', bd=0, command=lambda frame=postit_frame, postit_id=postit_id: excluir_postit(frame, postit_id))
    close_button.place(relx=1, rely=0, anchor='ne')

    titulo_entry.delete(0, 'end')
    descricao_entry.delete('1.0', 'end')

def excluir_postit(frame, postit_id):
    response = messagebox.askyesno("Excluir Post-it", "Deseja realmente excluir este post-it?")
    if response == tk.YES:
        # Conectar ao banco de dados
        conn = sqlite3.connect('postits.db')
        cursor = conn.cursor()

        # Remover o post-it do banco de dados
        cursor.execute("DELETE FROM postits WHERE id=?", (postit_id,))
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        frame.destroy()

root = tk.Tk()
root.title("Criador de Post-its")

canvas_frame = tk.Frame(root, bg='white')
canvas_frame.pack(fill='both', expand=True)

titulo_label = tk.Label(canvas_frame, text="Título:", font=('Arial', 12), fg='black', bg='white')
titulo_label.pack()

titulo_entry = tk.Entry(canvas_frame, font=('Arial', 12), fg='black', bg='white')
titulo_entry.pack(pady=5)

descricao_label = tk.Label(canvas_frame, text="Descrição:", font=('Arial', 12), fg='black', bg='white')
descricao_label.pack()

descricao_entry = tk.Text(canvas_frame, font=('Arial', 12), fg='black', bg='white', height=4)
descricao_entry.pack(pady=5)

prazo_label = tk.Label(canvas_frame, text="Prazo:", font=('Arial', 12, 'bold'), fg='black', bg='white')
prazo_label.pack()

data_frame = tk.Frame(canvas_frame, bg='white')
data_frame.pack()

dia_spinbox = tk.Spinbox(data_frame, from_=1, to=31, width=2)
dia_spinbox.grid(row=0, column=0, padx=5)

mes_spinbox = tk.Spinbox(data_frame, from_=1, to=12, width=2)
mes_spinbox.grid(row=0, column=1, padx=5)

ano_spinbox = tk.Spinbox(data_frame, from_=2023, to=9999, width=4)
ano_spinbox.grid(row=0, column=2, padx=5)

adicionar_button = tk.Button(canvas_frame, text="Adicionar Post-it", font=('Arial', 12), fg='black', bg='white', command=adicionar_postit)
adicionar_button.pack(pady=10)

root.mainloop()