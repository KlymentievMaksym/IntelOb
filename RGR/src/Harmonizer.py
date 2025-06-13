import numpy as np
from time import time

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
        return [Melody(self.target.instruments, self._generate_initial_pitches(), self.target.other_info) for _ in range(self.pop_size)]

    def _generate_initial_pitches(self):
        return [np.random.randint(MIN_PITCH, MAX_PITCH, size=self.target.notes_count[index]) for index in range(len(self.target.pitches))]

    def evolve(self, generations: int = 100, progress_bar: object = None):
        self.time_smooth = max(10, int(0.01*generations))
        self.time_hist = np.zeros(self.time_smooth)
        self.time_index = 0

        self.prev_time = time()

        for generation in range(generations):
            self._create_new_population()
            self._find_best_value("min")
            self.fitness_history.append(self.best_fitness)

            self.new_time = time()
            self.time_hist[self.time_index] = (self.new_time - self.prev_time) * (generations - generation - 1)
            self.prev_time = self.new_time

            self.time_index = (self.time_index + 1) % self.time_smooth
            time_left = np.mean(self.time_hist)

            if progress_bar:
                progress_bar.progress((generation + 1) / generations, text=f"🔎 Searching... {(time_left//3600):.0f}h {(time_left//60 % 60):.0f}m {(time_left % 60):.0f}s")

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
