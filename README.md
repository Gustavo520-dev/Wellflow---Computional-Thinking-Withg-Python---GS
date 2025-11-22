# 📘 WellFlow – Sistema de Acompanhamento de Bem-Estar do Colaborador

> Global Solution – Computational Thinking with Python  
> **Curso:** Engenharia de Software | **FIAP**

## 👨‍💻 Autor
**Nome:** Gustavo Cavalcanti - Brenda Thais Ribeiro dos Santos - Lucas Santana Silva

**RMs:** 565601 - 561258 - 566261 (respectivamente)

**Disciplina:** Computational Thinking with Python

**Apresentação da Solução WellFlow - GS Computational Thinking:** https://youtu.be/G9Q01RLKhWg

**WellFlow: Análise Técnica e Estruturas Python (Code Review): https://youtu.be/ZqMTg-5aRVc** 


---

## 🎯 Objetivo do Projeto
O **WellFlow** é uma solução desenvolvida em Python para monitorar a saúde mental e o clima organizacional de uma equipe. O sistema simula a coleta diária de feedback dos colaboradores, processa esses dados cruzando com perfis pré-existentes e gera diagnósticos automáticos para auxiliar a gestão na tomada de decisão.

O projeto foi construído atendendo rigorosamente aos requisitos de estruturas de programação fundamentais, incluindo manipulação de dados com Pandas e visualização com Matplotlib.

## 🚀 Funcionalidades
- **Área do Funcionário:**
  - Login via ID.
  - Registro de humor, conflitos e sobrecarga diária.
  - Feedback imediato com recomendações personalizadas.
- **Área do Gerente:**
  - Acesso protegido por senha.
  - Visualização de relatórios consolidados.
  - Geração de gráficos de desempenho/risco.
  - Consulta de dados cadastrais dos funcionários.
- **Inteligência de Dados:**
  - Cálculo de score de risco baseado em múltiplos fatores.
  - "Mini-IA" que seleciona a melhor situação/solução baseada no score.

## 🛠 Tecnologias Utilizadas
- **Python 3.x**
- **Pandas** (Manipulação de DataFrames e leitura de Excel/CSV)
- **Matplotlib** (Geração de gráficos)
- **OS/Sys** (Manipulação de sistema de arquivos e fluxo)

## 📋 Estruturas Obrigatórias Implementadas (Checklist GS)
O código integra os seguintes pilares de avaliação:

| Estrutura | Implementação no Código |
| :--- | :--- |
| **Entrada** | Coleta de dados via `input()` com validação de tipos. |
| **Saída** | Relatórios em console, exportação para CSV e Gráficos PNG. |
| **Repetição** | Loops `while True` para menus e validação de dados. |
| **Condição** | Estruturas `if/else/elif` para fluxo de decisão e lógica de negócio. |
| **Funções** | Código 100% modularizado em funções específicas. |
| **Função dentro de função (Interna)** | Uso de *Nested Functions* (`submenu` dentro de `menu_gerente`). |
| **DataFrame** | Leitura de base de dados (`xlsx`) e escrita de relatórios (`csv`). |

## ⚙️ Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter todos os requisitos instalados:

| Biblioteca     | Função                                 |
| -------------- | -------------------------------------- |
| **os**         | Criar e gerenciar diretórios           |
| **sys**        | Encerrar o programa corretamente       |
| **pandas**     | DataFrames, leitura Excel, escrita CSV |
| **matplotlib** | Geração de gráficos                    |
| **datetime**   | Registrar datas nos relatórios         |


