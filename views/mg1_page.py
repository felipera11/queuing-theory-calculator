import streamlit as st

from models.mg1_model import MG1
from utils.input_helpers import input_float_value, input_lambda
from utils.input_helpers import input_mi
from utils.ui import metric_grid


def render():

    st.header("Modelo M/G/1")
    st.caption("Informe σ (desvio-padrão). O sistema converte para σ² antes de calcular.")

    col1, col2, col3 = st.columns(3)

    with col1:
        lambda_ = input_lambda("mg1")

    with col2:
        mi = input_mi("mg1")

    with col3:
        sigma = input_float_value(
            "σ (desvio-padrão, opcional)",
            "mg1_sigma",
            placeholder="Opcional - Ex: 4",
            
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

        st.caption(f"σ informado: {sigma} | σ² usado no cálculo: {sigma_variance}")
        metric_grid([
            ("ρ", fila.rho),
            ("P0", fila.p0),
            ("Lq", fila.avg_clients_queue()),
            ("Wq", f"{fila.avg_time_queue():.4f} horas"),
            ("L", fila.avg_clients_system()),
            ("W", f"{fila.avg_time_system():.4f} horas"),
        ], columns=2)