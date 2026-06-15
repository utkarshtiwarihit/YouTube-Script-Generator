SYSTEM_PROMPT = """You are an expert YouTube script writer with years of experience creating 
viral, engaging content across all niches. You understand pacing, hooks, storytelling, and 
how to keep viewers watching till the end."""

def build_script_prompt(topic: str, tone: str, duration: str, audience: str, extra: str) -> str:
    duration_map = {
        "Short (3-5 min)": "3-5 minute video (~450-750 words)",
        "Medium (8-12 min)": "8-12 minute video (~1200-1800 words)",
        "Long (15-20 min)": "15-20 minute video (~2250-3000 words)",
    }
    word_guide = duration_map.get(duration, "8-12 minute video (~1200-1800 words)")

    return f"""Write a complete YouTube script for the following:

**Topic:** {topic}
**Tone:** {tone}
**Target Audience:** {audience}
**Video Length:** {word_guide}
{"**Additional Instructions:** " + extra if extra else ""}

Structure the script with these clearly labelled sections:

## 🎬 HOOK (first 15 seconds)
Start with a bold, attention-grabbing opening line that makes viewers NEED to keep watching.

## 📌 INTRO (30-60 seconds)
Briefly introduce yourself/channel (generic placeholder), tease what the viewer will learn.

## 📖 MAIN CONTENT
Break into clear sections with timestamps hints like [00:30], [02:00], etc.
Use natural conversational language. Include:
- Key points with examples
- Analogies or stories where helpful
- Engagement prompts like "comment below if..."

## 🎯 CALL TO ACTION
Encourage likes, subscribes, and comments. Tease the next video.

## 🔚 OUTRO (15-30 seconds)
Warm, memorable sign-off.

---
Write in a {tone.lower()} tone. Make it feel natural to speak aloud, not like an essay.
Use [B-ROLL: description] tags to suggest visuals where appropriate.
"""
