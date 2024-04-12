import streamlit as st

from src.common.translator import create_translator


def set_language_and_translator():
    lang = st.sidebar.selectbox("Select Language", ["en", "ja"])
    st.session_state.lang = lang
    translator = create_translator(lang)
    st.session_state.translator = translator
