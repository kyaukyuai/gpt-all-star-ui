import json

import streamlit as st
from gpt_all_star import gpt_all_star
from gpt_all_star.core.steps.steps import StepType


def init_session_states():
    default_states = {
        "models": lambda: json.load(open("models.json", "r")),
        "chat_ready": False,
        "gpt_all_star": gpt_all_star,
        "step_type": StepType.DEFAULT.name,
        "current_step_number": 0,
    }

    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value() if callable(value) else value
