import numpy as np
import itertools

import problem

def to_canon(A: list, restrictions_types: list, b: list, x_restrictions: list, c: list):
    N = list(range(len(c)))

    for i in range(len(x_restrictions)):
        if x_restrictions[i] == problem.Problem.RestrictionType.LEQ:
            for row in A:
                row[i] *= -1
            c[i] *= -1
            continue

        if x_restrictions[i] is None:
            N += [len(c)]

            for row in A:
                row += [row[i], -row[i]]
                row.pop(i)
            c += [c[i], -c[i]]
            c.pop(i)

        x_restrictions[i] = problem.Problem.RestrictionType.GEQ

    for i in range(len(restrictions_types)):
        if restrictions_types[i] == problem.Problem.RestrictionType.EQ:
            continue
        c += [0]

        val = 1 if restrictions_types[i] == problem.Problem.RestrictionType.LEQ else -1
        for j in range(len(A)):
            A[j] += [val * (i == j)]
        restrictions_types[i] = problem.Problem.RestrictionType.EQ

    x_restrictions += [problem.Problem.RestrictionType.GEQ] * (len(c) - len(x_restrictions) - 1)

    B = [i + len(N) for i in range(len(c) - len(N))]
    return N, B, A, b, c, 0


def brute_force(A: list, b: list, c: list, sign: int = 1):
    c = [sign * n for n in c]

    if len(A) >= len(A[0]):
        return []

    combs = []
    combs_indexes = []

    for i in itertools.combinations(list(range(len(A[0]))), len(A)):
        sub = np.array(A)[:, i]
        if np.linalg.det(sub) != 0:
            combs += [sub]
            combs_indexes += [i]

    bases = []
    for i in range(len(combs)):
        sol = np.linalg.solve(combs[i], b)
        if len(sol[sol < 0]) != 0 or len(sol[sol > 1e16]) != 0:
            continue

        basis = [0] * len(A[0])
        for j in range(len(combs_indexes[i])):
            basis[combs_indexes[i][j]] = sol[j]
        bases += [basis]

    return min(bases, key=lambda basis: np.dot(basis, c))
