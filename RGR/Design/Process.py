from Src.Melody import Melody
from Src.Harmonizer import GAHarmonizer
from Src.FitnessFunc import FitnessFunc
import streamlit as st
from .HelpFunc import play_sound

def process(melody: Melody):
    weights = {
        "exactly_like_original": st.session_state.exactly_like_original,
        "chord_variety": st.session_state.chord_variety,
        "chord_not_repeating_in_row": st.session_state.repeating_in_raw,
        "chord_not_repeating_very_much": st.session_state.repeating_very_much,
    }

    my_bar = st.progress(0, text="🔎 Searching for best melody...")

    fitness_func = FitnessFunc(melody, weights)
    harmonizer = GAHarmonizer(melody, st.session_state.population, st.session_state.mutation_rate, fitness_func)

    result = harmonizer.evolve(st.session_state.generations, my_bar)

    st.session_state.melody = melody
    st.session_state.result = result

    st.session_state.harmonizer = harmonizer
    if st.session_state.play_sound:
        play_sound()
