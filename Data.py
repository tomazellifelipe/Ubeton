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
        self.index = len(self.data)

    def parseData(self):
        self.data = [self.nome, self.endereco, self.estado, self.cep,
                     self.estagio, self.nomeCon, self.emailCon,
                     self.engenheiro, self.telEngenheiro, self.emailEngenheiro,
                     self.comprador, self.telComprador, self.emailComprador]
        self.index = len(self.data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]
