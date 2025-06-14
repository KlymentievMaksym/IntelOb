import numpy as np

from .Melody import Melody


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
            # mse = np.sum((pitches_true - pitches_pred)**2)
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
