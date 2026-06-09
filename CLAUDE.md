# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
```bash
python -m streamlit run app.py
pytest tests/
pytest tests/test_models.py::TestQueueModels::<test_name>
pytest --cov=models tests/
flake8
```

## Architecture
Streamlit queuing-theory calculator. Flow: `app.py` → `views/<model>_page.py` → `models/<model>_model.py`

- `models/` — pure Python, no Streamlit. Constructors raise `ValueError` on invalid input.
- `utils/input_helpers.py` — inputs accept arithmetic expressions (e.g. `1/200`) via safe `ast.parse` evaluator.
- `utils/ui.py` — `inject_theme()` (CSS), `metric_grid(items, columns)`.

## Models

| Model | Constructor | Gotcha |
|-------|-------------|--------|
| M/M/1 | `MM1(λ, μ)` | |
| M/M/s | `MMS(λ, μ, s)` | |
| M/M/1/K | `MM1K(λ, μ, K)` | |
| M/M/s/K | `MMsK(λ, μ, K, s)` | |
| M/M/1/N | `MM1N(λ, μ, N)` | |
| M/M/s/N | `MMsN(λ, μ, N, s)` | |
| M/G/1 | `MG1(λ, μ, σ²)` | σ² is variance, not std dev |
| Priority | `PriorityQueue(lambdas, μ, s, preemptive)` | `lambdas` is a list |

Tests are validated against course answer keys; comments cite the source exercise.
