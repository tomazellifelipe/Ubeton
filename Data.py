class Obra:
    def __init__(self):
        self.nome = None
        self.endereco = None
        self.estado = None
        self.cep = None
        self.estagio = None

    def parse(self):
        return self.__dict__


class Construtora:
    def __init__(self):
        self.nome = None
        self.email = None
        self.engenheiro = None
        self.telEngenheiro = None
        self.emailEngenheiro = None
        self.comprador = None
        self.telComprador = None
        self.emailComprador = None

    def parse(self):
        return self.__dict__
