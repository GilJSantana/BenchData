# 📊 BenchData - Dashboard de Salários na Área de Dados

Este projeto é um dashboard interativo desenvolvido em Python utilizando **Streamlit**. O objetivo é permitir a análise exploratória de dados salariais de profissionais da área de dados (Data Scientists, Engineers, Analysts, etc.) ao redor do mundo.

O dashboard oferece filtros dinâmicos, métricas principais (KPIs) e visualizações gráficas detalhadas sobre a distribuição de salários, tipos de contrato e localização.

## 🏗️ Arquitetura do Projeto (Padrão MVC)

Para garantir a organização, escalabilidade e facilidade de manutenção do código, o projeto foi refatorado seguindo o padrão de arquitetura **MVC (Model-View-Controller)** adaptado para o fluxo do Streamlit.

A estrutura de arquivos e responsabilidades está dividida da seguinte forma:

### 1. Model (`config_data.py`)
Responsável pela **lógica de dados**.
- **Função:** Carrega o dataset bruto (`dados-final.csv`) e processa as regras de negócio.
- **Responsabilidade:** Contém a função `filtrar_dados(filtros)`, que recebe os parâmetros selecionados pelo usuário e retorna um novo DataFrame filtrado, sem alterar os dados originais.
- **Isolamento:** Não possui código de interface (Streamlit widgets), garantindo que a lógica de dados seja pura.

### 2. View (`config_app.py`)
Responsável pela **interface do usuário (UI)**.
- **Função:** Define como os dados são apresentados na tela.
- **Componentes:**
    - `setup_page()`: Configura a página e desenha a Sidebar com os filtros.
    - `exibir_metricas()`: Renderiza os cartões de KPIs.
    - `exibir_graficos()`: Constrói e exibe os gráficos interativos com Plotly.
    - `exibir_tabela()`: Mostra os dados detalhados.
- **Isolamento:** Recebe os dados já processados pelo Controller e apenas os exibe.

### 3. Controller (`app.py`)
Responsável pela **orquestração**.
- **Função:** É o ponto de entrada da aplicação. Ele conecta a *View* e o *Model*.
- **Fluxo de Execução:**
    1. Chama a *View* (`setup_page`) para desenhar os filtros e capturar o input do usuário.
    2. Passa esses inputs para o *Model* (`filtrar_dados`) para obter os dados processados.
    3. Chama a validação (`validar_dados`).
    4. Se válido, passa os dados filtrados de volta para a *View* (`exibir_metricas`, `exibir_graficos`) para renderização final.

---

## 📂 Estrutura de Arquivos

```
BenchData/
├── app.py            # (Controller) Ponto de entrada e orquestração
├── config_app.py     # (View) Componentes visuais e gráficos
├── config_data.py    # (Model) Carga e filtragem de dados
├── data/
│   └── dados-final.csv  # Dataset
├── tests/
│   └── test_app.py      # Testes automatizados (pytest)
├── pyproject.toml    # Definição de dependências (uv)
├── uv.lock           # Lockfile de versões (uv)
└── README.md         # Documentação do projeto
```

## 🚀 Funcionalidades

- **Filtros Dinâmicos:** Filtragem por Ano, Senioridade, Tipo de Contrato e Empresa.
- **KPIs em Tempo Real:** Média salarial, Salário Máximo, Total de Registros e Cargo mais frequente.
- **Visualizações Gráficas (Plotly):**
    - Top 10 Cargos por Salário Médio (Barras).
    - Distribuição de Salários (Histograma).
    - Proporção de Trabalho Remoto vs. Presencial (Pizza).
    - Mapa Global de Salários para Data Scientists (Choropleth).
- **Tabela de Dados:** Visualização detalhada dos registros filtrados.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **uv:** Gerenciador de pacotes e projetos Python extremamente rápido.
- **Streamlit:** Framework para Web Apps de Dados.
- **Pandas:** Manipulação e análise de dados.
- **Plotly Express:** Criação de gráficos interativos.
- **Pytest:** Framework de testes automatizados.

## ▶️ Como Executar

Este projeto utiliza o **uv** para gerenciamento de dependências.

1. Instale as dependências do projeto:
   ```bash
   uv sync
   ```

2. Execute a aplicação:
   ```bash
   uv run streamlit run app.py
   ```

## 🧪 Como Testar

Para rodar a suíte de testes automatizados e garantir que tudo está funcionando:

1. Instale as dependências de desenvolvimento (se necessário):
   ```bash
   uv add --dev pytest
   ```

2. Execute os testes:
   ```bash
   uv run pytest
   ```

---
*Desenvolvido como exemplo de aplicação de boas práticas de desenvolvimento em Data Apps.*
