import re

import pandas as pd
from bs4 import BeautifulSoup

from Data import Obra


def cleanString(string):
    if string is not None:
        return re.sub(r"\s{2,}|^:\s|-$|^-\s", "", string.strip())
    return string


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
        obra.nome = cleanString(dadosDaObraPath.find(
            "b", string="Nome da Obra").next_sibling)
        obra.endereco = cleanString(dadosDaObraPath.find(
            "b", string="Endereço").next_sibling)
        obra.estado = cleanString(dadosDaObraPath.find(
            "b", string="Estado:").next_sibling)
        obra.cep = cleanString(dadosDaObraPath.find(
            "b", string="CEP:").next_sibling)
        obra.estagio = cleanString(dadosDaObraPath.find(
            "b", string="Estágio").next_sibling)

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
            obra.eng = cleanString(
                engenheiroPath.find_previous_sibling("td").string)
            engPath_tr = engenheiroPath.find_parent("tr")
            obra.telEngenheiro = cleanString(engPath_tr.find(
                string=re.compile(r"\(\d{2}\) \d{4}-\d{4}")))
            obra.emailEngenheiro = cleanString(engPath_tr.find(
                string=re.compile("@|restrito")))

        compradorPath = contatosDaObraPath.find(
            "td", string="COMPRADOR / MATERIAIS")

        if compradorPath is None:
            obra.comprador = None
            obra.telComprador = None
            obra.emailComprador = None
        else:
            obra.comprador = cleanString(compradorPath.find_previous_sibling(
                "td").string)
            obra.telComprador = cleanString(compradorPath.find_parent(
                "tr").find(
                string=re.compile(r"\(\d{2}\) \d{4}-\d{4}")))
            obra.emailComprador = cleanString(compradorPath.find_parent(
                "tr").find(
                string=re.compile("@|restrito")))

        obra.nomeCon = cleanString(path.find(
            "b", string="CONSTRUÇÃO CIVIL").next_sibling)
        obra.emailCon = cleanString(path.find(
            "b", string="Site:").next_sibling)
        obra.parseData()
        todasAsObras.append(obra)

    return todasAsObras


lista = htmlUbeton(r".\\HTML\\example.html")


def dataFrameUbeton(listaDeObras, *args):
    dictObras = {}
    for arg in args:
        dictObras[arg] = []
    for obra in listaDeObras:
        for key, value in zip(dictObras.keys(), obra.data):
            dictObras[key].append(value)
    return pd.DataFrame(dictObras)


dataFrameUbeton(lista, 'Obra', 'Endereco', 'UF', 'CEP', 'Estágio',
                'Construtora', 'E-mail', 'Engenheiro', 'Telefone Eng.',
                'E-mail Eng.', 'Comprador', 'Telefone Compr.',
                'E-mail Compr.').to_excel(r".\\EXCEL\\deletemelater.xlsx")
