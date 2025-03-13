# Завдання:
# • Ознайомитись з теоретичними відомостями до генетичних алгоритмів (схрещування, мутації, відбір).
# • Розробити програмне забезпечення для розв’язання задач оптимізації (використовувати готові рішення для генетичних алгоритмів заборонено).
# • Дослідити основні властивості генетичних алгоритмів на прикладі функцій пристосованості (функції зазначені вище). На додаткові бали можна запропонувати свій варіант використання генетичних алгоритмів.
# • Провести експерименти з різними параметрами генетичного алгоритму.
# • Для кожної функції:
    # ◦ Побудувати графічне зображення цільової функції
    # ◦ Показати процес пошуку глобального екстремуму. Тобто потрібно продемонструвати положення популяції на функції на кожній ітерації.
    # ◦ Отримані залежності представити в графічному вигляді (по осі абсцис відкладається номер ітерації, а по осі ординат – найкраще значення функції).
        # Для порівняння показати результати різних екскрементів (різні значення гіперпараметрів) на одному графіку.
# • Зробити звіт
# • Захистити роботу

import numpy as np
import matplotlib.pyplot as plt


import matplotlib.animation as animation


class GeneticAl:
    def __init__(self, pop_size, child_size, iterations, mutation_rate, limits, function, comes_to="min", **kwargs):
        self.pop_size = pop_size
        self.child_size = child_size
        self.iterations = iterations
        self.mutation_rate = mutation_rate
        self.function = function
        self.limits = limits
        self.comes_to = comes_to

        self.lim_size = len(limits)

        self.var_dep_history = []
        self.var_indep_history = []
        self.best_indep_var_history = []
        self.iterations_history = list(range(self.iterations))

        match comes_to:
            case "min":
                self.best_indep_var = float("inf")
            case "max":
                self.best_indep_var = -float("inf")
            case _:
                print("Wrong argument,", comes_to)

        self.__start
        self.__plot(**kwargs)

    @property
    def __start(self):
        match self.lim_size:
            case 1:
                # --------------------------------------------------- #
                # -------------------- Projection -------------------- #
                # --------------------------------------------------- #
                self.projection_x = np.arange(*self.limits[0], 1/(self.self.pop_size + self.child_size + 1))
                self.projection_y = np.array([self.function(x) for x in self.projection_x])
                # --------------------------------------------------- #
                # -------------------- Selection -------------------- #
                # --------------------------------------------------- #
                self.population = np.zeros(self.pop_size+self.child_size)
                for i in range(self.pop_size):
                    x = np.random.uniform(*self.limits[0])
                    self.population[i] = x

                for iteration in range(self.iterations):
                    # --------------------------------------------------- #
                    # ------------- Crossover and Mutation -------------- #
                    # --------------------------------------------------- #
                    for i in range(self.child_size):
                        if np.random.rand() < self.mutation_rate:
                            p1 = np.random.choice(self.population[:self.pop_size])
                            p2 = np.random.choice(self.population[:self.pop_size])
                            x = np.random.uniform(min(p1, p2), max(p1, p2))
                        else:
                            x = np.random.uniform(*self.limits[0])
                        self.population[i+self.pop_size] = x

                    # --------------------------------------------------- #
                    # --------------------- Elitism --------------------- #
                    # --------------------------------------------------- #
                    fitness_func = [self.function(self.population[i]) for i in range(self.pop_size + self.child_size)]

                    ind = np.argsort(fitness_func)
                    fitness_func = np.sort(fitness_func)
                    if self.comes_to == "max":
                        ind = ind[::-1]
                        fitness_func = fitness_func[::-1]

                    self.population = self.population[ind]

                    match self.comes_to:
                        case "min":
                            self.best_indep_var = min(self.best_indep_var, min(fitness_func))
                        case "max":
                            self.best_indep_var = max(self.best_indep_var, max(fitness_func))
                        case _:
                            print("Wrong argument,", self.comes_to)

                    # --------------------------------------------------- #
                    # ------------------ Save  History ------------------ #
                    # --------------------------------------------------- #
                    self.best_indep_var_history.append(self.best_indep_var)
                    self.var_dep_history.append(self.population[:self.pop_size])
                    self.var_indep_history.append(fitness_func[:self.pop_size])
            case 2:
                # --------------------------------------------------- #
                # -------------------- Projection -------------------- #
                # --------------------------------------------------- #
                self.projection_x1 = np.linspace(*self.limits[0], (self.pop_size + self.child_size))
                self.projection_x2 = np.linspace(*self.limits[1], (self.pop_size + self.child_size))

                self.projection_x1, self.projection_x2 = np.meshgrid(self.projection_x1, self.projection_x2)
                self.projection_y = self.function(self.projection_x1, self.projection_x2)

                # --------------------------------------------------- #
                # -------------------- Selection -------------------- #
                # --------------------------------------------------- #
                self.population = np.array([[0, 0]]*(self.pop_size + self.child_size))
                for i in range(self.pop_size):
                    x1 = np.random.uniform(*self.limits[0])
                    x2 = np.random.uniform(*self.limits[1])
                    self.population[i] = [x1, x2]

                for iteration in range(self.iterations):
                    # --------------------------------------------------- #
                    # ------------- Crossover and Mutation -------------- #
                    # --------------------------------------------------- #
                    for i in range(self.child_size):
                        if np.random.rand() < self.mutation_rate:
                            p1 = np.random.randint(self.pop_size)
                            p2 = np.random.randint(self.pop_size)
                            while p2 == p1:
                                p2 = np.random.randint(self.pop_size)
                            p1 = self.population[p1]
                            p2 = self.population[p2]
                            x1 = np.random.uniform(min(p1[0], p2[0]), max(p1[0], p2[0]))
                            x2 = np.random.uniform(min(p1[1], p2[1]), max(p1[1], p2[1]))
                        else:
                            x1 = np.random.uniform(*self.limits[0])
                            x2 = np.random.uniform(*self.limits[1])
                        self.population[i+self.pop_size] = [x1, x2]

                    # --------------------------------------------------- #
                    # --------------------- Elitism --------------------- #
                    # --------------------------------------------------- #
                    fitness_func = [self.function(*self.population[i]) for i in range(self.pop_size + self.child_size)]

                    ind = np.argsort(fitness_func)
                    fitness_func = np.sort(fitness_func)
                    if self.comes_to == "max":
                        ind = ind[::-1]
                        fitness_func = fitness_func[::-1]

                    self.population = self.population[ind]

                    match self.comes_to:
                        case "min":
                            self.best_indep_var = min(self.best_indep_var, min(fitness_func))
                        case "max":
                            self.best_indep_var = max(self.best_indep_var, max(fitness_func))
                        case _:
                            print("Wrong argument,", self.comes_to)

                    # --------------------------------------------------- #
                    # ------------------ Save  History ------------------ #
                    # --------------------------------------------------- #
                    self.best_indep_var_history.append(self.best_indep_var)
                    self.var_dep_history.append(self.population[:self.pop_size])
                    self.var_indep_history.append(fitness_func[:self.pop_size])
            case _:
                print("Wrong argument,", self.limits)
                raise NotImplementedError

    # @property
    def __plot(self, **kwargs):
        animation_do = kwargs.get("animation", False)
        animation_show = kwargs.get("animation_show", False) or kwargs.get("show_animation", False)
        animation_fps = kwargs.get("fps", 30)
        save_location = kwargs.get("save_loc", None)

        graph = kwargs.get("graph", True)
        graph_show = kwargs.get("graph_show", True) and kwargs.get("show_graph", True)

        label = kwargs.get("label", None)

        if graph:
            plt.plot(self.iterations_history, self.best_indep_var_history, label=label)
            plt.xlabel("Iterations")
            plt.ylabel("Fitness func best value")
            plt.grid()
            plt.legend()
            if graph_show:
                plt.show()
            if save_location:
                plt.savefig(save_location)
                plt.clf()

        match self.lim_size:
            case 1:
                if animation_do and (save_location or animation_show):
                    fig, ax1 = plt.subplots(1, 1)

                    def update(frame):
                        ax1.clear()
                        ax1.set_title(f"Best sol = {self.best_indep_var_history[frame]:.5f} | Iter: {frame}")
                        ax1.plot(self.projection_x, self.projection_y, label=label)
                        ax1.scatter(self.var_dep_history[frame], self.var_indep_history[frame], c='r', label="Population")
                        match self.comes_to:
                            case "min":
                                index = self.var_indep_history[frame].argmin()
                            case "max":
                                index = self.var_indep_history[frame].argmax()
                            case _:
                                print("Wrong argument,", self.comes_to)
                                raise NotImplementedError
                        ax1.scatter(self.var_dep_history[frame][index], self.var_indep_history[frame][index], marker="*", c='black', label="Best")

                    ani = animation.FuncAnimation(fig=fig, func=update, frames=self.iterations, interval=30)
                    if save_location:
                        ani.save(save_location, fps=animation_fps)
                    if animation_show:
                        plt.show()
            case 2:
                if animation_do and (save_location or animation_show):
                    fig = plt.figure(figsize=plt.figaspect(2.))
                    ax1 = fig.add_subplot(1, 1, 1, projection='3d')

                    def update(frame):
                        ax1.clear()
                        ax1.set_title(f"Best sol = {self.best_indep_var_history[frame]:.5f} | Iter: {frame}")

                        ax1.plot_surface(self.projection_x1, self.projection_x2, self.projection_y, edgecolor='royalblue', lw=0.5, alpha=0.3, cmap='coolwarm', zorder=1, label=label)

                        ax1.scatter(self.var_dep_history[frame][:, 0], self.var_dep_history[frame][:, 1], self.var_indep_history[frame], c='r', label="Population", zorder=2)
                        match self.comes_to:
                            case "min":
                                index = self.var_indep_history[frame].argmin()
                            case "max":
                                index = self.var_indep_history[frame].argmax()
                            case _:
                                print("Wrong argument,", self.comes_to)
                                raise NotImplementedError
                        ax1.scatter(self.var_dep_history[frame][index, 0], self.var_dep_history[frame][index, 1], self.var_indep_history[frame][index], marker="*", c='black', label="Best", zorder=3)
                        ax1.legend()

                    ani = animation.FuncAnimation(fig=fig, func=update, frames=self.iterations, interval=30)
                    if save_location:
                        ani.save(save_location, fps=animation_fps)
                    if animation_show:
                        plt.show()
            case _:
                print("Wrong argument,", self.limits)
                raise NotImplementedError


