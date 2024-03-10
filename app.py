import warnings

import streamlit as st

from st_components.st_init import st_init
from st_components.st_main import st_main
from st_components.st_session_states import init_session_states
from st_components.st_sidebar import st_sidebar

warnings.filterwarnings("ignore")

st_init()
st.title("🤖 GPT ALL STAR")
init_session_states()
st_sidebar()
st_main()
