# Importando os módulos necessários
from tkinter import *
from tkinter import ttk
import sqlite3

# Importando funcionalidades específicas do ReportLab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser 


# Criando uma janela tkinter
janela = Tk()

# Definindo uma classe chamada Relatorios
class Relatorios():
     # Método para abrir o arquivo PDF no navegador
    def print_cliente(self):
        webbrowser.open("cliente.pdf") 
     # Método para gerar um relatório de cliente
    def gerarRelatorioCliente(self):
    # Criando um objeto de canvas para desenhar no PDF
        self.c = canvas.Canvas("cliente.pdf")

        # Obtendo os dados dos campos de entrada
        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cidadeRel = self.cidade_entry.get()

        # Adicionando texto e dados ao PDF
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'ficha do cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Codigo: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 630, 'telefone: ')
        self.c.drawString(50, 600, 'Cidade: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 630, self.telefoneRel)
        self.c.drawString(150, 600, self.cidadeRel)

        self.c.rect(20, 550, 550, 5, fill=TRUE, stroke=False)

          # Salvando o PDF
        self.c.showPage()
        self.c.save()
         # Chamando o método para abrir o PDF no navegador
        self.print_cliente()

class funcs():

    # Este método limpa os campos de entrada na interface gráfica.
    def limpa_tela(self):
        self.codigo_entry.delete(0,END)
        self.nome_entry.delete(0,END)
        self.cidade_entry.delete(0,END)
        self.telefone_entry.delete(0,END)

     # Este método estabelece a conexão com o banco de dados SQLite.
    def conecta_db(self):
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor();print("banco de dados criado")

    # Este método fecha a conexão com o banco de dados.
    def desconecta_db(self):
        self.conn.close();print("desconectado")

     # Este método cria uma tabela 'clientes' no banco de dados, se ela não existir.
    def monta_tabela(self):
        self.conecta_db();print("conenctando ao banco de dados")
        ##criar tabela
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            cod INTEGER PRIMARY KEY,
            nome_cliente CHAR(40) NOT NULL,
            telefone INTEGER(20),
            cidade CHAR(40)
        );
        """)
        self.conn.commit()
        self.desconecta_db()

         # Este método adiciona um novo cliente ao banco de dados.
    def add_cliente(self):
        self.variaveis()
        self.conecta_db()
        self.cursor.execute("""INSERT INTO clientes (nome_cliente,telefone,cidade)
            VALUES(?, ?, ?) """, (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconecta_db()
        self.select_lista()
        self.limpa_tela()

         # Este método exibe a lista de clientes na interface gráfica.
    def select_lista(self):
        self.listaCLI.delete(*self.listaCLI.get_children())
        self.conecta_db()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            ORDER BY nome_cliente ASC """)
        for i in lista:
            self.listaCLI.insert("", END, values=i)
        self.desconecta_db()

        # Este método é chamado quando um item da lista é clicado duas vezes.
        # Ele preenche os campos de entrada com os detalhes do cliente selecionado.
    def onDoubleClick(self, event):
        self.limpa_tela()
        self.listaCLI.selection()

        for n in self.listaCLI.selection():
            col1, col2, col3, col4 = self.listaCLI.item(n, 'values')
            self.codigo_entry.insert(END,col1)
            self.nome_entry.insert(END,col2)
            self.telefone_entry.insert(END,col3)
            self.cidade_entry.insert(END,col4)

         # Este método deleta um cliente do banco de dados
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_db()
        self.cursor.execute(""" DELETE FROM clientes WHERE cod = ?  """, (self.codigo))
        self.conn.commit()
        self.desconecta_db()
        self.limpa_tela()
        self.select_lista()

        # Este método obtém os valores dos campos de entrada.
    def variaveis(self):   
        self.codigo= self.codigo_entry.get()
        self.nome = self.nome_entry.get() 
        self.telefone = self.telefone_entry.get() 
        self.cidade = self.cidade_entry.get()     

        # Este método altera os detalhes de um cliente no banco de dados.
    def  alterear_cliente(self):
        self.variaveis()
        self.conecta_db()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ? WHERE cod = ? """,(self.nome,self.telefone, self.cidade,self.codigo))
        self.conn.commit()
        self.desconecta_db()
        self.select_lista()
        self.limpa_tela()

        # Este método busca clientes com base no nome fornecido. 
    def busca_clientes(self):
        self.conecta_db()

        self.listaCLI.delete(*self.listaCLI.get_children())

        self.nome_entry.insert(END, '%')
        nome= self.nome_entry.get()
        self.cursor.execute("""SELECT cod, nome_cliente, telefone, cidade FROM clientes
                            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC """ % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCLI.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_db()


class Aplicação(funcs, Relatorios): #criando a class aplicaçao
    def __init__(self): #criando a funçao principal
         # Configurações da janela principal
        self.janela = janela
        self.tela()
        self.frames_da_tela()
        self.widgets_frame_1()
        self.lista_frame_2()
        self.monta_tabela()
        self.select_lista()
        self.menus()
        janela.mainloop() #deixa a janela em loop quando abrir 

    def tela(self):
        # Configuração da janela
        # ... (definição do título, cor, tamanho, etc.)

        self.janela.title("cadastro de clientes") #aplica o titulo da janela 
        self.janela.configure(background= '#8667f4') #dar a cor ao fundo da janela 
        self.janela.geometry("700x500") #define o tamanho da janela por padrao
        #self.janela.resizable(False,False) # nao deixando a tela aumentar de tamanho se for false ela perde a "responsividade"
        self.janela.maxsize(width= 900, height=700) #definindo tamanho maximo da tela
        self.janela.minsize(width= 400, height=300) #tamanho minimo

    def frames_da_tela(self):
        # Criação dos frames
        # ... (definição dos frames 1 e 2, posição, cor, etc.)

        self.frame_1 = Frame(self.janela, bd=4 , bg ='#8692f4',
                            highlightbackground= '#5952ed',highlightthickness=2 ) #definindo espaços na janela sao os frames o bd e bg sao do frame cor e borda 
        self.frame_1.place(relx=0.02 , rely=0.02, relwidth= 0.96, relheight=0.46) #colocando o frame em posiçao o relx/y faz com que o frame se ajuste conforme for mechendo
        
        self.frame_2 = Frame(self.janela, bd=4 , bg ='#8692f4',
                            highlightbackground= '#5952ed',highlightthickness=2 ) #definindo espaços na janela sao os frames o bd e bg sao do frame cor e borda 
        self.frame_2.place(relx=0.02 , rely=0.5, relwidth= 0.96, relheight=0.46)


    def widgets_frame_1(self):
        # Criação dos widgets no frame 1
        # ... (criação de botões, labels e entradas)

        ##criaçao do botao limpar 
        self.bt_limpar = Button(self.frame_1, text="Limpar",bd=2,bg='#cff4f8',fg='black',font=('verdana', 8 ,'bold'),command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2,rely=0.1,relwidth=0.1, relheight=0.15)
        #botao buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar",bd=2,bg='#cff4f8',fg='black',font=('verdana', 8 ,'bold'),command=self.busca_clientes)
        self.bt_buscar.place(relx=0.35,rely=0.1,relwidth=0.1, relheight=0.15)
        #botao novo
        self.bt_novo = Button(self.frame_1, text="Novo",bd=2,bg='#cff4f8',fg='black',font=('verdana', 8 ,'bold'),command=self.add_cliente)
        self.bt_novo.place(relx=0.50,rely=0.1,relwidth=0.1, relheight=0.15)
        #botao alterar
        self.bt_alterar = Button(self.frame_1, text="Alterar",bd=2,bg='#cff4f8',fg='black',font=('verdana', 8 ,'bold'),command=self.alterear_cliente)
        self.bt_alterar.place(relx=0.2,rely=0.25,relwidth=0.1, relheight=0.15)
        #botao apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar",bd=2,bg='#cff4f8',fg='black',font=('verdana', 8 ,'bold'),command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.35,rely=0.25,relwidth=0.1, relheight=0.15)

     #criançao das labels entrada do codigo
        self.lb_codigo = Label(self.frame_1, text="Código",bd = 2,bg='#8692f4',fg='black',font=('verdana', 8 ,'bold'))
        self.lb_codigo.place (relx=0.05,rely=0.05)
         #criando a entrada dessa label
        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05,rely=0.15, relwidth=0.07)

     #criançao das labels entrada do nome
        self.lb_nome = Label(self.frame_1, text="Nome",bd = 2,bg='#8692f4',fg='black',font=('verdana', 8 ,'bold'))
        self.lb_nome.place (relx=0.05,rely=0.35)
         #criando a entrada dessa label
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05,rely=0.45, relwidth=0.8)
        
     #criançao das labels entrada do telefone
        self.lb_telefone = Label(self.frame_1, text="Telefone",bd = 2,bg='#8692f4',fg='black',font=('verdana', 8 ,'bold'))
        self.lb_telefone.place (relx=0.05,rely=0.55)
         #criando a entrada dessa label
        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05,rely=0.65, relwidth=0.8)

     #criançao das labels entrada da cidade
        self.lb_cidade = Label(self.frame_1, text="Cidade",bd = 2,bg='#8692f4',fg='black',font=('verdana', 8 ,'bold'))
        self.lb_cidade.place (relx=0.05,rely=0.75)
         #criando a entrada dessa label
        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.05,rely=0.85, relwidth=0.8)


    def lista_frame_2(self): 
        # Criação da lista no frame 2 parte dos dados
        # ... (configuração da Treeview, Scrollbar, etc.)

        self.listaCLI = ttk.Treeview(self.frame_2, height=3, column=("col1","col2","col3","col4"))
        self.listaCLI.heading('#0',text = "")
        self.listaCLI.heading('#1',text = "codigo")
        self.listaCLI.heading('#2',text = "nome")
        self.listaCLI.heading('#3',text = "telefone")
        self.listaCLI.heading('#4',text = "cidade")

        self.listaCLI.column("#0", width=1)
        self.listaCLI.column("#1", width=50)
        self.listaCLI.column("#2", width=200)
        self.listaCLI.column("#3", width=125)
        self.listaCLI.column("#4", width=125)

        self.listaCLI.place(relx=0.01,rely=0.1,relwidth=0.95,relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCLI.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)

        self.listaCLI.bind("<Double-1>",self.onDoubleClick)
        

    def menus(self):
        # Configuração dos menus
        # ... (criação dos menus, opções e comandos associados)
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.janela.destroy()

        menubar.add_cascade(label= "opcoes", menu= filemenu)
        menubar.add_cascade(label= "relatorio", menu= filemenu2)

        filemenu.add_command(label="sair",command = Quit)
        filemenu.add_command(label= "limpa cliente", command=self.limpa_tela)
        
        filemenu2.add_command(label= "ficha do cliente", command=self.gerarRelatorioCliente)
        


    
Aplicação() #rodando a aplicaçao