class Funcionario:
    def __init__(self, id_func: int, name: str, setor: str):
        """
            Método construtor para inicializar as propriedades de funcionário.
            :param id_func: Identificador único do funcionário (int)
            :param name: Nome do funcionário (str)
            :param setor: Nome do setor do funcionário (str)
        """
        self.id = id_func
        self.name = name
        self.setor = setor