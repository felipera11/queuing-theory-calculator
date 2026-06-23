import streamlit as st
from models.mmsk_model import MMsK
from utils.input_helpers import input_integer, input_lambda, input_mi, input_n_with_operator
from utils.ui import metric_grid, show_n_prob


def render():
    st.header("Modelo M/M/s>1/K")
    st.info(
        "Chegadas Poisson (λ), atendimento exponencial (μ), **s servidores paralelos**, "
        "capacidade máxima **K** clientes. Clientes que chegam com o sistema cheio são **perdidos**. "
        "Requer K ≥ s. W e Wq são expressos na mesma unidade de tempo de λ e μ.",
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
            "s — Número de canais de serviço (servidores paralelos)",
            "mmsk_s",
            default=2,
            placeholder="Ex: 2",
            min_value=1,
            help_text="Quantidade de servidores atendendo simultaneamente. Deve ser ≤ K.",
        )

    n, n_op = input_n_with_operator("mmsk", max_value=int(k))

    st.divider()

    if st.button("Calcular", key="mmsk_btn"):

        try:
            fila = MMsK(lambda_, mi, k, s)
        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")
        metric_grid([
            ("ρ",  f"{fila.rho:.4g}",               "Taxa de ocupação por servidor (λ/(s·μ))"),
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
