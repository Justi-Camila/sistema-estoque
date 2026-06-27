import json
import os
from datetime import datetime
from scripts.Funcionario import Funcionario
from scripts.Produto import Produto


class Estoque:
    def __init__(self):
        self.produtos: list[Produto] = []

        self.carregar_produtos()

        self.func = None
        self.fazer_login()

    def fazer_login(self):
        while True:
            try:
                print("\n" + "-" * 10, "AUTENTICAÇÃO DO SISTEMA", "-" * 10)
                nome = input("Por favor digite o seu nome: ")

                id_func = int(input("Por favor, digite o seu ID: "))
                setor = input("Por favor, digite o nome do seu setor: ")
                print("-" * 45 + "\n")

                # Atualiza o funcionário ativo no sistema
                self.func = Funcionario(id_func, nome, setor)
                print(f"Bem-vindo(a), {self.func.name} do setor {self.func.setor}!")
                break
            except ValueError:
                print("Erro: Por favor, digite um número inteiro válido.")

    def selecionar_produto(self, id_prod: int) -> Produto | None:
        for prod in self.produtos:
            if prod.id == id_prod:
                return prod
        return None


    def registrar_produto(self, id_prod: int, name: str, qtd: int, data_entrada: str):
        prod = self.selecionar_produto(id_prod)

        if prod:
            prod.quantidade += qtd
            prod.data_entrada = data_entrada
            self.salvar_historico(f"ENTRADA - {qtd} unidades de '{prod.name}' por {self.func.name} (ID: {self.func.id})")
        else:
            novo_produto = Produto(id_prod, name, qtd, data_entrada)
            self.produtos.append(novo_produto)
            self.salvar_historico(
                f"CADASTRO E ENTRADA - {qtd} unidades de '{name}' por {self.func.name} (ID: {self.func.id})")

        self.salvar_produtos()


    def retirar_produto(self, id_prod: int, qtd: int):
        prod = self.selecionar_produto(id_prod)

        if not prod:
            print("Erro: Produto não encontrado no sistema.")
            return False

        if qtd > prod.quantidade:
            print(f"Erro: Quantidade solicitada ({qtd}) é maior que o estoque atual ({prod.quantidade}). Transação impedida.")
            return False
        elif qtd <= 0:
            print("Erro: A quantidade de retirada deve ser maior que zero.")
            return False

        prod.quantidade -= qtd
        self.salvar_historico(
            f"SAÍDA - {qtd} unidades de '{prod.name}' retiradas por {self.func.name} (ID: {self.func.id})")

        self.salvar_produtos()
        return True


    def consultar_produto(self):
        if not self.produtos:
            print("\nO estoque está completamente vazio.")
            return

        print("\n--- ATUAL ESTADO DO ESTOQUE ---")
        for produto in self.produtos:
            print(produto)
        print("--------------------------------")

    def salvar_historico(self, mensagem: str):
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        linha_log = f"[{data_hora}] {mensagem}\n"

        print(linha_log.strip())

        with open("historico_estoque.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(linha_log)

    def salvar_produtos(self):
        with open("produtos.json", "w", encoding="utf-8") as arquivo:
            dados = [p.to_dict() for p in self.produtos]
            json.dump(dados, arquivo, indent=4)

    def carregar_produtos(self):
        if os.path.exists("produtos.json"):
            with open("produtos.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                self.produtos = [Produto(d["id"], d["name"], d["quantidade"], d["data_entrada"]) for d in dados]


    def run(self):
        while True:
            print("MENU PRINCIPAL")
            print("1 - Selecionar/Consultar Produto por ID")
            print("2 - Registrar Produto (Entrada)")
            print("3 - Consultar Todos os Produtos")
            print("4 - Retirar Produto (Saída)")
            print("5 - Trocar de Usuário (Logout)")
            print("6 - Sair do Sistema")

            escolha = input("Escolha a opcao desejada: ")

            if escolha == "1":
                try:
                    produto_id = int(input("Por favor, digite o id do produto: "))
                    prod = self.selecionar_produto(produto_id)
                    if prod:
                        print(f"\n[PRODUTO ENCONTRADO] -> {prod}")
                    else:
                        print("\nProduto não localizado no estoque.")
                except ValueError:
                    print("Erro: Por favor, digite um número inteiro válido.")

            elif escolha == "2":
                if self.func.setor.lower() == "almoxarifado":
                    while True:
                        try:
                            id_produto = int(input("Por favor, insira o id do produto: "))
                            break
                        except ValueError:
                            print("Erro: Por favor, digite um número inteiro válido.")

                    prod_existente = self.selecionar_produto(id_produto)

                    if prod_existente:
                        print(f"-> Produto já cadastrado localizado: '{prod_existente.name}'")
                        nome = prod_existente.name
                    else:
                        print("-> ID não encontrado. Iniciando NOVO CADASTRO de produto.")
                        nome = input("Por favor, insira o nome do produto: ").strip()
                        while nome == "":
                            print("Erro: O nome do produto não pode ficar em branco.")
                            nome = input("Por favor, insira o nome do produto: ").strip()

                    while True:
                        try:
                            quantidade = int(input("Por favor, insira a quantidade do produto: "))
                            if quantidade <= 0:
                                print("Erro: A quantidade de entrada deve ser maior que zero.")
                                continue
                            break
                        except ValueError:
                            print("Erro: Por favor, digite um número inteiro válido.")

                    while True:
                        data_entrada = input("Por favor, insira a data de entrada (DD/MM/AAAA): ").strip()
                        try:
                            datetime.strptime(data_entrada, "%d/%m/%Y")
                            break
                        except ValueError:
                            print("Erro: Data inválida ou fora do formato DD/MM/AAAA. Tente novamente.")

                    self.registrar_produto(id_produto, nome, quantidade, data_entrada)

                else:
                    print("Você não está autorizado a fazer registros!")
                    print()

            elif escolha == "3":
                self.consultar_produto()

            elif escolha == "4":
                if self.func.setor.lower() == "almoxarifado":
                    while True:
                        try:
                            id_produto = int(input("Por favor, insira o id do produto: "))
                            break
                        except ValueError:
                            print("Erro: Por favor, digite um número inteiro válido.")

                    while True:
                        try:
                            quantidade = int(input("Por favor, insira a quantidade do produto: "))
                            if quantidade <= 0:
                                print("Erro: A quantidade de entrada deve ser maior que zero.")
                                continue
                            break
                        except ValueError:
                            print("Erro: Por favor, digite um número inteiro válido.")

                    self.retirar_produto(id_produto, quantidade)

                else:
                    print("Você não está autorizado a fazer retiradas!")
                    print()

            elif escolha == "5":
                print(f"Efetuando logout de {self.func.name}...")
                self.fazer_login()

            elif escolha == "6":
                print("Encerrando o sistema de estoque. Até logo!")
                break

            else:
                print("Escolha invalida\n")
