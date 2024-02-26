import xml.etree.ElementTree as ET
from tabulate import tabulate

# XML file of the NF (Nota fiscal)
xml_file_path = 'nfdsul.xml'
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
        if x == 'total' or x == 'vBC':   # Não conta para o total
            continue
        if 'vDesc' == x == 'vICMSDeson': # Desconta do total
            tags_itens['total'] -= tags_itens[x]
        else:                            # Soma no total
            tags_itens['total'] += tags_itens[x]


def calcTag(Xpath, tag):
    global xml_file_path
    global tags_itens
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    namespace = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    Xpath += tag
    tags_itens[tag] = sum(float(prod.text) for prod in root.findall(Xpath, namespace))


def print_itens():
    tab = []
    for x in tags_itens.keys():
        tab.append([x, tags_itens[x]])

    table = tabulate(tab, headers=["Tag", "Valor"])
    print(table)


if __name__ == "__main__":
    calc_itens()
    print_itens()
