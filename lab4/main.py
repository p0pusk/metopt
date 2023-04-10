#!/usr/bin/env python

from matplotlib import markers, pyplot as plt
from function import *
from gradient_descent import *


def print_solution(xs: list, grads: list, alphas: list, i: int, name: str = 'Gradient descent'):
    print(name + ':')

    print(f"xs: {xs}")
    print(f"grads: {grads}")
    print(f"alphas: {alphas}")
    print(f"number of iterations: {i}")
    print(f"min f(x) = f({xs[-1][0]}, {xs[-1][1]}) = {f(xs[-1])}")

    print()


def print_graph(xs: list, name: str = 'Gradient descent'):
    plt.title(name)
    x_range = np.arange(-0.15, 0, 0.0001)
    y_range = np.arange(-0.15, 0, 0.0001)
    x_grid, y_grid = np.meshgrid(x_range, y_range)
    cs = plt.contour(x_grid, y_grid, f([x_grid, y_grid]))

    for i in range(0, len(xs) - 1):
        plt.plot([xs[i][0], xs[i + 1][0]], [xs[i][1], xs[i + 1][1]], marker="o")

    cs.clabel()
    plt.show()


def main():
    eps_list = [0.1, 0.01, 0.001]

    for eps in eps_list:
        print(f"eps = {eps}:")
        print()

        xs, grads, alphas, i = gradient_descent(f, grad_f, eps=eps, search="backtracking_line")
        print_solution(xs, grads, alphas, i, 'Gradient descent 1st order approximation')
        print_graph(xs, "Gradient descent 1st order approximation")

        xs, grads, alphas, i = gradient_descent_dfp(f, grad_f, eps=eps, search="backtracking_line")
        print_solution(xs, grads, alphas, i, 'Gradient descent 2nd order approximation (DFP)')
        print_graph(xs, "Gradient descent 2nd order approximation (DFP)")


if __name__ == "__main__":
    main()
