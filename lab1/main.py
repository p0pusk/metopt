#!/usr/bin/env python

import interface
from problem import *
from simplex import *


if __name__ == "__main__":
    # values = interface.Interface().get_data()

    prb = Problem(
        dim=2,
        A=[[1, 1], [1, -2]],
        b=[7, 4],
        c=[-2, 3],
        restrictions_types=[Problem.RestrictionType.EQ, Problem.RestrictionType.LEQ],
        x_restrictions=[True, False],
    )

    prb.Print()
    prb.ToStandart()
    print("----------------")
    prb.Print()
    print("----------------")
    N, B, A, b, c, v = initialize_simplex(prb.A, prb.b, prb.c)
    print(simplex(N, B, A, b, c, v))
