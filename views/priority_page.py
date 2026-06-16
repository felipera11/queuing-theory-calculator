import streamlit as st

from models.priority_model import PriorityQueue
from utils.input_helpers import input_integer
from utils.ui import metric_grid


def render():
    st.header("Modelo com Prioridades")
    st.info(
        "Fila com **múltiplas classes de clientes** com prioridades distintas. "
        "Classe 1 tem a maior prioridade. "
        "**Com interrupção (preemptivo):** um cliente de alta prioridade pode interromper o atendimento em curso. "
        "**Sem interrupção (não-preemptivo):** aguarda o atendimento atual concluir.",
        icon="ℹ️",
    )

    mode = st.radio(
        "Tipo de prioridade",
        ["Com Interrupção (Preemptivo)", "Sem Interrupção (Não-preemptivo)"],
        horizontal=True,
        key="priority_mode",
    )

    preemptive = mode.startswith("Com Interrupção")

    st.divider()

    col_s, col_mu = st.columns(2)

    with col_s:
        s = input_integer(
            "s — Número de servidores",
            "priority_s",
            default=1,
            placeholder="Ex: 1",
            min_value=1,
            help_text="Quantidade de servidores compartilhados por todas as classes.",
        )

    with col_mu:
        mu_str = st.text_input(
            "μ — Taxa de serviço (clientes/hora)",
            value="40",
            key="priority_mu",
            help="Taxa de serviço comum a todas as classes (clientes/hora por servidor).",
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
        help_text="Quantas classes de clientes com prioridades diferentes existem no sistema.",
    )

    st.caption("Classe 1 = maior prioridade  |  Informe a taxa de chegada (λ) de cada classe")

    lambdas = []
    cols = st.columns(min(int(n_classes), 5))

    for k in range(int(n_classes)):
        col = cols[k % len(cols)]
        with col:
            lam_str = st.text_input(
                f"λ{k + 1} — Chegadas da Classe {k + 1} (clientes/hora)",
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

        mode_label = "Com interrupção (preemptivo)" if preemptive else "Sem interrupção (não-preemptivo)"
        st.subheader(f"Resultados — {mode_label}")

        metric_grid([("ρ total", fila.rho_total, "Utilização total do(s) servidor(es) por todas as classes")], columns=1)
        st.divider()

        for res in fila.results():
            k = res["classe"]
            st.markdown(f"**Classe {k}** — λ{k} = {res['lambda']} clientes/hora")
            metric_grid([
                ("W", f"{res['W']:.4f} h", "Tempo médio no sistema (horas)"),
                ("Wq", f"{res['Wq']:.4f} h", "Tempo médio aguardando na fila (horas)"),
                ("L", f"{res['L']:.4f}", "Número médio de clientes no sistema"),
                ("Lq", f"{res['Lq']:.4f}", "Número médio de clientes aguardando na fila"),
            ], columns=2)
            if k < len(fila.results()):
                st.divider()
