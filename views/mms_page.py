import streamlit as st
from models.mms_model import MMS
from utils.input_helpers import input_float_value, input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/s")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mms")

    with col2:
        mi = input_mi("mms")

    col3, = st.columns(1)

    with col3:
        s = input_integer("s (número de servidores)", "mms_s", default=2, placeholder="Ex: 2", min_value=2)

    

    col4, col5 = st.columns(2)

    with col4:
        n = input_integer("n (número de clientes, opcional)", "mms_n", default=0, placeholder="Opcional - Ex: 3", min_value=0)

    with col5:
        t = input_float_value(
            "t (tempo de observação, opcional)",
            "mms_t",
            default=None,
            placeholder="Opcional - Ex: 15 (minutos)",
        )

    st.divider()

    if st.button("Calcular", key="mms_btn"):

        try:
            fila = MMS(lambda_, mi, s)

            w_minutes = fila.avg_time_system() * 60
            wq_minutes = fila.avg_time_queue() * 60

        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados")
        metric_grid([
            ("ρ", fila.rho),
            ("P0", fila.p0),
            ("L", fila.avg_clients_system()),
            ("Lq", fila.avg_clients_queue()),
            ("W", f"{w_minutes:.4g} minutos"),
            ("Wq", f"{wq_minutes:.4g} minutos"),
        ], columns=2)

        if n > 0:
            prob_n = fila.prob_n(n)
            metric_grid([(f"P(N = {n})", prob_n)], columns=1)

        if t is not None:
            t_hours = t / 60
            prob_sys = fila.prob_wait_system_greater_than(t_hours)
            prob_q = fila.prob_wait_queue_greater_than(t_hours)
            metric_grid([
                ("P(W > t)", prob_sys),
                ("P(Wq > t)", prob_q),
            ], columns=2)