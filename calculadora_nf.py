import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class App(tk.Tk):
    # XML file of the NF (Nota fiscal)
    tags_itens = {}
    text_values = {}

    def __init__ (self):
        super().__init__()
        # Adiciona um título à janela
        self.title("Calculadora NF")

        # Define as dimensões da janela
        self.minsize(715,350)

        self.xml_file_path = tk.StringVar()

        self.inicia_tags_itens()

        self.create_widgets()

        self.show_results()

    def inicia_tags_itens(self):
        self.tags_itens['vProd'] = 0
        self.tags_itens['vDesc'] = 0     
        self.tags_itens['vICMSDeson'] = 0
        self.tags_itens['vST'] = 0       
        self.tags_itens['vFrete'] = 0    
        self.tags_itens['vSeg'] = 0      
        self.tags_itens['vOutro'] = 0
        self.tags_itens['vII'] = 0       
        self.tags_itens['vIPI'] = 0      
        self.tags_itens['vIPIdevol'] = 0
        self.tags_itens['vServ'] = 0     
        self.tags_itens['vBC'] = 0
        self.tags_itens['total'] = 0


    def calc_itens(self):
        if self.xml_file_path.get() == '':
            return

        self.inicia_tags_itens()

        self.calcTag('.//ns:det/ns:prod/ns:', 'vProd')
        self.calcTag('.//ns:det/ns:prod/ns:', 'vDesc')      # Tag não testada, verificar path
        self.calcTag('.//ns:det/ns:prod/ns:', 'vICMSDeson') # Tag não testada, verificar path
        self.calcTag('.//ns:det/ns:prod/ns:', 'vST')        # Tag não testada, verificar path
        self.calcTag('.//ns:det/ns:prod/ns:', 'vFrete')     # Tag não testada, verificar path
        self.calcTag('.//ns:det/ns:prod/ns:', 'vSeg')       # Tag não testada, verificar path
        self.calcTag('.//ns:det/ns:prod/ns:', 'vOutro')
        self.calcTag('.//ns:det/ns:prod/ns:', 'vII')        # Tag não testada, verificar path
        self.calcTag('.//ns:det/ns:prod/ns:', 'vIPI')       # Tag não testada, verificar path
        self.calcTag('.//ns:impostoDevol/ns:IPI/ns:', 'vIPIdevol')
        self.calcTag('.//ns:det/ns:prod/ns:', 'vServ')      # Tag não testada, verificar path
        self.calcTag('.//ns:imposto/ns:ICMS//ns:', 'vBC')

        self.calcTotItens()


    def calcTotItens(self):
        self.tags_itens['total'] = 0
        for x in self.tags_itens.keys():
            if x in ['total','vBC']:                  # Não conta para o total
                continue
            elif x in ['vDesc','vICMSDeson']:         # Desconta do total
                self.tags_itens['total'] -= self.tags_itens[x]
            else:                                     # Soma no total
                self.tags_itens['total'] += self.tags_itens[x]

        self.show_results()


    def calcTag(self, Xpath, tag):
        tree = ET.parse(self.xml_file_path.get())
        root = tree.getroot()
        namespace = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
        Xpath += tag
        self.tags_itens[tag] = sum(float(prod.text) for prod in root.findall(Xpath, namespace))


    # Função para lidar com o botão 'Selecionar Arquivo'
    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos XML", "*.xml")])
        self.xml_file_path.set(arquivo)

        self.show_arq_name()


    def create_select_file_button(self):
        # Arquivo
        frm_arq = ttk.Frame(self, padding=10)
        frm_arq.grid(row=0)

        ttk.Label(frm_arq,text='Selecionar Arquivo:').grid(column=0, row=0)
        self.text_arq = tk.Text(frm_arq, height = 1, width = 70)
        self.text_arq.grid(column=1, row=0)
        self.photo = tk.PhotoImage(file=r"select_file.png").subsample(40,40)
        ttk.Button(frm_arq, image=self.photo, command=self.selecionar_arquivo).grid(column=2, row=0)


    def create_toolbar(self):
        # Toolbar
        frm_toolbar = ttk.Frame(self, padding=10)
        frm_toolbar.grid(row=1)

        ttk.Button(frm_toolbar, text="Calcular", command=self.calc_itens).grid(column=0, row=0)
        ttk.Button(frm_toolbar, text="Quit", command=self.destroy).grid(column=1, row=0)


    def create_widgets(self):
        self.create_select_file_button()

        self.create_toolbar()

        frm = ttk.Frame(self, padding=10)
        frm.grid(row=2)

        rw = 0
        for x in self.tags_itens.keys():
            ttk.Label(frm,text=x+':').grid(column=0, row=rw)
            self.text_values[x] = tk.Text(frm, height = 1, width = 30)
            self.text_values[x].grid(column=1, row=rw)
            rw += 1


    def show_results(self):
        for x in self.tags_itens.keys():
            # Limpa os valores 
            self.text_values[x].delete("1.0", tk.END)

            # Insere os novos valores
            self.text_values[x].insert(tk.END, self.tags_itens[x])


    def show_arq_name(self):
        self.text_arq.delete("1.0",tk.END)

        self.text_arq.insert(tk.END, self.xml_file_path.get())


if __name__ == "__main__":
    app = App()
    app.mainloop()