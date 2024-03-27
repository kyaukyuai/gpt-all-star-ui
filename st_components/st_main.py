import ast
import os
import subprocess
import time

import requests
import streamlit as st
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.steps import StepType

from settings import settings
from st_components.st_fixed_component import fixed_component


def st_main():
    if not st.session_state["chat_ready"]:
        introduction()
    else:
        fixed_component(f"Current Step: {st.session_state['current_step']}")

        step_type = StepType[st.session_state["step_type"]]
        steps = get_steps(step_type)

        if step_type in [StepType.DEFAULT, StepType.SPECIFICATION]:
            st.session_state["messages"] = [
                Message.create_human_message(
                    message="Hey there, What do you want to build?"
                )
            ]
        else:
            st.session_state["messages"] = [
                Message.create_human_message(
                    message="Do you want to build the application?[Y/N]"
                )
            ]

        for message in st.session_state.messages:
            process_message(message)

        if prompt := st.chat_input():
            user_message = Message.create_human_message(name="user", message=prompt)
            st.session_state.messages.append(user_message)
            process_message(user_message)

            if st.session_state["current_step"] == "Not started":
                for step in steps:
                    st.session_state["current_step"] = step.name
                    fixed_component(f"Current Step: {st.session_state['current_step']}")
                    process_step(prompt, step)

                st.session_state["current_step"] = "EXECUTION"
                fixed_component(f"Current Step: {st.session_state['current_step']}")
                execute_message = Message.create_human_message(
                    message="Would you like to execute the application?[Y/N]"
                )
                st.session_state.messages.append(execute_message)
                process_message(execute_message)
            elif st.session_state["current_step"] == "EXECUTION":
                if prompt.lower() in ["y", "n"]:
                    if prompt.lower() == "y":
                        execute_application()
                    else:
                        st.stop()


def get_steps(step_type: StepType):
    if step_type == StepType.NONE:
        return []
    elif step_type == StepType.DEFAULT:
        return [
            StepType.SPECIFICATION,
            StepType.SYSTEM_DESIGN,
            StepType.DEVELOPMENT,
            StepType.UI_DESIGN,
            StepType.ENTRYPOINT,
        ]
    else:
        return [step_type]


def process_step(prompt, step_type):
    step_message = Message.create_human_message(message=f"Next Step: **{step_type}**")
    st.session_state.messages.append(step_message)
    process_message(step_message)

    with st.spinner("Running..."):
        for chunk in st.session_state.gpt_all_star.chat(
            message=prompt,
            step=step_type,
            project_name=st.session_state["project_name"],
        ):
            if chunk.get("messages") and chunk.get("next") is None:
                for message in chunk.get("messages"):
                    st.session_state.messages.append(step_message)
                    process_message(message)

    if step_type is StepType.SPECIFICATION:
        display_markdown_file(
            f"projects/{st.session_state['project_name']}/docs/specifications.md"
        )
    elif step_type is StepType.SYSTEM_DESIGN:
        display_markdown_file(
            f"projects/{st.session_state['project_name']}/docs/technologies.md"
        )


def execute_application():
    step_message = Message.create_human_message(message="Next Step: **execution**")
    st.session_state.messages.append(step_message)
    process_message(step_message)

    with st.spinner("Running..."):
        for chunk in st.session_state.gpt_all_star.execute(
            project_name=st.session_state["project_name"]
        ):
            if chunk.get("messages") and chunk.get("next") is None:
                for message in chunk.get("messages"):
                    process_message(message)


def process_message(message):
    if message.name in [setting["name"] for setting in settings]:
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


def load_markdown_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def display_markdown_file(path):
    md_content = load_markdown_file(path)
    with st.chat_message("assistant"):
        st.info("OUTPUT", icon="ℹ️")
        st.markdown(md_content, unsafe_allow_html=True)


def check_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def introduction():
    """
    Introduction:
    Display introductory messages for the user.
    """
    st.info("Set API Key, to be able to build your application.", icon="👉️")
