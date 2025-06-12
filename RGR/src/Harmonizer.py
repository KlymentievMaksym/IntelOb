import random
import numpy as np
from .Melody import Melody
from .FitnessFunc import FitnessFunc

MIN_PITCH, MAX_PITCH = 36, 84
# MIN_VELOCITY, MAX_VELOCITY = 20, 100


class GAHarmonizer:
    def __init__(self, target: Melody, population_size: int, mutation_rate: float, fitness_func: FitnessFunc):
        self.target = target
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.fitness_func = fitness_func

        self.population = self._create_initial_population()

        self.best_fitness = None
        self.best_melody = None

        self.fitness_history = []

    def _create_initial_population(self):
        shape = self.target.notes_count
        return [Melody(self.target.instruments, self._generate_initial_pitches(), self.target.other_info) for _ in range(self.pop_size)]

    def _generate_initial_pitches(self):
        return [np.random.randint(MIN_PITCH, MAX_PITCH, size=self.target.notes_count[index]) for index in range(len(self.target.pitches))]

    def evolve(self, generations: int = 100, progress_bar: object = None):
        for generation in range(generations):
            if progress_bar:
                progress_bar.progress((generation + 1) / generations, text="🔎 Searching for best melody...")

            self._create_new_population()

            self._find_best_value("min")

            self.fitness_history.append(self.best_fitness)
            # print(f"[{generation}] Best fitness: {self.best_fitness}")

        return self.best_fitness, self.best_melody

    def _find_best_value(self, typ: str = "max"):
        match typ:
            case "max":
                argfinder = np.argmax
                compare = 1
            case "min":
                argfinder = np.argmin
                compare = -1
            case _:
                print("Wrong argument,", typ)
                raise NotImplementedError

        best_fitness_ = [self.fitness_func(seq) for seq in self.population]
        best_fitness_index = argfinder(best_fitness_)
        if self.best_fitness is None or self.best_fitness < best_fitness_[best_fitness_index] * compare:
            self.best_fitness = best_fitness_[best_fitness_index] * compare
            self.best_melody = self.population[best_fitness_index]

    def _create_new_population(self):
        parents = self._select_parents()

        self.population = [child for index in range(0, len(parents), 2) for child in self._crossover(*parents[index:index + 2], parents[0])]

        for melody in self.population:
            self._mutation(melody)

    def _select_parents(self):
        fitness_values = [self.fitness_func(seq) for seq in self.population]
        return np.random.choice(self.population, size=self.pop_size, p=fitness_values/sum(fitness_values))
        # return random.choices(self.population, k=self.pop_size, weights=fitness_values)

    def _crossover(self, parent_1, parent_2, *args, **kwargs):
        return (Melody(self.target.instruments, self._notes_crossover(p1.pitches, p2.pitches), self.target.other_info) for p1, p2 in ((parent_1, parent_2), (parent_2, parent_1)))

    def _notes_crossover(self, pitches_1, pitches_2):
        cross_points = np.random.randint(1, self.target.notes_count - 1)
        pitches_return = []
        for cross_point_index in range(len(cross_points)):
            pitch_1 = pitches_1[cross_point_index][:cross_points[cross_point_index]]
            pitch_2 = pitches_2[cross_point_index][cross_points[cross_point_index]:]
            pitches_return.append(np.concatenate((pitch_1, pitch_2)))
        return pitches_return

    def _mutation(self, melody: Melody):
        counter = [0]*12
        for pitches in melody.pitches:  # A pitches for one isntrument
            for pitch in pitches:  # A pitch
                counter[pitch % 12] += 1
        main_note = np.argmax(counter)
        main_note_neighbors = np.array([main_note, (main_note+2) % 12, (main_note+4) % 12, (main_note+5) % 12, (main_note+7) % 12, (main_note+9) % 12, (main_note+11) % 12])
        # print("[?] Main Pitch Tonals", main_note_neighbors)

        dct = dict()
        for pitch_index in range(len(melody.pitches)):
            indexes = np.random.choice(range(0, len(melody.pitches[pitch_index]) - 1), size=max(int((len(melody.pitches[pitch_index])-1)*self.mutation_rate), 1), replace=False)
            # melody.pitches[pitch_index][indexes] = np.random.randint(MIN_PITCH, MAX_PITCH, size=len(indexes))

            for old_pitch_index in range(len(indexes)):
                old_pitch = melody.pitches[pitch_index][indexes[old_pitch_index]]
                already_exist = dct.get(old_pitch, None)
                if not already_exist:
                    values = np.array(range(old_pitch-12, old_pitch+12))

                    # print("[?] Values shape", values.shape)
                    mask = np.isin(values % 12, main_note_neighbors)
                    probabilities = np.where(mask, 0.9 / np.count_nonzero(mask), 0.1 / np.count_nonzero(~mask))
                    # print("[?] Sum of probabilities", sum(probabilities), "Exact probabilities", probabilities)

                    new_pitch = np.clip(np.random.choice(values, p=probabilities), MIN_PITCH, MAX_PITCH)
                    dct[old_pitch] = new_pitch
                    melody.pitches[pitch_index][indexes[old_pitch_index]] = new_pitch
                else:
                    melody.pitches[pitch_index][indexes[old_pitch_index]] = already_exist



"""
class GAComposer:
    def __init__(self, target, population_size=40, generations=50):
        self.target = target
        self.pop_size = population_size
        self.generations = generations
        self.population = self._init_population()
        self.fitness_history = []

    def _init_population(self):
        length = len(self.target.notes)
        if length == 0:
            raise ValueError("Target melody has no notes. Cannot evolve.")
        return [
            Melody([
                (random.randint(60, 72), i * 0.5, random.choice([0.25, 0.5, 1.0]))
                for i in range(length)
            ])
            for _ in range(self.pop_size)
        ]

    def _fitness(self, melody):
        tgt_int = self.target.intervals()
        mel_int = melody.intervals()
        pitch_score = -sum(abs(a - b) for a, b in zip(tgt_int, mel_int))

        tgt_key = self.target.key_signature()
        mel_key = melody.key_signature()
        key_score = -abs(tgt_key - mel_key)

        rhythm_score = -sum(abs(a[2] - b[2]) for a, b in zip(melody.notes, self.target.notes))

        return pitch_score + key_score + rhythm_score

    def _select_parents(self):
        return sorted(self.population, key=self._fitness, reverse=True)[:2]

    def _crossover(self, p1, p2):
        notes = []
        for n1, n2 in zip(p1.notes, p2.notes):
            notes.append(n1 if random.random() < 0.5 else n2)
        return Melody(notes)

    def _mutate(self, melody, rate=0.1):
        new_notes = []
        for pitch, start, duration in melody.notes:
            if random.random() < rate:
                pitch += random.choice([-2, -1, 1, 2])
                pitch = max(60, min(72, pitch))
            if random.random() < rate:
                duration = random.choice([0.25, 0.5, 1.0])
            new_notes.append((pitch, start, duration))
        return Melody(new_notes)

    def evolve(self):
        for _ in range(self.generations):
            new_pop = []
            best1, best2 = self._select_parents()
            for _ in range(self.pop_size):
                child = self._crossover(best1, best2)
                child = self._mutate(child)
                new_pop.append(child)
            self.population = new_pop
            best_fitness = self._fitness(self.best_melody())
            self.fitness_history.append(best_fitness)
        return self.best_melody()

    def best_melody(self):
        return max(self.population, key=self._fitness)
# """