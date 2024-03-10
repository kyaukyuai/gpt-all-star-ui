import streamlit as st


def set_page_config():
    st.set_page_config(
        page_title="GPT ALL STAR",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def set_style():
    with open("./st_components/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def st_init():
    set_page_config()
    set_style()
