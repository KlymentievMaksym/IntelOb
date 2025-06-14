import streamlit as st

from .HelpFunc import create_audio_and_download_button
from .Process import process

def get_result_page():
    st.subheader("Original Melody")
    create_audio_and_download_button(st.session_state.melody, name="original_melody")
    st.subheader("Harmonized Melody")
    create_audio_and_download_button(st.session_state.result[1], arg=1, changed=True, name="harmonized_melody")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔙 Back to Upload"):
            st.session_state.step = "upload"
            st.rerun()
    with col2:
        if st.button("🔄 Restart"):
            process(st.session_state.melody)
            st.rerun()
    with col3:
        if st.button("📊 Fitness Function"):
            st.session_state.step = "fitness"
            st.rerun()
