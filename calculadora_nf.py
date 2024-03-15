import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class App(tk.Tk):
    # XML file of the NF (Nota fiscal)
    tags_itens = {}

    def __init__ (self):
        super().__init__()
        # Adiciona um título à janela
        self.title("Calculadora NF")

        # Define as dimensões da janela
        self.geometry("400x400")

        self.xml_file_path = tk.StringVar()

        self.inicia_tags_itens()

        self.create_widgets()

        self.insert_result()

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

        self.insert_result()


    def calcTag(self, Xpath, tag):
        tree = ET.parse(self.xml_file_path.get())
        root = tree.getroot()
        namespace = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
        Xpath += tag
        self.tags_itens[tag] = sum(float(prod.text) for prod in root.findall(Xpath, namespace))


    # Função para lidar com o botão 'Selecionar Arquivo'
    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename()
        self.xml_file_path.set(arquivo)


    def create_widgets(self):
        frm2 = ttk.Frame(self, padding=10)
        frm2.grid(row=0)

        ttk.Button(frm2, text="Selecionar Arquivo", command=self.selecionar_arquivo).grid(column=0, row=0)
        ttk.Button(frm2, text="Calcular", command=self.calc_itens).grid(column=1, row=0)
        ttk.Button(frm2, text="Quit", command=self.destroy).grid(column=2, row=0)

        frm = ttk.Frame(self, padding=10)
        frm.grid(row=2)

        #vProd
        ttk.Label(frm,text='vProd:').grid(column=0, row=0)
        self.text_vProd = tk.Text(frm, height = 1, width = 30)
        self.text_vProd.grid(column=1, row=0)

        #vDesc
        ttk.Label(frm,text='vDesc:').grid(column=0, row=1)
        self.text_vDesc = tk.Text(frm, height = 1, width = 30)
        self.text_vDesc.grid(column=1, row=1)

        #vICMSDeson
        ttk.Label(frm,text='vICMSDeson:').grid(column=0, row=2)
        self.text_vICMSDeson = tk.Text(frm, height = 1, width = 30)
        self.text_vICMSDeson.grid(column=1, row=2)

        #vST
        ttk.Label(frm,text='vST:').grid(column=0, row=3)
        self.text_vST = tk.Text(frm, height = 1, width = 30)
        self.text_vST.grid(column=1, row=3)

        #vFrete
        ttk.Label(frm,text='vFrete:').grid(column=0, row=4)
        self.text_vFrete = tk.Text(frm, height = 1, width = 30)
        self.text_vFrete.grid(column=1, row=4)

        #vSeg
        ttk.Label(frm,text='vSeg:').grid(column=0, row=5)
        self.text_vSeg = tk.Text(frm, height = 1, width = 30)
        self.text_vSeg.grid(column=1, row=5)

        #vOutro
        ttk.Label(frm,text='vOutro:').grid(column=0, row=6)
        self.text_vOutro = tk.Text(frm, height = 1, width = 30)
        self.text_vOutro.grid(column=1, row=6)

        #vII
        ttk.Label(frm,text='vII:').grid(column=0, row=7)
        self.text_vII = tk.Text(frm, height = 1, width = 30)
        self.text_vII.grid(column=1, row=7)

        #vIPI
        ttk.Label(frm,text='vIPI:').grid(column=0, row=8)
        self.text_vIPI = tk.Text(frm, height = 1, width = 30)
        self.text_vIPI.grid(column=1, row=8)

        #vIPIdevol
        ttk.Label(frm,text='vIPIdevol:').grid(column=0, row=9)
        self.text_vIPIdevol = tk.Text(frm, height = 1, width = 30)
        self.text_vIPIdevol.grid(column=1, row=9)
        

        #vServ
        ttk.Label(frm,text='vServ:').grid(column=0, row=10)
        self.text_vServ = tk.Text(frm, height = 1, width = 30)
        self.text_vServ.grid(column=1, row=10)

        #vBC
        ttk.Label(frm,text='vBC:').grid(column=0, row=11)
        self.text_vBC = tk.Text(frm, height = 1, width = 30)
        self.text_vBC.grid(column=1, row=11)
        
        #Total
        ttk.Label(frm,text='Total:').grid(column=0, row=12)
        self.text_Total = tk.Text(frm, height = 1, width = 30)
        self.text_Total.grid(column=1, row=12)


    def insert_result(self):
        # Limpa os valores 
        self.text_vProd.delete("1.0", tk.END)
        self.text_vDesc.delete("1.0",tk.END)
        self.text_vICMSDeson.delete("1.0",tk.END)
        self.text_vST.delete("1.0",tk.END)
        self.text_vFrete.delete("1.0",tk.END)
        self.text_vSeg.delete("1.0",tk.END)
        self.text_vOutro.delete("1.0",tk.END)
        self.text_vII.delete("1.0",tk.END)
        self.text_vIPI.delete("1.0",tk.END)
        self.text_vIPIdevol.delete("1.0",tk.END)
        self.text_vServ.delete("1.0",tk.END)
        self.text_vBC.delete("1.0",tk.END)
        self.text_Total.delete("1.0",tk.END)

        # Insere os novos valores
        self.text_vProd.insert(tk.END, self.tags_itens['vProd'])
        self.text_vDesc.insert(tk.END, self.tags_itens['vDesc'])
        self.text_vICMSDeson.insert(tk.END, self.tags_itens['vICMSDeson'])
        self.text_vST.insert(tk.END, self.tags_itens['vST'])
        self.text_vFrete.insert(tk.END, self.tags_itens['vFrete'])
        self.text_vSeg.insert(tk.END, self.tags_itens['vSeg'])
        self.text_vOutro.insert(tk.END, self.tags_itens['vOutro'])
        self.text_vII.insert(tk.END, self.tags_itens['vII'])
        self.text_vIPI.insert(tk.END, self.tags_itens['vIPI'])
        self.text_vIPIdevol.insert(tk.END, self.tags_itens['vIPIdevol'])
        self.text_vServ.insert(tk.END, self.tags_itens['vServ'])
        self.text_vBC.insert(tk.END, self.tags_itens['vBC'])
        self.text_Total.insert(tk.END, self.tags_itens['total'])


if __name__ == "__main__":
    app = App()
    app.mainloop()