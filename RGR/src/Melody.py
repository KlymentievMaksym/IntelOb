import os
import numpy as np
import tempfile
import pretty_midi
from collections import Counter


class Melody:
    def __init__(self, instruments: list[list[str]] = None, pitches: list[np.ndarray[int]] = None, other_info: list[list[float]] = None):
        # self.notes = notes or []
        self.instruments = instruments
        self.pitches = pitches
        self.other_info = other_info

        self.instruments_count = len(instruments)
        self.notes_count = np.array([len(pitche) for pitche in pitches])
        self.notes_count_total = sum(self.notes_count)

    @staticmethod
    def from_midi(file_path):
        instruments = []
        pitches = []
        other_info = []
        try:
            print(f"[?] Loading MIDI file {file_path}")
            pm = pretty_midi.PrettyMIDI(file_path)
            print("[?] Available Instruments: ", [inst.name for inst in pm.instruments])
            # print("[?] Creating Instruments")
            for inst in pm.instruments:
                print(f"[?] Creating Instrument {inst.name}")
                notes = sorted([[note.velocity, note.pitch, note.start, note.end] for note in inst.notes], key=lambda x: x[2])

                instruments.append([inst.name, inst.program, inst.is_drum])
                pitches.append(np.array([note[1] for note in notes], dtype=int))
                other_info.append([[note[0], *note[2:]] for note in notes])

                # anotes.append([inst.name, inst.program, inst.is_drum, notes])
                # anotes[inst.name] = [notes, inst.program, inst.is_drum]
        except Exception as e:
            print(f"[!] Error loading MIDI file {file_path}: {e}")
            return Melody()
        return Melody(instruments, pitches, other_info)

    def to_midi(self):
        pm = pretty_midi.PrettyMIDI()
        for instrument, pitches, other_info in zip(self.instruments, self.pitches, self.other_info):
            print(f"[?] Loading Instrument {instrument[0]}")
            inst = pretty_midi.Instrument(program=instrument[1], is_drum=instrument[2], name=instrument[0])
            for pitch, info in zip(pitches, other_info):
                # if end - start > 0:
                inst.notes.append(pretty_midi.Note(velocity=info[0], pitch=pitch, start=info[1], end=info[2]))
            pm.instruments.append(inst)
        return pm

    def save(self, path):
        self.to_midi().write(path)

    def __repr__(self):
        return f"Melody(instruments={self.instruments_count}, notes={self.notes_count}, total={self.notes_count_total})"

    # def intervals(self):
    #     return [self.notes[i+1][0] - self.notes[i][0] for i in range(len(self.notes)-1)]

    # def key_signature(self):
    #     pitches = [p for p, _, _ in self.notes]
    #     counts = Counter(p % 12 for p in pitches)
    #     return counts.most_common(1)[0][0] if counts else 0

    # def play(self):
    #     midi = self.to_midi()
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp:
    #         midi.write(tmp.name)
    #         os.system(f"fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 {tmp.name} -F output.wav -r 44100 && aplay output.wav")
    #         os.remove(tmp.name)
    #         os.remove("output.wav")

    def __len__(self):
        return len(self.pitches)
