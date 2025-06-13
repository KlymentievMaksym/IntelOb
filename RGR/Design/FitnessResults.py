import streamlit as st
import matplotlib.pyplot as plt
from .Process import process


def get_fitness_page():
    st.subheader("Fitness Function")
    st.subheader("📈 Fitness Evolution")
    fig, ax = plt.subplots()
    ax.plot(st.session_state.harmonizer.fitness_history)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.set_title("Fitness over Time")
    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔙 Back to Upload"):
            st.session_state.step = "upload"
            st.rerun()
    with col2:
        if st.button("🔙 Back to Result"):
            st.session_state.step = "result"
            st.rerun()
    with col3:
        if st.button("🔄 Restart"):
            process(st.session_state.melody)
            st.rerun()
