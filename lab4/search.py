import numpy as np


def golden_section_search(f, a=0, b=1, eps=1e-4):
    """
    Метод золотого сечения для нахождения оптимального шага.

    :param f: функция, для которой нужно найти оптимальный шаг
    :param a: начало интервала поиска
    :param b: конец интервала поиска
    :param eps: точность поиска оптимального шага

    :return: оптимальный шаг
    """

    # Константа золотого сечения
    phi = (3 - np.sqrt(5)) / 2

    while abs(b - a) > eps:
        c = a + phi * (b - a)
        d = a + (1 - phi) * (b - a)

        # Сужение интервала
        if f(c) > f(d):
            a = c
        else:
            b = d

    # Возвращаем среднее значение интервала как оптимальный шаг
    return (a + b) / 2


def trial_point_search(f, a=0, b=1, eps=1e-4):
    """
    Метод пробных точек для поиска минимума функции f на отрезке [a, b] с точностью eps.

    :param f: Функция, минимум которой ищется.
    :param a: Левая граница отрезка поиска.
    :param b: Правая граница отрезка поиска.
    :param eps: Точность поиска.

    :return: Точка минимума функции f на отрезке [a, b].
    """
    while True:
        net = [a + (b - a) / 4 * i for i in range(1, 4)]

        if abs(b - a) < eps or f(net[0]) == f(net[1]):
            return (a + b) / 2

        if f(net[2]) < f(net[1]):
            a = net[1]
        elif f(net[0]) < f(net[1]):
            b = net[1]
        else:
            a = net[0]
            b = net[2]


def fibonacci_search(f, a=0, b=1, eps=1e-4):
    """
    Функция поиска оптимального шага методом Фибоначчи для метода ДФП (Девидона - Флетчера - Пауэлла).

    :param f: Целевая функция
    :param a: Начало отрезка поиска
    :param b: Конец отрезка поиска
    :param eps: Точность поиска
    :return: Оптимальный шаг
    """
    n = 0
    while (b - a) / eps >= fibonacci(n):
        n += 1

    for k in range(n - 1):
        lk = a + (fibonacci(n - k - 2) / fibonacci(n - k)) * (b - a)
        rk = a + (fibonacci(n - k - 1) / fibonacci(n - k)) * (b - a)
        if f(lk) > f(rk):
            a = lk
        else:
            b = rk

    return (a + b) / 2


def fibonacci(n):
    """
    Функция вычисления n-го числа Фибоначчи.

    :param n: Порядковый номер числа Фибоначчи
    :return: n-е число Фибоначчи
    """
    if n == 0:
        return 0
    if n == 1:
        return 1

    return fibonacci(n - 1) + fibonacci(n - 2)
