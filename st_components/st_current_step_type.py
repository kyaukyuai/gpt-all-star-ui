import streamlit as st


def display_current_step_type(content: str):
    style = """
    <style>
        .fixed-component {
            z-index: 100;
            background-color: white;
            font-size: 16px;
            border-radius: 8px;
            position: fixed;
            bottom: 100px;
            right: 80px;
            width: 280px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid 1px #EEE;
            box-shadow: 0 1px 1px 1px rgba(51,51,51,0.1);
        }
    </style>
    """
    html_content = f'<p class="fixed-component">{content}</p>'
    st.markdown(style + html_content, unsafe_allow_html=True)
