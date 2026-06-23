import streamlit as st
from models.mm1_model import MM1
from utils.input_helpers import input_float_value, input_lambda, input_mi, input_n_with_operator
from utils.ui import metric_grid, show_n_prob


def render():
    st.header("Modelo M/M/1")
    st.info(
        "Chegadas Poisson (λ), atendimento exponencial (μ), **1 servidor**, capacidade ilimitada. "
        "Condição de estabilidade: λ < μ. "
        "W e Wq são expressos na mesma unidade de tempo de λ e μ.",
        icon="ℹ️",
    )

    col1, col2 = st.columns(2)
    with col1:
        lambda_ = input_lambda("mm1")
    with col2:
        mi = input_mi("mm1")

    n, n_op = input_n_with_operator("mm1")

    col_t, _ = st.columns(2)
    with col_t:
        t = input_float_value(
            "t — Tempo de observação (opcional)",
            "mm1_t",
            default=None,
            placeholder="Ex: 15",
            help_text="Calcula P(W > t) e P(Wq > t).",
        )

    st.divider()

    if st.button("Calcular", key="mm1_btn"):

        if lambda_ <= 0 or mi <= 0:
            st.warning("Informe valores válidos para λ e μ.")
            return

        if lambda_ >= mi:
            st.error("Sistema instável: λ deve ser menor que μ.")
            return

        fila = MM1(lambda_, mi)

        st.subheader("Resultados")
        metric_grid([
            ("ρ",  f"{fila.rho:.4g}",               "Taxa de ocupação (λ/μ)"),
            ("P₀", f"{fila.prob_idle():.4g}",        "Probabilidade de o sistema estar vazio"),
            ("L",  f"{fila.avg_clients_system():.4g}", "Número médio de clientes no sistema"),
            ("Lq", f"{fila.avg_clients_queue():.4g}", "Número médio de clientes na fila"),
            ("W",  f"{fila.avg_time_system():.4g}",  "Tempo médio gasto no sistema"),
            ("Wq", f"{fila.avg_time_queue():.4g}",   "Tempo médio de espera na fila"),
        ], columns=2)

        show_n_prob(fila, n, n_op)

        if t is not None:
            prob_sys = fila.prob_wait_system_greater_than(t)
            prob_q = fila.prob_wait_queue_greater_than(t)
            metric_grid([
                ("P(W > t)",  f"{prob_sys:.4g}", f"Probabilidade do tempo no sistema exceder {t}"),
                ("P(Wq > t)", f"{prob_q:.4g}",  f"Probabilidade do tempo na fila exceder {t}"),
            ], columns=2)
