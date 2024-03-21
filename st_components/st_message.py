import html
import json
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


def display_user_message(text):
    avatar_url = "app/static/user.png"
    message_alignment = "flex-end"
    message_bg_color = "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)"
    avatar_class = "user-avatar"
    st.write(
        f"""
                <div style="display: flex; align-items: center; justify-content: {message_alignment};">
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 12px; font-family: ui-monospace;">
                        {text} \n </div>
                    <div style="display: flex; align-items: center; flex-flow: column; height: 100px; justify-content: space-around;">
                        <img src="{avatar_url}" class="{avatar_class}" alt="avatar"/>
                        <p style="font-size: 12px; font-family: ui-monospace;">You</p>
                    </div>
                </div>
            """,
        unsafe_allow_html=True,
    )


def display_agent_message(name, text):
    # Load agents.json to find the matching avatar for the given name
    with open("agents.json", "r") as file:
        agents = json.load(file)
    agent_info = next((agent for agent in agents if agent["name"] == name), None)
    if agent_info and "avatar" in agent_info and "color" in agent_info:
        avatar_url = agent_info["avatar"]
        message_bg_color = agent_info["color"]
    else:
        avatar_url = "app/static/user.png"
        message_bg_color = "#71797E"

    message_alignment = "flex-start"
    avatar_class = "bot-avatar"
    text = format_message(text)
    st.write(
        f"""
                <div style="display: flex; align-items: center; justify-content: {message_alignment};">
                    <div style="display: flex; align-items: center; flex-flow: column; height: 100px; justify-content: space-around; margin-right: 10px;">
                        <img src="{avatar_url}" class="{avatar_class}" alt="avatar" />
                        <p style="font-size: 12px; font-family: ui-monospace;">{name}</p>
                    </div>
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 12px; font-family: ui-monospace;">
                        {text} \n </div>
                </div>
            """,
        unsafe_allow_html=True,
    )


def display_copilot_message(text):
    avatar_url = "app/static/copilot.png"
    message_alignment = "flex-start"
    message_bg_color = "#71797E"
    avatar_class = "bot-avatar"
    text = format_message(text)
    st.write(
        f"""
                <div style="display: flex; align-items: center; justify-content: {message_alignment};">
                    <div style="display: flex; align-items: center; flex-flow: column; height: 100px; justify-content: space-around; margin-right: 10px;">
                        <img src="{avatar_url}" class="{avatar_class}" alt="avatar" />
                        <p style="font-size: 12px; font-family: ui-monospace;">Copilot</p>
                    </div>
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 12px; font-family: ui-monospace;">
                        {text} \n </div>
                </div>
            """,
        unsafe_allow_html=True,
    )