if __name__ == "__main__":

    # def y(x1, x2):
    #     a = 1
    #     b = 5.1 / (4*np.pi**2)
    #     c = 5 / np.pi
    #     r = 6
    #     s = 10
    #     t = 1 / (8*np.pi)
    #     return a*(x2-b*x1**2 + c*x1-r)**2 + s*(1-t)*np.cos(x1) + s
    # GeneticAl(20, 100, 50, 0.5, [[-5, 10], [0, 15]], y, 'min', graph=True, graph_show=False, label="20_100_0.5")
    # GeneticAl(100, 40, 50, 0.5, [[-5, 10], [0, 15]], y, 'min', graph=True, graph_show=False, label="100_40_0.5")
    # GeneticAl(20, 40, 50, 1, [[-5, 10], [0, 15]], y, 'min', graph=True, graph_show=False, label="20_40_1", save_loc="./Lab1/Images/Branin Function.png")
    # GeneticAl(20, 40, 50, 0.5, [[-5, 10], [0, 15]], y, 'min', graph=False, animation=True, animation_show=False, save_loc="./Lab1/Images/Branin Function.gif", fps=10)

    def y(x1, x2):
        return -np.cos(x1)*np.cos(x2)*np.exp(-(x1-np.pi)**2-(x2-np.pi)**2)
    # GeneticAl(20, 100, 50, 0.5, [[-100, 100], [-100, 100]], y, 'min', graph=True, graph_show=False, label="20_100_0.5")
    # GeneticAl(100, 40, 50, 0.5, [[-100, 100], [-100, 100]], y, 'min', graph=True, graph_show=False, label="100_40_0.5")
    # GeneticAl(20, 40, 50, 1, [[-100, 100], [-100, 100]], y, 'min', graph=True, graph_show=False, label="20_40_1", save_loc="./Lab1/Images/Easom function.png")
    # GeneticAl(20, 40, 50, 0.5, [[-100, 100], [-100, 100]], y, 'min', graph=False, animation=True, animation_show=False, save_loc="./Lab1/Images/Easom function.gif", fps=10)
    GeneticAl(20, 40, 50, 0.5, [[-100, 100], [-100, 100]], y, 'min', graph=True, animation=True, animation_show=True, fps=10)

    # def y(x1, x2):
    #     return (x1 + x2)*((x1*x2)/3)**2
    # GeneticAl(20, 100, 50, 0.5, [[-100, 100], [-100, 100]], y, 'min', graph=True, graph_show=False, label="20_100_0.5")
    # GeneticAl(100, 40, 50, 0.5, [[-100, 100], [-100, 100]], y, 'min', graph=True, graph_show=False, label="100_40_0.5")
    # GeneticAl(20, 40, 50, 1, [[-100, 100], [-100, 100]], y, 'min', graph=True, graph_show=False, label="20_40_1", save_loc="./Lab1/Images/Test.png")
    # GeneticAl(20, 40, 50, 0.5, [[-100, 100], [-100, 100]], y, 'min', graph=False, animation=True, animation_show=False, save_loc="./Lab1/Images/Test.gif", fps=10)
    # GeneticAl(20, 40, 50, 0.5, [[-100, 100], [-100, 100]], y, 'min', graph=False, animation=True, animation_show=True, fps=10)

    # def y(x1, x2):
    #     return ((1+(x1+x2+1)**2*(19-14*x1+3*x1**2-14*x2+6*x1*x2+3*x2**2)) * (30+(2*x1-3*x2)**2*(18-32*x1+12*x1**2+48*x2-36*x1*x2+27*x2**2)))
    # GeneticAl(20, 100, 50, 0.5, [[-2, 2], [-2, 2]], y, 'min', graph=True, graph_show=False, label="20_100_0.5")
    # GeneticAl(100, 40, 50, 0.5, [[-2, 2], [-2, 2]], y, 'min', graph=True, graph_show=False, label="100_40_0.5")
    # GeneticAl(20, 40, 50, 1, [[-2, 2], [-2, 2]], y, 'min', graph=True, graph_show=False, label="20_40_1", save_loc="./Lab1/Images/The Goldstein-Price function.png")
    # GeneticAl(20, 40, 50, 0.5, [[-2, 2], [-2, 2]], y, 'min', graph=False, animation=True, animation_show=False, save_loc="./Lab1/Images/The Goldstein-Price function.gif", fps=10)
    # GeneticAl(20, 40, 50, 0.5, [[-2, 2], [-2, 2]], y, 'min', graph=False, animation=True, animation_show=True, fps=10)

    # def y(x1, x2):
    #     return ((4-2.1*x1**2+(x1**4)/3)*x1**2+x1*x2+(-4+4*x2**2)*x2**2)
    # GeneticAl(20, 100, 50, 0.5, [[-3, 3], [-2, 2]], y, 'min', graph=True, graph_show=False, label="20_100_0.5")
    # GeneticAl(100, 40, 50, 0.5, [[-3, 3], [-2, 2]], y, 'min', graph=True, graph_show=False, label="100_40_0.5")
    # GeneticAl(20, 40, 50, 1, [[-3, 3], [-2, 2]], y, 'min', graph=True, graph_show=False, label="20_40_1", save_loc="./Lab1/Images/six-hump Camel function.png")
    # GeneticAl(20, 40, 50, 0.5, [[-3, 3], [-2, 2]], y, 'min', graph=False, animation=True, animation_show=False, save_loc="./Lab1/Images/six-hump Camel function.gif", fps=10)
