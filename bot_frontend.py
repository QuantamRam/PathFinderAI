"""
PathFinder-AI – Streamlit Front-End
Dark mode, no sidebar, zero legacy branding.
"""
import streamlit as st
import requests
from streamlit_chat import message

# ---------- CONFIG ----------
st.set_page_config(
    page_title="PathFinder AI",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- THEMING ----------
st.markdown(
    """
    <style>
        body {background:#0e0e16;color:#c9f7ff}
        .stChatFloatingInputContainer {bottom:20px;}
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SESSION ----------
if "generated" not in st.session_state:
    st.session_state.generated = ["🌌 Hi explorer—what career path intrigues you?"]
if "past" not in st.session_state:
    st.session_state.past = []

# ---------- HELPER ----------
API_URL = "http://localhost:8000/chat"  # FastAPI endpoint

def get_bot_reply(user_text: str) -> str:
    try:
        r = requests.post(API_URL, json={"text": user_text}, timeout=5)
        return r.json().get("reply", "No reply 😵")
    except Exception:
        return "Back-end unreachable—please run `uvicorn backend.main:app --reload`"

# ---------- MAIN ----------
st.title("🌠 PathFinder AI")
st.caption("Synthwave career compass powered by DistilBERT + FAISS")

# User input
user_input = st.chat_input("Ask about degrees, salaries, or next moves…")
if user_input:
    st.session_state.past.append(user_input)
    st.session_state.generated.append(get_bot_reply(user_input))

# Render chat
for i, (user, bot) in enumerate(zip(st.session_state.past, st.session_state.generated)):
    message(user, is_user=True, key=f"user_{i}")
    message(bot, key=f"bot_{i}")