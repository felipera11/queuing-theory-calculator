import streamlit as st
from models.mmsk_model import MMsK
from utils.input_helpers import input_integer, input_lambda, input_mi
from utils.probability_tables import mostrar_tabela_n


def render():
    st.header("Modelo M/M/s>1/K")
    st.info(
        "Chegadas Poisson (λ), atendimento exponencial (μ), **s servidores paralelos**, "
        "capacidade máxima **K** clientes. Clientes que chegam com o sistema cheio são **perdidos**. "
        "Requer K ≥ s. W e Wq são expressos na mesma unidade de tempo de λ e μ.",
        icon="ℹ️",
    )

    col1, col2 = st.columns(2)
    with col1:
        lambda_ = input_lambda("mmsk")
    with col2:
        mi = input_mi("mmsk")

    col3, col4 = st.columns(2)
    with col3:
        k = input_integer(
            "K — Capacidade máxima do sistema",
            "mmsk_k",
            default=5,
            placeholder="Ex: 5",
            min_value=1,
            help_text="Número máximo de clientes no sistema (fila + em atendimento).",
        )
    with col4:
        s = input_integer(
            "s — Número de canais de serviço (servidores paralelos)",
            "mmsk_s",
            default=2,
            placeholder="Ex: 2",
            min_value=1,
            help_text="Quantidade de servidores atendendo simultaneamente. Deve ser ≤ K.",
        )

    st.subheader("Parâmetros opcionais")

    col5, col6, col7 = st.columns(3)

    with col5:
        n = input_integer(
            "n",
            "mmsk_n",
            default=0,
            placeholder="Ex: 3",
            min_value=0,
            help_text="Calcula probabilidades P(N=n), P(N≤n) e P(N≥n).",
        )

    with col6:
        tipo_n = st.selectbox(
            "Tipo de probabilidade",
            ["P(N=n)", "P(N≤n)", "P(N≥n)"],
            key="mmsk_tipo_n",
        )

    with col7:
        poisson = input_integer(
            "Número de chegadas/atendimentos (x)",
            "mmsk_poisson",
            default=0,
            placeholder="Ex: 3",
            min_value=0,
            help_text="Valor inteiro usado no cálculo Poisson.",
        )

    st.divider()

    if st.button("Calcular", key="mmsk_btn"):

        try:
            fila = MMsK(lambda_, mi, k, s)
        except Exception as e:
            st.error(str(e))
            return

        st.subheader("Resultados principais")

        c1, c2, c3 = st.columns(3)

        with c1:
            with st.container(border=True):
                st.metric("Taxa de ocupação (ρ)", f"{fila.rho:.4g}")

        with c2:
            with st.container(border=True):
                st.metric(
                    "Prob. do sistema ocioso (P0)",
                    f"{fila.prob_idle():.4g}",
                    help=f"{fila.prob_idle() * 100:.2f}%",
                )
                st.caption("Probabilidade de nenhum cliente estar no sistema")

        with c3:
            with st.container(border=True):
                st.metric("Número médio no sistema (L)", f"{fila.avg_clients_system():.4g}")
                st.caption("Número médio de clientes no sistema (fila + em atendimento)")

        c4, c5, c6 = st.columns(3)

        with c4:
            with st.container(border=True):
                st.metric("Número médio na fila (Lq)", f"{fila.avg_clients_queue():.4g}")
                st.caption("Número médio de clientes aguardando atendimento na fila")

        with c5:
            with st.container(border=True):
                st.metric("Tempo médio no sistema (W)", f"{fila.avg_time_system():.4g}")
                st.caption("Tempo médio que um cliente passa no sistema (fila + atendimento)")

        with c6:
            with st.container(border=True):
                st.metric("Tempo médio na fila (Wq)", f"{fila.avg_time_queue():.4g}")
                st.caption("Tempo médio que um cliente espera na fila antes de ser atendido")

        with st.container(border=True):
            st.metric(
                f"P(K) — Prob. de bloqueio (N = {k})",
                f"{fila.prob_n(k):.4g}",
                help=f"{fila.prob_n(k) * 100:.2f}%",
            )
            st.caption(f"Probabilidade de o sistema estar cheio (K = {k}): cliente que chega é perdido")

        st.subheader("Resultados condicionais")

        c7, c8 = st.columns(2)

        if tipo_n == "P(N=n)":
            resultado_n = fila.prob_n(n)
            desc_n = f"Probabilidade de haver exatamente {n} clientes no sistema"
        elif tipo_n == "P(N≤n)":
            resultado_n = fila.prob_less_equal_n(n)
            desc_n = f"Probabilidade de haver no máximo {n} clientes no sistema"
        else:
            resultado_n = fila.prob_greater_equal_n(n)
            desc_n = f"Probabilidade de haver pelo menos {n} clientes no sistema"

        with c7:
            with st.container(border=True):
                st.metric(tipo_n, f"{resultado_n:.4g}", help=f"{resultado_n * 100:.2f}%")
                st.caption(desc_n)

        prob_chegadas = fila.prob_poisson(lambda_, poisson)
        prob_atendimentos = fila.prob_poisson(mi, poisson)

        with c8:
            with st.container(border=True):
                st.metric("Prob. chegadas", f"{prob_chegadas:.4g}", help=f"{prob_chegadas * 100:.2f}%")
                st.caption(f"Probabilidade Poisson de {poisson} chegadas (taxa λ = {lambda_})")

        c9, _ = st.columns(2)

        with c9:
            with st.container(border=True):
                st.metric("Prob. atendimentos", f"{prob_atendimentos:.4g}", help=f"{prob_atendimentos * 100:.2f}%")
                st.caption(f"Probabilidade Poisson de {poisson} atendimentos (taxa μ = {mi})")

        mostrar_tabela_n(fila)
