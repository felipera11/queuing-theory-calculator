import streamlit as st

from models.mg1_model import MG1
from utils.input_helpers import input_float_value, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/G/1")
    st.info(
        "Fila com chegadas Poisson (λ), **distribuição de serviço geral** e 1 servidor. "
        "A distribuição do tempo de serviço pode ser qualquer uma — basta informar a média (1/μ) e o desvio-padrão σ. "
        "Fórmula de Pollaczek-Khinchine (P-K).",
        icon="ℹ️",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        lambda_ = input_lambda("mg1")

    with col2:
        mi = input_mi("mg1")

    with col3:
        sigma = input_float_value(
            "σ — Desvio-padrão do tempo de serviço (opcional)",
            "mg1_sigma",
            placeholder="Ex: 0.05",
            help_text=(
                "Desvio-padrão da distribuição de serviço (em horas). "
                "O sistema calcula σ² internamente. "
                "Se omitido, usa σ = 0 (serviço determinístico → M/D/1)."
            ),
        )

    st.divider()

    if st.button("Calcular", key="mg1_btn"):

        try:
            sigma_variance = sigma ** 2 if sigma is not None else 0.0
            fila = MG1(lambda_, mi, sigma_variance)

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")
        st.caption(f"σ informado: {sigma}  |  σ² usado no cálculo: {sigma_variance:.6g}")

        w_minutes = fila.avg_time_system() * 60
        wq_minutes = fila.avg_time_queue() * 60

        metric_grid([
            ("ρ", fila.rho, "Utilização do servidor (λ/μ)"),
            ("P₀", fila.p0, "Probabilidade do sistema estar ocioso (P₀ = 1 − ρ)"),
            ("Lq", fila.avg_clients_queue(), "Número médio de clientes aguardando na fila"),
            ("Wq", f"{wq_minutes:.4g} min", "Tempo médio que um cliente aguarda na fila"),
            ("L", fila.avg_clients_system(), "Número médio de clientes no sistema"),
            ("W", f"{w_minutes:.4g} min", "Tempo médio que um cliente passa no sistema"),
        ], columns=2)
