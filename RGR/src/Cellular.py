import numpy as np
from time import time

from .Melody import Melody
from .Harmonizer import MIN_PITCH, MAX_PITCH
# MIN_PITCH, MAX_PITCH = 36, 84



def create_start_array(seconds: int, size: int, mutation_rate: float = 0.1):
    instruments = [["Standart", 0, False]]
    arange = np.arange(seconds, step=0.5)
    other_info = [[[100, start_time, start_time + duration] for start_time, duration in zip(np.random.choice(arange, replace=False if size < len(arange) else True, size=size), np.random.choice([1/8, 1/4, 1/2, 1], p=[0.1, 0.2, 0.4, 0.3], size=size))]]
    other_info = sorted(other_info, key=lambda x: [x[0][1], x[0][2]])
    pitches = [np.random.randint(MIN_PITCH, MAX_PITCH, size=size)]
    # pitches = [np.where(np.random.random(size) < mutation_rate, -1, np.random.randint(MIN_PITCH, MAX_PITCH, size=size))]

    return Melody(instruments, pitches, other_info)

def evolve(melody: Melody, mutation_rate: float = 0.1):
    counter = [0]*12
    for pitches in melody.pitches:  # A pitches for one isntrument
        for pitch in pitches:  # A pitch
            counter[pitch % 12] += 1
    main_note = np.argmax(counter)
    main_note_neighbors = np.array([main_note, (main_note+2) % 12, (main_note+4) % 12, (main_note+5) % 12, (main_note+7) % 12, (main_note+9) % 12, (main_note+11) % 12])

    dct = dict()
    for pitch_index in range(len(melody.pitches[0])):
        old_pitch = melody.pitches[0][pitch_index]
        if np.random.random() < mutation_rate:
            already_exist = dct.get(old_pitch, None)
            if not already_exist:
                values = np.array(range(old_pitch-2, old_pitch+3))

                mask = np.isin(values % 12, main_note_neighbors)
                probabilities = np.where(mask, 0.9 / np.count_nonzero(mask), 0.1 / np.count_nonzero(~mask))

                new_pitch = np.clip(np.random.choice(values, p=probabilities), MIN_PITCH, MAX_PITCH)
                dct[old_pitch] = new_pitch
                melody.pitches[0][pitch_index] = new_pitch
            else:
                melody.pitches[0][pitch_index] = already_exist
        elif np.random.random() < mutation_rate * 2:
            melody.pitches[0][pitch_index] = np.random.randint(MIN_PITCH, MAX_PITCH)
        else:
            melody.pitches[0][pitch_index] = old_pitch

    return melody


def cellular_automaton(seconds: int, size: int, generations: int = 100, mutation_rate: float = 0.1, progress_bar: object = None):
    time_smooth = max(10, int(0.01*generations))
    time_hist = np.zeros(time_smooth)
    time_index = 0

    prev_time = time()

    melody = create_start_array(seconds, size, mutation_rate=mutation_rate)
    for generation in range(generations):
        melody = evolve(melody, mutation_rate=mutation_rate)

        new_time = time()
        time_hist[time_index] = (new_time - prev_time) * (generations - generation - 1)
        prev_time = new_time

        time_index = (time_index + 1) % time_smooth
        time_left = np.mean(time_hist)

        if progress_bar:
            progress_bar.progress((generation + 1) / generations, text=f"🔎 Searching... {(time_left//3600):.0f}h {(time_left//60 % 60):.0f}m {(time_left % 60):.0f}s")

    return melody
