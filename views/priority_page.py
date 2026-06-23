import streamlit as st

from models.priority_model import PriorityQueue
from utils.input_helpers import _parse_numeric_expression


def _parse_rate(value_str, label):
    try:
        v = _parse_numeric_expression(value_str.replace(",", ".").strip()) if value_str else None
        return float(v) if v is not None else 0.0
    except (ValueError, TypeError):
        st.error(f"Valor inválido para {label}")
        return 0.0


def render():
    st.markdown("""
        <style>
        [data-testid="stMetric"] {
            text-align: center;
        }
        [data-testid="stMetricLabel"] {
            display: flex;
            justify-content: center;
        }
        [data-testid="stMetricValue"] {
            display: flex;
            justify-content: center;
        }
        </style>
        """, unsafe_allow_html=True)

    st.header("Modelo com Prioridades")
    st.info(
        "Fila com **múltiplas classes de clientes** com prioridades distintas. "
        "Classe 1 tem a maior prioridade. "
        "**Com interrupção (preemptivo):** cliente de alta prioridade interrompe o atendimento em curso. "
        "**Sem interrupção (não-preemptivo):** aguarda o atendimento atual concluir. "
        "W e Wq são expressos na mesma unidade de tempo de λ e μ.",
        icon="ℹ️",
    )

    preemptive = st.toggle(
        "Com interrupção (preemptivo)",
        value=False,
        help="Ligado = com interrupção | Desligado = sem interrupção",
        key="priority_mode",
    )

    st.divider()

    col_s, col_mu = st.columns(2)

    with col_s:
        s_str = st.text_input(
            "s — Número de servidores",
            value="1",
            key="priority_s",
            help="Quantidade de servidores compartilhados por todas as classes.",
        )
        try:
            s = int(float(s_str)) if s_str else 1
        except ValueError:
            st.error("Digite um número inteiro válido para s")
            s = 1

    with col_mu:
        mu_str = st.text_input(
            "μ — Taxa de atendimento (clientes/unidade de tempo)",
            value="40",
            key="priority_mu",
            help="Taxa de atendimento comum a todas as classes (por servidor). Aceita frações: ex. 1/3.",
        )
        mu = _parse_rate(mu_str, "μ")

    st.divider()

    n_classes_str = st.text_input(
        "Número de classes de prioridade",
        value="2",
        key="priority_n_classes",
        help="Quantas classes de clientes com prioridades distintas existem no sistema.",
    )
    try:
        n_classes = max(2, int(float(n_classes_str))) if n_classes_str else 2
    except ValueError:
        st.error("Digite um número inteiro válido para o número de classes")
        n_classes = 2

    st.caption("Classe 1 = maior prioridade")

    lambdas = []
    cols = st.columns(min(n_classes, 5))

    for k in range(n_classes):
        col = cols[k % len(cols)]
        with col:
            lam_str = st.text_input(
                f"λ{k + 1} — Chegadas Classe {k + 1}",
                value="10",
                key=f"priority_lambda_{k}",
            )
            lambdas.append(_parse_rate(lam_str, f"λ{k + 1}"))

    st.divider()

    if st.button("Calcular", key="priority_btn"):
        try:
            fila = PriorityQueue(
                lambdas=lambdas,
                mu=mu,
                s=s,
                preemptive=preemptive,
            )
        except Exception as e:
            st.error(str(e))
            return

        mode_label = "Com interrupção (preemptivo)" if preemptive else "Sem interrupção (não-preemptivo)"
        st.subheader(f"Resultados — {mode_label}")

        with st.container(border=True):
            st.metric("Taxa de ocupação total (ρ)", f"{fila.rho_total:.4g}")
            st.caption("Fração do tempo em que os servidores estão ocupados (λ_total / (s·μ))")

        resultados = fila.results()

        for res in resultados:
            st.divider()
            k = res["classe"]
            st.markdown(f"**Classe {k}** — λ{k} = {res['lambda']}  |  μ = {mu}")

            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    st.metric("Tempo médio no sistema (W)", f"{res['W']:.4f}")
                    st.caption("Tempo médio que um cliente da classe passa no sistema (fila + atendimento)")

            with col2:
                with st.container(border=True):
                    st.metric("Tempo médio na fila (Wq)", f"{res['Wq']:.4f}")
                    st.caption("Tempo médio que um cliente da classe espera na fila antes de ser atendido")

            col3, col4 = st.columns(2)

            with col3:
                with st.container(border=True):
                    st.metric("Número médio no sistema (L)", f"{res['L']:.4f}")
                    st.caption("Número médio de clientes da classe no sistema (fila + em atendimento)")

            with col4:
                with st.container(border=True):
                    st.metric("Número médio na fila (Lq)", f"{res['Lq']:.4f}")
                    st.caption("Número médio de clientes da classe aguardando na fila")


