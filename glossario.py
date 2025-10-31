import ttkbootstrap as ttk
from tkinter import messagebox
from tkinter import Listbox
import sqlite3

class Glossario:
    def __init__(self):
        


    
        # Janela Principal
        self.janela = ttk.Window(themename="minty",
                                        title="Glossário de Termos Técnicos")
        self.janela.geometry("720x700")
        self.janela.resizable(False, False)


        # Banco de Dados e Criação da Tabela
        conexao = sqlite3.connect("./bddados.sqlite")

        cursor = conexao.cursor()

        glossario = """
                        CREATE TABLE IF NOT EXISTS glossario(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        termo VARCHAR(200),
                        definicao VARCHAR(5000),
                        categoria VARCHAR(100));
        """

        cursor.execute(glossario)
        conexao.commit()

        cursor.close()
        conexao.close()


        # Labels
        self.titulo = ttk.Label(self.janela,
                        text="Glossário",
                        font=('Ink Free', 25)).pack()
        self.titulo2 = ttk.Label(self.janela,
                            text="Termos Técnicos",
                            font=('Ink Free', 25)).pack()

        self.etiqueta = ttk.Label(self.janela,
                            text="Crie seu próprio glossário de termos técnicos.").pack()

        self.termo = ttk.Label(self.janela,
                text="Digite o Termo:",
                font=('Arial', 13)).place(x=20, y=100)
        self.categoria = ttk.Label(self.janela, 
                            text="Digite a Categoria:",
                            font=('Arial', 13)).place(x=20, y=319 )

        self.definicao = ttk.Label(self.janela,
                            text="Digite a Definição:",
                            font=('Arial', 13)).place(x=20, y=210)
        

        # Campos de Entrada
        self.entrada_termo = ttk.Entry(self.janela,
                                width=110)
        self.entrada_termo.place(x=20, y=130)

        self.entrada_definicao = ttk.Entry(self.janela,
                                    width=110)
        self.entrada_definicao.place(x=20, y=240)
        
        self.entrada_categoria = ttk.Entry(self.janela,
                                    width=110)
        self.entrada_categoria.place(x=20, y=350)
        

        # TreeView (Tabela Visual)
        self.tw = ttk.Treeview(self.janela)
        self.tw.pack(side="bottom", fill="both")

        self.tw["columns"] = ("id","termo", "definicao", "categoria")

        self.tw["show"] = "headings"
        self.tw.heading("id", text="ID")
        self.tw.heading("termo", text="Termo")
        self.tw.heading("definicao", text="Definição")
        self.tw.heading("categoria", text="Categoria")
        
        self.tw.column("id", width=50)
        self.tw.column("termo", width=50)
        self.tw.column("definicao", width=90)
        self.tw.column("categoria", anchor="center")


        # Botões
        botoes = ttk.Frame(self.janela).pack(pady=130)
        
        self.adicionar = ttk.Button(botoes,
                            style="outline button",
                            text="Adicionar",
                            width=30,
                            command=self.adicionar_item).pack(padx=20, pady=10, side="left")

        self.excluir = ttk.Button(botoes,
                            style="outline button",
                            text="Excluir",
                            width=30,
                            command=self.excluir_itens).pack(padx=20, pady=10, side="left")

        self.alterar = ttk.Button(botoes,
                            style="outline button",
                            text="Alterar",
                            width=30).pack(padx=20, pady=10, side="left")

        self.carregar_treeview()

        
    # Adicionar Itens
    def adicionar_item(self):
        termos = self.entrada_termo.get()
        definicoes = self.entrada_definicao.get()
        categorias = self.entrada_categoria.get()

        conexao = sqlite3.connect("./bddados.sqlite")
        cursor = conexao.cursor()

       

        cursor.execute("""
                INSERT INTO glossario
                
                (termo,
                definicao,
                categoria)
                VALUES
                (?,
                ?,
                ?)
                    """,
                    [termos,
                     definicoes,
                     categorias] )

        conexao.commit()


        conexao.close()

        self.carregar_treeview()

       

    def carregar_treeview(self):
        # Limpa os dados anteriores
        for linha in self.tw.get_children():
            self.tw.delete(linha)

        conexao = sqlite3.connect("./bddados.sqlite")
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM glossario")
        dados = cursor.fetchall()

        for linha in dados:
            self.tw.insert("", "end", values=linha)

        conexao.close()


    def excluir_itens(self):
        selecionado = self.tw.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para excluir")
            return

        if selecionado:

            valores = self.tw.item(selecionado[0], "values")
            conexao = sqlite3.connect("./bddados.sqlite")
            cursor = conexao.cursor()

            cursor.execute("DELETE FROM glossario WHERE id = ?", (valores[0],))
            conexao.commit()
            cursor.close()
            conexao.close()

    def atualizar(self):
        selecionado = self.tw.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para alterar")
            return
        
        
  
       

    
    




        
                

    def run(self):
        self.janela.mainloop()


if __name__ == "__main__":
    gloss = Glossario()
    gloss.janela.mainloop()

