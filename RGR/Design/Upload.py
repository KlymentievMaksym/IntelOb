import streamlit as st
import io
from Src.Melody import Melody
from .HelpFunc import create_audio_and_download_button
from .Process import process
from Src.Cellular import cellular_automaton


def get_upload_page():
    uploaded_file = st.file_uploader("Upload a MIDI file", type=["mid", "midi"], accept_multiple_files=False)

    if uploaded_file:
        file = io.BytesIO(uploaded_file.read())
        melody = Melody.from_midi(file)
    else:
        seconds = st.number_input("Seconds", value=10, min_value=1, max_value=60)
        size = st.number_input("Size", value=20, min_value=1, max_value=1000)
        progress_bar = st.progress(0, text="🔎 Searching for best melody...")
        melody = cellular_automaton(seconds, size, st.session_state.generations, st.session_state.mutation_rate, progress_bar)

    if not melody:
        st.error("No notes found in the uploaded MIDI file.")
    else:
        st.success(f"Loaded melody with {melody.instruments_count} instruments and {melody.notes_count_total} notes in total.")
        create_audio_and_download_button(melody)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎶 Start Evolution"):
            process(melody)
            st.success("✅ Evolution complete!")

            st.session_state.step = "result"
            st.rerun()
    with col2:
        if st.button("🔄 Restart"):
            st.rerun()
