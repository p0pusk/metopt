from copy import copy, deepcopy
from enum import Enum
from numpy import obj2sctype
from scipy.optimize import linprog

import simplex
import bruteforce


class Problem:
    class RestrictionType(Enum):
        EQ = 0
        LEQ = 1
        GEQ = -1
        NONE = 3

    class ObjectiveDirection(Enum):
        MIN = -1
        MAX = 1

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
        x_restrictions: list[RestrictionType] = [],
        obj_direction: ObjectiveDirection = ObjectiveDirection.MIN,
    ) -> None:
        self.dim = int(dim)
        self.A = deepcopy(A)
        self.b = deepcopy(b)
        self.c = deepcopy(c)
        self.restrictions_types = deepcopy(restrictions_types)
        self.x_restrictions = deepcopy(x_restrictions)
        self.obj_direction = deepcopy(obj_direction)
        self.form = Problem.Form.GENERAL

        assert len(self.A[0]) == len(self.c)
        assert len(self.b) == len(self.A)
        assert len(self.restrictions_types) == len(self.b)

    def solve(self):
        print("=======================================================================")
        print("GENERAL:")
        self.print()
        print("=======================================================================")

        print("STANDART:")
        standart = self.get_standart()
        standart.print()
        print("=======================================================================")

        print("DUAL:")
        dual = self.get_dual()
        dual.print()
        print("=======================================================================")

        print("RESULTS:")
        print("Scipy ans:")
        x = linprog(
            A_ub=standart.A,
            b_ub=standart.b,
            c=[-standart.obj_direction.value * n for n in standart.c],
        ).x
        print(f"x = {x}")
        print(f"v = {sum(standart.c[i] * x[i] for i in range(len(x)))}")

        print()
        print("simplex ans:")
        try:
            spx = simplex.Simplex(standart.A, standart.b, standart.c)
        except Exception as e:
            print(e)
            return

        print(spx.simplex()[: self.dim])

        # print()
        # print("bruteforce ans:")
        # print(
        #     bruteforce.brute_force(
        #         standart.A, standart.b, standart.c, sign=standart.obj_direction.value
        #     )
        # )
        print("=======================================================================")

        print("RESULTS FOR DUAL:")

        neg_dual_A = deepcopy(dual.A)
        for col in range(len(neg_dual_A)):
            for i in range(len(neg_dual_A[0])):
                neg_dual_A[col][i] *= -1

        print("Scipy ans:")
        x = linprog(
            A_ub=neg_dual_A,
            b_ub=[-v for v in dual.b],
            c=[-dual.obj_direction.value * n for n in dual.c],
        ).x
        print(f"x = {x}")
        print(f"v = {sum(dual.c[i] * x[i] for i in range(len(x)))}")

        print()
        print("simplex ans:")
        dual_standart = dual.get_standart()
        spx = simplex.Simplex(dual_standart.A, dual_standart.b, dual_standart.c)

        print(spx.simplex()[: self.dim])

        # print()
        # print("bruteforce ans:")
        # print(
        #     bruteforce.brute_force(
        #         dual.A, dual.b, dual.c, sign=dual.obj_direction.value
        #     )
        # )

    def get_standart(self):
        standart = Problem(
            dim=self.dim,
            A=self.A,
            b=self.b,
            c=self.c,
            obj_direction=self.obj_direction,
            restrictions_types=self.restrictions_types,
            x_restrictions=self.x_restrictions,
        )

        if standart.form == Problem.Form.STANDART:
            return standart
        if standart.obj_direction == Problem.ObjectiveDirection.MIN:
            standart.c = [-v for v in standart.c]
            standart.obj_direction = Problem.ObjectiveDirection.MAX
        for i in range(len(standart.x_restrictions)):
            if standart.x_restrictions[i] == Problem.RestrictionType.NONE:
                standart.c.insert(i + 1, -standart.c[i])
                for j in range(len(standart.A)):
                    standart.A[j].insert(i + 1, -standart.A[j][i])
                standart.x_restrictions[i] = Problem.RestrictionType.GEQ
                standart.x_restrictions.insert(i + 1, Problem.RestrictionType.GEQ)
                standart.dim += 1
        for idx, r in enumerate(standart.restrictions_types):
            if r == Problem.RestrictionType.EQ:
                standart.restrictions_types[idx] = Problem.RestrictionType.GEQ
                standart.A.insert(idx + 1, standart.A[idx])
                standart.b.insert(idx + 1, standart.b[idx])
                standart.restrictions_types.insert(idx + 1, Problem.RestrictionType.LEQ)
        for idx, r in enumerate(standart.restrictions_types):
            if r == Problem.RestrictionType.GEQ:
                standart.A[idx] = [-v for v in standart.A[idx]]
                standart.b[idx] = -standart.b[idx]
                standart.restrictions_types[idx] = Problem.RestrictionType.LEQ
        standart.form = Problem.Form.STANDART

        return standart

    def to_canon(self):
        bruteforce.to_canon(
            self.A, self.restrictions_types, self.b, self.x_restrictions, self.c
        )
        self.form = Problem.Form.CANON

    def get_dual(self):
        # x_r = [None if r_t == Problem.RestrictionType.EQ else r_t for r_t in copy(self.restrictions_types)]
        standart = self.get_standart()
        x_r_types = []
        for i in range(len(standart.A[0])):
            if standart.restrictions_types[i] == Problem.RestrictionType.LEQ:
                x_r_types.append(Problem.RestrictionType.GEQ)
            else:
                x_r_types.append(Problem.RestrictionType.LEQ)

        return Problem(
            dim=len(standart.b),
            A=[list(i) for i in zip(*standart.A)],
            b=deepcopy(standart.c),
            c=deepcopy(standart.b),
            restrictions_types=x_r_types,
            x_restrictions=[
                Problem.RestrictionType.GEQ for _ in range(len(standart.A))
            ],
            obj_direction=Problem.ObjectiveDirection(-standart.obj_direction.value),
        )

        # return Problem(
        #     dim=self.dim,
        #     A=[list(i) for i in zip(*self.A)],
        #     b=self.c[:-1],
        #     c=self.b,
        #     restrictions_types=[Problem.RestrictionType(-x_r.value if x_r else 0) for x_r in self.x_restrictions],
        #     x_restrictions=[None if r_t == Problem.RestrictionType.EQ else r_t for r_t in self.restrictions_types],
        #     obj_direction=Problem.ObjectiveDirection(-self.obj_direction.value)
        # )

    def print(self):
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

        for i in range(len(self.A)):
            for j in range(len(self.A[0])):
                if self.A[i][j] >= 0 and j > 0:
                    print("+", end=" ")
                if self.A[i][j] < 0:
                    print("-", end=" ")

                print(f"{abs(self.A[i][j])}x_{j + 1}", end=" ")

            if self.restrictions_types[i] == Problem.RestrictionType.GEQ:
                print(">=", end=" ")
            elif self.restrictions_types[i] == Problem.RestrictionType.LEQ:
                print("<=", end=" ")
            elif self.restrictions_types[i] == Problem.RestrictionType.EQ:
                print("=", end=" ")

            print(self.b[i])

        for idx, r in enumerate(self.x_restrictions):
            if idx > 0 and idx != len(self.x_restrictions):
                print(",", end=" ")
            if r == Problem.RestrictionType.GEQ:
                print(f"x_{idx + 1} >= 0", end="")
            elif r == Problem.RestrictionType.LEQ:
                print(f"x_{idx + 1} <= 0", end="")
            elif r == Problem.RestrictionType.EQ:
                print(f"x_{idx + 1} = 0", end="")
        print("")
