# Sistema de Estoque 📦

Um sistema simples de gerenciamento de estoque desenvolvido em Python, rodando via linha de comando (CLI). Este projeto da faculdade permite gerenciar a entrada, saída e consulta de produtos, além de manter um histórico de movimentações e controle de acesso baseado no setor do funcionário.

## 🚀 Funcionalidades

- **Autenticação Simples**: Identificação do funcionário através de ID, Nome e Setor no momento do login.
- **Controle de Acesso**: Apenas funcionários do setor **Almoxarifado** possuem permissão para registrar entradas ou realizar retiradas de produtos.
- **Consulta de Produtos**:
  - Busca de produto específico por ID.
  - Listagem completa de todos os produtos no estoque.
- **Registro de Entrada**: Permite adicionar novos produtos ou incrementar a quantidade de itens já cadastrados.
- **Registro de Saída (Retirada)**: Permite dar baixa em itens do estoque (apenas se houver saldo suficiente).
- **Histórico e Auditoria**: Todas as transações de entrada e saída são registradas com data, hora e dados do funcionário responsável, e podem ser consultadas no sistema.
- **Persistência de Dados**:
  - Os produtos e suas quantidades são salvos no arquivo `produtos.json`.
  - O histórico de movimentações é salvo no arquivo `historico_estoque.txt`.

## 📂 Estrutura do Projeto

```
📦 trabalho-faculdade-engenharia-software
 ┣ 📂 scripts
 ┃ ┣ 📜 Estoque.py       # Lógica principal do sistema e menus
 ┃ ┣ 📜 Funcionario.py   # Classe Funcionario
 ┃ ┗ 📜 Produto.py       # Classe Produto
 ┣ 📜 main.py            # Ponto de entrada da aplicação
 ┣ 📜 produtos.json      # Arquivo de persistência do estoque (banco de dados em JSON)
 ┗ 📜 historico_estoque.txt # Log de auditoria e movimentações
```

## 🛠️ Como Executar

### Pré-requisitos
- Ter o  [Python](https://www.python.org/downloads/) (versão 3.x) instalado na sua máquina.

### Passos para rodar

1. **Obter o código**:
   - Clone este repositório usando `git clone https://github.com/Justi-Camila/sistema-estoque.git` **OU** faça o download do arquivo ZIP e extraia a pasta.


2. **Acessar a pasta do projeto pelo terminal**:
   ```bash
   cd sistema-estoque
   
3. Execute o arquivo principal:
   ```bash
   python main.py
   ```

## ⚠️ Observações de Uso

- Ao iniciar o sistema, você será solicitado a informar seu Nome, ID e Setor.
- Para testar as funcionalidades de **Registro de Produto (Entrada)** e **Retirada de Produto (Saída)**, certifique-se de preencher o setor exatamente como **`almoxarifado`** (não faz distinção entre maiúsculas ou minúsculas, mas deve ser essa palavra). Caso contrário, o sistema bloqueará essas operações por falta de permissão.
