from Algorithms.PSO import PSO

import numpy as np
import matplotlib.pyplot as plt


# Дослідити основні властивості алгоритму оптимізації роєм часток на прикладі
# функцій пристосованості:
# ◦ Ackley's function
# ◦ Функція Розенброка
# ◦ Cross-in-tray function
# ◦ Hölder table function
# ◦ McCormick function
# ◦ Styblinski–Tang function
# --------------------------------------- #
def Ackley(X):
    x, y = X
    return -20 * np.exp(-0.2 * np.sqrt(0.5*(x**2 + y**2))) - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + np.exp(1) + 20


Ackley_limits = [[-5, 5]]*2


# --------------------------------------- #
def Rozenbrock(X):
    result = 0
    for x_index in range(len(X)-1):
        result += 100*(X[x_index + 1] - X[x_index]**2)**2 + (X[x_index] - 1)**2
    return result


Rozenbrock_limits = [[-10, 10]]


# --------------------------------------- #
def CrossInTray(X):
    x, y = X
    return -0.0001 * (abs(np.sin(x) * np.sin(y) * np.exp(abs(100 - np.sqrt(x**2 + y**2) / np.pi))) + 1) ** 0.1


CrossInTray_limits = [[-10, 10]]*2


# --------------------------------------- #
def Holder(X):
    x, y = X
    return -np.abs(np.sin(x) * np.cos(y) * np.exp(np.abs(1 - np.sqrt(x**2 + y**2)/np.pi)))


Holder_limits = [[-10, 10]]*2


# --------------------------------------- #
def McCormick(X):
    x, y = X
    return np.sin(x+y) + (x-y)**2 - 1.5*x + 2.5*y + 1


McCormick_limits = [[-1.5, 4], [-3, 4]]


# --------------------------------------- #
def StyblinskiTang(X):
    result = 0
    for x in X:
        result = np.sum(x**4 - 16*x**2 + 5*x)
    return result/2


StyblinskiTang_limits = [[-5, 5]]*2


# PSO(50, 50, [0, 4], [-.3, .3], Ackley, Ackley_limits, d2=True, show=True, savep="Lab2/Images/Ackley.png", save="Lab2/Images/Ackley.gif").run()
# PSO(50, 50, [0, 4], [-.3, .3], Rozenbrock, Rozenbrock_limits*2, d2=True, show=True, savep="Lab2/Images/Rozenbrock.png", save="Lab2/Images/Rozenbrock.gif").run()
# PSO(50, 50, [0, 4], [-.3, .3], CrossInTray, CrossInTray_limits, d2=True, show=True, plot=True, style="arange", savep="Lab2/Images/CrossInTray.png", save="Lab2/Images/CrossInTray.gif").run()
# PSO(50, 50, [0, 4], [-.3, .3], Holder, Holder_limits, d2=True, show=True, plot=True, savep="Lab2/Images/Holder.png", save="Lab2/Images/Holder.gif").run()
# PSO(50, 50, [0, 4], [-.3, .3], McCormick, McCormick_limits, d2=True, show=True, plot=True, savep="Lab2/Images/McCormick.png", save="Lab2/Images/McCormick.gif").run()
# PSO(50, 50, [0, 4], [-.3, .3], StyblinskiTang, StyblinskiTang_limits, d2=True, show=True, plot=True, savep="Lab2/Images/StyblinskiTang.png", save="Lab2/Images/StyblinskiTang.gif").run()

# PSO(50, 50, [0, 4], [-.3, .3], Ackley, Ackley_limits, d3=True, show=True).run()
# PSO(50, 50, [0, 4], [-.3, .3], Rozenbrock, Rozenbrock_limits*2, d3=True, show=True).run()
# PSO(50, 50, [0, 4], [-.3, .3], CrossInTray, CrossInTray_limits, d3=True, show=True, plot=True, style="arange").run()
# PSO(50, 50, [0, 4], [-.3, .3], Holder, Holder_limits, d3=True, show=True, plot=True).run()
# PSO(50, 50, [0, 4], [-.3, .3], McCormick, McCormick_limits, d3=True, show=True, plot=True).run()
# PSO(50, 50, [0, 4], [-.3, .3], StyblinskiTang, StyblinskiTang_limits, d3=True, show=True, plot=True).run()



# • На додаткові бали можна запропонувати свій варіант використання генетичних
# алгоритмів.
def Reductor(X):
    x1, x2, x3, x4, x5, x6, x7, = X
    f1 = 27 / (x1 * x2**2 * x3) - 1  <= 0
    f2 = 397.5 / (x1 * x2**2 * x3**2) - 1 <= 0
    f3 = 1.93 * x4**3 / (x2 * x3 * x6**4) - 1 <= 0
    f4 = 1.93 / (x2 * x3 * x7**4) - 1 <= 0
    f5 = 1.0/(110 * x6**3) * np.sqrt(((745*x4) / (x2 * x3))**2 + 16.9 * 10**6) - 1 <= 0
    f6 = 1.0/(85 * x7**3) * np.sqrt(((745*x5) / (x2 * x3))**2 + 157.5 * 10**6) - 1 <= 0
    f7 = (x2*x3) / 40 - 1 <= 0
    f8 = 5*x2 / x1 - 1 <= 0
    f9 = x1 / (12 * x2) - 1 <= 0
    f10 = (1.5 * x6 + 1.9) / x4 - 1 <= 0
    f11 = (1.1 * x7 + 1.9) / x5 - 1 <= 0
    if f1 and f2 and f3 and f4 and f5 and f6 and f7 and f8 and f9 and f10 and f11:
        return 0.7854*x1*x2**2*(3.3333*x3**2 + 14.9334*x3 - 43.0934) - 1.508*x1*(x6**2 + x7**2) + 7.4777*(x6**3 + x7**3) + 0.7854*(x4*x6**2 + x5*x7**2)
    return float('inf')


