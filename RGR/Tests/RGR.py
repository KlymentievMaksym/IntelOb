import GeneticAlg as GA

import pretty_midi


def midi_to_note_duration_list(filename: str, use_rounded_durations=True):
    pm = pretty_midi.PrettyMIDI(filename)
    all_notes = []

    for instrument in pm.instruments:
        if instrument.is_drum:
            continue  # Skip percussion

        for note in instrument.notes:
            name = pretty_midi.note_number_to_name(note.pitch)
            duration = note.end - note.start
            if use_rounded_durations:
                duration = round(duration / pm.resolution)  # optional rough quantization
                if duration == 0:
                    duration = 1  # avoid zero-length
            all_notes.append((name, duration))

    # Sort by start time
    all_notes.sort(key=lambda x: x[1])  # not perfect — refine for polyphony

    return all_notes


# twinkle_twinkle_melody = midi_to_note_duration_list('./RGR/Beethoven-Moonlight-Sonata.mid')
# twinkle_twinkle_melody = midi_to_note_duration_list('./RGR/Undertale_-_Megalovania.mid')
# twinkle_twinkle_melody = midi_to_note_duration_list('./RGR/twinkle-twinkle-little-star.mid')
# """
twinkle_twinkle_melody = [
    ("C5", 1),
    ("C5", 1),
    ("G5", 1),
    ("G5", 1),
    ("A5", 1),
    ("A5", 1),
    ("G5", 2),  # Twinkle, twinkle, little star,
    ("F5", 1),
    ("F5", 1),
    ("E5", 1),
    ("E5", 1),
    ("D5", 1),
    ("D5", 1),
    ("C5", 2),  # How I wonder what you are!
    ("G5", 1),
    ("G5", 1),
    ("F5", 1),
    ("F5", 1),
    ("E5", 1),
    ("E5", 1),
    ("D5", 2),  # Up above the world so high,
    ("G5", 1),
    ("G5", 1),
    ("F5", 1),
    ("F5", 1),
    ("E5", 1),
    ("E5", 1),
    ("D5", 2),  # Like a diamond in the sky.
    ("C5", 1),
    ("C5", 1),
    ("G5", 1),
    ("G5", 1),
    ("A5", 1),
    ("A5", 1),
    ("G5", 2),  # Twinkle, twinkle, little star,
    ("F5", 1),
    ("F5", 1),
    ("E5", 1),
    ("E5", 1),
    ("D5", 1),
    ("D5", 1),
    ("C5", 2)  # How I wonder what you are!
]
# """
weights = {
    "chord_melody_congruence": 0.4,
    "chord_variety": 0.1,
    "harmonic_flow": 0.3,
    "functional_harmony": 0.2
}
chord_mappings = {
    "C": ["C", "E", "G"],
    "Dm": ["D", "F", "A"],
    "Em": ["E", "G", "B"],
    "F": ["F", "A", "C"],
    "G": ["G", "B", "D"],
    "Am": ["A", "C", "E"],
    "Bdim": ["B", "D", "F"]
}
preferred_transitions = {
    "C": ["G", "Am", "F"],
    "Dm": ["G", "Am"],
    "Em": ["Am", "F", "C"],
    "F": ["C", "G"],
    "G": ["Am", "C"],
    "Am": ["Dm", "Em", "F", "C"],
    "Bdim": ["F", "Am"]
}

# Instantiate objects for generating harmonization
melody_data = GA.Generator.MelodyData(twinkle_twinkle_melody)
fitness_evaluator = GA.FitnessFunc(
    melody_data=melody_data,
    weights=weights,
    chord_mappings=chord_mappings,
    preferred_transitions=preferred_transitions,
)
harmonizer = GA.GeneticHarmonizer(
    melody_data=melody_data,
    chords=list(chord_mappings.keys()),
    population_size=100,
    mutation_rate=0.05,
    fitness_func=fitness_evaluator,
)

# Generate chords with genetic algorithm
generated_chords = harmonizer.generate(iterations=1000)[1]

# Render to music21 score and show it
music21_score = GA.Generator.create_score(
    twinkle_twinkle_melody, generated_chords, chord_mappings
)
music21_score.show()
