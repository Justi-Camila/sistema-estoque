from datetime import date


class Produto:

    def __init__(self, id_prod: int, name: str, quantidade: int = 0):
        self.id = id_prod
        self.name = name
        self.data_entrada = date.today()
        self.data_saida = date
        self.quantidade = quantidade

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.name} | Qtd em Estoque: {self.quantidade} | Entrada: {self.data_entrada}"