import copy

import numpy as np
import itertools
import problem


def to_canonical(A: list, restrictions_types: list, b: list, x_restrictions: list, c: list):
    N = list(range(len(c)))
    # копирование данных, чтобы исходные остались прежними
    # A = copy.deepcopy(A)
    # restrictions_types = copy.deepcopy(restrictions_types)
    # b = copy.deepcopy(b)
    # x_restrictions = copy.deepcopy(x_restrictions)
    # c = copy.deepcopy(c)
    # приводим к канонической форме
    # сначала заменяем все знаки на равенства
    for i in range(len(A)):
        if restrictions_types[i] == problem.Problem.RestrictionType.LEQ:
            for j in range(len(A)):
                if j == i:
                    # A[j].insert(-1, 1.0)
                    A[j] += [1.0]

                    # x_restrictions.append(len(A[j]) - 2)
                    if len(A[j]) - 1 >= len(x_restrictions):
                        x_restrictions += [problem.Problem.RestrictionType.NONE] * (len(A[j]) - len(x_restrictions))
                    x_restrictions[len(A[j]) - 1] = problem.Problem.RestrictionType.GEQ
                else:
                    # A[j].insert(-1, 0.0)
                    A[j] += [0.0]
            # c.append(0.0)
            c += [0.0]
            # restrictions_types[i] = '='
            restrictions_types[i] = problem.Problem.RestrictionType.EQ
        if restrictions_types[i] == problem.Problem.RestrictionType.GEQ:
            for j in range(len(A)):
                if j == i:
                    # A[j].insert(-1, -1.0)
                    A[j] += [-1.0]
                    # x_restrictions.append(len(A[j]) - 2)
                    if len(A[j]) - 1 >= len(x_restrictions):
                        x_restrictions += [problem.Problem.RestrictionType.NONE] * (len(A[j]) - len(x_restrictions))
                    x_restrictions[len(A[j]) - 1] = problem.Problem.RestrictionType.GEQ
                else:
                    # A[j].insert(-1, 0.0)
                    A[j] += [0.0]
            # c.append(0.0)
            c += [0.0]
            # restrictions_types[i] = '='
            restrictions_types[i] = problem.Problem.RestrictionType.EQ
    # теперь переменные без ограничения на знак заменяем новыми
    # в том числе в ф-ии цели
    to_delete = []
    for i in range(len(A[0])):
        if x_restrictions[i] == problem.Problem.RestrictionType.NONE:
            # значит на знак нет ограничения
            for j in range(len(A)):  # заменяем переменную без ограничения на u-v
                A[j] += [A[j][i]]
                A[j] += [-A[j][i]]
            # c += [c[i]]
            # c += [-c[i]]
            c.insert(-1, c[i])
            c.insert(-1, -c[i])
            to_delete.append(i)
    to_delete = to_delete[::-1]
    for i in range(len(A)):
        for j in to_delete:
            A[i].pop(j)
    for j in to_delete:
        c.pop(j)
    # x_restrictions = [i for i in range(len(A[0]))]
    x_restrictions = [problem.Problem.RestrictionType.GEQ] * len(A[0])

    B = [i + len(N) for i in range(len(c) - len(N))]
    return N, B, A, b, c, 0

def to_canon(A: list, restrictions_types: list, b: list, x_restrictions: list, c: list):
    # Создаем список индексов базисных переменных N
    N = list(range(len(c)))

    # Преобразуем ограничения
    # Изменяем соответствующие строки матрицы A и вектор c
    for i in range(len(x_restrictions)):
        print("for 1")
        if x_restrictions[i] == problem.Problem.RestrictionType.LEQ:
            for row in A:
                print("for 1 1")
                row[i] *= -1
            c[i] *= -1
            continue

        # Если ограничения на переменную x_i нет, добавляем
        # Обновляем соответствующие строки матрицы A и вектор c
        # Добавляем новую переменную в список индексов базисных переменных N
        if x_restrictions[i] is problem.Problem.RestrictionType.NONE:
            N += [len(c)]

            for row in A:
                print("for 1 2")
                row += [row[i], -row[i]]
                row.pop(i)
            c += [c[i], -c[i]]
            c.pop(i)

        # Обновляем ограничения на переменную x_i
        x_restrictions[i] = problem.Problem.RestrictionType.GEQ

    # Преобразуем ограничения типа x_i >= b
    # Добавляем новые нулевые коэффициенты в вектор c и соответствующие переменные в матрицу A
    # Обновляем типы ограничений на равенства
    for i in range(len(restrictions_types)):
        print("for 2")
        if restrictions_types[i] == problem.Problem.RestrictionType.EQ:
            continue
        c += [0]

        val = 1 if restrictions_types[i] == problem.Problem.RestrictionType.LEQ else -1
        for j in range(len(A)):
            print("for 2 1")
            A[j] += [val * (i == j)]
        restrictions_types[i] = problem.Problem.RestrictionType.EQ

    # Добавляем ограничения на добавленные переменные
    x_restrictions += [problem.Problem.RestrictionType.GEQ] * (
        len(c) - len(x_restrictions) - 1
    )

    # Создаем список индексов небазисных переменных B
    B = [i + len(N) for i in range(len(c) - len(N))]

    # Возвращаем все преобразованные данные
    return N, B, A, b, c, 0


def brute_force(A: list, b: list, c: list, sign: int):
    A = copy.deepcopy(A)
    b = b.copy()
    c = c.copy()
    c = [sign * n for n in c]

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
