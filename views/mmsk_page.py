import streamlit as st
from models.mmsk_model import MMsK
from utils.input_helpers import input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/s/K")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mmsk")

    with col2:
        mi = input_mi("mmsk")

    col3, col4 = st.columns(2)
    with col3:
        k = input_integer("K (capacidade máxima)", "mmsk_k", default=1, placeholder="Ex: 5", min_value=1)

    with col4:
        s = input_integer("s (número de servidores)", "mmsk_s", default=1, placeholder="Ex: 2", min_value=1)

    

    col5, col6 = st.columns(2)

    with col5:
        n = input_integer("n (número de clientes, opcional)", "mmsk_n", default=0, placeholder="Opcional - Ex: 3", min_value=0, max_value=int(k))

    st.divider()

    if st.button("Calcular", key="mmsk_btn"):

        try:
            fila = MMsK(lambda_, mi, k, s)

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