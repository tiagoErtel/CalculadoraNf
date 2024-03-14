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
    window.geometry("400x300")

    #vProd
    ttk.Label(text='vProd:').grid(column=0, row=0)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=0)
    text.insert(tk.END, tags_itens['vProd'])

    #vDesc
    ttk.Label(text='vDesc:').grid(column=0, row=1)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=1)
    text.insert(tk.END, tags_itens['vDesc'])

    #vICMSDeson
    ttk.Label(text='vICMSDeson:').grid(column=0, row=2)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=2)
    text.insert(tk.END, tags_itens['vICMSDeson'])

    #vST
    ttk.Label(text='vST:').grid(column=0, row=3)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=3)
    text.insert(tk.END, tags_itens['vST'])

    #vFrete
    ttk.Label(text='vFrete:').grid(column=0, row=4)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=4)
    text.insert(tk.END, tags_itens['vFrete'])

    #vSeg
    ttk.Label(text='vSeg:').grid(column=0, row=5)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=5)
    text.insert(tk.END, tags_itens['vSeg'])

    #vOutro
    ttk.Label(text='vOutro:').grid(column=0, row=6)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=6)
    text.insert(tk.END, tags_itens['vOutro'])

    #vII
    ttk.Label(text='vII:').grid(column=0, row=7)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=7)
    text.insert(tk.END, tags_itens['vII'])

    #vIPI
    ttk.Label(text='vIPI:').grid(column=0, row=8)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=8)
    text.insert(tk.END, tags_itens['vIPI'])

    #vIPIdevol
    ttk.Label(text='vIPIdevol:').grid(column=0, row=9)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=9)
    text.insert(tk.END, tags_itens['vIPIdevol'])

    #vServ
    ttk.Label(text='vServ:').grid(column=0, row=10)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=10)
    text.insert(tk.END, tags_itens['vServ'])

    #vBC
    ttk.Label(text='vBC:').grid(column=0, row=11)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=11)
    text.insert(tk.END, tags_itens['vBC'])

    #Total
    ttk.Label(text='Total:').grid(column=0, row=12)
    text = tk.Text(window, height = 1, width = 30)
    text.grid(column=1, row=12)
    text.insert(tk.END, tags_itens['total'])

    # Inicia o loop principal da aplicação
    window.mainloop()


if __name__ == "__main__":
    calc_itens()
    openWindow()
