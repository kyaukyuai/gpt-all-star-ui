import html
import re

import streamlit as st


def format_message(text):
    text_blocks = re.split(r"```[\s\S]*?```", text)
    code_blocks = re.findall(r"```([\s\S]*?)```", text)

    text_blocks = [html.escape(block) for block in text_blocks]

    formatted_text = ""
    for i in range(len(text_blocks)):
        formatted_text += text_blocks[i].replace("\n", "<br>")
        if i < len(code_blocks):
            formatted_text += f"""
            <pre style="white-space: pre-wrap; word-wrap: break-word;"><code>{html.escape(code_blocks[i])}</code></pre>
            """

    return formatted_text


def display_message(text, is_user=False, is_df=False):
    if is_user:
        avatar_url = "app/static/user.png"
        message_alignment = "flex-end"
        message_bg_color = "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)"
        avatar_class = "user-avatar"
        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px; font-family: ui-monospace;">
                        {text} \n </div>
                    <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
                </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        avatar_url = "app/static/user.png"
        message_alignment = "flex-start"
        message_bg_color = "#71797E"
        avatar_class = "bot-avatar"

        if is_df:
            st.write(
                f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                        <img src="https://pbs.twimg.com/profile_images/1274363897676521474/qgbqYYuV_400x400.jpg" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
                    </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(text)
            return
        else:
            text = format_message(text)

        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px; font-family: ui-monospace;">
                        {text} \n </div>
                </div>
            """,
            unsafe_allow_html=True,
        )


def _append_chat_history(question, answer):
    st.session_state.history.append((question, answer))


def append_message(content, role="assistant"):
    st.session_state.messages.append({"role": role, "content": content})
    if role != "data":
        _append_chat_history(st.session_state.messages[-2]["content"], content)