Reductor_limits = [[2.6, 3.6], [0.7, 0.8], [17, 28], [7.3, 8.3], [7.8, 8.3], [2.9, 3.9], [5.0, 5.5]]


# PSO(50, 50, [0, 4], [-1.3, 1.3], Reductor, Reductor_limits, show=True, plot=True, savep="Lab2/Images/Reductor.png", integer=[2]).run()

# • Провести експерименти з різними параметрами алгоритму оптимізації роєм часток.

# • Для кожної з функції:
# ◦ Побудувати графічне зображення цільової функції. Можна використовувати код з попередньої лабораторної роботи.
# ◦ Показати процес пошуку глобального екстремуму. Тобто потрібно продемонструвати положення популяції на функції на кожній ітерації (В звіт можна вставити тільки для однієї функції).
# ◦ Отримані залежності представити в графічному вигляді (по осі абсцис відкладається номер ітерації, а по осі ординат – найкраще значення функції).
# Для порівняння показати результати різних екскрементів (різні значення гіперпараметрів) на одному графіку.

# PSO(100, 50, [0, 4], [-.3, .3], Ackley, Ackley_limits, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="100 50 [-.3, .3]").run()
# PSO(50, 100, [0, 4], [-.3, .3], Ackley, Ackley_limits, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="50 100 [-.3, .3]").run()
# PSO(50, 50, [0, 4], [-1.3, 1.3], Ackley, Ackley_limits, d2=False, break_faster=True, count=10, close=False, show=True, label="50 50 [-1.3, 1.3]", savep="Lab2/Images/Ackley_dif.png").run()

# PSO(100, 50, [0, 4], [-.3, .3], Rozenbrock, Rozenbrock_limits*2, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="100 50 [-.3, .3]").run()
# PSO(50, 100, [0, 4], [-.3, .3], Rozenbrock, Rozenbrock_limits*2, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="50 100 [-.3, .3]").run()
# PSO(50, 50, [0, 4], [-1.3, 1.3], Rozenbrock, Rozenbrock_limits*2, d2=False, break_faster=True, count=10, close=False, show=True, label="50 50 [-1.3, 1.3]", savep="Lab2/Images/Rozenbrock_dif.png").run()

# PSO(100, 50, [0, 4], [-.3, .3], CrossInTray, CrossInTray_limits, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="100 50 [-.3, .3]").run()
# PSO(50, 100, [0, 4], [-.3, .3], CrossInTray, CrossInTray_limits, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="50 100 [-.3, .3]").run()
# PSO(50, 50, [0, 4], [-1.3, 1.3], CrossInTray, CrossInTray_limits, d2=False, break_faster=True, count=10, close=False, show=True, label="50 50 [-1.3, 1.3]", savep="Lab2/Images/CrossInTray_dif.png").run()

# PSO(100, 50, [0, 4], [-.3, .3], Holder, Holder_limits, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="100 50 [-.3, .3]").run()
# PSO(50, 100, [0, 4], [-.3, .3], Holder, Holder_limits, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="50 100 [-.3, .3]").run()
# PSO(50, 50, [0, 4], [-1.3, 1.3], Holder, Holder_limits, d2=False, break_faster=True, count=10, close=False, show=True, label="50 50 [-1.3, 1.3]", savep="Lab2/Images/Holder_dif.png").run()

# PSO(100, 50, [0, 4], [-.3, .3], McCormick, McCormick_limits, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="100 50 [-.3, .3]").run()
# PSO(50, 100, [0, 4], [-.3, .3], McCormick, McCormick_limits, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="50 100 [-.3, .3]").run()
# PSO(50, 50, [0, 4], [-1.3, 1.3], McCormick, McCormick_limits, d2=False, break_faster=True, count=10, close=False, show=True, label="50 50 [-1.3, 1.3]", savep="Lab2/Images/McCormick_dif.png").run()

# PSO(100, 50, [0, 4], [-.3, .3], StyblinskiTang, StyblinskiTang_limits, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="100 50 [-.3, .3]").run()
# PSO(50, 100, [0, 4], [-.3, .3], StyblinskiTang, StyblinskiTang_limits, d2=False, break_faster=True, count=10, close=False, show=True, plot=False, label="50 100 [-.3, .3]").run()
# PSO(50, 50, [0, 4], [-1.3, 1.3], StyblinskiTang, StyblinskiTang_limits, d2=False, break_faster=True, count=10, close=False, show=True, label="50 50 [-1.3, 1.3]", savep="Lab2/Images/StyblinskiTang_dif.png").run()


# PSO(100, 50, [0, 4], [-1.3, 1.3], Reductor, Reductor_limits, d2=False, break_faster=True, count=10, integer=[2], close=False, show=True, plot=False, label="100 50 [-1.3, 1.3]").run()
# PSO(50, 100, [0, 4], [-1.3, 1.3], Reductor, Reductor_limits, d2=False, break_faster=True, count=10, integer=[2], close=False, show=True, plot=False, label="50 100 [-1.3, 1.3]").run()
# print(PSO(50, 50, [0, 4], [-5.3, 5.3], Reductor, Reductor_limits, d2=False, break_faster=True, count=10, integer=[2], close=False, show=True, label="50 50 [-5.3, 5.3]", savep="Lab2/Images/Reductor_dif.png").run())
