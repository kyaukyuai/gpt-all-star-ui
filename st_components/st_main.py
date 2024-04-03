import streamlit as st
from gpt_all_star.core.message import Message

from src.common.file import load_file
from src.models.extended_step_type import ExtendedStepType, get_steps
from st_components.st_current_step_type import display_current_step_type
from st_components.st_introduction import introduction
from st_components.st_message import append_and_display_message, display_message

MESSAGE = {
    "improve": """
    Is this okay? If so, please enter [Y].  \n
    If you want to make any corrections, please enter them.
    """,
    "execute": "Do you want to execute the application?[Y/N]",
}


def st_main():
    if not st.session_state["chat_ready"]:
        return introduction()

    steps = get_steps(st.session_state["step_type"])

    current_step = (
        steps.pop(st.session_state["current_step_number"])
        if len(steps) > st.session_state["current_step_number"]
        else ExtendedStepType.FINISHED
    )
    display_current_step_type(f"{current_step.name}")

    if "messages" not in st.session_state:
        initialize_messages(current_step)

    for message in st.session_state.messages:
        display_message(message)

    if current_step in [
        ExtendedStepType.SYSTEM_DESIGN,
        ExtendedStepType.UI_DESIGN,
        ExtendedStepType.DEVELOPMENT,
        ExtendedStepType.ENTRYPOINT,
    ]:
        process_step("", current_step.value)
        next_step(steps)
        st.rerun()

    if prompt := st.chat_input():
        append_and_display_message(
            Message.create_human_message(name="user", message=prompt)
        )

        step_actions = {
            ExtendedStepType.SPECIFICATION: lambda: process_step(
                prompt, ExtendedStepType.SPECIFICATION.value
            ),
            ExtendedStepType.SPECIFICATION_IMPROVE: lambda: handle_improvement_step(
                prompt, ExtendedStepType.SPECIFICATION
            ),
            ExtendedStepType.SYSTEM_DESIGN_IMPROVE: lambda: handle_improvement_step(
                prompt, ExtendedStepType.SYSTEM_DESIGN
            ),
            ExtendedStepType.UI_DESIGN_IMPROVE: lambda: handle_improvement_step(
                prompt, ExtendedStepType.UI_DESIGN
            ),
            ExtendedStepType.EXECUTION: execute_application,
        }

        action = step_actions.get(current_step, lambda: st.error("Invalid step type"))
        action()

        if current_step not in [ExtendedStepType.EXECUTION]:
            next_step(steps)
            st.rerun()


def handle_improvement_step(prompt: str, step_type: ExtendedStepType):
    if prompt.lower() != "y":
        improve_step(prompt, step_type.value)
        append_and_display_message(
            Message.create_human_message(message=MESSAGE["improve"])
        )
        st.rerun()


def next_step(steps):
    current_step = (
        steps.pop(st.session_state["current_step_number"])
        if len(steps) > st.session_state["current_step_number"]
        else ExtendedStepType.FINISHED
    )
    st.session_state["current_step_number"] += 1
    display_current_step_type(f"{current_step.name}")

    step_messages = {
        ExtendedStepType.SPECIFICATION_IMPROVE: MESSAGE["improve"],
        ExtendedStepType.SYSTEM_DESIGN_IMPROVE: MESSAGE["improve"],
        ExtendedStepType.UI_DESIGN_IMPROVE: MESSAGE["improve"],
        ExtendedStepType.EXECUTION: MESSAGE["execute"],
    }

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
        ExtendedStepType.UI_DESIGN.name: "ui_design.html",
    }

    if step_type.name in doc_files:
        file_path = f"projects/{st.session_state['project_name']}/docs/{doc_files[step_type.name]}"
        content = load_file(file_path)
        append_and_display_message(Message.create_human_message(message=content))


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
        ExtendedStepType.UI_DESIGN.name: "ui_design.html",
    }

    if step_type.name in doc_files:
        file_path = f"projects/{st.session_state['project_name']}/docs/{doc_files[step_type.name]}"
        content = load_file(file_path)
        append_and_display_message(Message.create_human_message(message=content))


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


def initialize_messages(current_step: ExtendedStepType):
    step_messages = {
        ExtendedStepType.SPECIFICATION: "Hey there, What do you want to build?",
    }
    default_message = MESSAGE["execute"]
    message_text = step_messages.get(current_step, default_message)
    st.session_state["messages"] = [Message.create_human_message(message=message_text)]
