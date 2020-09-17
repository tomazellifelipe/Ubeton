from bs4 import BeautifulSoup
import re


with open("example.html", encoding="utf8") as fp:
    soup = BeautifulSoup(fp, features="html.parser")

container = soup.find_all("div", "container pg")

# Nome da obra

nomeObras = []
for nObra in container:
    obra = nObra.table.b.next_sibling
    obra = obra[2:].strip()
    obra = re.sub(r"\n| {2,}", " ", obra)
    nomeObras.append(obra)
