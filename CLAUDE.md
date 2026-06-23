# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
```bash
python -m streamlit run app.py        # start the web app
pytest tests/                          # run all 74 tests
pytest tests/test_models.py::TestQueueModels::<test_name>
pytest --cov=models tests/             # coverage report
flake8                                 # lint
python gerar_guia_pdf.py              # regenerate guia_calculadora_filas.pdf
```

## Architecture
Streamlit queuing-theory calculator. Flow: `app.py` → `views/<model>_page.py` → `models/<model>_model.py`

- `models/` — pure Python, no Streamlit. Constructors raise `ValueError` on invalid input.
- `views/` — one `render()` function per model; reads inputs, calls model, calls `metric_grid`.
- `utils/input_helpers.py` — `input_lambda`, `input_mi`, `input_integer`, `input_float_value`, `input_n_with_operator`. All rate fields accept arithmetic expressions (e.g. `1/200`) via safe `ast.parse` evaluator.
- `utils/ui.py` — `inject_theme()` (dark CSS), `metric_grid(items, columns)`, `show_n_prob(fila, n, op)`.
- `gerar_guia_pdf.py` — standalone script (uses `reportlab`) that produces `guia_calculadora_filas.pdf`.

## Terminology (matches apostilas P108 — Prof. Paulo Maia)
- Menu names: **M/M/1**, **M/M/s>1**, **M/M/1/K**, **M/M/s>1/K**, **M/M/1/N**, **M/M/s>1/N**, **M/G/1**, **Prioridades**
- Metric labels: W = "Tempo médio gasto no sistema", Wq = "Tempo médio de espera na fila", ρ = "Taxa de ocupação", P₀ = "Probabilidade de o sistema estar vazio"
- W and Wq display raw values — **no unit conversion** (output unit = same as 1/λ = 1/μ)
- K = total system capacity (queue + servers), consistent with apostila slide definition
- σ² field in M/G/1 is **variance**, not std dev. Exponential: σ² = 1/μ². Deterministic: σ² = 0.

## Models

| Model | Constructor | Notes |
|-------|-------------|-------|
| M/M/1 | `MM1(λ, μ)` | raises if λ ≥ μ |
| M/M/s>1 | `MMS(λ, μ, s)` | s ≥ 2; raises if λ ≥ s·μ |
| M/M/1/K | `MM1K(λ, μ, K)` | stable even with ρ ≥ 1 |
| M/M/s>1/K | `MMsK(λ, μ, K, s)` | K ≥ s required; uses standard formula (K = total capacity, no off-by-one) |
| M/M/1/N | `MM1N(λ, μ, N)` | λ is per-client rate; effective λ_n = (N−n)·λ |
| M/M/s>1/N | `MMsN(λ, μ, N, s)` | same as MM1N but with s servers |
| M/G/1 | `MG1(λ, μ, σ²)` | σ² is variance, not std dev; P-K formula |
| Priority | `PriorityQueue(lambdas, μ, s, preemptive, mus=None, sigma2s=None)` | `lambdas` is a list; class 1 = highest priority; `mus` (per-class rates) only for s=1 non-preemptive; `sigma2s` requires `mus` |

### MMsK formula note
The previous codebase had an `effective_k = k-1 for s>1` bug. It was removed. `prob_idle()`, `prob_n()`, and `avg_clients_queue()` now use `self._k` directly (standard M/M/s/K formula). Two lista tests were updated to reflect the mathematically correct values.

### PriorityQueue general service
When `mus` is provided, uses the generalized P-K formula:
`Wq_k = Σλᵢ(σᵢ²+1/μᵢ²) / [2(1−σ_{k-1})(1−σ_k)]` where `σ_k = Σᵢ₌₁ᵏ λᵢ/μᵢ`.
Stability check: `ρ_total = Σλᵢ/μᵢ` (per-class) or `Σλᵢ/(s·μ)` (equal-μ).

## Tests
74 tests across three classes in `tests/test_models.py`:
- `TestQueueModels` — functional tests validated against apostila answer keys (comments cite source exercise)
- `TestValidation` — every `ValueError` path in model constructors
- `TestAdditionalCoverage` — edge cases and secondary methods

Test sources: apostila teoria examples + lista de exercícios answer keys. When apostila and lista diverge, apostila values take precedence (lista had some expected values computed with the old MMsK off-by-one).
