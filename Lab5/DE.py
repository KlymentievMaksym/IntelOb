import numpy as np
from tqdm import tqdm

import matplotlib.pyplot as plt
import matplotlib.animation as animation


def Plot(history_f, history_pops, history_best_f, history_best_pop, max_f, function, limits, **kwargs):
    if limits.shape[1] == 2:
        fig, [ax1, ax2, ax3] = plt.subplots(3)

        x_low, x_high = limits[:, 0], limits[:, 1]
        dim = len(limits)

        dots = 200
        projection_dep_val = np.linspace(x_low, x_high, dots)
        space = np.array([projection_dep_val[:, i] for i in range(dim)])
        space = np.meshgrid(*space)
        projection = np.array([[function(np.array([space[i][j, k] for i in range(dim)])) for k in range(dots)] for j in range(dots)])
        colorbar = ax3.contourf(*space, projection)
        fig.colorbar(colorbar, ax=ax3)

        def update(frame):
            plt.suptitle(f"Best solution: {history_best_f[frame]:.5f} | Iter {frame}")
            ax1.clear()
            ax2.clear()
            ax3.clear()

            ax1.set_ylim([0, max_f])
            ax1.plot(history_f[frame], label="Fitness")

            ax2.set_ylim([0, max_f])
            ax2.plot(history_best_f[:frame], label="Best")

            ax3.contourf(*space, projection)
            ax3.scatter(history_pops[frame, :, 0], history_pops[frame, :, 1], label="Population")
            ax3.scatter(history_best_pop[frame, 0], history_best_pop[frame, 1], label="Best")

            ax1.set_xlabel("Pop Part")
            ax1.set_ylabel("Fitness")
            ax2.set_xlabel("Iteration")
            ax2.set_ylabel("Fitness")
            ax3.set_xlabel("x1")
            ax3.set_ylabel("x2")

            ax1.legend()
            ax2.legend()
            ax3.legend()

            ax1.grid()
            ax2.grid()
            ax3.grid()

        anim = animation.FuncAnimation(fig, update, frames=range(len(history_f)), interval=100)
        plt.show()


def DE(pop_size, iterations, function, limits, **kwargs):
    plot_do = kwargs.get("plot", False)
    dim = len(limits)
    limits = np.array(limits)
    # print(limits)
    x_low = limits[:, 0]
    x_high = limits[:, 1]

    population = np.random.uniform(x_low, x_high, (pop_size, dim))

    max_f = 0
    best_f = float('inf')
    best_pop = np.zeros(dim)

    if plot_do:
        history_f = np.zeros((iterations, pop_size))
        history_pops = np.zeros((iterations, pop_size, dim))

        history_best_f = np.zeros(iterations)
        history_best_pop = np.zeros((iterations, dim))

    # print(population)
    for iteration in tqdm(
        range(iterations),
        desc="Processing",
        unit="step",
        bar_format="{l_bar}{bar:40}{r_bar}",
        colour='cyan',
        total=iterations
    ):
        for i in range(pop_size):
            F = np.random.uniform(1e-6, 2)
            P = np.random.uniform(1e-6, 1)
            r = np.random.uniform(1e-6, 1, dim)
            x1, x2, x3 = np.random.choice(population.shape[0], size=3, replace=False)
            while np.all(population[x1] == population[i]) or np.all(population[x2] == population[i]) or np.all(population[x3] == population[i]):
                x1, x2, x3 = np.random.choice(population.shape[0], size=3, replace=False)
            mutant_vector = population[x1] + F * (population[x2] - population[x3])
            mutant_vector[r < P] = population[i][r < P]
            if function(population[i]) > function(mutant_vector):
                population[i] = mutant_vector
        fitness = np.array([function(X) for X in population])
        el_min = np.argmin(fitness)
        if best_f > fitness[el_min]:
            best_f = fitness[el_min]
            best_pop = population[el_min].copy()
        el_max = np.max(fitness)
        if max_f < el_max:
            max_f = el_max

        if plot_do:
            history_best_f[iteration] = best_f
            history_best_pop[iteration] = best_pop.copy()
            history_f[iteration] = fitness.copy()
            history_pops[iteration] = population.copy()

    if plot_do:
        Plot(history_f, history_pops, history_best_f, history_best_pop, max_f, function, limits)

    return best_f, best_pop


if __name__ == "__main__":
    def func(X):
        return np.sum(X**2)
    func_limit = [[-4, 4]] * 2

    de = DE(100, 100, func, func_limit)
    print(de)
