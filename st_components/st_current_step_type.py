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
            width: 240px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid 1px #4638e4;
            box-shadow: 0 1px 1px 0 #4638e4;
        }
    </style>
    """
    html_content = f'<p class="fixed-component">{content}</p>'
    st.markdown(style + html_content, unsafe_allow_html=True)
