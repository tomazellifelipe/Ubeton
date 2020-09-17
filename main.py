from bs4 import BeautifulSoup
import re


with open("example.html", encoding="utf8") as fp:
    soup = BeautifulSoup(fp, features="html.parser")

container = soup.find_all("div", "container pg")

# Nome das obras
nomeObras = []
for iObra in container:
    obra = iObra.find("b", string="Nome da Obra").next_sibling
    obra = obra[2:].strip()
    obra = re.sub(r"\n| {2,}", " ", obra)
    nomeObras.append(obra)

# Endereço das obras
enderecoObras = []
for iEndereco in container:
    endereco = iEndereco.find("b", string="Endereço").next_sibling
    endereco = endereco[2:].strip()
    endereco = re.sub(r"\n| {2,}", " ", endereco)
    enderecoObras.append(endereco)
