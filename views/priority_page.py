import streamlit as st

from models.priority_model import PriorityQueue
from utils.input_helpers import input_integer
from utils.ui import metric_grid


def render():
    st.header("Modelo com Prioridades")

    mode = st.radio(
        "Tipo de prioridade",
        ["Com Interrupção", "Sem Interrupção"],
        horizontal=True,
        key="priority_mode",
    )

    preemptive = mode == "Com Interrupção"

    st.divider()

    col_s, col_mu = st.columns(2)

    with col_s:
        s = input_integer("s (número de servidores)", "priority_s", default=1, placeholder="Ex: 2", min_value=1)

    with col_mu:
        mu_str = st.text_input(
            "μ (taxa de serviço)",
            value="40",
            key="priority_mu",
        )
        try:
            mu = float(mu_str.replace(",", ".")) if mu_str else 0.0
        except ValueError:
            st.error("Digite um número válido para μ")
            mu = 0.0

    st.divider()

    n_classes = input_integer(
        "Número de classes de prioridade",
        "priority_n_classes",
        default=2,
        placeholder="Ex: 2",
        min_value=2,
        max_value=10,
    )

    st.caption("Classe 1 = maior prioridade")

    lambdas = []
    cols = st.columns(min(int(n_classes), 5))

    for k in range(int(n_classes)):
        col = cols[k % len(cols)]
        with col:
            lam_str = st.text_input(
                f"λ{k + 1} (taxa de chegada da classe {k + 1})",
                value="10",
                key=f"priority_lambda_{k}",
            )
            try:
                lam = float(lam_str.replace(",", ".")) if lam_str else 0.0
            except ValueError:
                st.error(f"λ{k + 1} inválido")
                lam = 0.0
            lambdas.append(lam)

    st.divider()

    if st.button("Calcular", key="priority_btn"):
        try:
            fila = PriorityQueue(
                lambdas=lambdas,
                mu=mu,
                s=int(s),
                preemptive=preemptive,
            )
        except Exception as e:
            st.error(str(e))
            return

        mode_label = "Com interrupção" if preemptive else "Sem interrupção"
        st.subheader(f"Resultados — {mode_label}")

        metric_grid([("ρ total", fila.rho_total)], columns=1)
        st.divider()

        for res in fila.results():
            k = res["classe"]
            st.markdown(f"**Classe {k}** (λ{k} = {res['lambda']})")
            metric_grid([
                ("W", f"{res['W']:.4f}"),
                ("Wq", f"{res['Wq']:.4f}"),
                ("L", f"{res['L']:.4f}"),
                ("Lq", f"{res['Lq']:.4f}"),
            ], columns=2)