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

# • Розробити програмне забезпечення для розв’язання задач оптимізації (використовувати готові рішення для генетичних алгоритмів заборонено).
class GeneticAl:
    # def __init__(self, fx, xs_limits: list[list]): # var_dep_count: int, 
    #     # self.var_dep_count = var_dep_count
    #     self.fx = fx
    #     self.xs_limits = xs_limits
        
    #     x = []
    #     y = []
        
    #     match len(xs_limits):
    #         case 1:
    #             for xi in range(xs_limits[0][0], xs_limits[0][1]):
    #                 x += [xi]
    #                 y += [fx(xi)]
    def __init__(self, pop_size, child_size, iterations, mutation_rate, limits, function, comes_to="min"):
        self.pop_size = pop_size
        self.child_size = child_size
        self.iterations = iterations
        self.mutation_rate = mutation_rate 
        self.function = function
        # self.limits = limits

        self.lim_size = len(limits)
        self.population = np.zeros(pop_size+child_size)

        self.var_dep_history = []
        self.var_indep_history = []

        self.best_sol = None
        match comes_to:
            case "min":
                self.best_indep_var = float("inf")
            case "max":
                self.best_indep_var = -float("inf")
            case _:
                print("Wrong argument,", comes_to)

        match self.lim_size:
            case 1:
                # selection
                for i in range(pop_size):
                    x = np.random.uniform(*limits[0])
                    self.population[i] = x
                # print(self.population)
                for iteration in range(self.iterations):
                    # crossover
                    for i in range(child_size):
                        p1 = np.random.choice(self.population[:pop_size])
                        p2 = np.random.choice(self.population[:pop_size])
                        x = np.random.uniform(min(p1, p2), max(p1, p2))
                        self.population[i+pop_size] = x
                    # print(self.population)

                    # selection
                    fitness_func = [self.function(self.population[i]) for i in range(self.pop_size + self.child_size)]

                    ind = np.argsort(fitness_func)#[::-1] 
                    fitness_func = np.sort(fitness_func)#[::-1] 
                    if comes_to == "max":
                        ind = ind[::-1] 
                        fitness_func = fitness_func[::-1] 
                        
                    self.population = self.population[ind]

                    self.var_dep_history.append(self.population[:pop_size])
                    self.var_indep_history.append(fitness_func[:pop_size])

                fig, ax = plt.subplots()
                plt.xlim(*limits[0])
                plt.plot(self.var_dep_history[0], self.var_indep_history[0])
                def update(frame):
                    fig.clear(True)
                    plt.xlim(*limits[0])
                    plt.plot(self.var_dep_history[frame], self.var_indep_history[frame])
                # print(self.population, fitness_func)
                # plt.plot(self.population, fitness_func)
                ani = animation.FuncAnimation(fig=fig, func=update, frames=iterations, interval=300)
                plt.show()
            case 2:
                for i in range(pop_size):
                    x1 = np.random.uniform(*limits[0])
                    x2 = np.random.uniform(*limits[1])
                    self.population[i] = [x1, x2]
                    # self.population.append([x1, x2])
            case _:
                print("Wrong argument,", limits)
                raise NotImplementedError

            
        
        
    # TRY TO DO DYNAMICALY...
    #     for key, val in self.xs_limits.items():
    #         exec(key + '=val')
    #     exec(self.fx)

    #     vars_dep = list(locals())[-1*len(self.xs_limits)-1:-1]
    #     for var in vars_dep:
    #         print(locals()[var])

    #     print(locals()['y'])

    # def fr(self, vars_dep, var_value, size, index=0):
    #     var = vars_dep[index]
    #     locals()[var + "_i"] = 0
    #     vr = locals()[-1]
    #     index += 1
    #     for vr in range(var_value[0], var_value[1]):
    #         if index < size:
    #             fr(self, vars_dep, size, index)


if __name__ == "__main__":
    def y(x):
        return 3*x**3 + 4
    GeneticAl(20, 20, 100, 0.5, [[10, 20]], y, 'min')
