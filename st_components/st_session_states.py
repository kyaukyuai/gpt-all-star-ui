import json

import streamlit as st
from gpt_all_star import gpt_all_star
from gpt_all_star.core.steps.steps import StepType

INITIAL_MESSAGE = [
    dict(
        name="assistant",
        content="""Hey there, I'm copilot of GPT ALL STAR,
What type of application would you like to build?
""",
    ),
]


def init_session_states():
    default_states = {
        "models": lambda: json.load(open("models.json", "r")),
        "messages": INITIAL_MESSAGE,
        "chat_ready": False,
        "gpt_all_star": gpt_all_star,
        "project_name": "sample",
        "step_type": StepType.DEFAULT.name,
    }

    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value() if callable(value) else value
