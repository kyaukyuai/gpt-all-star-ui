import ast
import os
import subprocess
import time
import toml

import streamlit as st
from gpt_all_star.core.message import Message

from settings import settings
from src.common.browser import check_url

from src.common.translator import create_translator

config = toml.load(".streamlit/app_config.toml")
lang = config['language']['useLanguage']
_ = create_translator("en" if lang == "en" else "ja")


def display_message(message: Message):
    if message.name in [setting["name"] for setting in settings]:
        setting = next((s for s in settings if s["name"] == message.name), None)
        with st.chat_message(message.name, avatar=setting["avatar_url"]):
            try:
                content_data = ast.literal_eval(message.content)
                st.write(_("%s is working...") % _(message.name))
                st.info("TODO LIST", icon="ℹ️")
                st.json(content_data, expanded=False)
            except (SyntaxError, ValueError):
                st.write(_("%s is working...") % _(message.name))
                st.markdown(message.content)
    elif message.name is not None:
        with st.chat_message(message.name):
            st.markdown(message.content, unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            try:
                content_data = ast.literal_eval(message.content)
                url = content_data["url"]
                command = content_data["command"]
                os.chdir(f"projects/{st.session_state['project_name']}/app/")
                subprocess.Popen(command, shell=True)
                while not check_url(url):
                    time.sleep(1)
                st.markdown(
                    f'<iframe src="{url}" width="740" height="620" style="border: 1px solid #ccc; border-radius: 5px; margin: 0 10px 10px 0;"></iframe>',
                    unsafe_allow_html=True,
                )
            except (SyntaxError, ValueError):
                st.markdown(message.content, unsafe_allow_html=True)


def append_message(message: Message):
    st.session_state["messages"].append(message)


def append_and_display_message(message: Message):
    append_message(message)
    display_message(message)
