import ttkbootstrap as ttk
from tkinter import messagebox
from tkinter import Listbox
import sqlite3

class Glossario:
    def __init__(self):
        


    
        #------------------ Janela Principal --------------------------------------
        self.janela = ttk.Window(themename="minty",
                                        title="Glossário de Termos Técnicos")
        self.janela.geometry("720x700")
        self.janela.resizable(False, False)


        #---------------- Banco de Dados e Criação da Tabela ---------------------
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


        #------------------------ Labels -----------------------------------------
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
        
        self.pesquisa = ttk.Label(self.janela,
                                  text="Digite o Termo...",
                                  font=('Arial', 10)).place(x=580)
        

        #------------------------ Campos de Entrada ----------------------------------
        self.entrada_termo = ttk.Entry(self.janela,
                                width=110)
        self.entrada_termo.place(x=20, y=130)

        self.entrada_definicao = ttk.Entry(self.janela,
                                    width=110)
        self.entrada_definicao.place(x=20, y=240)
        
        self.entrada_categoria = ttk.Entry(self.janela,
                                    width=110)
        self.entrada_categoria.place(x=20, y=350)

        self.entrada_pesquisa = ttk.Entry(self.janela,
                                          width=15)
        self.entrada_pesquisa.place(x=580, y=30)

        # vincula o evento de digitação na função de filtrar
        self.entrada_pesquisa.bind("<KeyRelease>", self.filtrar_tw)
        

        #--------------------------- TreeView (Tabela Visual) ----------------------
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


        #----------------------------------------- Botões ----------------------------------
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
                            command=self.atualizar,
                            width=30).pack(padx=20, pady=10, side="left")

        self.carregar_treeview()

        
    #------------------------------------------- Adicionar Itens ---------------------------------
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

       
    #------------------------------ Carregar a TreeView (Fazer ela aparecer) -------------------
    def carregar_treeview(self):
        # limpa os dados anteriores
        for linha in self.tw.get_children():
            self.tw.delete(linha)

        conexao = sqlite3.connect("./bddados.sqlite")
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM glossario")
        dados = cursor.fetchall()

        # insere os dados na treeview
        for linha in dados:
            self.tw.insert("", "end", values=linha)

        conexao.close()

    #------------------------- Excluir Itens -----------------------------
    def excluir_itens(self):
        selecionado = self.tw.selection()
        
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para excluir")
            return

        if selecionado:
            
            # pega o ID dos itens selecionados
            valores = self.tw.item(selecionado[0], "values")
            conexao = sqlite3.connect("./bddados.sqlite")
            cursor = conexao.cursor()

            cursor.execute("DELETE FROM glossario WHERE id = ?", (valores[0],))
            conexao.commit()
            cursor.close()
            conexao.close()

        self.tw.delete(selecionado)

    #---------------------------- Atualizar Itens -------------------------------------
    def atualizar(self):
        selecionado = self.tw.selection()
        

        if not selecionado:
            messagebox.showerror("Aviso", "Selecione um item para alterar")
            return
        
        
        item = self.tw.item(selecionado[0])
        valores = item["values"]
        id = valores[0]

        # pega os novos itens dos campos de entrada
        termos = self.entrada_termo.get()
        definicoes = self.entrada_definicao.get()
        categoria = self.entrada_categoria.get()

        

        conexao = sqlite3.connect("./bddados.sqlite")
        cursor = conexao.cursor()


        cursor.execute("""
                           UPDATE glossario
                           SET termo = ?, definicao = ?, categoria = ?
                           WHERE id = ? """, [termos, definicoes, categoria, id])
            
        conexao.commit()
        conexao.close()

        self.carregar_treeview()

        messagebox.showinfo("Parabéns", "Alterado com sucesso!")

    #-------------------------- Desafio Final ---------------------
    def filtrar_tw(self, event):
        #strip para remover os espaços em branco e o lower para deixar tudo em minusculo
        busca = self.entrada_pesquisa.get().strip().lower()

        for linha in self.tw.get_children():
            self.tw.delete(linha)

        
        conexao = sqlite3.connect("./bddados.sqlite")
        cursor = conexao.cursor()

        if busca == "":
            cursor.execute("SELECT * FROM glossario")
        
        #lower do sql para transformar os termos da coluna em minusculo
        else:
            cursor.execute("""
                 SELECT * FROM glossario
                WHERE LOWER(termo) LIKE ?
""", (busca + "%",))
            # A "," serve para criar uma tupla
            
        dados = cursor.fetchall()

        for linha in dados:
            self.tw.insert("", "end", values=linha)
        
        conexao.close()




        



            

        
        
  
       

    
    




        
                

    def run(self):
        self.janela.mainloop()


if __name__ == "__main__":
    gloss = Glossario()
    gloss.janela.mainloop()

