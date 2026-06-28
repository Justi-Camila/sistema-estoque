class Produto:

    def __init__(self, id_prod: int, name: str, quantidade: int = 0, data_entrada: str = ""):
        """
            Método constutor para inicializar as propriedades do produto.
            :param id_prod: Identificador único do produto (int)
            :param name: Nome do produto (str)
            :param quantidade: Quantidade inicial em estoque (int, padrão 0)
            :param data_entrada: Data do registro de entrada (str)
        """
        self.id = id_prod
        self.name = name
        self.data_entrada = data_entrada
        self.quantidade = quantidade

    def __str__(self):
        return f"ID: {self.id} | Nome: {self.name} | Qtd em Estoque: {self.quantidade} | Entrada: {self.data_entrada}"

    def to_dict(self):
        """
            Converte as propriedades do objeto Produto em um dicionário.
            :return: Dicionário contendo os dados estruturados do produto (dict)
        """
        return {
            "id": self.id,
            "name": self.name,
            "quantidade": self.quantidade,
            "data_entrada": self.data_entrada
        }