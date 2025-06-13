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


def create_audio_and_download_button(melody: Melody):
    waveform = melody.to_midi().fluidsynth(fs=SAMPLING_RATE)
    waveform_int16 = np.int16(waveform * 32767)

    audio_segment = AudioSegment(
        waveform_int16.tobytes(),
        frame_rate=SAMPLING_RATE,
        sample_width=2,
        channels=1
    )

    mp3_bytes_io = io.BytesIO()
    audio_segment.export(mp3_bytes_io, format="mp3")
    mp3_bytes = mp3_bytes_io.getvalue()


    global DOWNLOAD_BUTTON_COUNT
    st.audio(waveform, format="audio/midi", sample_rate=SAMPLING_RATE, start_time=0)
    st.download_button(label="Download Audio", data=mp3_bytes, file_name="harmonized_melody.mp3", mime="audio/mpeg", on_click='ignore', key=DOWNLOAD_BUTTON_KEY.format(DOWNLOAD_BUTTON_COUNT))
    DOWNLOAD_BUTTON_COUNT += 1
