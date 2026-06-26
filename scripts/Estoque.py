from scripts.Funcionario import Funcionario

class Estoque:
    def __init__(self):
        self.func = Funcionario(21, "Camila", "Ti")

    def run(self):
        while True:
            print("MENU PRINCIPA")
            print("1 - Registrar Produto")
            print("2 - Consultar Produto")
            print("3 - Retirar Produto")
            print("4 - Sair")

            escolha = input("Escolha a opcao desejada:")

            if escolha == "1":
                nome = input("Por favor, insira o nome do produto: ")
                id_produto = int(input("Por favor, insira o id do produto: "))
                quantidade = int(input("Por favor, insira a quantidade do produto: "))
                self.func.registrarProduto(id_produto, nome, quantidade)

            elif escolha == "2":
                self.func.consultarProduto()

            elif escolha == "3":
                id_produto = int(input("Por favor, insira o id do produto: "))
                quantidade = int(input("Por favor, insira a quantidade do produto: "))
                self.func.retirarProduto(id_produto, quantidade)

            elif escolha == 4:
                print("SAIDA")
                break

            else:
                print("Escolha invaldia")
