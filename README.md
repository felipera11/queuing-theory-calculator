# Simulador de Teoria de Filas

Calculadora interativa de modelos de teoria de filas, desenvolvida com Streamlit para a disciplina P108 do Inatel.

## Modelos Disponíveis

| Modelo | Descrição |
|--------|-----------|
| M/M/1 | Fila simples com um servidor, capacidade infinita |
| M/M/s | Fila com múltiplos servidores paralelos |
| M/M/1/K | Fila com um servidor e capacidade finita K |
| M/M/s/K | Fila com múltiplos servidores e capacidade finita K |
| M/M/1/N | Fila com um servidor e população finita N |
| M/M/s/N | Fila com múltiplos servidores e população finita N |
| M/G/1 | Fila com um servidor e distribuição de serviço geral |
| Prioridades | Fila com múltiplas classes de prioridade (preemptivo ou não) |

## Requisitos

- Python 3.10+

## Instalação

```bash
# Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv .env
source .env/bin/activate   # Linux/macOS
.env\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt
```

## Execução

```bash
python -m streamlit run app.py
```

Acesse `http://localhost:8501` no navegador.

## Testes

```bash
# Rodar todos os testes
pytest tests/

# Rodar testes de um modelo específico
pytest tests/test_models.py::TestQueueModels::<test_name>

# Cobertura de código
pytest --cov=models tests/
```

## Arquitetura

```
app.py                  # Ponto de entrada — configura página e sidebar
├── views/              # Camada de UI por modelo (Streamlit)
│   ├── mm1_page.py
│   ├── mms_page.py
│   ├── mm1k_page.py
│   ├── mmsk_page.py
│   ├── mm1n_page.py
│   ├── mmsn_page.py
│   ├── mg1_page.py
│   └── priority_page.py
├── models/             # Lógica de cálculo pura (sem Streamlit)
│   ├── mm1_model.py
│   ├── mms_model.py
│   ├── mm1k_model.py
│   ├── mmsk_model.py
│   ├── mm1n_model.py
│   ├── mmsn_model.py
│   ├── mg1_model.py
│   └── priority_model.py
├── utils/
│   ├── input_helpers.py  # Campos de entrada com suporte a expressões aritméticas
│   └── ui.py             # Tema CSS e utilitário metric_grid
└── tests/
    └── test_models.py    # Testes validados contra gabaritos da disciplina
```

## Observações

- Os campos de entrada aceitam expressões aritméticas (ex: `1/200`, `3*60`).
- Os construtores de modelos lançam `ValueError` para entradas inválidas (sistema instável, parâmetros negativos etc.).
- Para o modelo M/G/1, o parâmetro σ² representa a **variância** do tempo de serviço, não o desvio padrão.
- Para Prioridades, `lambdas` é uma lista com a taxa de chegada de cada classe.

## Lint

```bash
flake8
```
