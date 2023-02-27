from enum import Enum


class Problem:
    class RestrictionType(Enum):
        EQ = 0
        LEQ = -1
        GEQ = 1

    class ObjectiveDirection(Enum):
        MIN = 1
        MAX = -1

    class Form(Enum):
        GENERAL = 0
        STANDART = 1
        CANON = 2

    def __init__(
        self,
        dim: int,
        A: list[list],
        b: list,
        c: list,
        restrictions_types: list[RestrictionType] = [],
        x_restrictions: list[bool] = [],
        obj_direction: ObjectiveDirection = ObjectiveDirection.MIN,
    ) -> None:
        self.dim = int(dim)
        self.A = A
        self.b = b
        self.c = c
        self.restrictions_types = restrictions_types
        self.x_restrictions = x_restrictions
        self.obj_direction = obj_direction
        self.n = self.dim
        self.m = len(b)
        self.form = Problem.Form.GENERAL

        assert self.n == len(A[0])
        assert self.m == len(A)
        assert len(self.c) == self.n
        assert len(restrictions_types) == self.m

    def ToStandart(self):
        if self.form == Problem.Form.STANDART:
            return
        if self.obj_direction == Problem.ObjectiveDirection.MIN:
            self.c = [-v for v in self.c]
            self.obj_direction = Problem.ObjectiveDirection.MAX
        for i in range(len(self.x_restrictions)):
            if not self.x_restrictions[i]:
                self.dim = self.dim + 1
                self.c.insert(i + 1, -self.c[i])
                for j in range(len(self.A)):
                    self.A[j].insert(i + 1, -self.A[j][i])
                self.x_restrictions[i] = True
                self.x_restrictions.insert(i + 1, True)
                self.n = self.n + 1
        for idx, r in enumerate(self.restrictions_types):
            if r == Problem.RestrictionType.EQ:
                self.restrictions_types[idx] = Problem.RestrictionType.GEQ
                self.A.insert(idx + 1, self.A[idx])
                self.b.insert(idx + 1, self.b[idx])
                self.restrictions_types.insert(idx + 1, Problem.RestrictionType.LEQ)
                self.m = self.m + 1
        for idx, r in enumerate(self.restrictions_types):
            if r == Problem.RestrictionType.GEQ:
                self.A[idx] = [-v for v in self.A[idx]]
                self.b[idx] = -self.b[idx]
                self.restrictions_types[idx] = Problem.RestrictionType.LEQ
        self.form = Problem.Form.STANDART

    def ToCanon(self):
        pass

    def GetDual(self):
        pass

    def Print(self):
        for idx, c in enumerate(self.c):
            if c >= 0 and idx > 0:
                print("+", end=" ")
            if c < 0:
                print("-", end=" ")

            print(f"{abs(c)}x_{idx + 1}", end=" ")
        if self.obj_direction == Problem.ObjectiveDirection.MIN:
            print("--> MIN")
        else:
            print("--> MAX")

        for i in range(self.m):
            for j in range(self.n):
                if self.A[i][j] >= 0 and j > 0:
                    print("+", end=" ")
                if self.A[i][j] < 0:
                    print("-", end=" ")

                print(f"{abs(self.A[i][j])}x_{j+1}", end=" ")

            if self.restrictions_types[i] == Problem.RestrictionType.GEQ:
                print(">=", end=" ")
            elif self.restrictions_types[i] == Problem.RestrictionType.LEQ:
                print("<=", end=" ")
            elif self.restrictions_types[i] == Problem.RestrictionType.EQ:
                print("=", end=" ")

            print(self.b[i])

        for idx, r in enumerate(self.x_restrictions):
            if idx > 0:
                print(",", end=" ")
            if r:
                print(f"x_{idx + 1}", end="")
        print(" >= 0")
