from bs4 import BeautifulSoup
import re
import pandas as pd

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

# Endereço: uf das obras
ufObras = []
for iufObra in container:
    uf = iufObra.find("b", string="Estado:").next_sibling
    uf = uf.strip()
    uf = re.sub(r"\n| -", "", uf)
    ufObras.append(uf)

# Endereço: cep das obras
cepObras = []
for icepObra in container:
    cep = icepObra.find("b", string="CEP:").next_sibling
    cep = cep.strip()
    cep = re.sub(r"\n| {1,}", "", cep)
    cepObras.append(cep)

# Estado das obras
estagioObras = []
for iEstagio in container:
    estagio = iEstagio.find("b", string="Estágio").next_sibling
    estagio = estagio[2:].strip()
    estagioObras.append(estagio)

# ----------------------------------------------------------------
# Nome da construtora
nomeConstrutora = []
for iConstrutora in container:
    construtora = iConstrutora.find(
        "b", string="CONSTRUÇÃO CIVIL").next_sibling
    construtora = construtora[3:].strip()
    nomeConstrutora.append(construtora)

# E-mail da construtora
emailConstrutora = []
for iConstrutora in container:
    emailConstr = iConstrutora.find("b", string="Site:").next_sibling
    emailConstr = emailConstr.strip()
    emailConstrutora.append(emailConstr)


# ----------------------------------------------------------------
# Nome do engenheiro responsável
nomeEngenheiro = []
for iEngenheiro in container:
    procuraDado = iEngenheiro.find(string="ENG. RESPONSÁVEL OBRA")
    if procuraDado == None:
        nomeEngenheiro.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        engenheiro = newPath.td.string
        nomeEngenheiro.append(engenheiro)

# Telefone do engenheiro responsável
telEngenheiro = []
for iTelEngenheiro in container:
    procuraDado = iTelEngenheiro.find(string="ENG. RESPONSÁVEL OBRA")
    if procuraDado == None:
        telEngenheiro.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        telEng = newPath.find(string=re.compile("\(\d{2}\) \d{4}-\d{4}"))
        telEngenheiro.append(telEng)

# E-mail do engenheiro responsável
emailEngenheiro = []
for iemailEngenheiro in container:
    procuraDado = iemailEngenheiro.find(string="ENG. RESPONSÁVEL OBRA")
    if procuraDado == None:
        emailEngenheiro.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        emailEng = newPath.find(string=re.compile("@|restrito"))
        if emailEng == None:
            emailEngenheiro.append("Sem dado")
        else:
            emailEngenheiro.append(emailEng)

# ----------------------------------------------------------------
# Nome do comprador
nomeComprador = []
for iComprador in container:
    procuraDado = iComprador.find(string="COMPRADOR / MATERIAIS")
    if procuraDado == None:
        nomeComprador.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        comprador = newPath.td.string
        nomeComprador.append(comprador)

# Telefone do comprador
telComprador = []
for iComprador in container:
    procuraDado = iComprador.find(string="COMPRADOR / MATERIAIS")
    if procuraDado == None:
        telComprador.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        telCompra = newPath.find(string=re.compile("\(\d{2}\) \d{4}-\d{4}"))
        telComprador.append(telCompra)


# E-mail do comprador
emailComprador = []
for iComprador in container:
    procuraDado = iComprador.find(string="COMPRADOR / MATERIAIS")
    if procuraDado == None:
        emailComprador.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        emailCompra = newPath.find(string=re.compile("@|restrito"))
        if emailEng == None:
            emailComprador.append("Sem dado")
        else:
            emailComprador.append(emailCompra)

# ------------------------------------------------
# PANDAS E EXCEL
# ------------------------------------------------
data = {"Nome da Obra": nomeObras, "Endereço da Obra": enderecoObras,
        "UF da Obra": ufObras, "CEP da Obra": cepObras,
        "Estágio da Obra": estagioObras, "Construtora": nomeConstrutora, "E-mail Construtora": emailConstrutora,
        "Engenheiro": nomeEngenheiro, "Tel Eng.": telEngenheiro,
        "E-mail Eng.": emailEngenheiro, "Comprador": nomeComprador,
        "Tel Comprador": telComprador, "E-mail Comprador": emailComprador}

dt = pd.DataFrame(data).to_excel("Dados_Intec2.xlsx")
