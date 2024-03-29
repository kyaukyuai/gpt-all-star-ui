import os

import streamlit as st

from st_components.st_session_states import ExtendedStepType

OPEN_AI = "OpenAI"
AZURE_OPEN_AI = "Azure OpenAI"


def get_project_dirs():
    project_base_dir = "projects/"
    return [
        d
        for d in os.listdir(project_base_dir)
        if os.path.isdir(os.path.join(project_base_dir, d))
    ]


def st_sidebar():
    with st.sidebar:
        project_dirs = get_project_dirs()

        if "project_name" not in st.session_state:
            st.session_state["project_name"] = ""

        project_options = project_dirs + ["New Project"]

        selected_project = st.selectbox(
            "Select or create a project:",
            project_options,
            index=(
                project_options.index(st.session_state["project_name"])
                if st.session_state["project_name"] in project_options
                else len(project_options) - 1
            ),
        )

        if selected_project == "New Project":
            st.session_state["project_name"] = st.text_input(
                "Enter a new project name:",
                value=(
                    st.session_state["project_name"]
                    if st.session_state["project_name"] not in project_dirs
                    else ""
                ),
                key="new_project_name",
            )
        else:
            st.session_state["project_name"] = selected_project

        st.session_state["step_type"] = st.selectbox(
            "Step Type",
            [
                ExtendedStepType.DEFAULT.name,
                ExtendedStepType.BUILD.name,
                ExtendedStepType.NONE.name,
            ],
        )

        st.divider()

        api_server = st.selectbox(
            "API Server",
            [OPEN_AI, AZURE_OPEN_AI],
        )

        if api_server == OPEN_AI:
            set_open_ai_credentials()
        elif api_server == AZURE_OPEN_AI:
            set_azure_open_ai_credentials()


def set_open_ai_credentials():
    expander = st.expander(
        label="Settings", expanded=(not st.session_state.get("chat_ready", False))
    )
    with expander:
        openai_key = st.text_input(
            "OpenAI Key:", type="password", value=st.secrets.get("OPENAI_API_KEY")
        )
        model_options = list(
            st.session_state.get("models", {}).get("openai", {}).keys()
        )
        model = st.selectbox(label="🔌 models", options=model_options, index=0)

        if st.button("Save", key="open_ai_save_model_configs") and openai_key:
            update_open_ai_environment(openai_key, model)
            st.session_state["chat_ready"] = True
            st.rerun()


def update_open_ai_environment(openai_key, model):
    os.environ["ENDPOINT"] = "OPENAI"
    os.environ["OPENAI_API_KEY"] = openai_key
    os.environ["OPENAI_API_MODEL_NAME"] = model


def set_azure_open_ai_credentials():
    expander = st.expander(
        label="Settings", expanded=(not st.session_state.get("chat_ready", False))
    )
    with expander:
        azure_openai_key = st.text_input(
            "Azure OpenAI Key:",
            type="password",
            value=st.secrets.get("AZURE_OPENAI_API_KEY"),
        )
        azure_endpoint = st.text_input(
            "Azure endpoint",
            placeholder="https://{your-resource-name}.openai.azure.com",
            value=st.secrets.get("AZURE_OPENAI_ENDPOINT"),
        )
        deployment_id = st.text_input(
            "Deployment ID",
            help="The deployment name you chose when you deployed the model.",
            value=st.secrets.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
        )
        if (
            st.button("Save", key="azure_open_ai_save_model_configs")
            and azure_openai_key
        ):
            update_azure_open_ai_environment(
                azure_openai_key, azure_endpoint, deployment_id
            )
            st.session_state["chat_ready"] = True
            st.rerun()


def update_azure_open_ai_environment(azure_openai_key, azure_endpoint, deployment_id):
    os.environ["ENDPOINT"] = "AZURE"
    os.environ["AZURE_OPENAI_API_KEY"] = azure_openai_key
    os.environ["AZURE_OPENAI_ENDPOINT"] = azure_endpoint
    os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = deployment_id
