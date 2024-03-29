import streamlit as st
from gpt_all_star.core.message import Message

from src.common.file import load_file
from src.models.extended_step_type import get_steps
from st_components.st_current_step_type import display_current_step_type
from st_components.st_introduction import introduction
from st_components.st_message import append_and_display_message, display_message
from st_components.st_session_states import ExtendedStepType


def st_main():
    if not st.session_state["chat_ready"]:
        return introduction()

    steps = get_steps(st.session_state["step_type"])

    st.session_state["current_step"] = (
        steps.pop(st.session_state["current_step_number"])
        if len(steps) > st.session_state["current_step_number"]
        else ExtendedStepType.FINISHED
    )
    display_current_step_type(f"Current Step: {st.session_state['current_step'].name}")

    if "messages" not in st.session_state:
        initialize_messages()

    for message in st.session_state.messages:
        display_message(message)

    if st.session_state["current_step"] == ExtendedStepType.SYSTEM_DESIGN:
        process_step("", ExtendedStepType.SYSTEM_DESIGN.value)
        next_step(steps)
    elif st.session_state["current_step"] == ExtendedStepType.DEVELOPMENT:
        process_step("", ExtendedStepType.DEVELOPMENT.value)
        next_step(steps)
    elif st.session_state["current_step"] == ExtendedStepType.UI_DESIGN:
        process_step("", ExtendedStepType.UI_DESIGN.value)
        next_step(steps)
    elif st.session_state["current_step"] == ExtendedStepType.ENTRYPOINT:
        process_step("", ExtendedStepType.ENTRYPOINT.value)
        next_step(steps)

    if prompt := st.chat_input():
        append_and_display_message(
            Message.create_human_message(name="user", message=prompt)
        )

        if st.session_state["current_step"] == ExtendedStepType.SPECIFICATION:
            process_step(prompt, ExtendedStepType.SPECIFICATION.value)
        elif st.session_state["current_step"] == ExtendedStepType.SPECIFICATION_CHECK:
            improve_step(prompt, ExtendedStepType.SPECIFICATION.value)
        elif st.session_state["current_step"] == ExtendedStepType.SYSTEM_DESIGN_CHECK:
            improve_step(prompt, ExtendedStepType.SYSTEM_DESIGN.value)
        elif st.session_state["current_step"] == ExtendedStepType.EXECUTION:
            execute_application()
        else:
            st.error("Invalid step type")

        next_step(steps)
        st.rerun()


def next_step(steps):
    st.session_state["current_step"] = (
        steps.pop(st.session_state["current_step_number"])
        if len(steps) > st.session_state["current_step_number"]
        else ExtendedStepType.FINISHED
    )
    st.session_state["current_step_number"] += 1
    display_current_step_type(f"Current Step: {st.session_state['current_step'].name}")

    step_messages = {
        ExtendedStepType.SPECIFICATION: "Hey there, What do you want to build?",
        ExtendedStepType.SPECIFICATION_CHECK: "What do you want to improve?",
        ExtendedStepType.SYSTEM_DESIGN_CHECK: "What do you want to improve?",
        ExtendedStepType.EXECUTION: "Do you want to execute the application?[Y/N]",
    }

    current_step = st.session_state["current_step"]
    if current_step in step_messages:
        append_and_display_message(
            Message.create_human_message(message=step_messages[current_step])
        )


def process_step(prompt, step_type):
    append_and_display_message(
        Message.create_human_message(message=f"Next Step: **{step_type}**")
    )

    with st.spinner("Running..."):
        for chunk in st.session_state.gpt_all_star.chat(
            message=prompt,
            step=step_type,
            project_name=st.session_state["project_name"],
        ):
            if chunk.get("messages") and chunk.get("next") is None:
                for message in chunk.get("messages"):
                    append_and_display_message(message)

    doc_files = {
        ExtendedStepType.SPECIFICATION.name: "specifications.md",
        ExtendedStepType.SYSTEM_DESIGN.name: "technologies.md",
    }

    if step_type.name in doc_files:
        md_file_path = f"projects/{st.session_state['project_name']}/docs/{doc_files[step_type.name]}"
        md_content = load_file(md_file_path)
        append_and_display_message(Message.create_human_message(message=md_content))


def improve_step(prompt, step_type):
    with st.spinner("Running..."):
        for chunk in st.session_state.gpt_all_star.improve(
            message=prompt,
            step=step_type,
            project_name=st.session_state["project_name"],
        ):
            if chunk.get("messages") and chunk.get("next") is None:
                for message in chunk.get("messages"):
                    append_and_display_message(message)

    doc_files = {
        ExtendedStepType.SPECIFICATION.name: "specifications.md",
        ExtendedStepType.SYSTEM_DESIGN.name: "technologies.md",
    }

    if step_type.name in doc_files:
        md_file_path = f"projects/{st.session_state['project_name']}/docs/{doc_files[step_type.name]}"
        md_content = load_file(md_file_path)
        append_and_display_message(Message.create_human_message(message=md_content))


def execute_application():
    append_and_display_message(
        Message.create_human_message(message="Next Step: **execution**")
    )

    with st.spinner("Running..."):
        for chunk in st.session_state.gpt_all_star.execute(
            project_name=st.session_state["project_name"]
        ):
            if chunk.get("messages") and chunk.get("next") is None:
                for message in chunk.get("messages"):
                    append_and_display_message(message)


def initialize_messages():
    if st.session_state["current_step"] == ExtendedStepType.SPECIFICATION:
        message_text = "Hey there, What do you want to build?"
    elif st.session_state["current_step"] in [
        ExtendedStepType.SPECIFICATION_CHECK,
        ExtendedStepType.SYSTEM_DESIGN_CHECK,
    ]:
        message_text = "What do you want to improve?"
    elif st.session_state["current_step"] == ExtendedStepType.DEVELOPMENT:
        message_text = "Do you want to build the application?[Y/N]"
    else:
        message_text = "Do you want to execute the application?[Y/N]"
    st.session_state["messages"] = [Message.create_human_message(message=message_text)]
