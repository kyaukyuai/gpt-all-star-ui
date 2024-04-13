import streamlit as st
from gpt_all_star.core.message import Message

from src.common.file import load_file
from st_components.st_current_step_type import display_current_step_type
from st_components.st_introduction import introduction
from st_components.st_message import append_and_display_message, display_message
from st_components.st_models.extended_step_type import ExtendedStepType, get_steps


class MessageContent:
    def __init__(self, translator):
        self._ = translator

    def get_message(self):
        return {
            "improve": self._(
                """
                Is this okay? If so, please enter [Y].  \n
                If you want to make any corrections, please enter them.
                """
            ),
            "execute": self._("Do you want to execute the application?[Y/N]"),
            "deploy": self._("Do you want to push the code to GitHub?[Y/N]"),
        }


def st_main():
    _ = st.session_state.translator
    if not (
        st.session_state.get("chat_ready") and st.session_state.get("project_name")
    ):
        return introduction()

    steps = get_steps(st.session_state["step_type"])

    current_step = (
        steps.pop(st.session_state["current_step_number"])
        if len(steps) > st.session_state["current_step_number"]
        else ExtendedStepType.FINISHED
    )
    display_current_step_type(f"{current_step.display_name}")

    if "messages" not in st.session_state:
        initialize_messages(current_step)

    for message in st.session_state.messages:
        display_message(message)

    if current_step in [
        ExtendedStepType.SYSTEM_DESIGN,
        ExtendedStepType.UI_DESIGN,
        ExtendedStepType.DEVELOPMENT,
        ExtendedStepType.QUALITY_ASSURANCE,
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
            ExtendedStepType.DEPLOYMENT: deploy_application,
        }

        action = step_actions.get(current_step, lambda: st.error("Invalid step type"))
        action()

        if current_step not in [ExtendedStepType.EXECUTION]:
            next_step(steps)
            st.rerun()


def handle_improvement_step(prompt: str, step_type: ExtendedStepType):
    _ = st.session_state.translator
    if prompt.lower() != "y":
        improve_step(prompt, step_type.value)
        append_and_display_message(
            Message.create_human_message(
                message=MessageContent(_).get_message()["improve"]
            )
        )
        st.rerun()


def next_step(steps):
    _ = st.session_state.translator
    current_step = (
        steps.pop(st.session_state["current_step_number"])
        if len(steps) > st.session_state["current_step_number"]
        else ExtendedStepType.FINISHED
    )
    st.session_state["current_step_number"] += 1
    display_current_step_type(f"{current_step.display_name}")

    step_messages = {
        ExtendedStepType.SPECIFICATION_IMPROVE: MessageContent(_).get_message()[
            "improve"
        ],
        ExtendedStepType.SYSTEM_DESIGN_IMPROVE: MessageContent(_).get_message()[
            "improve"
        ],
        ExtendedStepType.UI_DESIGN_IMPROVE: MessageContent(_).get_message()["improve"],
        ExtendedStepType.EXECUTION: MessageContent(_).get_message()["execute"],
        ExtendedStepType.DEPLOYMENT: MessageContent(_).get_message()["deploy"],
    }

    if current_step in step_messages:
        append_and_display_message(
            Message.create_human_message(message=step_messages[current_step])
        )


def process_step(prompt, step_type):
    _ = st.session_state.translator
    with st.spinner(_("Running...")):
        for chunk in st.session_state.gpt_all_star.chat(
            message=prompt,
            step=step_type,
            project_name=st.session_state["project_name"],
            japanese_mode=st.session_state["lang"] == "ja",
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
    _ = st.session_state.translator
    with st.spinner(_("Running...")):
        for chunk in st.session_state.gpt_all_star.improve(
            message=prompt,
            step=step_type,
            project_name=st.session_state["project_name"],
            japanese_mode=st.session_state["lang"] == "ja",
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
    _ = st.session_state.translator
    with st.spinner(_("Running...")):
        for chunk in st.session_state.gpt_all_star.execute(
            project_name=st.session_state["project_name"],
            japanese_mode=st.session_state["lang"] == "ja",
        ):
            if chunk.get("messages") and chunk.get("next") is None:
                for message in chunk.get("messages"):
                    append_and_display_message(message)


def deploy_application():
    _ = st.session_state.translator
    with st.spinner(_("Running...")):
        for chunk in st.session_state.gpt_all_star.deploy(
            project_name=st.session_state["project_name"],
            japanese_mode=st.session_state["lang"] == "ja",
        ):
            if chunk.get("messages") and chunk.get("next") is None:
                for message in chunk.get("messages"):
                    append_and_display_message(message)


def initialize_messages(current_step: ExtendedStepType):
    _ = st.session_state.translator
    step_messages = {
        ExtendedStepType.SPECIFICATION: _("Hey there, What do you want to build?"),
        ExtendedStepType.DEPLOYMENT: _("Do you want to push the code to GitHub?[Y/N]"),
    }
    default_message = MessageContent(_).get_message()["execute"]
    message_text = step_messages.get(current_step, default_message)
    st.session_state["messages"] = [Message.create_human_message(message=message_text)]
