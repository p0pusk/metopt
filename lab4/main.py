import math

dim = 2

coefs_default = [2, 5, 3]
coefs_count = 3


def f(x: list, coefs: list = None):
    if len(x) != dim:
        return ValueError("Wrong vector dimension")

    if coefs is None:
        coefs = coefs_default
    elif len(coefs) != coefs_count:
        return ValueError("Wrong number of coefficients")

    return coefs[0] * x[0] + x[1] + 4 * math.sqrt(1 + coefs[1] * (x[0] ** 2) + coefs[2] * (x[1] ** 2))


def grad_f(x: list, coefs: list = None):
    if len(x) != dim:
        return ValueError("Wrong vector dimension")

    if coefs is None:
        coefs = coefs_default
    elif len(coefs) != coefs_count:
        return ValueError("Wrong number of coefficients")

    dx = coefs[0] + (4 * coefs[1] * x[0]) / math.sqrt(1 + coefs[1] * (x[0] ** 2) + coefs[2] * (x[1] ** 2))
    dy = 1 + (4 * coefs[2] * x[1]) / math.sqrt(1 + coefs[1] * (x[0] ** 2) + coefs[2] * (x[1] ** 2))

    return [dx, dy]


def main():
    print("")


if __name__ == "__main__":
    main()
