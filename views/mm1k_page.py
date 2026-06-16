import streamlit as st
from models.mm1k_model import MM1K
from utils.input_helpers import input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/1/K")
    st.info(
        "Fila com **capacidade máxima K** (total de clientes em serviço + na fila), 1 servidor. "
        "Clientes que chegam quando o sistema está cheio são **descartados** (perdidos). "
        "Não exige λ < μ para estabilidade.",
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

    col4, col5 = st.columns(2)

    with col4:
        n = input_integer(
            "n — Número de clientes (opcional)",
            "mm1k_n",
            default=0,
            placeholder="Ex: 3",
            min_value=0,
            help_text="Calcula P(N = n): probabilidade de exatamente n clientes no sistema.",
        )

    st.divider()

    if st.button("Calcular", key="mm1k_btn"):

        try:
            fila = MM1K(lambda_, mi, k)

        except Exception as e:
            st.error(str(e))
            return

        w_minutes = fila.avg_time_system() * 60
        wq_minutes = fila.avg_time_queue() * 60

        st.subheader("Resultados")
        metric_grid([
            ("ρ", fila.rho, "Utilização do servidor (λ/μ, sem considerar perdas)"),
            ("P₀", fila.prob_idle(), "Probabilidade do sistema estar ocioso (vazio)"),
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
