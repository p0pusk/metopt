import numpy as np


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
