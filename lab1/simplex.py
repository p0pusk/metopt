import copy
import math
import bruteforce
import problem as prb


class Simplex:
    # In standart form
    def __init_table(
        self, N: list, B: list, A: list[list], b: list, c: list, v: float
    ) -> None:
        N, B, A, b, c = (
            copy.deepcopy(N),
            copy.deepcopy(B),
            copy.deepcopy(A),
            copy.deepcopy(b),
            copy.deepcopy(c),
        )
        n = len(N)
        m = len(B)
        self.N = N
        self.B = B
        self.A = [[0.0] * (n + m)] * (n + m)
        self.b = [0.0] * (n + m)
        self.c = [0.0] * (n + m)
        self.v = v

        for i in B:
            self.b[i] = b[i]
            for j in N:
                self.A[i][j] = A[B.index(i)][N.index(j)]

        for j in N:
            self.c[j] = c[j]

    def pivot(
        self,
        N: list,
        B: list,
        A: list[list],
        b: list,
        c: list,
        v: float,
        l: int,
        e: int,
    ):
        n = len(N)
        m = len(B)
        self.N = [0.0] * n
        self.B = [0.0] * m
        self.A = [[0.0] * (n + m)] * (n + m)
        self.b = [0.0] * (n + m)
        self.c = [0.0] * (n + m)
        self.v = v

        self.b[e] = b[l] / A[l][e]
        for j in N:
            if j != e:
                self.A[e][j] = A[l][j] / A[l][e]
        self.A[e][l] = 1 / A[l][e]

        for i in B:
            if i != l:
                self.b[i] = b[i] - A[i][e] * self.b[e]
                for j in N:
                    if j != e:
                        self.A[i][j] = A[i][j] - A[i][e] * self.A[e][j]
                self.A[i][l] = -A[i][e] * self.A[e][l]

        self.v = v + c[e] * self.b[e]

        for j in N:
            if j != e:
                self.c[j] = c[j] - c[e] * self.A[e][j]
        self.c[l] = -c[e] * self.A[e][l]

        self.N = copy.deepcopy(N)
        self.N.pop(N.index(e))
        self.N.append(l)
        self.B = copy.deepcopy(B)
        self.B.pop(B.index(l))
        self.B.append(e)

        return self.N, self.B, self.A, self.b, self.c, self.v

    def __init__(self, A: list[list], b: list, c: list):
        m = len(A)
        n = len(A[0])
        N = []
        B = []
        v = 0

        # find minimum b_k
        k = 0
        min = math.inf
        for i in range(len(b)):
            if b[i] < min:
                min = b[i]
                k = i

        if b[k] >= 0:
            self.N = [*range(n)]
            self.B = [*range(n, n + m)]
            self.v = 0
            self.__init_table(N, B, A, b, c, v)
            return

        # L_aux
        self.c = [0.0] * (n + m + 1)
        self.c[0] = -1
        self.A = [[0.0] * (n + m + 1) for _ in range(n + m + 1)]
        for i in range(n + 1, n + m + 1):
            self.A[i][0] = -1
        self.b = [0.0] * (n + m + 1)
        self.v = v
        self.N = [*range(n + 1)]
        self.B = [*range(n + 1, n + m + 1)]

        for i in range(m):
            self.b[n + 1 + i] = b[i]
            for j in range(n):
                self.A[n + 1 + i][j + 1] = A[i][j]

        self.print()

        l = n + 1 + k

        self.pivot(self.N, self.B, self.A, self.b, self.c, self.v, l, 0)

        delta = [0.0] * m
        while any(self.c[j] > 0 for j in N):
            self.print()
            e = -1
            for i in self.N:
                if self.c[i] > 0:
                    e = i
                    break
            for i in self.B:
                if self.A[i][e] > 0:
                    delta[i] = self.b[i] / A[i][e]
                else:
                    delta[i] = math.inf
            l = minimizing_index(delta, self.B)
            if delta[l] == math.inf:
                raise Exception("Задача неограниченная")
            else:
                self.pivot(self.N, self.B, self.A, self.b, self.c, self.v, l, e)

        self.print()
        x = [0.0] * (n + m + 1)
        for i in range(n + 1):
            if i in B:
                x[i] = self.b[i]
            else:
                x[i] = 0
        if x[0] == 0 and 0 in B:
            self.pivot(self.N, self.B, self.A, self.b, self.c, self.v, 0, N[0])
            self.N.pop(N.index(0))
            self.A.pop(0)
            for i in range(n):
                A[i].pop(0)
            self.b.pop(0)
            self.c.pop(0)
            self.c = copy.deepcopy(c)
            self.v = v
            for i in range(len(self.c)):
                if i in self.B:
                    for j in range(len(self.A[i])):
                        c[j] -= c[i] * A[i][j]
                    self.v += b[i]
        else:
            raise Exception("Задача неразрешима")

    def print(self):
        print("=======================================================================")
        print("N:")
        print(self.N)
        print("B:")
        print(self.B)
        print("A:")
        print(self.A)
        print("b:")
        print(self.b)
        print("c:")
        print(self.c)
        print("v:")
        print(self.v)
        print("=======================================================================")

    def simplex(self, N: list, B: list, A: list, b: list, c: list, v: int):
        x = list()

        while True:
            delta = [0 for m in range(len(A))]

            e = -1
            for j in N:
                if c[j] > 0:
                    e = j
            if e == -1:
                break

            for i in B:
                if A[i][e] > 0:
                    delta[i] = b[i] / A[i][e]
                else:
                    delta[i] = "inf"

            l = minimizing_index(delta, B)
            if delta[l] == "inf":
                raise Exception("Задача не ограничена")
            else:
                N, B, A, b, c, v = _pivot(N, B, A, b, c, v, l, e)

        for i in range(len(A)):
            if i in B:
                x.append(b[i])
            else:
                x.append(0)

        return x


def minimizing_index(delta: list, B: list):
    min_idx = -1
    min = math.inf
    for idx, val in enumerate(delta):
        if idx not in B:
            continue

        min = val
        min_idx = idx

        if min != math.inf:
            break

    if min == math.inf:
        return min_idx

    for idx, val in enumerate(delta):
        if idx not in B:
            continue

        if val < min:
            min = val
            min_idx = idx

    return min_idx
