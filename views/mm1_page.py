import streamlit as st
from models.mm1_model import MM1
from utils.input_helpers import input_float_value, input_integer, input_lambda, input_mi
from utils.ui import metric_grid


def render():
    st.header("Modelo M/M/1")

    col1, col2 = st.columns(2)

    with col1:
        lambda_ = input_lambda("mm1")

    with col2:
        mi = input_mi("mm1")

    

    col3, col4, col5 = st.columns(3)

    with col3:
        n = input_integer("n (número de clientes, opcional)", "mm1_n", default=0, placeholder="Opcional - Ex: 3", min_value=0)

    with col4:
        t = input_float_value(
            "t (tempo de observação, opcional)",
            "mm1_t",
            default=None,
            placeholder="Opcional - Ex: 15 (minutos)",
        )

    with col5:
        r = input_integer("r (limite de clientes, opcional)", "mm1_r", default=0, placeholder="Opcional - Ex: 2", min_value=0)

    st.divider()

    if st.button("Calcular", key="mm1_btn"):

        if lambda_ <= 0 or mi <= 0:
            st.warning("Informe valores válidos para λ e μ.")
            return

        if lambda_ >= mi:
            st.error("Sistema instável (λ ≥ μ)")
            return

        fila = MM1(lambda_, mi)

        w_minutes = fila.avg_time_system() * 60
        wq_minutes = fila.avg_time_queue() * 60

        st.subheader("Resultados")
        metric_grid([
            ("ρ", fila.rho),
            ("P0", fila.prob_idle()),
            ("L", fila.avg_clients_system()),
            ("Lq", fila.avg_clients_queue()),
            ("W", f"{w_minutes:.4g} minutos"),
            ("Wq", f"{wq_minutes:.4g} minutos"),
        ], columns=2)

        

        if n > 0:
            prob_n = fila.prob_n(n)
            metric_grid([(f"P(N = {n})", prob_n)], columns=1)

        if r > 0:
            prob_r = fila.prob_greater_r(r)
            metric_grid([(f"P(N > {r})", prob_r)], columns=1)

        if t is not None:
            t_hours = t / 60
            prob_sys = fila.prob_wait_system_greater_than(t_hours)
            prob_q = fila.prob_wait_queue_greater_than(t_hours)
            metric_grid([
                ("P(W > t)", prob_sys),
                ("P(Wq > t)", prob_q),
            ], columns=2)