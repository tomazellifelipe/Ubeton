from bs4 import BeautifulSoup
import re
import pandas as pd
from Data import Obra

with open("example.html", encoding="utf8") as fp:
    soup = BeautifulSoup(fp, features="html.parser")

containers = soup.find_all("div", "container pg")  # raíz dos blocos
for path in containers:
    # DADOS DA OBRA PATH
    obra = Obra()
    dadosDaObraPath = path.find("td", style="width:85% !important;")
    nomeDaObra = dadosDaObraPath.find("b", string="Nome da Obra").next_sibling
    enderecoDaObra = dadosDaObraPath.find("b", string="Endereço").next_sibling
    ufDaObra = dadosDaObraPath.find("b", string="Estado:").next_sibling
    cepDaObra = dadosDaObraPath.find("b", string="CEP:").next_sibling
    estagiodaObra = dadosDaObraPath.find("b", string="Estágio").next_sibling

    # CONTADOS DA OBRA
    contatosPath = path.find("b", string="CONTATO(s) DA OBRA").find_parent(
        "p").find_next_sibling("table")
    engPath = contatosPath.find("td", string="ENG. RESPONSÁVEL OBRA")
    if engPath is None:
        nomeDoEng = None
        telDoEng = None
        emailDoEng = None
    else:
        nomeDoEng = engPath.find_previous_sibling("td").string
        engPath_tr = engPath.find_parent("tr")
        telDoEng = engPath_tr.find(
            string=re.compile("\(\d{2}\) \d{4}-\d{4}"))
        emailDoEng = engPath_tr.find(
            string=re.compile("@|restrito"))
    compradorPath = contatosPath.find("td", string="COMPRADOR / MATERIAIS")
    if engPath is None:
        nomeDoComprador = None
        telDoComprador = None
        emailDoComprador = None
    else:
        nomeDoComprador = compradorPath.find_previous_sibling("td").string
        telDoComprador = compradorPath.find_parent("tr").find(
            string=re.compile("\(\d{2}\) \d{4}-\d{4}"))
        emailDoComprador = compradorPath.find_parent("tr").find(
            string=re.compile("@|restrito"))
    print(contatosPath)


# Nome das obras
nomeObras = []
enderecoObras = []
ufObras = []
cepObras = []
estagioObras = []
nomeConstrutora = []
emailConstrutora = []
nomeEngenheiro = []
telEngenheiro = []
emailEngenheiro = []
nomeComprador = []
telComprador = []
emailComprador = []

for iObra in containers:
    obra = iObra.find("b", string="Nome da Obra").next_sibling
    obra = obra[2:].strip()
    obra = re.sub(r"\n| {2,}", " ", obra)
    nomeObras.append(obra)

# Endereço das obras
for iEndereco in containers:
    endereco = iEndereco.find("b", string="Endereço").next_sibling
    endereco = endereco[2:].strip()
    endereco = re.sub(r"\n| {2,}", " ", endereco)
    enderecoObras.append(endereco)

# Endereço: uf das obras
for iufObra in containers:
    uf = iufObra.find("b", string="Estado:").next_sibling
    uf = uf.strip()
    uf = re.sub(r"\n| -", "", uf)
    ufObras.append(uf)

# Endereço: cep das obras
for icepObra in containers:
    cep = icepObra.find("b", string="CEP:").next_sibling
    cep = cep.strip()
    cep = re.sub(r"\n| {1,}", "", cep)
    cepObras.append(cep)

# Estado das obras
for iEstagio in containers:
    estagio = iEstagio.find("b", string="Estágio").next_sibling
    estagio = estagio[2:].strip()
    estagioObras.append(estagio)

# ----------------------------------------------------------------
# Nome da construtora
for iConstrutora in containers:
    construtora = iConstrutora.find(
        "b", string="CONSTRUÇÃO CIVIL").next_sibling
    construtora = construtora[3:].strip()
    nomeConstrutora.append(construtora)

# E-mail da construtora
for iConstrutora in containers:
    emailConstr = iConstrutora.find("b", string="Site:").next_sibling
    emailConstr = emailConstr.strip()
    emailConstrutora.append(emailConstr)


# ----------------------------------------------------------------
# Nome do engenheiro responsável
for iEngenheiro in containers:
    procuraDado = iEngenheiro.find(string="ENG. RESPONSÁVEL OBRA")
    if procuraDado is None:
        nomeEngenheiro.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        engenheiro = newPath.td.string
        nomeEngenheiro.append(engenheiro)

# Telefone do engenheiro responsável
for iTelEngenheiro in containers:
    procuraDado = iTelEngenheiro.find(string="ENG. RESPONSÁVEL OBRA")
    if procuraDado is None:
        telEngenheiro.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        telEng = newPath.find(string=re.compile("\(\d{2}\) \d{4}-\d{4}"))
        telEngenheiro.append(telEng)

# E-mail do engenheiro responsável
for iemailEngenheiro in containers:
    procuraDado = iemailEngenheiro.find(string="ENG. RESPONSÁVEL OBRA")
    if procuraDado is None:
        emailEngenheiro.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        emailEng = newPath.find(string=re.compile("@|restrito"))
        if emailEng is None:
            emailEngenheiro.append("Sem dado")
        else:
            emailEngenheiro.append(emailEng)

# ----------------------------------------------------------------
# Nome do comprador
for iComprador in containers:
    procuraDado = iComprador.find(string="COMPRADOR / MATERIAIS")
    if procuraDado is None:
        nomeComprador.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        comprador = newPath.td.string
        nomeComprador.append(comprador)

# Telefone do comprador
for iComprador in containers:
    procuraDado = iComprador.find(string="COMPRADOR / MATERIAIS")
    if procuraDado is None:
        telComprador.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        telCompra = newPath.find(string=re.compile("\(\d{2}\) \d{4}-\d{4}"))
        telComprador.append(telCompra)


# E-mail do comprador
for iComprador in containers:
    procuraDado = iComprador.find(string="COMPRADOR / MATERIAIS")
    if procuraDado is None:
        emailComprador.append("Sem dado")
    else:
        newPath = procuraDado.find_parent("tr")
        emailCompra = newPath.find(string=re.compile("@|restrito"))
        if emailEng is None:
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
