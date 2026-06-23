import pandas as pd
import streamlit as st


def mostrar_tabela_n(fila, titulo="Tabela de probabilidades para N de 1 a 10"):
    st.subheader(titulo)

    dados_n = []

    for i in range(1, 11):
        linha = {"n": i}

        if hasattr(fila, "prob_n"):
            linha["P(N=n)"] = fila.prob_n(i)

        if hasattr(fila, "prob_less_equal_n"):
            linha["P(N≤n)"] = fila.prob_less_equal_n(i)

        if hasattr(fila, "prob_greater_equal_n"):
            linha["P(N≥n)"] = fila.prob_greater_equal_n(i)

        dados_n.append(linha)

    df_n = pd.DataFrame(dados_n)

    formatos = {
        col: "{:.4f}"
        for col in df_n.columns
        if col != "n"
    }

    st.dataframe(
        df_n.style.format(formatos),
        use_container_width=True,
        hide_index=True
    )