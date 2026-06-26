from datetime import date

from scripts.Produto import Produto


class Funcionario:
    def __init__(self, id_func: int, name: str, setor: str):
        self.id = id_func
        self.name = name
        self.setor = setor
        self.produtos: list[Produto] = []

    def registrarProduto(self, id_prod: int, name: str, qtd: int):
        for prod in self.produtos:
            if prod.id == id_prod:
                prod.quantidade += qtd
                prod.data_entrada = date.today()
                print(f"[HISTORICO] {date.today()} - ENTRADA - {qtd} unidades de '{name}' por {self.name} (ID: {self.id})")

        novo_produto = Produto(id_prod, name, qtd)
        self.produtos.append(novo_produto)
        print(f"[HISTÓRICO] {date.today()} - CADASTRO E ENTRADA - {qtd} unidades de '{name}' por {self.name}")
        return self.produtos

    def retirarProduto(self, id_prod: int, qtd: int):
        for prod in self.produtos:
            if prod.id == id_prod:
                if qtd > prod.quantidade:
                    print(f"Erro: Quantidade solicitada ({qtd}) é maior que o estoque atual ({prod.quantidade}). Transação impedida.")
                    return False
                elif qtd <= 0:
                    print("Erro: A quantidade de retirada deve ser maior que zero.")
                    return False

                prod.quantidade -= qtd
                print(f"[HISTÓRICO] {date.today()} - SAÍDA - {qtd} unidades de '{prod.name}' retiradas por {self.name}")
                return True

        print("Erro: Produto não encontrado no sistema.")
        return False

    def consultarProduto(self):
        if not self.produtos:
            print("\nO estoque está completamente vazio.")
            return

        print("\n--- ATUAL ESTADO DO ESTOQUE ---")
        for produto in self.produtos:
            print(produto)
        print("--------------------------------")
