import streamlit as st

from models.priority_model import PriorityQueue
from utils.input_helpers import input_integer, _parse_numeric_expression
from utils.ui import metric_grid


def _parse_rate(value_str, label):
    try:
        v = _parse_numeric_expression(value_str.replace(",", ".").strip()) if value_str else None
        return float(v) if v is not None else 0.0
    except (ValueError, TypeError):
        st.error(f"Valor inválido para {label}")
        return 0.0


def render():
    st.header("Modelo com Prioridades")
    st.info(
        "Fila com **múltiplas classes de clientes** com prioridades distintas. "
        "Classe 1 tem a maior prioridade. "
        "**Com interrupção (preemptivo):** cliente de alta prioridade interrompe o atendimento em curso. "
        "**Sem interrupção (não-preemptivo):** aguarda o atendimento atual concluir. "
        "W e Wq são expressos na mesma unidade de tempo de λ e μ.",
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
            "s — Número de canais de serviço (servidores)",
            "priority_s",
            default=1,
            placeholder="Ex: 1",
            min_value=1,
            help_text="Quantidade de servidores compartilhados por todas as classes.",
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

    n_classes = input_integer(
        "Número de classes de prioridade",
        "priority_n_classes",
        default=2,
        placeholder="Ex: 2",
        min_value=2,
        max_value=10,
        help_text="Quantas classes de clientes com prioridades distintas existem no sistema.",
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

        metric_grid([("ρ total", f"{fila.rho_total:.4g}", "Taxa de ocupação total do(s) servidor(es)")], columns=1)
        st.divider()

        results = fila.results()
        for res in results:
            k = res["classe"]
            mu_label = f"μ{k} = {res['mu']}" if use_per_class_mu else f"μ = {mu}"
            st.markdown(f"**Classe {k}** — λ{k} = {res['lambda']}  |  {mu_label}")
            metric_grid([
                ("W",  f"{res['W']:.4f}",  "Tempo médio gasto no sistema"),
                ("Wq", f"{res['Wq']:.4f}", "Tempo médio de espera na fila"),
                ("L",  f"{res['L']:.4f}",  "Número médio de clientes no sistema"),
                ("Lq", f"{res['Lq']:.4f}", "Número médio de clientes na fila"),
            ], columns=2)
            if k < len(results):
                st.divider()
