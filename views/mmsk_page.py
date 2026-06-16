import streamlit as st
from models.mmsk_model import MMsK
from utils.input_helpers import input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/s/K")
    st.info(
        "Fila com capacidade máxima K e **s servidores paralelos**. "
        "Clientes que chegam quando o sistema está cheio (N = K) são **descartados**. "
        "Requer K ≥ s.",
        icon="ℹ️",
    )

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mmsk")

    with col2:
        mi = input_mi("mmsk")

    col3, col4 = st.columns(2)
    with col3:
        k = input_integer(
            "K — Capacidade máxima do sistema",
            "mmsk_k",
            default=5,
            placeholder="Ex: 5",
            min_value=1,
            help_text="Número máximo de clientes no sistema (fila + em atendimento).",
        )

    with col4:
        s = input_integer(
            "s — Número de servidores paralelos",
            "mmsk_s",
            default=2,
            placeholder="Ex: 2",
            min_value=1,
            help_text="Quantidade de servidores atendendo simultaneamente. Deve ser ≤ K.",
        )

    col5, col6 = st.columns(2)

    with col5:
        n = input_integer(
            "n — Número de clientes (opcional)",
            "mmsk_n",
            default=0,
            placeholder="Ex: 3",
            min_value=0,
            max_value=int(k),
            help_text="Calcula P(N = n): probabilidade de exatamente n clientes no sistema.",
        )

    st.divider()

    if st.button("Calcular", key="mmsk_btn"):

        try:
            fila = MMsK(lambda_, mi, k, s)

        except Exception as e:
            st.error(str(e))
            return

        w_minutes = fila.avg_time_system() * 60
        wq_minutes = fila.avg_time_queue() * 60

        st.subheader("Resultados")
        metric_grid([
            ("ρ", fila.rho, "Utilização por servidor (λ / (s·μ))"),
            ("P₀", fila.prob_idle(), "Probabilidade do sistema estar completamente ocioso"),
            ("L", fila.avg_clients_system(), "Número médio de clientes no sistema"),
            ("Lq", fila.avg_clients_queue(), "Número médio de clientes aguardando na fila"),
            ("W", f"{w_minutes:.4g} min", "Tempo médio que um cliente passa no sistema"),
            ("Wq", f"{wq_minutes:.4g} min", "Tempo médio que um cliente aguarda na fila"),
        ], columns=2)

        metric_grid([
            (f"PK (P{k})", fila.prob_n(k), f"Probabilidade de bloqueio: sistema cheio (N = {k}), clientes são perdidos"),
        ], columns=1)

        if n > 0:
            prob_n = fila.prob_n(n)
            metric_grid([(f"P(N = {n})", prob_n, f"Probabilidade de exatamente {n} clientes no sistema")], columns=1)