[funcionariosMC.xlsx](https://github.com/user-attachments/files/23685895/funcionariosMC.xlsx)

[situacoesMC.xlsx](https://github.com/user-attachments/files/23685894/situacoesMC.xlsx)

Mudar caminho no codigo da leitura dos xlsx

### 📄 2. Documentação Técnica e Explicação das Estruturas (Para Entrega/PDF)

Este texto cobre o requisito: *"Explicar cada função/estrutura criada (2,0)"*.

---

# Documentação Técnica do Projeto WellFlow

## 1. Visão Geral da Arquitetura
O sistema **WellFlow** foi projetado utilizando uma arquitetura modular. O fluxo de dados inicia na leitura de arquivos Excel (Input de Arquivo), passa pela interação com o usuário (Input de Console), processamento lógico (Cálculo de Score e Seleção de Situação) e termina na geração de persistência de dados e visualização (Output em CSV e Gráfico).

## 2. Detalhamento das Funções e Estruturas

Abaixo, a explicação técnica de cada componente do código, justificando seu uso conforme os requisitos da Global Solution.

### 📥 2.1. Carregamento e Tratamento de Dados (DataFrames)
**Função:** `carregar_dados()`
- **Descrição:** Responsável por ler as bases de dados externas (`funcionariosMC.xlsx` e `situacoesMC.xlsx`).
- **Técnica:** Utiliza a biblioteca **Pandas** (`pd.read_excel`) para transformar planilhas em DataFrames manipuláveis. Realiza também a limpeza dos nomes das colunas (`strip()`) para evitar erros de digitação.
- **Requisito Atendido:** *Dataframe - manipulação estruturada de dados.*

### ⌨️ 2.2. Coleta de Dados (Inputs e Repetição)
**Função:** `coletar_inputs(nome)`
- **Descrição:** Interage com o usuário para capturar o estado diário (humor, conflito, sobrecarga).
- **Técnica:** Utiliza um loop infinito (`while True`) combinado com tratamento de exceções (`try/except`) para garantir que o humor seja um número inteiro entre 1 e 5. Só quebra o loop (`break`) quando o dado é válido.
- **Requisito Atendido:** *Estrutura de entrada* e *Estrutura de repetição.*

### 🛡️ 2.3. Segurança e Tratamento de Erros
**Função:** `safe_get(row, key, default=0)`
- **Descrição:** Uma função utilitária criada para evitar que o programa quebre (crash) caso encontre células vazias ou dados corrompidos nas planilhas Excel.
- **Técnica:** Tenta buscar o valor; se falhar ou for nulo (`pd.isna`), retorna um valor padrão.
- **Requisito Atendido:** *Estrutura de condição* (tratamento de falhas).

### 🧠 2.4. Lógica de Negócio (Cálculo de Score)
**Função:** `calcular_score(func, entrada)`
- **Descrição:** O "cérebro" matemático do sistema. Calcula um índice de risco somando fatores estáticos (perfil do funcionário) com fatores dinâmicos (dia atual).
- **Técnica:** Realiza operações aritméticas ponderadas. Exemplo: Conflitos e Sobrecarga têm peso 2, aumentando o risco.
- **Requisito Atendido:** *Funções - organização modular.*

### 🤖 2.5. Tomada de Decisão Inteligente
**Funções:** `escolher_situacao(df_sit, score_func)` e `calcular_situacao(sit, score_func)`
- **Descrição:** Simula uma inteligência artificial simples. O sistema varre todas as situações possíveis cadastradas no banco de dados, calcula qual delas tem o "score" mais próximo do estado atual do funcionário e retorna a recomendação mais adequada.
- **Técnica:** Itera sobre um DataFrame, gera uma lista de candidatos e ordena (`sorted`) para pegar o melhor match.
- **Requisito Atendido:** *Estrutura de repetição* (iterar linhas do DF) e *Condição* (lógica de escolha).

### 📦 2.6. Processamento Central
**Função:** `processar_funcionario(func, df_sit, entrada)`
- **Descrição:** Função Wrapper (envelope) que orquestra as chamadas anteriores. Recebe os dados brutos e devolve um dicionário estruturado pronto para ser salvo.

### 💾 2.7. Saída de Dados (Relatórios e Gráficos)
**Funções:** `salvar_relatorio(dados)` e `gerar_graficos()`
- **Descrição:** Persistem os resultados.
    - `salvar_relatorio`: Converte o dicionário processado em um DataFrame e exporta para CSV.
    - `gerar_graficos`: Lê o CSV gerado e cria um gráfico de barras usando **Matplotlib**, salvando-o como imagem PNG.
- **Requisito Atendido:** *Estrutura de saída.*

### 🔐 2.8. Encapsulamento Avançado (Nested Functions)
**Função:** `menu_gerente(df_func)` contendo `submenu()`
- **Descrição:** Controla o acesso administrativo. A função `submenu()` é definida **dentro** de `menu_gerente()`.
- **Motivativa:** Isso garante que o `submenu` só exista e só possa ser chamado se a autenticação do gerente (senha) tiver ocorrido com sucesso. O escopo da função interna fica protegido.
- **Requisito Atendido:** *Função dentro de função - encapsulamento avançado.*

### 🔄 2.9. Fluxo Principal
**Função:** `menu()`
- **Descrição:** O ponto de entrada da aplicação (`main`). Gerencia a navegação entre as áreas de Funcionário, Gerente e Saída.

## 3. Conclusão
A solução apresentada integra conceitos de Engenharia de Dados (Pandas), Engenharia de Software (Modularização e Tratamento de Erros) e Lógica de Programação (Estruturas de controle), entregando uma ferramenta funcional para a gestão de pessoas.

