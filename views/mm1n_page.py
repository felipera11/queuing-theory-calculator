import streamlit as st
from models.mm1n_model import MM1N
from utils.input_helpers import input_integer, input_lambda, input_mi, input_n_with_operator
from utils.ui import metric_grid, show_n_prob


def render():
    st.header("Modelo M/M/1 com População Finita (M/M/1/N)")
    st.info(
        "Chegadas Poisson (λ), atendimento exponencial (μ), **1 servidor**, **população finita N**. "
        "A taxa efetiva de chegada diminui conforme mais clientes já estão no sistema. "
        "λ é a taxa individual de cada cliente. "
        "W e Wq são expressos na mesma unidade de tempo de λ e μ.",
        icon="ℹ️",
    )

    col1, col2 = st.columns(2)
    with col1:
        lambda_ = input_lambda("mm1n")
    with col2:
        mi = input_mi("mm1n")

    col3, = st.columns(1)
    with col3:
        N = input_integer(
            "N — Tamanho da população (número total de clientes)",
            "mm1n_N",
            default=10,
            placeholder="Ex: 10",
            min_value=1,
            help_text="Número total de clientes na população. Um cliente já no sistema não pode chegar novamente.",
        )

    n, n_op = input_n_with_operator("mm1n", max_value=int(N))

    st.divider()

    if st.button("Calcular", key="mm1n_btn"):

        try:
            fila = MM1N(lambda_, mi, N)
        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")
        metric_grid([
            ("ρ",  f"{fila.rho:.4g}",               "Taxa de ocupação (Nλ/μ)"),
            ("P₀", f"{fila.prob_idle():.4g}",        "Probabilidade de o sistema estar vazio"),
            ("L",  f"{fila.avg_clients_system():.4g}", "Número médio de clientes no sistema"),
            ("Lq", f"{fila.avg_clients_queue():.4g}", "Número médio de clientes na fila"),
            ("W",  f"{fila.avg_time_system():.4g}",  "Tempo médio gasto no sistema"),
            ("Wq", f"{fila.avg_time_queue():.4g}",   "Tempo médio de espera na fila"),
        ], columns=2)

        show_n_prob(fila, n, n_op)
