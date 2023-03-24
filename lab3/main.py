from function import *


def f(x: float):
    return pow(x, 6) + 3 * pow(x, 2) + 6 * x - 1


if __name__ == "__main__":
    # "x^6 + 3*x^2 + 6*x - 1"
    a = -1
    b = 0
    eps_list = [0.1, 0.01, 0.001]
    function = Function(a, b, f)

    for eps in eps_list:
        min, iter = function.bruteforce(eps)
        print(f"=========================================")
        print(f"eps = {eps}")
        print(f"min bruteforce = {min}")
        print(f"f_min bruteforce = {function.f(min)}")
        print(f"iter bruteforce = {iter}")
        print(f"-----------------------------------------")
        min, iter = function.goldenSectionSearch(eps=0.1)
        print(f"min golden section = {min}")
        print(f"f_min golden section = {function.f(min)}")
        print(f"iter golden section = {iter}")
        print(f"-----------------------------------------")
        min, iter = function.dichotomy_method(eps)
        print(f"min dichotomy = {min}")
        print(f"f_min dichotomy = {function.f(min)}")
        print(f"iter dichotomy = {iter}")
    function.plot()
