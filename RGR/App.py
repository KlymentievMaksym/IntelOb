import streamlit as st

import Design as des

st.session_state.pitches = []
st.session_state.waveforms = []
st.session_state.mp3_bytes = []
st.session_state.midi_bytes = []

st.set_page_config(page_title="Genetic MIDI Composer", layout="centered")
st.title("🎼 Music Composer")

des.get_settings()


if "step" not in st.session_state:
    st.session_state.dict = {
        "upload": des.get_upload_page,
        "result": des.get_result_page,
        "fitness": des.get_fitness_page,
    }
    st.session_state.step = "upload"

st.session_state.dict.get(st.session_state.step)()
