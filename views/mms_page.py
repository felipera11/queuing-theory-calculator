import streamlit as st
from models.mms_model import MMS
from utils.input_helpers import input_float_value, input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/s")
    st.info(
        "Fila com chegadas Poisson (λ), serviço exponencial (μ) e **s servidores paralelos** com capacidade ilimitada. "
        "Cada servidor atende à taxa μ; estabilidade requer λ < s·μ.",
        icon="ℹ️",
    )

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mms")

    with col2:
        mi = input_mi("mms")

    col3, = st.columns(1)

    with col3:
        s = input_integer(
            "s — Número de servidores paralelos",
            "mms_s",
            default=2,
            placeholder="Ex: 2",
            min_value=2,
            help_text="Quantidade de servidores atendendo simultaneamente. Mínimo: 2 (use M/M/1 para 1 servidor).",
        )

    col4, col5 = st.columns(2)

    with col4:
        n = input_integer(
            "n — Número de clientes (opcional)",
            "mms_n",
            default=0,
            placeholder="Ex: 3",
            min_value=0,
            help_text="Calcula P(N = n): probabilidade de exatamente n clientes no sistema.",
        )

    with col5:
        t = input_float_value(
            "t — Tempo de observação em minutos (opcional)",
            "mms_t",
            default=None,
            placeholder="Ex: 15",
            help_text="Calcula P(W > t) e P(Wq > t): probabilidade do tempo exceder t minutos.",
        )

    st.divider()

    if st.button("Calcular", key="mms_btn"):

        try:
            fila = MMS(lambda_, mi, s)

            w_minutes = fila.avg_time_system() * 60
            wq_minutes = fila.avg_time_queue() * 60

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")
        metric_grid([
            ("ρ", fila.rho, "Utilização por servidor (λ / (s·μ))"),
            ("P₀", fila.p0, "Probabilidade do sistema estar completamente ocioso"),
            ("L", fila.avg_clients_system(), "Número médio de clientes no sistema"),
            ("Lq", fila.avg_clients_queue(), "Número médio de clientes aguardando na fila"),
            ("W", f"{w_minutes:.4g} min", "Tempo médio que um cliente passa no sistema"),
            ("Wq", f"{wq_minutes:.4g} min", "Tempo médio que um cliente aguarda na fila"),
        ], columns=2)

        if n > 0:
            prob_n = fila.prob_n(n)
            metric_grid([(f"P(N = {n})", prob_n, f"Probabilidade de exatamente {n} clientes no sistema")], columns=1)

        if t is not None:
            t_hours = t / 60
            prob_sys = fila.prob_wait_system_greater_than(t_hours)
            prob_q = fila.prob_wait_queue_greater_than(t_hours)
            metric_grid([
                ("P(W > t)", prob_sys, f"Prob. do tempo no sistema exceder {t} minutos"),
                ("P(Wq > t)", prob_q, f"Prob. do tempo na fila exceder {t} minutos"),
            ], columns=2)
