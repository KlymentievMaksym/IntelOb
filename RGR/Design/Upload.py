import streamlit as st
import io
from Src.Melody import Melody
from .HelpFunc import create_audio_and_download_button
from .Process import process

def get_upload_page():
    uploaded_file = st.file_uploader("Upload a MIDI file", type=["mid", "midi"], accept_multiple_files=False)

    if uploaded_file:
        file = io.BytesIO(uploaded_file.read())
        melody = Melody.from_midi(file)

        if not melody:
            st.error("No notes found in the uploaded MIDI file.")
        else:
            st.success(f"Loaded melody with {melody.instruments_count} instruments and {melody.notes_count_total} notes in total.")

            create_audio_and_download_button(melody)

            if st.button("🎶 Start Evolution"):
                process(melody)
                st.success("✅ Evolution complete!")

                st.session_state.step = "result"
                st.rerun()
