import ttkbootstrap as ttk
def apagar():
    selecionado = treeview.selection()
    treeview.delete(selecionado)

janela = ttk.Window(themename="minty")

treeview = ttk.Treeview(janela)
treeview.pack(side="bottom")

#não é o nome que aparece na coluna
treeview["columns"] = ("nome", "idade", "cidade")

treeview["show"] = "headings"
treeview.heading("nome", text="Nome completo")
treeview.heading("idade", text="Idade")
treeview.heading("cidade", text="Cidade")

treeview.column("idade", width=50)
treeview.column("nome", width=110)
treeview.column("cidade", width=90)

treeview.insert("", "end", values=["Ana", 23, "Uberlândia"])
treeview.insert("", "end", values=["Felipa", 25, "Uberlândia"])

ttk.Button(janela, text="deletar", command=apagar).pack()





janela.mainloop()

