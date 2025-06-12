import numpy as np
import random as rng
from tqdm import tqdm


class GeneticHarmonizer:
    def __init__(self, melody_data: list, chords: list, population_size: int, mutation_rate: float, fitness_func):
        self.melody_data = melody_data
        self.chords = chords
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.fitness_func = fitness_func
        self._population = []
        self.number_of_bars = melody_data.number_of_bars

    def generate(self, iterations: int = 100):
        self._population = self._create_population()

        for iteration in tqdm(range(iterations)):
            self._population = self._create_new_population()

        return self._find_best_fit()

    def _create_population(self):
        return [[np.random.choice(self.chords) for _ in range(self.number_of_bars)]]

    def _create_new_population(self):
        fitness_values = [self.fitness_func(seq) for seq in self._population]
        # summ = sum(fitness_values)
        # fitness_values = [fit / summ for fit in fitness_values]
        parents = rng.choices(self._population, weights=fitness_values, k=self.population_size)

        population_new = []

        for part in range(0, self.population_size, 2):
            child_1, child_2 = self._crossover(parents[part], parents[part + 1])

            child_1, child_2 = self._mutation(child_1), self._mutation(child_2)

            population_new.extend([child_1, child_2])

        return population_new

    def _crossover(self, parent_1, parent_2):
        cross_point = np.random.randint(1, self.number_of_bars - 1)
        child_1 = parent_1[:cross_point] + parent_2[cross_point:]
        child_2 = parent_2[:cross_point] + parent_1[cross_point:]
        return child_1, child_2

    def _mutation(self, child):
        if np.random.rand() < self.mutation_rate:
            index = np.random.randint(0, self.number_of_bars - 1)
            child[index] = np.random.choice(self.chords)
        return child

    def _find_best_fit(self):
        fitness_values = [self.fitness_func(seq) for seq in self._population]
        best_index = np.argmax(fitness_values)
        return fitness_values[best_index], self._population[best_index]


# class GeneticMelodyHarmonizer:
#     """
#     Generates chord accompaniments for a given melody using a genetic algorithm.
#     It evolves a population of chord sequences to find one that best fits the
#     melody based on a fitness function.

#     Attributes:
#         melody_data (MusicData): Data containing melody information.
#         chords (list): Available chords for generating sequences.
#         population_size (int): Size of the chord sequence population.
#         mutation_rate (float): Probability of mutation in the genetic algorithm.
#         fitness_evaluator (FitnessEvaluator): Instance used to assess fitness.
#     """

#     def __init__(
#         self,
#         melody_data,
#         chords,
#         population_size,
#         mutation_rate,
#         fitness_evaluator,
#     ):
#         """
#         Initializes the generator with melody data, chords, population size,
#         mutation rate, and a fitness evaluator.

#         Parameters:
#             melody_data (MusicData): Melody information.
#             chords (list): Available chords.
#             population_size (int): Size of population in the algorithm.
#             mutation_rate (float): Mutation probability per chord.
#             fitness_evaluator (FitnessEvaluator): Evaluator for chord fitness.
#         """
#         self.melody_data = melody_data
#         self.chords = chords
#         self.mutation_rate = mutation_rate
#         self.population_size = population_size
#         self.fitness_evaluator = fitness_evaluator
#         self._population = []

#     def generate(self, generations=1000):
#         """
#         Generates a chord sequence that harmonizes a melody using a genetic
#         algorithm.

#         Parameters:
#             generations (int): Number of generations for evolution.

#         Returns:
#             best_chord_sequence (list): Harmonization with the highest fitness
#                 found in the last generation.
#         """
#         self._population = self._initialise_population()
#         for _ in range(generations):
#             parents = self._select_parents()
#             new_population = self._create_new_population(parents)
#             self._population = new_population
#         best_chord_sequence = (
#             self.fitness_evaluator.get_chord_sequence_with_highest_fitness(
#                 self._population
#             )
#         )
#         return best_chord_sequence

#     def _initialise_population(self):
#         """
#         Initializes population with random chord sequences.

#         Returns:
#             list: List of randomly generated chord sequences.
#         """
#         return [
#             self._generate_random_chord_sequence()
#             for _ in range(self.population_size)
#         ]

#     def _generate_random_chord_sequence(self):
#         """
#         Generate a random chord sequence with as many chords as the numbers
#         of bars in the melody.

#         Returns:
#             list: List of randomly generated chords.
#         """
#         return [
#             random.choice(self.chords)
#             for _ in range(self.melody_data.number_of_bars)
#         ]

#     def _select_parents(self):
#         """
#         Selects parent sequences for breeding based on fitness.

#         Returns:
#             list: Selected parent chord sequences.
#         """
#         fitness_values = [
#             self.fitness_evaluator.evaluate(seq) for seq in self._population
#         ]
#         return random.choices(
#             self._population, weights=fitness_values, k=self.population_size
#         )

#     def _create_new_population(self, parents):
#         """
#         Generates a new population of chord sequences from the provided parents.

#         This method creates a new generation of chord sequences using crossover
#         and mutation operations. For each pair of parent chord sequences,
#         it generates two children. Each child is the result of a crossover
#         operation between the pair of parents, followed by a potential
#         mutation. The new population is formed by collecting all these
#         children.

#         The method ensures that the new population size is equal to the
#         predefined population size of the generator. It processes parents in
#         pairs, and for each pair, two children are generated.

#         Parameters:
#             parents (list): A list of parent chord sequences from which to
#                 generate the new population.

#         Returns:
#             list: A new population of chord sequences, generated from the
#                 parents.

#         Note:
#             This method assumes an even population size and that the number of
#             parents is equal to the predefined population size.
#         """
#         new_population = []
#         for i in range(0, self.population_size, 2):
#             child1, child2 = self._crossover(
#                 parents[i], parents[i + 1]
#             ), self._crossover(parents[i + 1], parents[i])
#             child1 = self._mutate(child1)
#             child2 = self._mutate(child2)
#             new_population.extend([child1, child2])
#         return new_population

#     def _crossover(self, parent1, parent2):
#         """
#         Combines two parent sequences into a new child sequence using one-point
#         crossover.

#         Parameters:
#             parent1 (list): First parent chord sequence.
#             parent2 (list): Second parent chord sequence.

#         Returns:
#             list: Resulting child chord sequence.
#         """
#         cut_index = random.randint(1, len(parent1) - 1)
#         return parent1[:cut_index] + parent2[cut_index:]

#     def _mutate(self, chord_sequence):
#         """
#         Mutates a chord in the sequence based on mutation rate.

#         Parameters:
#             chord_sequence (list): Chord sequence to mutate.

#         Returns:
#             list: Mutated chord sequence.
#         """
#         if random.random() < self.mutation_rate:
#             mutation_index = random.randint(0, len(chord_sequence) - 1)
#             chord_sequence[mutation_index] = random.choice(self.chords)
#         return chord_sequence