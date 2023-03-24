import math
from collections.abc import Callable
import matplotlib.pyplot as plt
import numpy as np


class Function:
    def __init__(self, a: float, b: float, f: Callable[[float], float]) -> None:
        self.a = a
        self.b = b
        self.f = f
        self.min_gs = float("nan")
        self.min_bf = float("nan")
        self.min_hy = float("nan")
        self.iter_gs = 0
        self.iter_bf = 0
        self.iter_hy = 0

    def plot(self):
        x_list = np.linspace(self.a, self.b, 1000)
        y_list = [self.f(x) for x in x_list]
        plt.plot(x_list, y_list)
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("$xlnx$")
        plt.plot(self.min_gs, self.f(self.min_gs), "ro", label="Golden Section min")
        plt.plot(self.min_bf, self.f(self.min_bf), "bo", label="Bruteforce min")
        plt.plot(self.min_hy, self.f(self.min_hy), "mo", label="Dychotomy min")
        plt.legend()
        plt.show()

    def goldenSectionSearch(self, eps: float):
        r = self.b
        l = self.a
        phi = (1 + math.sqrt(5)) / 2
        resphi = 2 - phi
        x1 = l + resphi * (r - l)
        x2 = r - resphi * (r - l)
        f1 = self.f(x1)
        f2 = self.f(x2)
        iterations = 1
        while abs(r - l) > eps:
            iterations += 1
            if f1 < f2:
                r = x2
                x2 = x1
                f2 = f1
                x1 = l + resphi * (r - l)
                f1 = self.f(x1)
            else:
                l = x1
                x1 = x2
                f1 = f2
                x2 = r - resphi * (r - l)
                f2 = self.f(x2)

        self.min_gs = (x1 + x2) / 2
        self.iter_gs = iterations
        return (x1 + x2) / 2, iterations

    def bruteforce(self, eps):
        n = int((self.b - self.a) / eps)
        x = np.linspace(self.a, self.b, n)
        min_idx = -1
        min = math.inf
        iterations = 0
        for i in range(n):
            iterations += 1
            if self.f(x[i]) < min:
                min = self.f(x[i])
                min_idx = i

        self.min_bf = x[min_idx]
        self.iter_bf = iterations
        return x[min_idx], iterations

    def dichotomy_method(self, eps: float):
        a = self.a
        b = self.b
        alpha = (b - a) / 100
        iterations = 1
        while abs(b - a) > eps:
            tmp = (a + b) / 2
            if self.f(tmp - alpha) < self.f(tmp + alpha):
                b = tmp
            else:
                a = tmp
            iterations += 1
        self.min_hy = (a + b) / 2
        self.iter_hy = iterations
        return (a + b) / 2, iterations
