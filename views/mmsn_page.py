import streamlit as st
from models.mmsn_model import MMsN
from utils.input_helpers import input_integer, input_lambda, input_mi, input_n_with_operator
from utils.ui import metric_grid, show_n_prob


def render():
    st.header("Modelo M/M/s>1 com População Finita (M/M/s>1/N)")
    st.info(
        "Chegadas Poisson (λ), atendimento exponencial (μ), **s servidores paralelos**, **população finita N**. "
        "A taxa efetiva de chegada diminui conforme mais clientes já estão no sistema. "
        "λ é a taxa individual de cada cliente. "
        "W e Wq são expressos na mesma unidade de tempo de λ e μ.",
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
            "N — Tamanho da população (número total de clientes)",
            "mmsn_N",
            default=10,
            placeholder="Ex: 10",
            min_value=1,
            help_text="Número total de clientes na população.",
        )
    with col4:
        s = input_integer(
            "s — Número de canais de serviço (servidores paralelos)",
            "mmsn_s",
            default=2,
            placeholder="Ex: 2",
            min_value=1,
            help_text="Quantidade de servidores atendendo simultaneamente.",
        )

    n, n_op = input_n_with_operator("mmsn", max_value=int(N))

    st.divider()

    if st.button("Calcular", key="mmsn_btn"):

        try:
            fila = MMsN(lambda_, mi, N, s)
        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")
        metric_grid([
            ("ρ",  f"{fila.rho:.4g}",               "Taxa de ocupação (Nλ/(s·μ))"),
            ("P₀", f"{fila.prob_idle():.4g}",        "Probabilidade de o sistema estar vazio"),
            ("L",  f"{fila.avg_clients_system():.4g}", "Número médio de clientes no sistema"),
            ("Lq", f"{fila.avg_clients_queue():.4g}", "Número médio de clientes na fila"),
            ("W",  f"{fila.avg_time_system():.4g}",  "Tempo médio gasto no sistema"),
            ("Wq", f"{fila.avg_time_queue():.4g}",   "Tempo médio de espera na fila"),
        ], columns=2)

        show_n_prob(fila, n, n_op)
