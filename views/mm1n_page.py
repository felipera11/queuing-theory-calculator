import streamlit as st
from models.mm1n_model import MM1N
from utils.input_helpers import input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/1/N")
    st.info(
        "Fila com **população finita de N clientes**, 1 servidor. "
        "A taxa efetiva de chegada diminui conforme mais clientes estão no sistema "
        "(clientes que já estão na fila não podem chegar novamente). "
        "λ informado é a taxa individual de cada cliente.",
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
            "N — Tamanho da população de clientes",
            "mm1n_N",
            default=10,
            placeholder="Ex: 10",
            min_value=1,
            help_text="Número total de clientes na população. Nenhum novo cliente pode chegar se todos já estiverem no sistema.",
        )

    col4, col5 = st.columns(2)

    with col4:
        n = input_integer(
            "n — Número de clientes (opcional)",
            "mm1n_n",
            default=0,
            placeholder="Ex: 3",
            min_value=0,
            help_text="Calcula P(N = n): probabilidade de exatamente n clientes no sistema.",
        )

    st.divider()

    if st.button("Calcular", key="mm1n_btn"):

        try:
            fila = MM1N(lambda_, mi, N)

        except Exception as e:
            st.error(str(e))
            return

        w_minutes = fila.avg_time_system() * 60
        wq_minutes = fila.avg_time_queue() * 60

        st.subheader("Resultados")
        metric_grid([
            ("ρ", fila.rho, "Utilização do servidor (λ/μ individual)"),
            ("P₀", fila.prob_idle(), "Probabilidade do sistema estar ocioso (sem clientes)"),
            ("L", fila.avg_clients_system(), "Número médio de clientes no sistema"),
            ("Lq", fila.avg_clients_queue(), "Número médio de clientes aguardando na fila"),
            ("W", f"{w_minutes:.4g} min", "Tempo médio que um cliente passa no sistema"),
            ("Wq", f"{wq_minutes:.4g} min", "Tempo médio que um cliente aguarda na fila"),
        ], columns=2)

        if n > 0:
            prob_n = fila.prob_n(n)
            metric_grid([(f"P(N = {n})", prob_n, f"Probabilidade de exatamente {n} clientes no sistema")], columns=1)