def render():
    st.markdown("""
        <style>
        [data-testid="stMetric"] {
            text-align: center;
        }
        [data-testid="stMetricLabel"] {
            display: flex;
            justify-content: center;
        }
        [data-testid="stMetricValue"] {
            display: flex;
            justify-content: center;
        }
        </style>
        """, unsafe_allow_html=True)

    st.header("Modelo com Prioridades")
    st.info(
        "Fila com **múltiplas classes de clientes** com prioridades distintas. "
        "Classe 1 tem a maior prioridade. "
        "**Com interrupção (preemptivo):** cliente de alta prioridade interrompe o atendimento em curso. "
        "**Sem interrupção (não-preemptivo):** aguarda o atendimento atual concluir. "
        "W e Wq são expressos na mesma unidade de tempo de λ e μ.",
        icon="ℹ️",
    )

    preemptive = st.toggle(
        "Com interrupção (preemptivo)",
        value=False,
        help="Ligado = com interrupção | Desligado = sem interrupção",
        key="priority_mode",
    )

    st.divider()

    col_s, col_mu = st.columns(2)

    with col_s:
        s = st.text_input(
            "s — Número de canais de serviço (servidores)",
            value="1",
            key="priority_s",
            help="Quantidade de servidores compartilhados por todas as classes.",
        )

    with col_mu:
        mu_str = st.text_input(
            "μ — Taxa de atendimento (clientes/unidade de tempo)",
            value="3",
            key="priority_mu",
            help="Taxa de atendimento comum a todas as classes (por servidor). Aceita frações: ex. 1/3.",
        )
        mu = _parse_rate(mu_str, "μ")

    use_per_class_mu = st.checkbox(
        "μ diferente por classe (e opcionalmente σ² por classe)",
        value=False,
        key="priority_per_class",
        help="Ativa taxas de atendimento individuais por classe (apenas para s=1 sem interrupção). "
             "Permite também informar a variância σ² do tempo de serviço por classe.",
    )

    if use_per_class_mu:
        use_sigma2 = st.checkbox(
            "Informar σ² (variância) por classe",
            value=False,
            key="priority_use_sigma2",
            help="Se marcado, informe a variância do tempo de serviço de cada classe. "
                 "Caso contrário, assume distribuição exponencial (σ²ᵢ = 1/μᵢ²).",
        )
    else:
        use_sigma2 = False

    st.divider()

    n_classes = st.text_input(
        "Número de classes de prioridade",
        value="2",
        key="priority_n_classes",
        help="Quantas classes de clientes com prioridades distintas existem no sistema.",
    )
        

    st.caption("Classe 1 = maior prioridade")

    lambdas = []
    mus_per_class = []
    sigma2s_per_class = []

    cols = st.columns(min(int(n_classes), 5))

    for k in range(int(n_classes)):
        col = cols[k % len(cols)]
        with col:
            lam_str = st.text_input(
                f"λ{k + 1} — Chegadas Classe {k + 1}",
                value="10",
                key=f"priority_lambda_{k}",
            )
            lambdas.append(_parse_rate(lam_str, f"λ{k+1}"))

            if use_per_class_mu:
                mu_k_str = st.text_input(
                    f"μ{k + 1} — Atendimento Classe {k + 1}",
                    value=mu_str or "3",
                    key=f"priority_mu_{k}",
                )
                mus_per_class.append(_parse_rate(mu_k_str, f"μ{k+1}"))

                if use_sigma2:
                    s2_str = st.text_input(
                        f"σ²{k + 1} — Variância serviço Classe {k + 1}",
                        value="0",
                        key=f"priority_sigma2_{k}",
                    )
                    sigma2s_per_class.append(_parse_rate(s2_str, f"σ²{k+1}"))

    st.divider()

    if st.button("Calcular", key="priority_btn"):
        try:
            kwargs = dict(
                lambdas=lambdas,
                mu=mu,
                s=int(s),
                preemptive=preemptive,
            )
            if use_per_class_mu:
                kwargs["mus"] = mus_per_class
            if use_sigma2 and use_per_class_mu:
                kwargs["sigma2s"] = sigma2s_per_class

            fila = PriorityQueue(**kwargs)
        except Exception as e:
            st.error(str(e))
            return

        mode_label = "Com interrupção (preemptivo)" if preemptive else "Sem interrupção (não-preemptivo)"
        st.subheader(f"Resultados — {mode_label}")

        with st.container(border=True):
            st.metric("Taxa de ocupação total (ρ)", f"{fila.rho_total:.4g}")

        results = fila.results()
        for res in results:
            st.divider()
            k = res["classe"]
            mu_label = f"μ{k} = {res['mu']}" if use_per_class_mu else f"μ = {mu}"
            st.markdown(f"**Classe {k}** — λ{k} = {res['lambda']}  |  {mu_label}")

            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.metric("Tempo médio no sistema (W)", f"{res['W']:.4f}")
            with col2:
                with st.container(border=True):
                    st.metric("Tempo médio na fila (Wq)", f"{res['Wq']:.4f}")

            col3, col4 = st.columns(2)
            with col3:
                with st.container(border=True):
                    st.metric("Número médio no sistema (L)", f"{res['L']:.4f}")
            with col4:
                with st.container(border=True):
                    st.metric("Número médio na fila (Lq)", f"{res['Lq']:.4f}")
