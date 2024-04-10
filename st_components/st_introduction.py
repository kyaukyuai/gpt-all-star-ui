import streamlit as st
import toml

from src.common.translator import create_translator

config = toml.load(".streamlit/app_config.toml")
lang = config["language"]["useLanguage"]
_ = create_translator("en" if lang == "en" else "ja")


def introduction():
    """
    Introduction:
    Display introductory messages for the user.
    """
    st.info(_("Set API Key, to be able to build your application."), icon="👉️")
