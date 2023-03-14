import copy
import math


class Simplex:
    # In standart form
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
        self.N = [0] * n
        self.B = [0] * m
        self.A = [[0.0] * (n + m) for _ in range(n + m)]
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

    def __init__(self, A: list[list], b: list, c: list):
        m = len(A)
        n = len(A[0])
        self.N = []
        self.B = []
        self.v = 0

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
            self.A = [[0.0] * (n + m) for _ in range(n + m)]
            self.b = [0.0] * (n + m)
            self.c = [0.0] * (n + m)

            for i in range(m):
                self.b[n + i] = b[i]
                for j in range(n):
                    self.A[n + i][j] = A[i][j]

            for j in range(n):
                self.c[j] = c[j]
            return

        print("L_AUX")
        # L_aux
        self.c = [0.0] * (n + m + 1)
        self.c[0] = -1
        self.A = [[0.0] * (n + m + 1) for _ in range(n + m + 1)]
        for i in range(n + 1, n + m + 1):
            self.A[i][0] = -1
        self.b = [0.0] * (n + m + 1)
        self.N = [*range(n + 1)]
        self.B = [*range(n + 1, n + m + 1)]

        for i in range(m):
            self.b[n + 1 + i] = b[i]
            for j in range(n):
                self.A[n + 1 + i][j + 1] = A[i][j]

        l = n + 1 + k

        self.pivot(self.N, self.B, self.A, self.b, self.c, self.v, l, 0)

        delta = [0.0] * (n + m + 1)
        while any(self.c[j] > 0 for j in self.N):
            e = -1
            for i in self.N:
                if self.c[i] > 0:
                    e = i
                    break
            for i in self.B:
                if self.A[i][e] > 0:
                    delta[i] = self.b[i] / self.A[i][e]
                else:
                    delta[i] = math.inf
            l = minimizing_index(delta, self.B)
            if delta[l] == math.inf:
                raise Exception("Задача неограниченная")
            else:
                self.pivot(self.N, self.B, self.A, self.b, self.c, self.v, l, e)

        x = [0.0] * (n + m + 1)
        for i in range(n + 1):
            if i in self.B:
                x[i] = self.b[i]
            else:
                x[i] = 0
        if x[0] == 0:
            if 0 in self.B:
                self.pivot(self.N, self.B, self.A, self.b, self.c, self.v, 0, self.N[0])
            self.N.pop(self.N.index(0))
            for i in range(len(self.N)):
                self.N[i] -= 1
            for i in range(len(self.B)):
                self.B[i] -= 1
            self.A.pop(0)
            for i in range(len(self.A)):
                self.A[i].pop(0)
            self.b.pop(0)
            self.c.pop(0)
            for i in range(len(self.c)):
                if i < len(c):
                    self.c[i] = c[i]
                else:
                    self.c[i] = 0
            self.v = self.v
            for i in range(len(self.c)):
                if i in self.B:
                    for j in range(len(self.A[i])):
                        self.c[j] -= self.c[i] * self.A[i][j]
                    self.v += self.c[i] * self.b[i]
                    self.c[i] = 0
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

    def simplex(self):
        n = len(self.c)
        m = len(self.b)

        delta = [0.0] * (n + m)
        while any(self.c[j] > 0 for j in self.N):
            e = -1
            for i in self.N:
                if self.c[i] > 0:
                    e = i
                    break
            for i in self.B:
                if self.A[i][e] > 0:
                    delta[i] = self.b[i] / self.A[i][e]
                else:
                    delta[i] = math.inf
            l = minimizing_index(delta, self.B)
            if delta[l] == math.inf:
                raise Exception("Задача неограниченная")
            else:
                self.pivot(self.N, self.B, self.A, self.b, self.c, self.v, l, e)
        x = [0.0] * n
        for i in range(n):
            if i in self.B:
                x[i] = self.b[i]
            else:
                x[i] = 0.0
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
