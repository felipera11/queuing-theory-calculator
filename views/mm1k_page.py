import streamlit as st
from models.mm1k_model import MM1K
from utils.input_helpers import input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/1/K")

    col1, col2, col3 = st.columns(3)

    with col1:
        lambda_ = input_lambda("mm1k")

    with col2:
        mi = input_mi("mm1k")

    with col3:
        k = input_integer("K (capacidade máxima)", "mm1k_k", default=1, placeholder="Ex: 5", min_value=1)

    

    col4, col5 = st.columns(2)

    with col4:
        n = input_integer("n (número de clientes, opcional)", "mm1k_n", default=0, placeholder="Opcional - Ex: 3", min_value=0)

    st.divider()

    if st.button("Calcular", key="mm1k_btn"):

        try:
            fila = MM1K(lambda_, mi, k)

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")
        metric_grid([
            ("ρ", fila.rho),
            ("P0", fila.prob_idle()),
            ("L", fila.avg_clients_system()),
            ("Lq", fila.avg_clients_queue()),
            ("W", fila.avg_time_system()),
            ("Wq", fila.avg_time_queue()),
        ], columns=2)

       

        if n > 0:
            prob_n = fila.prob_n(n)
            metric_grid([(f"P(N = {n})", prob_n)], columns=1)