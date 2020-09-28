class Obra:
    def __init__(self):
        self.nome = None
        self.endereco = None
        self.estado = None
        self.cep = None
        self.estagio = None
        self.nomeCon = None
        self.emailCon = None
        self.engenheiro = None
        self.telEngenheiro = None
        self.emailEngenheiro = None
        self.comprador = None
        self.telComprador = None
        self.emailComprador = None
        self.data = []

    def parseData(self):
        for value in self.__dict__.values():
            if value is not []:
                self.data.append(value)
