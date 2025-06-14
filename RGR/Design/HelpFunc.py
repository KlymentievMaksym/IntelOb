import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from pydub import AudioSegment
import io
from Src.Melody import Melody


SAMPLING_RATE = 44100
DOWNLOAD_BUTTON_COUNT = 0
DOWNLOAD_BUTTON_KEY = "DOWNLOAD_BUTTON_KEY_{0}"


def play_sound():
    components.html(
        """
        <audio autoplay>
            <source src="https://assets.mixkit.co/sfx/preview/mixkit-correct-answer-tone-2870.mp3" type="audio/mpeg">
        </audio>
        """,
        height=0,
    )


def create_audio_and_download_button(melody: Melody, arg: int = 0, changed: bool = False, name: str = "original_melody"):
    # if st.session_state.pitches and np.all(np.isin(st.session_state.pitches, melody.pitches)):
    if st.session_state.pitches and not changed and arg < len(st.session_state.pitches):
        # arg = np.argwhere(np.isin(st.session_state.pitches, melody.pitches))[0][0]
        waveform = st.session_state.waveforms[arg]
        mp3_bytes = st.session_state.mp3_bytes[arg]
        midi_bytes = st.session_state.midi_bytes[arg]
    else:
        waveform = melody.to_midi().fluidsynth(fs=SAMPLING_RATE)
        waveform_int16 = np.int16(waveform * 32767)

        audio_segment = AudioSegment(
            waveform_int16.tobytes(),
            frame_rate=SAMPLING_RATE,
            sample_width=2,
            channels=1
        )

        mp3_bytes_io = io.BytesIO()
        midi_bytes_io = io.BytesIO()

        audio_segment.export(mp3_bytes_io, format="mp3")
        mp3_bytes = mp3_bytes_io.getvalue()

        melody.save(midi_bytes_io)
        midi_bytes = midi_bytes_io.getvalue()

        st.session_state.pitches.append(melody.pitches)
        st.session_state.waveforms.append(waveform)
        st.session_state.mp3_bytes.append(mp3_bytes)
        st.session_state.midi_bytes.append(midi_bytes)

    global DOWNLOAD_BUTTON_COUNT
    st.audio(waveform, format="audio/midi", sample_rate=SAMPLING_RATE, start_time=0)
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(label="Download Audio", data=mp3_bytes, file_name=f"{name}.mp3", mime="audio/mpeg", on_click='ignore', key=DOWNLOAD_BUTTON_KEY.format(DOWNLOAD_BUTTON_COUNT))
        DOWNLOAD_BUTTON_COUNT += 1
    with col2:
        st.download_button(label="Download MIDI", data=midi_bytes, file_name=f"{name}.mid", mime="audio/midi", on_click='ignore', key=DOWNLOAD_BUTTON_KEY.format(DOWNLOAD_BUTTON_COUNT))
        DOWNLOAD_BUTTON_COUNT += 1
