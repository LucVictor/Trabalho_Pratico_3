# Trabalho Avaliativo - Unidade 3 - Métodos Numéricos

Este rositepório contém o código desenvolvido para o trabalho avaliativo da Unidade 3 da disciplina de Métodos Numéricos do curso de Engenharia de Produção. O projeto é uma aplicação web desenvolvida em Python utilizando Flask, Numpy, HTML, Bootstrap e SQLite.

## Objetivo do Projeto

O objetivo principal da aplicação é otimizar a gestão de trabalhadores e produtos recicláveis dentro da cooperativa, permitindo um controle eficiente dos recursos e auxiliando na maximização dos rendimentos da empresa.

## Funcionalidades

- **Gestão de Produtos Recicláveis:**
  - Cadastro, visualização e remoção de produtos recicláveis.
  - Limite de produtos cadastrados, conforme modelo de otimização.

- **Gestão de Trabalhadores:**
  - Cadastro, visualização e remoção de trabalhadores da cooperativa.
  - Limite de trabalhadores cadastrados, conforme modelo de otimização.

- **Cálculos de Otimização:**
  - Funções para calcular e visualizar a alocação de recursos e maximização de rendimentos.
  - **Implementação do Método de Gauss-Jordan:** Utilizado para resolver sistemas lineares que surgem no processo de otimização, permitindo encontrar soluções viáveis para a distribuição dos recursos.

## Tecnologias Utilizadas

- **Python 3.8+**
- **Flask:** Framework web utilizado para desenvolvimento da aplicação.
- **SQLAlchemy:** ORM utilizado para gerenciamento do banco de dados SQLite.
- **Numpy:** Biblioteca utilizada para operações matemáticas, incluindo a implementação do Método de Gauss-Jordan.
- **HTML & Bootstrap:** Utilizados para a interface do usuário.
- **MariaDB:** Banco de dados para salvar as informações.

## Estrutura do Projeto

- **`app.py`:** Arquivo principal da aplicação, define as rotas e a lógica de negócios.
- **`templates/`:** Diretório que contém os arquivos HTML.
- **`static/`:** Diretório para arquivos estáticos como CSS, imagens e JavaScript.
- **`database.db`:** Arquivo de banco de dados SQLite que armazena os dados da aplicação.
- **`requirements.txt`:** Lista de dependências do projeto.

## Considerações Finais

Este sistema foi desenvolvido para auxiliar a cooperativa de reciclagem de Belém na gestão de seus recursos e na maximização de seus rendimentos, com base em conceitos de programação linear apresentados na ENEGEP 2022. A aplicação também implementa o Método de Gauss-Jordan para resolver sistemas lineares, que são essenciais no processo de otimização.

Contribuições para melhorias no sistema são bem-vindas!

## Licença

Este projeto é licenciado sob os termos da licença MIT.
