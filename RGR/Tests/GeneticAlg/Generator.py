
from dataclasses import dataclass
import music21


@dataclass(frozen=True)
class MelodyData:
    """
    A data class representing the data of a melody.

    This class encapsulates the details of a melody including its notes, total
    duration, and the number of bars. The notes are represented as a list of
    tuples, with each tuple containing a pitch and its duration. The total
    duration and the number of bars are computed based on the notes provided.

    Attributes:
        notes (list of tuples): List of tuples representing the melody's notes.
            Each tuple is in the format (pitch, duration).
        duration (int): Total duration of the melody, computed from notes.
        number_of_bars (int): Total number of bars in the melody, computed from
            the duration assuming a 4/4 time signature.

    Methods:
        __post_init__: A method called after the data class initialization to
            calculate and set the duration and number of bars based on the
            provided notes.
    """

    notes: list
    duration: int = None  # Computed attribute
    number_of_bars: int = None  # Computed attribute

    def __post_init__(self):
        object.__setattr__(
            self, "duration", sum(duration for _, duration in self.notes)
        )
        object.__setattr__(self, "number_of_bars", self.duration // 4)


def create_score(melody, chord_sequence, chord_mappings):
    """
    Create a music21 score with a given melody and chord sequence.

    Args:
        melody (list): A list of tuples representing notes in the format
            (note_name, duration).
        chord_sequence (list): A list of chord names.

    Returns:
        music21.stream.Score: A music score containing the melody and chord
            sequence.
    """
    # Create a Score object
    score = music21.stream.Score()

    # Create the melody part and add notes to it
    melody_part = music21.stream.Part()
    for note_name, duration in melody:
        melody_note = music21.note.Note(note_name, quarterLength=duration)
        melody_part.append(melody_note)

    # Create the chord part and add chords to it
    chord_part = music21.stream.Part()
    current_duration = 0  # Track the duration for chord placement

    for chord_name in chord_sequence:
        # Translate chord names to note lists
        chord_notes_list = chord_mappings.get(chord_name, [])
        # Create a music21 chord
        chord_notes = music21.chord.Chord(
            chord_notes_list, quarterLength=4
        )  # Assuming 4/4 time signature
        chord_notes.offset = current_duration
        chord_part.append(chord_notes)
        current_duration += 4  # Increase by 4 beats

    # Append parts to the score
    score.append(melody_part)
    score.append(chord_part)

    return score
