import pyodbc
import tkinter as tk
from tkinter import ttk

def conecta_ao_banco():
    conexao = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-UDRTM8C\\SQLEXPRESS;"
    "DATABASE=Hospital;"
    "Trusted_Connection=yes;")
    return conexao

def cadastrar_medico(nome, crm, especialidade):
    cursor = conexao.cursor()
    cursor.execute("""
                   INSERT INTO Tb_Medicos (NOME, CRM, ESPECIALIDADE_ID)
                   VALUES (?, ?, ?)
                   """, (nome, crm, especialidade))
    conexao.commit()



def cadastrar_consulta(id_paciente, id_medico, data_consulta, diagnostico=None):
    cursor = conexao.cursor()
    cursor.execute("""
                   INSERT INTO Tb_Consultas (ID_PACIENTE, ID_MEDICO, DATA_CONSULTA, DIAGNOSTICO)
                   VALUES ( ?, ?, ?, ?)
                   """, (id_paciente, id_medico, data_consulta, diagnostico))
    conexao.commit()


def cadastrar_paciente(nome, data_nascimento, telefone):
    cursor = conexao.cursor()
    cursor.execute("""
                   INSERT INTO Tb_Pacientes (NOME, DATA_NASCIMENTO, TELEFONE)
                   VALUES (?, ?, ?)
                   """, (nome, data_nascimento, telefone))
    conexao.commit()

conexao = conecta_ao_banco()
print("Conectado Com Sucesso!")

# criação da janela do aplicativo

janela = tk.Tk()
janela.title("Sistema Hospital")
janela.geometry("300x200")

# cria o notebook (container de abas)
abas = ttk.Notebook(janela)
abas.pack(fill="both", expand=True)

# Cria as abas
aba_paciente = ttk.Frame(abas)
aba_medico   = ttk.Frame(abas)
aba_consulta = ttk.Frame(abas)

# adiciona as abas ao notebook com seus nomes
abas.add(aba_paciente, text="Paciente")
abas.add(aba_medico, text="Medico")
abas.add(aba_consulta, text="Consulta")


# aba de paciente

tk.Label(aba_paciente, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
campo_nome_pac = tk.Entry(aba_paciente, width=30)
campo_nome_pac.grid(row=0, column=1, padx=10, pady=5)

tk.Label(aba_paciente, text="data Nasc:").grid(row=1, column=0, padx=10, pady=5)
campo_data = tk.Entry(aba_paciente, width=30)
campo_data.grid(row=1, column=1, padx=10, pady=5)

tk.Label(aba_paciente, text="Telefone:").grid(row=2, column=0, padx=10, pady=5)
campo_telefone = tk.Entry(aba_paciente, width=30)
campo_telefone.grid(row=2, column=1, padx=10, pady=5)

def salvar_paciente():
    try:
        nome= campo_nome_pac.get()
        data= campo_data.get()
        tel= campo_telefone.get()
        cadastrar_paciente(nome, data, tel)
        print("Cadastrado")
        messagebox.showinfo("Sucesso", "Paciente cadastrado!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

tk.Button(aba_paciente, text="Cadastrar", command=salvar_paciente).grid(row=3, column=1, pady=10)

# aba medico

tk.Label(aba_medico, text="Nome:").grid(row=0, column=0, padx=10, pady=5)
campo_med_nome = tk.Entry(aba_medico, width=30)
campo_med_nome.grid(row=0, column=1, padx=10, pady=5)

tk.Label(aba_medico, text="CRM/CRP:").grid(row=1, column=0, padx=10, pady=5)
campo_crm = tk.Entry(aba_medico, width=30)
campo_crm.grid(row=1, column=1, padx=10, pady=5)

tk.Label(aba_medico, text="Area:").grid(row=2, column=0, padx=10, pady=5)
campo_id_especialidade = tk.Entry(aba_medico, width=30)
campo_id_especialidade.grid(row=2, column=1, padx=10, pady=5)

def buscar_id_especialidade(nome):
    cursor = conexao.cursor()
    cursor.execute("SELECT ID FROM Tb_Especialidades WHERE NOME = ?", (nome,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None
    
def salvar_medico():
    try:
        nome= campo_med_nome.get()
        crm= campo_crm.get()
        id_especialidade = buscar_id_especialidade(campo_id_especialidade.get())

        cadastrar_medico(nome, crm, id_especialidade)
        print("Cadastrado")
        messagebox.showinfo("Sucesso", "Medico cadastrado!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

tk.Button(aba_medico, text="Cadastrar", command=salvar_medico).grid(row=3, column=1, pady=10)


# Aba consultas

tk.Label(aba_consulta, text="Nome Paciente:").grid(row=0, column=0, padx=10, pady=5)
campo_id_pac = tk.Entry(aba_consulta, width=30)
campo_id_pac.grid(row=0, column=1, padx=10, pady=5)

tk.Label(aba_consulta, text="Nome Médico:").grid(row=1, column=0, padx=10, pady=5)
campo_id_med = tk.Entry(aba_consulta, width=30)
campo_id_med.grid(row=1, column=1, padx=10, pady=5)

tk.Label(aba_consulta, text="Data Consulta:").grid(row=2, column=0, padx=10, pady=5)
campo_data_con = tk.Entry(aba_consulta, width=30)
campo_data_con.grid(row=2, column=1, padx=10, pady=5)

tk.Label(aba_consulta, text="Diagnóstico:").grid(row=3, column=0, padx=10, pady=5)
campo_diag = tk.Entry(aba_consulta, width=30)
campo_diag.grid(row=3, column=1, padx=10, pady=5)

# definição para procurar ID do paciente para cadastro do SQL pelo nome

def buscar_id_paciente(nome):
    cursor = conexao.cursor()
    cursor.execute("SELECT ID FROM Tb_Pacientes WHERE NOME = ?", (nome,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None
    
# definição para buscar id do medico pelo nome dele pelo SQL

def buscar_id_medico(nome):
    cursor = conexao.cursor()
    cursor.execute("SELECT ID FROM Tb_Medicos WHERE NOME = ?", (nome,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
    else:
        return None

# definição para salvar a consulta no sql Linkado
def salvar_consulta():
    try:
        id_pac = buscar_id_paciente(campo_id_pac.get())
        id_med = buscar_id_medico(campo_id_med.get())
        if id_pac is None:
            messagebox.showerror("Erro", "Paciente não encontrado!")
            return
        if id_med is None:
            messagebox.showerror("Erro", "Médico não encontrado!")
            return

        cadastrar_consulta(id_pac, id_med, campo_data_con.get(), campo_diag.get())
        messagebox.showinfo("Sucesso", "Consulta cadastrada!")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

tk.Button(aba_consulta, text="Cadastrar", command=salvar_consulta).grid(row=4, column=1, pady=10)




janela.mainloop()