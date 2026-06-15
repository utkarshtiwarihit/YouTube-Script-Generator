import streamlit as st
from claude_handler import generate_script, estimate_read_time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Script Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF0000, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .subtitle {
        color: #888;
        font-size: 1rem;
        margin-top: -10px;
        margin-bottom: 24px;
    }
    .stat-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 12px 20px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .script-output {
        background: #1e1e2e;
        color: #cdd6f4;
        border-radius: 12px;
        padding: 24px;
        font-family: 'Courier New', monospace;
        font-size: 0.92rem;
        line-height: 1.7;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">🎬 YouTube Script Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Groq AI (Free ⚡) · Generate engaging scripts in seconds</p>', unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Script Settings")

    tone = st.selectbox(
        "Tone / Style",
        ["Energetic & Enthusiastic", "Educational & Informative",
         "Conversational & Casual", "Professional & Formal",
         "Humorous & Entertaining", "Inspirational & Motivational"],
        help="The overall vibe of your script"
    )

    duration = st.selectbox(
        "Video Length",
        ["Short (3-5 min)", "Medium (8-12 min)", "Long (15-20 min)"],
        index=1,
    )

    audience = st.text_input(
        "Target Audience",
        placeholder="e.g. beginners in Python, fitness enthusiasts",
        help="Who is this video for?"
    )

    extra = st.text_area(
        "Additional Instructions (optional)",
        placeholder="e.g. Include 3 real-life examples, avoid jargon, mention a product review...",
        height=100,
    )

    st.divider()
    st.caption("💡 Tip: Be specific with your topic for better results!")
    st.caption("📌 Scripts are streamed in real-time.")

# ── Main content ───────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input(
        "🎯 Video Topic",
        placeholder="e.g. 10 Python tips every beginner should know",
        label_visibility="visible",
    )
with col2:
    st.write("")  # spacing
    st.write("")
    generate_btn = st.button("✨ Generate Script", use_container_width=True, type="primary")

st.divider()

# ── Generation ─────────────────────────────────────────────────────────────────
if generate_btn:
    if not topic.strip():
        st.warning("⚠️ Please enter a video topic first.")
    else:
        st.subheader("📝 Your Script")

        # Streaming placeholder
        script_placeholder = st.empty()
        full_script = ""

        with st.spinner("Claude is writing your script..."):
            for chunk in generate_script(
                topic=topic,
                tone=tone,
                duration=duration,
                audience=audience if audience else "general YouTube viewers",
                extra=extra,
            ):
                full_script += chunk
                script_placeholder.markdown(full_script + "▌")

        # Final render (remove cursor)
        script_placeholder.markdown(full_script)

        # ── Stats ──────────────────────────────────────────────────────────────
        st.divider()
        c1, c2, c3 = st.columns(3)
        word_count = len(full_script.split())
        with c1:
            st.metric("📄 Word count", f"{word_count:,}")
        with c2:
            st.metric("🎙️ Est. speak time", estimate_read_time(full_script))
        with c3:
            st.metric("🎯 Tone", tone.split(" ")[0])

        # ── Download ───────────────────────────────────────────────────────────
        st.divider()
        clean_topic = "".join(c for c in topic if c.isalnum() or c in " _-").strip()[:40]
        filename = f"script_{clean_topic.replace(' ', '_')}.txt"

        download_content = f"""YouTube Script
==============
Topic    : {topic}
Tone     : {tone}
Duration : {duration}
Audience : {audience or "General viewers"}
Words    : {word_count}
Read time: {estimate_read_time(full_script)}

{"=" * 60}

{full_script}
"""
        st.download_button(
            label="⬇️ Download Script (.txt)",
            data=download_content,
            file_name=filename,
            mime="text/plain",
            use_container_width=True,
        )

        # Save to session state for re-display
        st.session_state["last_script"] = full_script
        st.session_state["last_topic"] = topic

# ── Show previous script if page reloads ──────────────────────────────────────
elif "last_script" in st.session_state and not generate_btn:
    st.info(f"📌 Previously generated script for: **{st.session_state['last_topic']}**")
    st.markdown(st.session_state["last_script"])

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center; padding: 60px 0; color: #aaa;">
        <div style="font-size: 3rem">🎬</div>
        <p style="font-size: 1.1rem; margin-top: 12px;">Enter a topic and hit <strong>Generate Script</strong> to get started</p>
        <p style="font-size: 0.9rem;">Your script will stream here in real-time</p>
    </div>
    """, unsafe_allow_html=True)
