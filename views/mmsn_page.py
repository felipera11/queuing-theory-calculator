import streamlit as st
from models.mmsn_model import MMsN
from utils.input_helpers import input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/s/N")
    st.info(
        "Fila com **população finita de N clientes** e **s servidores paralelos**. "
        "A taxa efetiva de chegada cai conforme mais clientes estão no sistema. "
        "λ informado é a taxa individual de cada cliente.",
        icon="ℹ️",
    )

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mmsn")

    with col2:
        mi = input_mi("mmsn")

    col3, col4 = st.columns(2)
    with col3:
        N = input_integer(
            "N — Tamanho da população de clientes",
            "mmsn_N",
            default=10,
            placeholder="Ex: 10",
            min_value=1,
            help_text="Número total de clientes na população.",
        )

    with col4:
        s = input_integer(
            "s — Número de servidores paralelos",
            "mmsn_s",
            default=2,
            placeholder="Ex: 2",
            min_value=1,
            help_text="Quantidade de servidores atendendo simultaneamente.",
        )

    col5, col6 = st.columns(2)

    with col5:
        n = input_integer(
            "n — Número de clientes (opcional)",
            "mmsn_n",
            default=0,
            placeholder="Ex: 3",
            min_value=0,
            help_text="Calcula P(N = n): probabilidade de exatamente n clientes no sistema.",
        )

    st.divider()

    if st.button("Calcular", key="mmsn_btn"):

        try:
            fila = MMsN(lambda_, mi, N, s)

        except Exception as e:
            st.error(str(e))
            return

        w_minutes = fila.avg_time_system() * 60
        wq_minutes = fila.avg_time_queue() * 60

        st.subheader("Resultados")
        metric_grid([
            ("ρ", fila.rho, "Utilização por servidor (λ/μ individual)"),
            ("P₀", fila.prob_idle(), "Probabilidade do sistema estar completamente ocioso"),
            ("L", fila.avg_clients_system(), "Número médio de clientes no sistema"),
            ("Lq", fila.avg_clients_queue(), "Número médio de clientes aguardando na fila"),
            ("W", f"{w_minutes:.4g} min", "Tempo médio que um cliente passa no sistema"),
            ("Wq", f"{wq_minutes:.4g} min", "Tempo médio que um cliente aguarda na fila"),
        ], columns=2)

        if n > 0:
            prob_n = fila.prob_n(n)
            metric_grid([(f"P(N = {n})", prob_n, f"Probabilidade de exatamente {n} clientes no sistema")], columns=1)
