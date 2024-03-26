import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

class App(tk.Tk):
    version = '1.0'
    tags_items = {}
    text_values = {}

    def __init__ (self):
        super().__init__()
        # Adds a title to the window
        self.title("Calculadora NF" + ' - ' + self.version)

        # Define the size of the window
        self.minsize(700,370)

        self.xml_file_path = tk.StringVar()

        self.start_tags_items()

        self.create_select_file_button()

        self.create_toolbar()

        self.create_widgets()

        self.show_results()


    def start_tags_items(self):
        self.tags_items['vProd']      = 0
        self.tags_items['vDesc']      = 0     
        self.tags_items['vICMSDeson'] = 0
        self.tags_items['vST']        = 0       
        self.tags_items['vFrete']     = 0    
        self.tags_items['vSeg']       = 0      
        self.tags_items['vOutro']     = 0
        self.tags_items['vII']        = 0       
        self.tags_items['vIPI']       = 0      
        self.tags_items['vIPIdevol']  = 0
        self.tags_items['vServ']      = 0     
        self.tags_items['vBC']        = 0
        self.tags_items['total']      = 0


    def show_alert(self, msg):
        tk.messagebox.showinfo("Alert!", msg)


    def file_is_valid(self):
        if os.path.exists(self.xml_file_path.get()):
            if not os.path.isfile(self.xml_file_path.get()):
                self.show_alert("The specified path does't match to a file.")
            else:
                return True
        else:
            self.show_alert("The specified file does't exists.")
        return False

    def calc_itens(self):
        if self.xml_file_path.get() == '':
            self.show_alert("Select a xml to calculate!")
            return
        
        if not self.file_is_valid():
            return

        self.start_tags_items()

        self.calc_tag('.//ns:det/ns:prod/ns:',         'vProd')
        self.calc_tag('.//ns:det/ns:prod/ns:',         'vDesc')      # Tag não testada, verificar path
        self.calc_tag('.//ns:det/ns:prod/ns:',         'vICMSDeson') # Tag não testada, verificar path
        self.calc_tag('.//ns:det/ns:prod/ns:',         'vST')        # Tag não testada, verificar path
        self.calc_tag('.//ns:det/ns:prod/ns:',         'vFrete')     # Tag não testada, verificar path
        self.calc_tag('.//ns:det/ns:prod/ns:',         'vSeg')       # Tag não testada, verificar path
        self.calc_tag('.//ns:det/ns:prod/ns:',         'vOutro')
        self.calc_tag('.//ns:det/ns:prod/ns:',         'vII')        # Tag não testada, verificar path
        self.calc_tag('.//ns:det/ns:prod/ns:',         'vIPI')       # Tag não testada, verificar path
        self.calc_tag('.//ns:impostoDevol/ns:IPI/ns:', 'vIPIdevol')
        self.calc_tag('.//ns:det/ns:prod/ns:',         'vServ')      # Tag não testada, verificar path
        self.calc_tag('.//ns:imposto/ns:ICMS//ns:',    'vBC')

        self.calc_total()


    def calc_total(self):
        self.tags_items['total'] = 0
        for x in self.tags_items.keys():
            if x in ['total','vBC']:                  # Não conta para o total
                continue

            elif x in ['vDesc','vICMSDeson']:         # Desconta do total
                self.tags_items['total'] -= self.tags_items[x]

            else:                                     # Soma no total
                self.tags_items['total'] += self.tags_items[x]

        self.show_results()


    def calc_tag(self, Xpath, tag):
        tree = ET.parse(self.xml_file_path.get())
        root = tree.getroot()
        namespace = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
        Xpath += tag
        self.tags_items[tag] = sum(float(prod.text) for prod in root.findall(Xpath, namespace))


    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("XML File", "*.xml")])
        self.xml_file_path.set(file)
        self.show_arq_name()


    def create_select_file_button(self):
        # File
        frm_file = ttk.Frame(self, padding=10)
        frm_file.grid(row=0)

        ttk.Label(frm_file,text='Select File:').grid(column=0, row=0)
        self.text_arq = tk.Text(frm_file, height = 1, width = 70)
        self.text_arq.grid(column=1, row=0)
        self.photo = tk.PhotoImage(file=r"select_file.png").subsample(40,40)
        ttk.Button(frm_file, image=self.photo, command=self.select_file).grid(column=2, row=0)


    def create_toolbar(self):
        # Toolbar
        frm_toolbar = ttk.Frame(self, padding=10)
        frm_toolbar.grid(row=1)

        ttk.Button(frm_toolbar, text="Calculate", command=self.calc_itens).grid(column=0, row=0)
        ttk.Button(frm_toolbar, text="Quit", command=self.destroy).grid(column=1, row=0)


    def create_widgets(self):
        # Widgets
        frm = ttk.Frame(self, padding=10)
        frm.grid(row=2)

        rw = 0
        cl = 0
        for x in self.tags_items.keys():
            ttk.Label(frm,text=x+':', padding=2).grid(column=cl, row=rw)
            cl +=1
            self.text_values[x] = tk.Text(frm, height = 1, width = 30, state=tk.DISABLED)
            self.text_values[x].grid(column=cl, row=rw)
            cl +=1
            if cl == 2:
                continue
            else:
                cl = 0
            rw += 1


    def show_results(self):
        for x in self.tags_items.keys():
            # Enable the field to update the value
            self.text_values[x]["state"] = tk.NORMAL
            # Cleans the field
            self.text_values[x].delete("1.0", tk.END)

            # Insert the new value
            self.text_values[x].insert(tk.END, self.tags_items[x])

            # Disable the field to not alow edit
            self.text_values[x]["state"] = tk.DISABLED


    def show_arq_name(self):
        self.text_arq.delete("1.0",tk.END)

        self.text_arq.insert(tk.END, self.xml_file_path.get())


if __name__ == "__main__":
    app = App()
    app.mainloop()