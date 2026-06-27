class Produto:

    def __init__(self, id_prod: int, name: str, quantidade: int = 0, data_entrada: str = ""):
        self.id = id_prod
        self.name = name
        self.data_entrada = data_entrada
        self.quantidade = quantidade

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.name} | Qtd em Estoque: {self.quantidade} | Entrada: {self.data_entrada}"

    def to_dict(self):
        """Converte o objeto para dicionário."""
        return {
            "id": self.id,
            "name": self.name,
            "quantidade": self.quantidade,
            "data_entrada": self.data_entrada
        }