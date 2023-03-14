import copy
import itertools
import numpy as np


# Функция, преобразующая исходные данные транспортной задачи в канонический вид
def to_canon(supply: list, demand: list, costs: list):
    # Получаем размеры
    m = len(supply)
    n = len(demand)

    # Создаем списки для коэффициентов матрицы A,
    # вектора свободных членов b и вектора ценовых коэффициентов c
    A = [[0] * (m * n) for _ in range(m + n)]
    b = copy.deepcopy(supply) + copy.deepcopy(demand)
    c = list()

    # Проходимся по всем возможным парам складов и пунктов назначения
    for i, j in itertools.product(range(m), range(n)):
        # Добавляем ценовой коэффициент в вектор c
        c += [costs[i][j]]

        # Заполняем соответствующие ячейки в матрице A
        A[i][i * n + j] = A[m + j][i * n + j] = 1

    # Возвращаем полученные коэффициенты в каноническом виде
    return A, b, c


# Метод перебора
def brute_force(A: list, b: list, c: list):
    A = copy.deepcopy(A)
    b = copy.deepcopy(b)
    c = copy.deepcopy(c)

    # Проверка размерности A и b
    if len(A) != len(b):
        raise ValueError("Размерность матрицы A и вектора b не совпадают")

    # Списки для хранения базисных матриц и соответствующих им индексов комбинаций столбцов
    combs = []
    combs_indexes = []

    # Генерация всех возможных комбинаций столбцов матрицы A
    for i in itertools.combinations(list(range(len(A[0]))), len(A)):
        # Выбираем столбцы текущей комбинации
        sub = np.array(A)[:, i]

        # Проверка полноранговости матрицы
        if np.linalg.matrix_rank(sub) == len(A):
            combs += [sub]
            combs_indexes += [i]

    # Список базисных векторов
    bases = []

    for i in range(len(combs)):
        # Проверка детерминанта
        if np.linalg.det(combs[i]) == 0:
            continue

        # Решение СЛАУ
        sol = np.linalg.solve(combs[i], b)

        # Проверка неотрицательности решения
        if len(sol[sol < 0]) != 0:
            continue

        # Составление базисного вектора из решения СЛАУ
        basis = [0] * len(A[0])
        for j in range(len(combs_indexes[i])):
            basis[combs_indexes[i][j]] = sol[j]
        bases += [basis]

    # Если не было найдено ни одного базисного вектора, то задача не имеет решения
    if len(bases) == 0:
        return ValueError("Задача не имеет решения")

    # Возвращаем минимальное значение целевой функции по базисным векторам
    return min(bases, key=lambda basis: np.dot(basis, c))
