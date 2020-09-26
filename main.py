from bs4 import BeautifulSoup
import re
import pandas as pd
from Data import Obra


def htmlUbeton(fileName):
    with open(fileName, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, features="html.parser")

    containers = soup.find_all("div", "container pg")  # raíz dos blocos

    todasAsObras = []
    for path in containers:
        # DADOS DA OBRA PATH
        obra = Obra()
        dadosDaObraPath = path.find(
            "td", style="width:85% !important;")
        obra.nome = dadosDaObraPath.find(
            "b", string="Nome da Obra").next_sibling
        obra.endereco = dadosDaObraPath.find(
            "b", string="Endereço").next_sibling
        obra.estado = dadosDaObraPath.find(
            "b", string="Estado:").next_sibling
        obra.cep = dadosDaObraPath.find(
            "b", string="CEP:").next_sibling
        obra.estagio = dadosDaObraPath.find(
            "b", string="Estágio").next_sibling

        # CONTADOS DA OBRA
        contatosDaObraPath = path.find(
            "b", string="CONTATO(s) DA OBRA").find_parent(
            "p").find_next_sibling("table")
        engenheiroPath = contatosDaObraPath.find(
            "td", string="ENG. RESPONSÁVEL OBRA")

        if engenheiroPath is None:
            obra.engenheiro = None
            obra.telEngenheiro = None
            obra.emailEngenheiro = None
        else:
            obra.eng = engenheiroPath.find_previous_sibling("td").string
            engPath_tr = engenheiroPath.find_parent("tr")
            obra.telEngenheiro = engPath_tr.find(
                string=re.compile("\(\d{2}\) \d{4}-\d{4}"))
            obra.emailEngenheiro = engPath_tr.find(
                string=re.compile("@|restrito"))

        compradorPath = contatosDaObraPath.find(
            "td", string="COMPRADOR / MATERIAIS")

        if compradorPath is None:
            obra.comprador = None
            obra.telComprador = None
            obra.emailComprador = None
        else:
            obra.comprador = compradorPath.find_previous_sibling(
                "td").string
            obra.telComprador = compradorPath.find_parent(
                "tr").find(
                string=re.compile("\(\d{2}\) \d{4}-\d{4}"))
            obra.emailComprador = compradorPath.find_parent(
                "tr").find(
                string=re.compile("@|restrito"))

        obra.nomeCon = path.find(
            "b", string="CONSTRUÇÃO CIVIL").next_sibling
        obra.emailCon = path.find(
            "b", string="Site:").next_sibling
        obra.parseData()
        todasAsObras.append(obra)

    return todasAsObras


lista = htmlUbeton(".\HTML\example.html")


def dataFrameUbeton(listaDeObras):
    dictObras = {"Obra": [], "Endereço": [], "UF": [], "CEP": [],
                 "Estágio": [], "Construtora": [], "Email": [],
                 "Engenheiro": [], "Telefone-Eng": [], "Email-Eng": [],
                 "Comprador": [], "Telefone-Comp": [], "Email-Comp": []}
    for obra in listaDeObras:
        for key, value in zip(dictObras.keys(), obra.data):
            dictObras[key].append(value)
    return pd.DataFrame(dictObras)


dataFrameUbeton(lista).to_excel(".\EXCEL\deletemelater.xlsx")
