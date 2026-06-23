import streamlit as st

from models.mg1_model import MG1
from utils.input_helpers import input_float_value, input_lambda, input_mi
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
        sigma2 = input_float_value(
            "σ² — Variância do tempo de serviço (opcional)",
            "mg1_sigma2",
            default=None,
            placeholder="Ex: 0.0025",
            help_text=(
                "Variância da distribuição do tempo de serviço (na mesma unidade de tempo). "
                "Para distribuição exponencial: σ² = 1/μ². "
                "Se omitido, usa σ² = 0 (serviço determinístico, M/D/1)."
            ),
        )

    st.divider()

    if st.button("Calcular", key="mg1_btn"):

        try:
            sigma2_val = sigma2 if sigma2 is not None else 0.0
            fila = MG1(lambda_, mi, sigma2_val)

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")
        st.caption(f"σ² usado no cálculo: {sigma2_val:.6g}")

        metric_grid([
            ("ρ",  f"{fila.rho:.4g}", "Taxa de ocupação (λ/μ)"),
            ("P₀", f"{fila.p0:.4g}", "Probabilidade de o sistema estar vazio (P₀ = 1 − ρ)"),
            ("Lq", f"{fila.avg_clients_queue():.4g}", "Número médio de clientes na fila"),
            ("Wq", f"{fila.avg_time_queue():.4g}", "Tempo médio de espera na fila"),
            ("L",  f"{fila.avg_clients_system():.4g}", "Número médio de clientes no sistema"),
            ("W",  f"{fila.avg_time_system():.4g}", "Tempo médio gasto no sistema"),
        ], columns=2)
