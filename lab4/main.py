from function import *
from gradient_descent import *


def main():
    print("Gradient descent first order approximation:")

    xs, grads, alphas, i = gradient_descent(f, grad_f, search='backtracking_line')
    print(f"xs: {xs}")
    print(f"grads: {grads}")
    print(f"alphas: {alphas}")
    print(f"i: {i}")
    print(f"min f(x) = f({xs[-1][0]}, {xs[-1][1]}) = {f(xs[-1])}")

    print()

    print("Gradient descent second order approximation:")
    xs, grads, alphas, i = gradient_descent_dfp(f, grad_f, search='backtracking_line')
    print(f"xs: {xs}")
    print(f"grads: {grads}")
    print(f"alphas: {alphas}")
    print(f"i: {i}")
    print(f"min f(x) = f({xs[-1][0]}, {xs[-1][1]}) = {f(xs[-1])}")


if __name__ == "__main__":
    main()
