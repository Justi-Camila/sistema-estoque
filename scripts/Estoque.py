import json
import os
from datetime import datetime
from scripts.Funcionario import Funcionario
from scripts.Produto import Produto


class Estoque:
    def __init__(self):
        """
            Método construtor do estoque. Inicializa a lista de produtos, carrega os dados salvos e força a autenticação do usuário.
        """
        self.produtos: list[Produto] = []

        self.carregar_produtos()

        self.func = None
        self.fazer_login()


    def fazer_login(self):
        """
        Gerencia o sistema de login, capturando os dados do funcionário e tratando exceções de entrada de dados.
        """
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
        """
            Busca um produto específico na lista de estoque através do ID.
            :param id_prod: Identificador único de um produto (int).
            :return: O objeto Produto correspondente se encontrado, ou None caso contrário (Produto | None).
        """
        for prod in self.produtos:
            if prod.id == id_prod:
                return prod
        return None


    def registrar_produto(self, id_prod: int, name: str, qtd: int, data_entrada: str):
        """
            Registra a entrada de produtos. Se o produto já existir, incrementa o estoque; se não, realiza o cadastro de um novo produto.
            Ao final, gera o log e persiste os dados.
            :param id_prod: Identificador único de um produto (int).
            :param name: Nome de um produto (str).
            :param qtd: Quantidade de um produto (int).
            :param data_entrada: Data de entrada de um produto (str).
        """
        prod = self.selecionar_produto(id_prod)

        if prod:
            prod.quantidade += qtd
            prod.data_entrada = data_entrada
            self.salvar_historico(f"ENTRADA - {qtd} unidades de '{prod.name}' por {self.func.name} (ID: {self.func.id})")
            print()
        else:
            novo_produto = Produto(id_prod, name, qtd, data_entrada)
            self.produtos.append(novo_produto)
            self.salvar_historico(f"CADASTRO E ENTRADA - {qtd} unidades de '{name}' por {self.func.name} (ID: {self.func.id})")
            print()

        self.salvar_produtos()


    def retirar_produto(self, id_prod: int, qtd: int):
        """
            Realiza a saída de produtos do estoque após validar a existência do item e o saldo disponível.
            :param id_prod: Identificador único de um produto (int).
            :param qtd: Quantidade de um produto (int).
            :return: True se a retirada foi realizada com sucesso, False se foi impedida (bool).
        """
        prod = self.selecionar_produto(id_prod)

        if not prod:
            print("Erro: Produto não encontrado no sistema.\n")
            return False

        if qtd > prod.quantidade:
            print(f"Erro: Quantidade solicitada ({qtd}) é maior que o estoque atual ({prod.quantidade}). Transação impedida.\n")
            return False
        elif qtd <= 0:
            print("Erro: A quantidade de retirada deve ser maior que zero.\n")
            return False

        prod.quantidade -= qtd
        self.salvar_historico(f"SAÍDA - {qtd} unidades de '{prod.name}' retiradas por {self.func.name} (ID: {self.func.id})")
        print()

        self.salvar_produtos()
        return True


    def consultar_produto(self):
        """
            Exibe no terminal a listagem visual de todos os produtos cadastrados e seus saldos atuais.
        """
        if not self.produtos:
            print("\nO estoque está completamente vazio.")
            return

        print("\n--- ATUAL ESTADO DO ESTOQUE ---")
        for produto in self.produtos:
            print(produto)
        print("--------------------------------\n")


    def salvar_historico(self, mensagem: str):
        """
            Gera uma linha de log com timestamp e grava de forma incremental no arquivo de auditoria.
            :param mensagem: Detalhes da movimentação gerada pelo sistema (str).
        """
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        linha_log = f"[{data_hora}] {mensagem}\n"

        print(linha_log.strip())

        with open("historico_estoque.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(linha_log)


    def salvar_produtos(self):
        """
            Converte a lista de objetos de produtos ativos em JSON e salva o arquivo para garantir a persistência.
        """
        with open("produtos.json", "w", encoding="utf-8") as arquivo:
            dados = [p.to_dict() for p in self.produtos]
            json.dump(dados, arquivo, indent=4)


    def carregar_produtos(self):
        """
            Verifica a existência do arquivo JSON e reconstrói a lista de objetos Produto em memória.
        """
        if os.path.exists("produtos.json"):
            with open("produtos.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                self.produtos = [Produto(d["id"], d["name"], d["quantidade"], d["data_entrada"]) for d in dados]


    def exibir_historico(self):
        """
            Abre e lê o arquivo de auditoria (.txt), exibindo todo o histórico de movimentações na tela do terminal.
        """
        print("\n--- HISTÓRICO COMPLETO DE MOVIMENTAÇÕES ---")
        if os.path.exists("historico_estoque.txt"):
            with open("historico_estoque.txt", "r", encoding="utf-8") as arquivo:
                print(arquivo.read())
        else:
            print("Nenhuma movimentação registrada até o momento.")
        print("-------------------------------------------")


    def run(self):
        """
            Inicia o loop principal do sistema, exibindo o menu de opções e gerenciando o fluxo de chamadas dos métodos.
        """
        while True:
            print("MENU PRINCIPAL")
            print("1 - Selecionar/Consultar Produto por ID")
            print("2 - Registrar Produto (Entrada)")
            print("3 - Consultar Todos os Produtos")
            print("4 - Retirar Produto (Saída)")
            print("5 - Trocar de Usuário (Logout)")
            print("6 - Visualizar Histórico de Movimentações")
            print("7 - Sair do Sistema")

            escolha = input("\nEscolha a opcao desejada: ")

            if escolha == "1":
                try:
                    produto_id = int(input("Por favor, digite o id do produto: "))
                    prod = self.selecionar_produto(produto_id)
                    if prod:
                        print(f"\n[PRODUTO ENCONTRADO] -> {prod}")
                    else:
                        print("\nProduto não localizado no estoque.\n")
                except ValueError:
                    # Tratamento de erro para evitar que o programa encerre se digitarem letras.
                    print("Erro: Por favor, digite um número inteiro válido.\n")

            elif escolha == "2":
                # Restrição de acesso, apenas o setor de Almoxarifado pode registrar produtos.
                if self.func.setor.lower() == "almoxarifado":

                    while True:
                        try:
                            id_produto = int(input("Por favor, insira o id do produto: "))
                            break
                        except ValueError:
                            # Tratamento de erro para evitar que o programa encerre se digitarem letras.
                            print("Erro: Por favor, digite um número inteiro válido.\n")

                    prod_existente = self.selecionar_produto(id_produto)

                    if prod_existente:
                        # Se o produto já existe, o seu nome é reaproveitado para evitar duplicidade.
                        print(f"-> Produto já cadastrado localizado: '{prod_existente.name}'")
                        nome = prod_existente.name
                    else:
                        print("-> ID não encontrado. Iniciando NOVO CADASTRO de produto.")
                        nome = input("Por favor, insira o nome do produto: ").strip()
                        # Validação para impedir produtos com nome vazio.
                        while nome == "":
                            print("Erro: O nome do produto não pode ficar em branco.")
                            nome = input("Por favor, insira o nome do produto: ").strip()

                    while True:
                        try:
                            quantidade = int(input("Por favor, insira a quantidade do produto: "))
                            #Validação para impedir quantidades menores ou iguais a zero
                            if quantidade <= 0:
                                print("Erro: A quantidade de entrada deve ser maior que zero.")
                                continue
                            break
                        except ValueError:
                            # Tratamento de erro para evitar que o programa encerre se digitarem letras.
                            print("Erro: Por favor, digite um número inteiro válido.\n")

                    while True:
                        data_entrada = input("Por favor, insira a data de entrada (DD/MM/AAAA): ").strip()
                        try:
                            datetime.strptime(data_entrada, "%d/%m/%Y")
                            break
                        except ValueError:
                            # Tratamento de erro para evitar que insira datas fora do formato.
                            print("Erro: Data inválida ou fora do formato DD/MM/AAAA. Tente novamente.")

                    self.registrar_produto(id_produto, nome, quantidade, data_entrada)

                else:
                    print("Você não está autorizado a fazer registros!\n")

            elif escolha == "3":
                # Exibe a listagem completa de itens cadastrados.
                self.consultar_produto()

            elif escolha == "4":
                # Restrição de acesso, apenas o setor de Almoxarifado pode retirar produtos.
                if self.func.setor.lower() == "almoxarifado":

                    while True:
                        try:
                            id_produto = int(input("Por favor, insira o id do produto: "))
                            prod_existente = self.selecionar_produto(id_produto)

                            # Validação: Verifica se o produto de fato existe antes de pedir a quantidade.
                            if not prod_existente:
                                print(f"Produto não localizado\n")
                            break
                        except ValueError:
                            print("Erro: Por favor, digite um número inteiro válido.\n")

                    # O fluxo de retirada só acontece se o id for válido e localizado.
                    if prod_existente:
                        while True:
                            try:
                                quantidade = int(input("Por favor, insira a quantidade do produto: "))
                                # Validação para impedir quantidades menores ou iguais a zero.
                                if quantidade <= 0:
                                    print("Erro: A quantidade de retirada deve ser maior que zero.\n")
                                else:
                                    self.retirar_produto(id_produto, quantidade)
                            except ValueError:
                                # Tratamento de erro para evitar que o programa encerre se digitarem letras.
                                print("Erro: Por favor, digite um número inteiro válido.\n")

                else:
                    print("Você não está autorizado a fazer retiradas!\n")

            elif escolha == "5":
                # Desconecta o usuário atual e força uma nova autenticação no sistema
                print(f"Efetuando logout de {self.func.name}...")
                self.fazer_login()

            elif escolha == "6":
                # Recupera e exibe em tela o histórico contido no arquivo de texto
                self.exibir_historico()

            elif escolha == "7":
                # Finaliza o loop e encerra a execução do programa
                print("Encerrando o sistema de estoque. Até logo!\n")
                break

            else:
                print("Escolha invalida\n")
