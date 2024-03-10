import os

import streamlit as st

OPEN_AI = "OpenAI"
AZURE_OPEN_AI = "Azure OpenAI"


def st_sidebar():
    with st.sidebar:
        api_server = st.selectbox(
            "Your API Server",
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
        openai_key = st.text_input("OpenAI Key:", type="password")
        model_options = list(
            st.session_state.get("models", {}).get("openai", {}).keys()
        )
        model = st.selectbox(label="🔌 models", options=model_options, index=0)

        if st.button("Save Changes 🚀", key="open_ai_save_model_configs") and openai_key:
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
        azure_openai_key = st.text_input("Azure OpenAI Key:", type="password")
        azure_endpoint = st.text_input(
            "Azure endpoint",
            placeholder="https://{your-resource-name}.openai.azure.com",
        )
        deployment_id = st.text_input(
            "Deployment ID",
            help="The deployment name you chose when you deployed the model.",
        )
        if (
            st.button("Save Changes 🚀", key="azure_open_ai_save_model_configs")
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