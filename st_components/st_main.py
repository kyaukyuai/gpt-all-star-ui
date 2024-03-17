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
        prompt = st.chat_input()
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})

        for message in st.session_state.messages:
            if message["role"] == "user":
                display_user_message(message["content"])
            elif message["role"] == "copilot":
                display_copilot_message(message["content"])

        if prompt:
            for chunk in st.session_state.gpt_all_star.chat(
                message=prompt,
                step=StepType.SPECIFICATION,
                project_name=st.session_state["project_name"],
            ):
                # st.write(chunk)
                if chunk.get("messages"):
                    for message in chunk.get("messages"):
                        if isinstance(message, HumanMessage):
                            if message.name is not None:
                                st.session_state.messages.append(
                                    {"role": "assistant", "content": message.content}
                                )
                                display_agent_message(message.name, message.content)
                            else:
                                display_copilot_message(message.content)

            display_markdown_file(
                f"projects/{st.session_state['project_name']}/specifications.md"
            )


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
