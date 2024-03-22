import os
import warnings

import streamlit as st

from st_components.st_init import st_init
from st_components.st_main import st_main
from st_components.st_session_states import init_session_states
from st_components.st_sidebar import st_sidebar

warnings.filterwarnings("ignore")

os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]

st_init()
st.image("static/logo-wide.png", width=420)
init_session_states()
st_sidebar()
st_main()
