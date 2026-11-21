
import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="Smart Notes Organizer",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Smart Notes Organizer")
st.write(
    "Transform scattered notes into organized "
    "topic-wise study material using AI."
)

st.divider()

# User input
notes = st.text_area(
    "Paste your notes here:",
    height=250,
    placeholder="Paste notes from different subjects or sources..."
)

if st.button("✨ Organize My Notes", use_container_width=True):

    if not notes.strip():
        st.warning("Please paste some notes first.")

    elif not API_KEY:
        st.error("Gemini API key not found. Check your .env file.")

    else:
        try:
            with st.spinner("AI is organizing your notes..."):

                client = genai.Client(api_key=API_KEY)

                prompt = f"""
                You are an intelligent Smart Notes Organizer.

                Organize the student's scattered notes by topic.

                Instructions:
                1. Read all notes carefully.
                2. Identify related concepts and topics.
                3. Group similar information together.
                4. Generate clear headings.
                5. Use bullet points.
                6. Remove unnecessary repetition.
                7. Preserve important facts and details.
                8. Do not invent information.
                9. Use clean Markdown formatting.

                Notes:
                {notes}

                Return organized notes with headings and bullet points.
                """

                response = None

                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=prompt,
                            config={
                                "http_options": {
                                    "timeout": 30000
                                }
                            }
                        )
                        break

                    except Exception:
                        if attempt == 2:
                            raise
                        time.sleep(3)

                if not response or not response.text:
                    raise ValueError("The AI returned an empty response.")

                organized_notes = response.text

            st.success("Your notes have been organized!")
            st.subheader("📚 Organized Notes")
            st.markdown(organized_notes)

            st.download_button(
                label="⬇️ Download Organized Notes",
                data=organized_notes,
                file_name="organized_notes.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.divider()

st.caption(
    "Smart Notes Organizer | GenAI Mini Project | Roll No. 48"
)


