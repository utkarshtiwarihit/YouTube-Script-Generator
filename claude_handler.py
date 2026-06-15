from groq import Groq
import streamlit as st
from prompts import SYSTEM_PROMPT, build_script_prompt

GROQ_MODEL = "llama-3.3-70b-versatile"


def get_client() -> Groq:
    """Initialize Groq client using Streamlit secrets."""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        st.error("⚠️ API key not found. Add GROQ_API_KEY to your Streamlit secrets.")
        st.stop()
    return Groq(api_key=api_key)


def generate_script(topic: str, tone: str, duration: str, audience: str, extra: str):
    """Stream a YouTube script from Groq and yield text chunks."""
    client = get_client()
    prompt = build_script_prompt(topic, tone, duration, audience, extra)

    stream = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=4096,
        temperature=0.8,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def estimate_read_time(text: str) -> str:
    """Rough speaking-speed estimate: ~130 words per minute."""
    words = len(text.split())
    minutes = words / 130
    if minutes < 1:
        return "< 1 min"
    return f"~{int(round(minutes))} min"


def estimate_read_time(text: str) -> str:
    """Rough speaking-speed estimate: ~130 words per minute."""
    words = len(text.split())
    minutes = words / 130
    if minutes < 1:
        return "< 1 min"
    return f"~{int(round(minutes))} min"
