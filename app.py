import streamlit as st
from views import mm1_page, mms_page, mm1k_page, mmsk_page, mm1n_page, mmsn_page, mg1_page, priority_page
from utils.ui import inject_theme


st.set_page_config(page_title="Simulador de Filas", page_icon="📊", layout="wide")

inject_theme()

pages = {
    "M/M/1": mm1_page,
    "M/M/s": mms_page,
    "M/M/1/K": mm1k_page,
    "M/M/s/K": mmsk_page,
    "M/M/1/N": mm1n_page,
    "M/M/s/N": mmsn_page,
    "M/G/1": mg1_page,
    "Prioridades": priority_page,
}

MODEL_LABELS = {
    "M/M/1":       "M/M/1  —  1 servidor, cap. ∞",
    "M/M/s":       "M/M/s  —  s servidores, cap. ∞",
    "M/M/1/K":     "M/M/1/K  —  1 servidor, cap. K",
    "M/M/s/K":     "M/M/s/K  —  s servidores, cap. K",
    "M/M/1/N":     "M/M/1/N  —  pop. finita N",
    "M/M/s/N":     "M/M/s/N  —  s servidores, pop. N",
    "M/G/1":       "M/G/1  —  serviço geral",
    "Prioridades": "Prioridades  —  múltiplas classes",
}

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "M/M/1"


with st.sidebar:
    st.markdown("## 📊 Simulador de Filas")
    st.caption("Calculadora de Teoria das Filas")
    st.divider()
    st.markdown("**Selecione o modelo:**")
    st.radio(
        "Modelos",
        list(pages.keys()),
        key="selected_model",
        label_visibility="collapsed",
        format_func=lambda x: MODEL_LABELS.get(x, x),
    )

pages[st.session_state.selected_model].render()
