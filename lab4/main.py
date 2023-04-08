import math
import numpy as np
import matplotlib.pyplot as plt

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

    return np.array([dx, dy])


def golden_section_search(f, a=0, b=1, eps=1e-2):
    """
    Метод золотого сечения для нахождения оптимального шага.

    :param f: функция, для которой нужно найти оптимальный шаг
    :param a: начало интервала поиска
    :param b: конец интервала поиска
    :param eps: точность поиска оптимального шага

    :return: оптимальный шаг
    """

    # Константа золотого сечения
    phi = (1 + np.sqrt(5)) / 2

    # Границы в новом интервале
    c = b - (b - a) / phi
    d = a + (b - a) / phi

    while abs(c - d) > eps:
        # Сужение интервала
        if f(c) < f(d):
            b = d
        else:
            a = c

        # Новые точки c и d для следующей итерации
        c = b - (b - a) / phi
        d = a + (b - a) / phi

    # Возвращаем среднее значение интервала как оптимальный шаг
    return (a + b) / 2


def backtracking_line_search(f, grad_f, x, d, alpha=1, rho=0.5, c=0.1):
    """Метод пробных точек для поиска оптимального шага

    :param f: функция, для которой определяется оптимальный шаг
    :param grad_f: градиент функции
    :param x: текущая точка
    :param d: направление поиска
    :param alpha: начальное значение шага
    :param rho: множитель для уменьшения шага
    :param c: константа для условия Армихо

    :return: оптимальный шаг alpha
    """

    while f(x + alpha * d) > f(x) + c * alpha * np.dot(grad_f(x), d):
        alpha *= rho

    return alpha


def norm(x):
    return np.sqrt(x[0] ** 2 + x[1] ** 2)


# Градиентный метод первого порядка наискорейшего спуска
def gradient_descent(f, grad_f, x0, eps=1e-2):
    """Ищет минимум функции f методом градиентного спуска.

        Args:
            f: callable. Целевая функция.
            grad_f: callable. Градиент целевой функции.
            x0: np.ndarray. Начальное значение.
            eps: float. Точность, по умолчанию равна 1e-2.

        Returns:
            tuple:
                xs: List[np.ndarray]. Список всех точек на линии спуска.
                grads: List[np.ndarray]. Список всех градиентов в этих точках.
                alphas: List[float]. Список всех найденных оптимальных шагов.
                i: int. Количество итераций.

        """

    alphas = []
    xs = [x0]
    grads = [grad_f(x0)]

    i = 0
    while norm(grads[-1]) > eps:
        # alpha = golden_section_search(lambda a: f(xs[-1] - a * grads[-1]))
        alpha = backtracking_line_search(f, grad_f, xs[-1], -grads[-1])

        x = xs[-1] - alpha * grads[-1]
        grad = grad_f(x)

        alphas += [alpha]
        xs += [x]
        grads += [grad]

        # Проверка ортогональности звеньев градиентной ломаной
        if abs(np.dot(grad, grads[-1])) < eps:
            break
        i += 1

    return xs, grads, alphas, i


def main():
    # Вызов градиентного метода первого порядка наискорейшего спуска
    x0 = np.array([3, -2])
    xs, grads, alphas, i = gradient_descent(f, grad_f, x0)
    print(f"xs:{xs}")
    print(f"grads:{grads}")
    print(f"alphas:{alphas}")
    print(f"i:{i}")
    print(f"f(x) = f({xs[-1]} = {f(xs[-1])}")


if __name__ == "__main__":
    main()
