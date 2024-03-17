import streamlit as st
from gpt_all_star.core.steps.steps import StepType
from langchain_core.messages import HumanMessage

from st_components.st_message import (
    display_agent_message,
    display_copilot_message,
    display_user_message,
)


def st_main():
    if not st.session_state["chat_ready"]:
        introduction()
    else:
        handle_chat_interaction()


def handle_chat_interaction():
    prompt = st.chat_input()
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

    display_messages()

    if prompt:
        process_prompt(prompt, StepType.SPECIFICATION, "specifications.md")
        process_prompt(None, StepType.SYSTEM_DESIGN, "technologies.md")
        process_prompt(None, StepType.DEVELOPMENT, None)
        process_prompt(None, StepType.UI_DESIGN, None)
        process_prompt(None, StepType.ENTRYPOINT, None)


def process_prompt(prompt, step_type, markdown_file):
    for chunk in st.session_state.gpt_all_star.chat(
        message=prompt,
        step=step_type,
        project_name=st.session_state["project_name"],
    ):
        if chunk.get("messages"):
            for message in chunk.get("messages"):
                process_message(message)

    if markdown_file:
        display_markdown_file(
            f"projects/{st.session_state['project_name']}/docs/{markdown_file}"
        )


def process_message(message):
    if isinstance(message, HumanMessage):
        if message.name is not None:
            st.session_state.messages.append(
                {"role": "assistant", "content": message.content}
            )
            display_agent_message(message.name, message.content)
        else:
            display_copilot_message(message.content)


def display_messages():
    for message in st.session_state.messages:
        if message["role"] == "user":
            display_user_message(message["content"])
        elif message["role"] == "copilot":
            display_copilot_message(message["content"])


def load_markdown_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def display_markdown_file(path):
    md_content = load_markdown_file(path)
    with st.chat_message("assistant"):
        st.markdown(md_content, unsafe_allow_html=True)


def introduction():
    """
    Introduction:
    Display introductory messages for the user.
    """
    st.info("👋 Hey, we're very happy to see you here.")
    st.info("👉 Set your api key, to be able to run code while you generate it.")
