import streamlit as st
from .Process import process

import Src.Harmonizer as Hz
import Src.Cellular as Cell


def get_settings():
    with st.sidebar:
        st.session_state.play_sound = st.checkbox("Play sound after evolution", value=True)
        st.session_state.autoupdate = st.checkbox("Autoupdate", value=False)

        generations = st.slider("Number of generations", 10, 1000, 100, step=10)
        population = st.slider("Population size", 10, 200, 10, step=5)
        mutation_rate = st.slider("Mutation rate", 0.0, 1.0, 0.25, step=0.05)

        exactly_like_original = st.slider("Exactly Like Original", 0.0, 1.0, 0.80, step=0.05)
        chord_variety = st.slider("Chord Variety", 0.0, 1.0, 0.5, step=0.05)

        repeating_in_raw = st.slider("Repeating in Raw", 0.0, 1.0, 0.10, step=0.05)
        repeating_very_much = st.slider("Repeating Very Much", 0.0, 1.0, 0.05, step=0.05)

        Hz.MIN_PITCH, Hz.MAX_PITCH = st.slider("Pitch range", 0, 127, (36, 84), step=1)
        Cell.MIN_PITCH, Cell.MAX_PITCH = Hz.MIN_PITCH, Hz.MAX_PITCH

        st.session_state.lst = ["generations", "population", "mutation_rate", "exactly_like_original", "chord_variety", "repeating_in_raw", "repeating_very_much"]
        st.session_state.lst_prev = ["prev_" + name for name in st.session_state.lst]

        for i in range(len(st.session_state.lst)):
            st.session_state[st.session_state.lst[i]] = locals()[st.session_state.lst[i]]

        for i in range(len(st.session_state.lst_prev)):
            if st.session_state.lst_prev[i] not in st.session_state:
                st.session_state[st.session_state.lst_prev[i]] = st.session_state[st.session_state.lst[i]]

        def check_update():
            for i in range(len(st.session_state.lst)):
                if st.session_state[st.session_state.lst[i]] != st.session_state[st.session_state.lst_prev[i]]:
                    return True
            return False

    if st.session_state.autoupdate:
        if (st.session_state.step != "upload" and check_update()):
            process(st.session_state.melody)
            for i in range(len(st.session_state.lst_prev)):
                st.session_state[st.session_state.lst_prev[i]] = st.session_state[st.session_state.lst[i]]
            st.rerun()
