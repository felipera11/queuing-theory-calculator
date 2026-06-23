import streamlit as st


def render():

    st.header("📚 Guia para encontrar λ e μ")

    st.info(
        "Clique em cada bloco para abrir as fórmulas e macetes."
    )

    with st.expander("1️⃣ Conceito de λ - Taxa de chegada"):
        st.markdown("""
        **λ representa quantos clientes chegam por unidade de tempo.**

        Exemplos:

        - Chegam 3 clientes por hora → λ = 3
        - Chegam 10 clientes por minuto → λ = 10
        - Chega 1 cliente a cada 15 minutos → λ = 1/15 cliente/min
        - Chega 1 paciente a cada 30 minutos → λ = 2 pacientes/h
        """)

    with st.expander("2️⃣ Conceito de μ - Taxa de atendimento"):
        st.markdown("""
        **μ representa quantos clientes um servidor atende por unidade de tempo.**

        Exemplos:

        - Atende 8 clientes por hora → μ = 8
        - Tempo médio de atendimento = 15 min → μ = 1/15 cliente/min
        - Médico leva 20 min por paciente → μ = 3 pacientes/h
        """)

    with st.expander("3️⃣ Fórmulas válidas para todos os modelos"):
        st.markdown("A Lei de Little funciona para praticamente todos os modelos de filas.")

        st.latex(r"L=\lambda W")
        st.latex(r"L_q=\lambda W_q")

        st.markdown("Logo:")

        st.latex(r"\lambda=\frac{L}{W}")
        st.latex(r"\lambda=\frac{L_q}{W_q}")

        st.success(
            "Se o professor fornecer L e W ou Lq e Wq, você encontra λ diretamente."
        )

    with st.expander("4️⃣ Modelos com 1 servidor"):
        st.markdown("""
        Serve para:

        - M/M/1
        - M/M/1/K
        - M/M/1/N
        - M/G/1
        """)

        st.latex(r"\rho=\frac{\lambda}{\mu}")

        st.markdown("Isolando:")

        st.latex(r"\lambda=\rho\mu")
        st.latex(r"\mu=\frac{\lambda}{\rho}")

    with st.expander("5️⃣ Modelos com vários servidores"):
        st.markdown("""
        Serve para:

        - M/M/s
        - M/M/s/K
        - M/M/s/N

        onde **s** é o número de servidores.
        """)

        st.latex(r"\rho=\frac{\lambda}{s\mu}")

        st.markdown("Isolando:")

        st.latex(r"\lambda=\rho s\mu")
        st.latex(r"\mu=\frac{\lambda}{\rho s}")

    with st.expander("6️⃣ Quando o exercício fornece W"):
        st.markdown("Para **M/M/1**:")

        st.latex(r"W=\frac{1}{\mu-\lambda}")

        st.markdown("Logo:")

        st.latex(r"\mu-\lambda=\frac{1}{W}")

    with st.expander("7️⃣ Quando o exercício fornece Wq"):
        st.markdown("Para **M/M/1**:")

        st.latex(r"W_q=\frac{\lambda}{\mu(\mu-\lambda)}")

        st.markdown("Também pode usar:")

        st.latex(r"W_q=\frac{\rho}{\mu-\lambda}")

    with st.expander("8️⃣ Quando o exercício fornece L"):
        st.markdown("Para **M/M/1**:")

        st.latex(r"L=\frac{\lambda}{\mu-\lambda}")

        st.markdown("Mas, se tiver W também, use Little:")

        st.latex(r"\lambda=\frac{L}{W}")

    with st.expander("9️⃣ Quando o exercício fornece Lq"):
        st.markdown("Para **M/M/1**:")

        st.latex(r"L_q=\frac{\lambda^2}{\mu(\mu-\lambda)}")

        st.markdown("ou:")

        st.latex(r"L_q=\frac{\rho^2}{1-\rho}")

        st.markdown("Mas, se tiver Wq também, use Little:")

        st.latex(r"\lambda=\frac{L_q}{W_q}")

    with st.expander("🔟 Macete rápido para prova", expanded=True):
        st.table({
            "O enunciado diz": [
                "Chegam X por hora",
                "Chega 1 a cada T",
                "Atende X por hora",
                "Atendimento leva T",
                "ρ e μ",
                "ρ e λ",
                "L e W",
                "Lq e Wq"
            ],
            "O que fazer": [
                "λ = X",
                "λ = 1/T",
                "μ = X",
                "μ = 1/T",
                "λ = ρ·μ",
                "μ = λ/ρ",
                "λ = L/W",
                "λ = Lq/Wq"
            ]
        })

    with st.expander("🧮 Calculadora rápida"):
        tipo = st.selectbox(
            "O que o exercício forneceu?",
            [
                "Chegadas por tempo",
                "Tempo entre chegadas",
                "Atendimentos por tempo",
                "Tempo médio de atendimento",
                "ρ e μ",
                "ρ e λ",
                "L e W",
                "Lq e Wq"
            ]
        )

        if tipo == "Chegadas por tempo":
            valor = st.number_input(
                "Quantidade que chega por unidade de tempo",
                min_value=0.0
            )
            st.metric("λ", f"{valor:.4g}")

        elif tipo == "Tempo entre chegadas":
            tempo = st.number_input(
                "Tempo entre chegadas",
                min_value=0.0001
            )
            st.metric("λ = 1/T", f"{1/tempo:.4g}")

        elif tipo == "Atendimentos por tempo":
            valor = st.number_input(
                "Quantidade atendida por unidade de tempo",
                min_value=0.0
            )
            st.metric("μ", f"{valor:.4g}")

        elif tipo == "Tempo médio de atendimento":
            tempo = st.number_input(
                "Tempo médio de atendimento",
                min_value=0.0001
            )
            st.metric("μ = 1/T", f"{1/tempo:.4g}")

        elif tipo == "ρ e μ":
            rho = st.number_input(
                "ρ",
                min_value=0.0,
                max_value=0.9999
            )
            mi = st.number_input(
                "μ",
                min_value=0.0001
            )
            st.metric("λ = ρ · μ", f"{rho * mi:.4g}")

        elif tipo == "ρ e λ":
            rho = st.number_input(
                "ρ",
                min_value=0.0001,
                max_value=0.9999
            )
            lambda_ = st.number_input(
                "λ",
                min_value=0.0001
            )
            st.metric("μ = λ / ρ", f"{lambda_ / rho:.4g}")

        elif tipo == "L e W":
            l = st.number_input(
                "L",
                min_value=0.0
            )
            w = st.number_input(
                "W",
                min_value=0.0001
            )
            st.metric("λ = L / W", f"{l / w:.4g}")

        elif tipo == "Lq e Wq":
            lq = st.number_input(
                "Lq",
                min_value=0.0
            )
            wq = st.number_input(
                "Wq",
                min_value=0.0001
            )
            st.metric("λ = Lq / Wq", f"{lq / wq:.4g}")
