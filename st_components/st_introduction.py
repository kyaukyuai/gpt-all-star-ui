import streamlit as st


def introduction():
    _ = st.session_state.translator
    """
    Introduction:
    Display introductory messages for the user.
    """
    st.info(_("Set API Key, to be able to build your application."), icon="👉️")
