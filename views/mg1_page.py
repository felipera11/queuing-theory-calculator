import math
import streamlit as st

from models.mg1_model import MG1
from utils.input_helpers import input_float_value, input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/G/1")
    st.info(
        "Chegadas Poisson (λ), **distribuição de serviço geral**, 1 servidor. "
        "Informe a média (1/μ) e a variância σ² do tempo de serviço. "
        "Fórmula de Pollaczek-Khinchine (P-K). "
        "W e Wq são expressos na mesma unidade de tempo de λ e μ.",
        icon="ℹ️",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        lambda_ = input_lambda("mg1")

    with col2:
        mi = input_mi("mg1")

    with col3:
        sigma = input_float_value(
            "σ — Desvio padrão do tempo de serviço (opcional)",
            "mg1_sigma2",
            default=None,
            placeholder="Ex: 0.05",
            help_text=(
                "Desvio padrão da distribuição do tempo de serviço (na mesma unidade de tempo). "
                "Para distribuição exponencial: σ = 1/μ. "
                "Se omitido, usa σ = 0 (serviço determinístico, M/D/1)."
            ),
        )

    st.divider()

    poisson = input_integer(
        "Número de chegadas/atendimentos (x)",
        "mg1_poisson",
        default=0,
        placeholder="Ex: 3",
        min_value=0,
        help_text="Valor inteiro usado no cálculo Poisson.",
    )

    if st.button("Calcular", key="mg1_btn"):

        try:
            sigma_val = sigma if sigma is not None else 0.0
            fila = MG1(lambda_, mi, sigma_val)

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")
        st.caption(f"σ = {fila.sigma:.6g}  |  σ² = {fila.sigma2:.6g}")

        metric_grid([
            ("ρ",  f"{fila.rho:.4g}", "Taxa de ocupação (λ/μ)"),
            ("P₀", f"{fila.p0:.4g}", "Probabilidade de o sistema estar vazio (P₀ = 1 − ρ)"),
            ("Lq", f"{fila.avg_clients_queue():.4g}", "Número médio de clientes na fila"),
            ("Wq", f"{fila.avg_time_queue():.4g}", "Tempo médio de espera na fila"),
            ("L",  f"{fila.avg_clients_system():.4g}", "Número médio de clientes no sistema"),
            ("W",  f"{fila.avg_time_system():.4g}", "Tempo médio gasto no sistema"),
        ], columns=2)

        prob_chegadas = fila.prob_poisson(lambda_, poisson)
        prob_atendimentos = fila.prob_poisson(mi, poisson)

        c7, c8 = st.columns(2)

        with c7:
            with st.container(border=True):
                st.metric(
                    "Prob. chegadas",
                    f"{prob_chegadas:.4g}",
                    help=f"{prob_chegadas * 100:.2f}%",
                )
                st.caption(f"Probabilidade Poisson de {poisson} chegadas (taxa λ = {lambda_})")

        with c8:
            with st.container(border=True):
                st.metric(
                    "Prob. atendimentos",
                    f"{prob_atendimentos:.4g}",
                    help=f"{prob_atendimentos * 100:.2f}%",
                )
                st.caption(f"Probabilidade Poisson de {poisson} atendimentos (taxa μ = {mi})")
