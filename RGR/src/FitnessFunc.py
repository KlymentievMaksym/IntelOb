import numpy as np

from collections import defaultdict

from .Melody import Melody
MIN_PITCH, MAX_PITCH = 36, 84


class FitnessFunc:
    def __init__(self, target_true: Melody, weights: dict):
        self.target_true = target_true
        # self.target_pred = target_pred , target_pred: Melody
        self.weights = weights

    def evaluate(self, target_pred: Melody):
        return sum(self.weights[func] * getattr(self, f"_{func}", 0)(target_pred) for func in self.weights)

    def __call__(self, target_pred: Melody):
        return self.evaluate(target_pred)

    def _exactly_like_original(self, target_pred: Melody):
        score = 0
        for pitches_true, pitches_pred in zip(self.target_true.pitches, target_pred.pitches):
            mse = np.sqrt(np.mean((pitches_true - pitches_pred)**2))
            score += mse
        return score  #/ self.target_true.instruments_count

    def _chord_variety(self, target_pred: Melody):
        score = 0
        for pitches_true, pitches_pred in zip(self.target_true.pitches, target_pred.pitches):
            unique_pitches_true = np.unique(pitches_true)
            unique_pitches_pred = np.unique(pitches_pred)
            score += abs(len(unique_pitches_true) / len(pitches_true) - len(unique_pitches_pred) / len(pitches_pred))
        return score  #/ target_pred.instruments_count

    def _chord_not_repeating_in_row(self, target_pred: Melody):
        score = 0
        for pitches_pred in target_pred.pitches:
            prev_pitch = None
            for pitch in pitches_pred:
                if pitch == prev_pitch:
                    score += 1
                prev_pitch = pitch
        return score

    def _chord_not_repeating_very_much(self, target_pred: Melody):
        score = 0
        for pitches_pred in target_pred.pitches:
            prev_pitch = None
            for pitch in pitches_pred:
                if pitch == prev_pitch:
                    score += 1
                else:
                    score = 0
                prev_pitch = pitch
                if score > 3:
                    return score * 100
        return score


    def _harmonic_flow(self, target_pred: Melody):
        score = 0
        # for instrument_pred in target_pred.notes:
        #     score = 0
        #     notes = instrument_pred[-1]
        #     total_chords = len(notes)
        #     for i in range(total_chords - 1):
        #         current_chord = notes[i]
        #         next_chord = notes[i + 1]
        #         score += self._preferred_transitions_pitch(current_chord[1], next_chord[1]) + self._preferred_transitions_velocity(current_chord[0], next_chord[0])
        #     summ += score / ((total_chords - 1) * 2)
        return score  #/ target_pred.instruments_count

    def _functional_harmony(self, target_pred: Melody):
        summ = 0
        # for instrument_pred in target_pred.notes:
        #     score = 0
        #     chord_sequence = instrument_pred[-1]
        #     if chord_sequence[0][1] % 12 == 0 or chord_sequence[0][1] in [45, 48, 52, 57, 60, 64, 69, 72, 76, 81, 84]:
        #         score += 1
        #     if chord_sequence[-1][1] % 12 == 0:
        #         score += 1
        #     F_major = {5, 9, 0}   # F, A, C
        #     G_major = {7, 11, 2}  # G, B, D

        #     groups = defaultdict(set)
        #     for vel, pitch, start, end in chord_sequence:
        #         groups[start].add(pitch % 12)

        #     # Check for F and G major chords
        #     has_f = any(F_major.issubset(pitches) for pitches in groups.values())
        #     has_g = any(G_major.issubset(pitches) for pitches in groups.values())

        #     if has_f and has_g:
        #         score += 1
        #     summ += score / 3
        return summ  #/ target_pred.instruments_count

    def _preferred_transitions_pitch(self, pitch, pitch_next):
        step_choices = np.arange(9)  # 0 to 8 semitones
        # affordable_pitches = np.intersect1d(np.ones_like(step_choices) * pitch + step_choices, np.ones_like(step_choices) * pitch - step_choices)
        # print("[Preferred Transitions] Current Pitch: ", pitch, "Next Pitch: ", pitch_next)
        affordable_pitches = np.intersect1d(pitch + step_choices, pitch - step_choices)
        if pitch_next == pitch:
            return 0.9
        elif pitch_next in affordable_pitches:
            step_score = [0.2, 0.2, 0.5, 1, 1, 1, 1, 1, 0.5, 1, 0.5, 1, 1, 1, 1, 1, 0.5, 0.2, 0.2]
            return step_score[affordable_pitches.tolist().index(pitch_next)]
        return 0
        # step = np.random.choice(step_choices, p=step_probs)
        # direction = np.random.choice([-1, 1])
        # new_pitch = pitch + direction * step
        # return int(np.clip(new_pitch, MIN_PITCH, MAX_PITCH))
