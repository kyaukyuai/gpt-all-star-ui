import ast

import streamlit as st
from gpt_all_star.core.steps.steps import StepType

from settings import settings


def st_main():
    if not st.session_state["chat_ready"]:
        introduction()
    else:
        handle_chat_interaction()


def handle_chat_interaction():
    prompt = st.chat_input()
    if prompt:
        st.session_state.messages.append({"name": "user", "content": prompt})
        process_chat_prompt(prompt)
    else:
        display_messages()


def process_chat_prompt(prompt):
    display_messages()
    step_type = StepType[st.session_state["step_type"]]
    process_step_type(prompt, step_type)
    check_for_execution_prompt(prompt)


def process_step_type(prompt, step_type):
    if step_type == StepType.NONE:
        return
    elif step_type == StepType.DEFAULT:
        default_step_process(prompt)
    elif step_type in [StepType.SPECIFICATION, StepType.SYSTEM_DESIGN]:
        process_prompt(
            prompt if step_type == StepType.SPECIFICATION else None,
            step_type,
            f"{step_type.name.lower()}.md",
        )
    else:
        process_prompt(None, step_type, None)


def default_step_process(prompt):
    for step in [
        StepType.SPECIFICATION,
        StepType.SYSTEM_DESIGN,
        StepType.DEVELOPMENT,
        StepType.UI_DESIGN,
        StepType.ENTRYPOINT,
    ]:
        process_prompt(
            prompt if step == StepType.SPECIFICATION else None,
            step,
            (
                f"{step.name.lower()}.md"
                if step in [StepType.SPECIFICATION, StepType.SYSTEM_DESIGN]
                else None
            ),
        )


def check_for_execution_prompt(prompt):
    if prompt.lower() == "y":
        execute_application()
    else:
        with st.chat_message("assistant"):
            st.markdown("Would you like to execute the application?(y/n)")


def execute_application():
    with st.chat_message("assistant"):
        st.markdown("Next Step: **execution**")
    with st.spinner("Running..."):
        for chunk in st.session_state.gpt_all_star.execute(
            project_name=st.session_state["project_name"]
        ):
            if chunk.get("messages") and chunk.get("next") is None:
                for message in chunk.get("messages"):
                    process_message(message)
        st.markdown(
            '<iframe src="http://localhost:3000" width="800" height="600" style="border: 2px solid #ccc;"></iframe>',
            unsafe_allow_html=True,
        )


def process_prompt(prompt, step_type, markdown_file):
    with st.chat_message("assistant"):
        st.markdown(f"Next Step: **{step_type}**")

    with st.spinner("Running..."):
        for chunk in st.session_state.gpt_all_star.chat(
            message=prompt,
            step=step_type,
            project_name=st.session_state["project_name"],
        ):
            if chunk.get("messages") and chunk.get("next") is None:
                for message in chunk.get("messages"):
                    process_message(message)

    if markdown_file:
        display_markdown_file(
            f"projects/{st.session_state['project_name']}/docs/{markdown_file}"
        )


def process_message(message):
    if message.name is not None:
        setting = next((s for s in settings if s["name"] == message.name), None)
        with st.chat_message(message.name, avatar=setting["avatar_url"]):
            try:
                content_data = ast.literal_eval(message.content)
                st.write(f"{message.name} is working...")
                st.info("TODO LIST", icon="ℹ️")
                st.json(content_data, expanded=False)
            except (SyntaxError, ValueError):
                st.write(f"{message.name} is working...")
                st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)


def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["name"]):
            st.markdown(message["content"])


def load_markdown_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def display_markdown_file(path):
    md_content = load_markdown_file(path)
    with st.chat_message("assistant"):
        st.info("OUTPUT", icon="ℹ️")
        st.markdown(md_content, unsafe_allow_html=True)


def introduction():
    """
    Introduction:
    Display introductory messages for the user.
    """
    st.info("Hey, we're very happy to see you here.", icon="👋")
    st.info("Set API Key, to be able to build your application.", icon="👉️")
