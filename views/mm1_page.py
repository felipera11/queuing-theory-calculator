import streamlit as st
from models.mm1_model import MM1
from utils.input_helpers import input_float_value, input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/1")
    st.info(
        "Fila com chegadas Poisson (λ), serviço exponencial (μ), **1 servidor** e capacidade ilimitada. "
        "O sistema é estável somente quando λ < μ.",
        icon="ℹ️",
    )

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mm1")

    with col2:
        mi = input_mi("mm1")

    col3, col4, col5 = st.columns(3)

    with col3:
        n = input_integer(
            "n — Número de clientes (opcional)",
            "mm1_n",
            default=0,
            placeholder="Ex: 3",
            min_value=0,
            help_text="Calcula P(N = n): probabilidade de exatamente n clientes no sistema.",
        )

    with col4:
        t = input_float_value(
            "t — Tempo de observação em minutos (opcional)",
            "mm1_t",
            default=None,
            placeholder="Ex: 15",
            help_text="Calcula P(W > t) e P(Wq > t): probabilidade do tempo exceder t minutos.",
        )

    with col5:
        r = input_integer(
            "r — Limite de clientes (opcional)",
            "mm1_r",
            default=0,
            placeholder="Ex: 2",
            min_value=0,
            help_text="Calcula P(N > r): probabilidade de mais de r clientes no sistema.",
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

        w_minutes = fila.avg_time_system() * 60
        wq_minutes = fila.avg_time_queue() * 60

        st.subheader("Resultados")
        metric_grid([
            ("ρ", fila.rho, "Utilização do servidor (fração do tempo ocupado)"),
            ("P₀", fila.prob_idle(), "Probabilidade do sistema estar ocioso (vazio)"),
            ("L", fila.avg_clients_system(), "Número médio de clientes no sistema"),
            ("Lq", fila.avg_clients_queue(), "Número médio de clientes aguardando na fila"),
            ("W", f"{w_minutes:.4g} min", "Tempo médio que um cliente passa no sistema"),
            ("Wq", f"{wq_minutes:.4g} min", "Tempo médio que um cliente aguarda na fila"),
        ], columns=2)

        if n > 0:
            prob_n = fila.prob_n(n)
            metric_grid([(f"P(N = {n})", prob_n, f"Probabilidade de exatamente {n} clientes no sistema")], columns=1)

        if r > 0:
            prob_r = fila.prob_greater_r(r)
            metric_grid([(f"P(N > {r})", prob_r, f"Probabilidade de mais de {r} clientes no sistema")], columns=1)

        if t is not None:
            t_hours = t / 60
            prob_sys = fila.prob_wait_system_greater_than(t_hours)
            prob_q = fila.prob_wait_queue_greater_than(t_hours)
            metric_grid([
                ("P(W > t)", prob_sys, f"Prob. do tempo no sistema exceder {t} minutos"),
                ("P(Wq > t)", prob_q, f"Prob. do tempo na fila exceder {t} minutos"),
            ], columns=2)
