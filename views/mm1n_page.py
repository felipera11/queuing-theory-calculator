import streamlit as st
from models.mm1n_model import MM1N
from utils.input_helpers import input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/1/N")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mm1n")

    with col2:
        mi = input_mi("mm1n")

    col3, = st.columns(1)
    with col3:
        N = input_integer("N (número de clientes)", "mm1n_N", default=1, placeholder="Ex: 10", min_value=1)

    

    col4, col5 = st.columns(2)

    with col4:
        n = input_integer("n (número de clientes, opcional)", "mm1n_n", default=0, placeholder="Opcional - Ex: 3", min_value=0)

    st.divider()

    if st.button("Calcular", key="mm1n_btn"):

        try:
            fila = MM1N(lambda_, mi, N)

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