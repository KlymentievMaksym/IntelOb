import pretty_midi
import numpy as np
import random
import tempfile
import os
from collections import Counter
import subprocess





SOUNDFONT_PATH = "D://Soundfonts//FluidR3_GM//FluidR3_GM.sf2"


def midi_to_wav(midi_path, wav_path):
    if not os.path.exists(SOUNDFONT_PATH):
        raise FileNotFoundError(f"SoundFont not found at {SOUNDFONT_PATH}")
    subprocess.run([
        "fluidsynth", "-ni", SOUNDFONT_PATH, midi_path,
        "-F", wav_path, "-r", "44100"
    ], check=True)