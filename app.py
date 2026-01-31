import streamlit as st
from audio_recorder_streamlit import audio_recorder
from datetime import datetime
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from services.deepgram_service import (
    transcribe_audio_file,
    extract_readable_transcript,
    save_transcript_json,
    save_transcript_text,
)

from services.gemini_service import (
    extract_action_items,
    save_action_items,
)

from services.report_service import (
    generate_pdf,
    generate_excel,
)


# -------------------------------------------------
# Streamlit page setup
# -------------------------------------------------
st.set_page_config(page_title="Meeting Action-Item Generator ", layout="centered")
st.title("Meeting Audio Recorder")

# -------------------------------------------------
# Session state initialization
# -------------------------------------------------
if "audio_saved" not in st.session_state:
    st.session_state.audio_saved = False

if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

if "meeting_id" not in st.session_state:
    st.session_state.meeting_id = None

if "transcript_text" not in st.session_state:
    st.session_state.transcript_text = None

if "action_items" not in st.session_state:
    st.session_state.action_items = None

st.info("Click the mic → speak → click stop")

# -------------------------------------------------
# Audio recorder (browser mic)
# -------------------------------------------------
audio_bytes = audio_recorder(
    sample_rate=16000,
    pause_threshold=2.0,
    key="recorder",
)

# -------------------------------------------------
# Capture audio ONLY after recording stops
# -------------------------------------------------
if audio_bytes and not st.session_state.audio_saved:
    st.session_state.audio_bytes = audio_bytes
    st.session_state.audio_saved = True
    st.session_state.meeting_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# -------------------------------------------------
# Save audio exactly once
# -------------------------------------------------
if st.session_state.audio_saved and st.session_state.audio_bytes:
    os.makedirs("data/audio/raw", exist_ok=True)

    file_path = f"data/audio/raw/meeting_{st.session_state.meeting_id}.wav"

    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(st.session_state.audio_bytes)

    st.success("Recording saved successfully")
    st.code(file_path)

    st.audio(st.session_state.audio_bytes, format="audio/wav")

    # -------------------------------------------------
    # Deepgram transcription
    # -------------------------------------------------
    if st.button("Generate Transcript"):
        with st.spinner("Transcribing with Deepgram..."):
            response = transcribe_audio_file(file_path)

            json_path = save_transcript_json(
                response, st.session_state.meeting_id
            )

            transcript_text = extract_readable_transcript(response)

            text_path = save_transcript_text(
                transcript_text, st.session_state.meeting_id
            )

            st.session_state.transcript_text = transcript_text

        st.success("Transcription completed")
        st.caption(f"Saved JSON: {json_path}")
        st.caption(f"Saved Text: {text_path}")

# -------------------------------------------------
# Show transcript
# -------------------------------------------------
if st.session_state.transcript_text:
    st.subheader("Meeting Transcript")
    st.text_area(
        "Transcript",
        st.session_state.transcript_text,
        height=400
    )

    # -------------------------------------------------
    # Gemini action-item extraction
    # -------------------------------------------------
    if st.button("Generate Action Items"):
        with st.spinner("Extracting action items..."):
            action_data = extract_action_items(
                st.session_state.transcript_text
            )

            action_path = save_action_items(
                action_data,
                st.session_state.meeting_id
            )

            st.session_state.action_items = action_data

        st.success("Action items extracted")
        st.caption(f"Saved to {action_path}")

# -------------------------------------------------
# Show action items + report generation
# -------------------------------------------------
if st.session_state.action_items:
    st.subheader("Action Items (JSON)")
    st.json(st.session_state.action_items)

    st.divider()
    st.subheader("Generate Reports")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate PDF"):
            pdf_path = generate_pdf(
                st.session_state.action_items,
                st.session_state.meeting_id
            )
            st.success("PDF generated")
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "Download PDF",
                    f,
                    file_name="action_items.pdf",
                    mime="application/pdf"
                )

    with col2:
        if st.button("Generate Excel"):
            excel_path = generate_excel(
                st.session_state.action_items,
                st.session_state.meeting_id
            )
            st.success("Excel generated")
            with open(excel_path, "rb") as f:
                st.download_button(
                    "Download Excel",
                    f,
                    file_name="action_items.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

# -------------------------------------------------
# Reset workflow
# -------------------------------------------------
if st.button("Record another meeting"):
    st.session_state.audio_saved = False
    st.session_state.audio_bytes = None
    st.session_state.meeting_id = None
    st.session_state.transcript_text = None
    st.session_state.action_items = None

