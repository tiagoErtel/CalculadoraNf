import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk
from tabulate import tabulate

# XML file of the NF (Nota fiscal)
xml_file_path = 'nfdsulagoravai.xml'
tags_itens = {}

def calc_itens():
    calcTag('.//ns:det/ns:prod/ns:', 'vProd')
    calcTag('.//ns:det/ns:prod/ns:', 'vDesc')      # Tag não testada, verificar path
    calcTag('.//ns:det/ns:prod/ns:', 'vICMSDeson') # Tag não testada, verificar path
    calcTag('.//ns:det/ns:prod/ns:', 'vST')        # Tag não testada, verificar path
    calcTag('.//ns:det/ns:prod/ns:', 'vFrete')     # Tag não testada, verificar path
    calcTag('.//ns:det/ns:prod/ns:', 'vSeg')       # Tag não testada, verificar path
    calcTag('.//ns:det/ns:prod/ns:', 'vOutro')
    calcTag('.//ns:det/ns:prod/ns:', 'vII')        # Tag não testada, verificar path
    calcTag('.//ns:det/ns:prod/ns:', 'vIPI')       # Tag não testada, verificar path
    calcTag('.//ns:impostoDevol/ns:IPI/ns:', 'vIPIdevol')
    calcTag('.//ns:det/ns:prod/ns:', 'vServ')      # Tag não testada, verificar path
    calcTag('.//ns:imposto/ns:ICMS//ns:', 'vBC')

    calcTotItens()


def calcTotItens():
    tags_itens['total'] = 0
    for x in tags_itens.keys():
        if x in ['total','vBC']:                  # Não conta para o total
            continue
        elif x in ['vDesc','vICMSDeson']:         # Desconta do total
            tags_itens['total'] -= tags_itens[x]
        else:                                     # Soma no total
            tags_itens['total'] += tags_itens[x]


def calcTag(Xpath, tag):
    global xml_file_path
    global tags_itens
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    namespace = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    Xpath += tag
    tags_itens[tag] = sum(float(prod.text) for prod in root.findall(Xpath, namespace))


def openWindow():
    # Cria uma instância da classe Tk, que é a janela principal do aplicativo
    window = tk.Tk()

    # Adiciona um título à janela
    window.title("Calculadora NF")

    # Define as dimensões da janela
    window.geometry("1366x768")

    #vProd
    label = ttk.Label(text='vProd:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vProd'])

    #vDesc
    label = ttk.Label(text='vDesc:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vDesc'])

    #vICMSDeson
    label = ttk.Label(text='vICMSDeson:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vICMSDeson'])

    #vST
    label = ttk.Label(text='vST:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vST'])

    #vFrete
    label = ttk.Label(text='vFrete:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vFrete'])

    #vSeg
    label = ttk.Label(text='vSeg:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vSeg'])

    #vOutro
    label = ttk.Label(text='vOutro:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vOutro'])

    #vII
    label = ttk.Label(text='vII:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vII'])

    #vIPI
    label = ttk.Label(text='vIPI:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vIPI'])

    #vIPIdevol
    label = ttk.Label(text='vIPIdevol:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vIPIdevol'])

    #vServ
    label = ttk.Label(text='vServ:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vServ'])

    #vBC
    label = ttk.Label(text='vBC:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['vBC'])

    #Total
    label = ttk.Label(text='Total:')
    label.pack()
    text = tk.Text(window, height = 1, width = 30)
    text.pack()
    text.insert(tk.END, tags_itens['total'])

    # Inicia o loop principal da aplicação
    window.mainloop()


if __name__ == "__main__":
    calc_itens()
    openWindow()
