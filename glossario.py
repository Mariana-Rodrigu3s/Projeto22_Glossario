import ttkbootstrap as ttk
from tkinter import messagebox
import sqlite3



janela = ttk.Window(themename="minty",
                                 title="Glossário de Termos Técnicos")
janela.geometry("720x700")
janela.resizable(False, False)

tw = ttk.Treeview(janela)
tw.pack(side="bottom", fill="both")

tw["columns"] = ("termo", "definição", "categoria")

tw["show"] = "headings"
tw.heading("termo", text="Termo")
tw.heading("definição", text="Definição")
tw.heading("categoria", text="Categoria")


termo = ttk.Label(janela,
          text="Digite o Termo:",
          font=('Arial', 13)).place(x=20, y=27)
entrada_termo = ttk.Entry(janela,
                        width=110).place(x=20, y=54)

definicao = ttk.Label(janela,
                      text="Digite a Definição:",
                      font=('Arial', 13)).place(x=20, y=150)
entrada_definicao = ttk.Entry(janela,
                              width=110).place(x=20, y=180)

categoria = ttk.Label(janela, 
                      text="Digite a Categoria:",
                      font=('Arial', 13)).place(x=20, y=270 )

entrada_categoria = ttk.Entry(janela,
                              width=110).place(x=20, y=298)

botoes = ttk.Frame(janela).pack(pady=120)



adicionar = ttk.Button(botoes,
                       style="outline button",
                       text="Adicionar").pack(side="left", padx=10)

excluir = ttk.Button(botoes,
                     style="outline button",
                     text="Excluir").pack(side="left", padx=10)

alterar = ttk.Button(botoes,
                     style="outline button",
                     text="Alterar").pack(side="left", padx=10)

conexao = sqlite3.connect("./bddados.sqlite")


        

janela.mainloop()

