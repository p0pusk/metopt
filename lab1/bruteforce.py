import numpy as np
import itertools
import problem


def to_canon(A: list, restrictions_types: list, b: list, x_restrictions: list, c: list):
    # Создаем список индексов базисных переменных N
    N = list(range(len(c)))

    # Преобразуем ограничения
    # Изменяем соответствующие строки матрицы A и вектор c
    for i in range(len(x_restrictions)):
        if x_restrictions[i] == problem.Problem.RestrictionType.LEQ:
            for row in A:
                row[i] *= -1
            c[i] *= -1
            continue

        # Если ограничения на переменную x_i нет, добавляем
        # Обновляем соответствующие строки матрицы A и вектор c
        # Добавляем новую переменную в список индексов базисных переменных N
        if x_restrictions[i] is problem.Problem.RestrictionType.NONE:
            N += [len(c)]

            for row in A:
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
        if restrictions_types[i] == problem.Problem.RestrictionType.EQ:
            continue
        c += [0]

        val = 1 if restrictions_types[i] == problem.Problem.RestrictionType.LEQ else -1
        for j in range(len(A)):
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


def brute_force(A: list, b: list, c: list):
    # Проверка размерности A и b
    if len(A) != len(b):
        raise ValueError("Размерность матрицы A и вектора b не совпадают")

    combs = []
    combs_indexes = []

    # Генерируем все возможные комбинации столбцов матрицы A с длиной, равной количеству строк в A
    for i in itertools.combinations(list(range(len(A[0]))), len(A)):
        sub = np.array(A)[:, i]
        # Проверка полноранговости матрицы
        if np.linalg.matrix_rank(sub) == len(A):
            combs += [sub]
            combs_indexes += [i]

    bases = []
    for i in range(len(combs)):
        if np.linalg.det(combs[i]) == 0:
            continue

        # Для каждой матрицы из combs находим вектор решения системы линейных уравнений
        sol = np.linalg.solve(combs[i], b)

        # Проверка на неотрицательность вектора решения
        if len(sol[sol < 0]) != 0:
            continue

        # Создаем базисный вектор из найденного вектора решения
        basis = [0] * len(A[0])
        for j in range(len(combs_indexes[i])):
            basis[combs_indexes[i][j]] = sol[j]
        bases += [basis]

    if len(bases) == 0:
        raise ValueError("Задача линейного программирования не имеет решения")

    # Возвращаем базисный вектор с наименьшим значением целевой функции
    return min(bases, key=lambda basis: np.dot(basis, c))
