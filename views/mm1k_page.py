import streamlit as st
from models.mm1k_model import MM1K
from utils.input_helpers import input_integer, input_lambda, input_mi, input_n_with_operator
from utils.ui import metric_grid, show_n_prob


def render():
    st.header("Modelo M/M/1/K")
    st.info(
        "Chegadas Poisson (λ), atendimento exponencial (μ), **1 servidor**, capacidade máxima **K** clientes "
        "(fila + em atendimento). Clientes que chegam com o sistema cheio são **perdidos** (bloqueados). "
        "W e Wq são expressos na mesma unidade de tempo de λ e μ.",
        icon="ℹ️",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        lambda_ = input_lambda("mm1k")
    with col2:
        mi = input_mi("mm1k")
    with col3:
        k = input_integer(
            "K — Capacidade máxima do sistema",
            "mm1k_k",
            default=5,
            placeholder="Ex: 5",
            min_value=1,
            help_text="Número máximo de clientes no sistema (fila + em atendimento). Chegadas extras são rejeitadas.",
        )

    n, n_op = input_n_with_operator("mm1k", max_value=int(k))

    st.divider()

    if st.button("Calcular", key="mm1k_btn"):

        try:
            fila = MM1K(lambda_, mi, k)
        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")
        metric_grid([
            ("ρ",  f"{fila.rho:.4g}",               "Taxa de ocupação (λ/μ, sem considerar perdas)"),
            ("P₀", f"{fila.prob_idle():.4g}",        "Probabilidade de o sistema estar vazio"),
            ("L",  f"{fila.avg_clients_system():.4g}", "Número médio de clientes no sistema"),
            ("Lq", f"{fila.avg_clients_queue():.4g}", "Número médio de clientes na fila"),
            ("W",  f"{fila.avg_time_system():.4g}",  "Tempo médio gasto no sistema"),
            ("Wq", f"{fila.avg_time_queue():.4g}",   "Tempo médio de espera na fila"),
        ], columns=2)

        metric_grid([
            (f"P{k}", f"{fila.prob_n(k):.4g}", f"Probabilidade de bloqueio: sistema cheio (N = {k})"),
        ], columns=1)

        show_n_prob(fila, n, n_op)
