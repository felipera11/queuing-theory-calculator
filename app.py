import streamlit as st
from views import mm1_page, mms_page, mm1k_page, mmsk_page, mm1n_page, mmsn_page, mg1_page, priority_page
from utils.ui import inject_theme


st.set_page_config(page_title="Simulador de Filas", page_icon="📈", layout="wide")

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

if "show_models" not in st.session_state:
    st.session_state.show_models = False

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "M/M/1"


with st.sidebar:
    toggle_label = "Ocultar modelos" if st.session_state.show_models else "Mostrar modelos"
    if st.button(toggle_label, use_container_width=True, key="toggle_models"):
        st.session_state.show_models = not st.session_state.show_models
        st.rerun()

    if st.session_state.show_models:
        st.radio(
            "Modelos",
            list(pages.keys()),
            key="selected_model",
            label_visibility="collapsed",
        )

pages[st.session_state.selected_model].render()