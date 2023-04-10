#!/usr/bin/env python

from matplotlib import markers
from function import *
from gradient_descent import *


def main():
    print("Gradient descent first order approximation:")

    xs, grads, alphas, i = gradient_descent(f, grad_f, search="backtracking_line")
    print(f"xs: {xs}")
    print(f"grads: {grads}")
    print(f"alphas: {alphas}")
    print(f"i: {i}")
    print(f"min f(x) = f({xs[-1][0]}, {xs[-1][1]}) = {f(xs[-1])}")

    # Graphics
    x_range = np.arange(-0.15, 0, 0.0001)
    y_range = np.arange(-0.15, 0, 0.0001)
    x_grid, y_grid = np.meshgrid(x_range, y_range)
    cs = plt.contour(x_grid, y_grid, f([x_grid, y_grid]))

    print(xs)
    for i in range(0, len(xs) - 1):
        plt.plot([xs[i][0], xs[i + 1][0]], [xs[i][1], xs[i + 1][1]], marker="o")

    cs.clabel()
    plt.show()

    print()

    print("Gradient descent second order approximation:")
    xs, grads, alphas, i = gradient_descent_dfp(f, grad_f, search="backtracking_line")
    print(f"xs: {xs}")
    print(f"grads: {grads}")
    print(f"alphas: {alphas}")
    print(f"i: {i}")
    print(f"min f(x) = f({xs[-1][0]}, {xs[-1][1]}) = {f(xs[-1])}")


if __name__ == "__main__":
    main()
