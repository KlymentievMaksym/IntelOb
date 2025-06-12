import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from src.Melody import Melody
from pydub import AudioSegment
import matplotlib.pyplot as plt
from src.Harmonizer import GAHarmonizer
from src.FitnessFunc import FitnessFunc
# from RGR.src.music_ga import Melody, GAComposer, midi_to_wav
import os
import io

SAMPLING_RATE = 44100


def play_sound():
    components.html(
        """
        <audio autoplay>
            <source src="https://assets.mixkit.co/sfx/preview/mixkit-correct-answer-tone-2870.mp3" type="audio/mpeg">
        </audio>
        """,
        height=0,
    )


st.set_page_config(page_title="Genetic MIDI Composer", layout="centered")
st.title("🎼 Genetic Algorithm Music Composer")

uploaded_file = st.file_uploader("Upload a MIDI file", type=["mid", "midi"], accept_multiple_files=False)

with st.sidebar:
    generations = st.slider("Number of generations", 10, 2000, 10, step=10)
    population = st.slider("Population size", 10, 1000, 10, step=5)
    mutation_rate = st.slider("Mutation rate", 0.0, 1.0, 0.1, step=0.05)

    exactly_like_original = st.slider("Exactly Like Original", 0.0, 1.0, 1.0, step=0.05)
    chord_variety = st.slider("Chord Variety", 0.0, 1.0, 1.0, step=0.05)
    harmonic_flow = st.slider("Harmonic Flow", 0.0, 1.0, 0.0, step=0.05)
    functional_harmony = st.slider("Functional Harmony", 0.0, 1.0, 0.0, step=0.05)

if uploaded_file:
    path_temp = os.path.dirname(__file__) + "/temp/input.mid"
    with open(path_temp, "wb") as f:
        f.write(uploaded_file.read())

    melody = Melody.from_midi(path_temp)

    if not melody:
        st.error("No notes found in the uploaded MIDI file.")
    else:
        st.success(f"Loaded melody with {melody.instruments_count} instruments and {melody.notes_count_total} notes in total.")

        waveform = melody.to_midi().fluidsynth(fs=SAMPLING_RATE)
        st.audio(waveform, format="audio/midi", sample_rate=SAMPLING_RATE, start_time=0)

        if st.button("🎶 Start Evolution"):
            # with st.status("🔎 Searching for best melody..."):
            weights = {
                # "chord_melody_congruence": 0.4,
                "exactly_like_original": exactly_like_original,
                "chord_variety": chord_variety,
                "harmonic_flow": harmonic_flow,
                "functional_harmony": functional_harmony
            }
            my_bar = st.progress(0, text="🔎 Searching for best melody...")  #
            fitness_func = FitnessFunc(melody, weights)
            harmonizer = GAHarmonizer(melody, population, mutation_rate, fitness_func)
            result = harmonizer.evolve(generations, my_bar)
            # composer = GAComposer(melody, population, generations)
            # result = composer.evolve()
            play_sound()
            st.success("✅ Evolution complete!")
            midi_object = result[1].to_midi()
            waveform = midi_object.fluidsynth(fs=SAMPLING_RATE)
            waveform_int16 = np.int16(waveform * 32767)

            # Create MP3 from raw waveform
            audio_segment = AudioSegment(
                waveform_int16.tobytes(),
                frame_rate=SAMPLING_RATE,
                sample_width=2,  # 2 bytes = 16-bit audio
                channels=1
            )

            st.audio(waveform, format="audio/midi", sample_rate=SAMPLING_RATE, start_time=0)

            mp3_bytes_io = io.BytesIO()
            audio_segment.export(mp3_bytes_io, format="mp3")
            mp3_bytes = mp3_bytes_io.getvalue()

            st.download_button(label="Download Audio", data=mp3_bytes, file_name="harmonized_melody.mp3", mime="audio/midi", on_click='ignore')

            st.subheader("📈 Fitness Evolution")
            fig, ax = plt.subplots()
            ax.plot(harmonizer.fitness_history)
            ax.set_xlabel("Generation")
            ax.set_ylabel("Fitness")
            ax.set_title("Fitness over Time")
            st.pyplot(fig)
