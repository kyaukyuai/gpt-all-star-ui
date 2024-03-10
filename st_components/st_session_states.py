import json
import uuid

import streamlit as st
from gpt_all_star import gpt_all_star

INITIAL_MESSAGE = [
    {"role": "user", "content": "Hi!"},
    dict(
        role="assistant",
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
        "user_id": lambda: str(uuid.uuid4()),
        "gpt_all_star": gpt_all_star,
    }

    for key, value in default_states.items():
        if key not in st.session_state:
            st.session_state[key] = value() if callable(value) else value