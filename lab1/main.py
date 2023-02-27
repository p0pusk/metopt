#!/usr/bin/env python

import interface
from problem import *
from simplex import *
from bruteforce import *


if __name__ == "__main__":
    # values = interface.Interface().get_data()

    prb = Problem(
        dim=5,
        A=[
            [1, 2, 3, 4, 1],
            [2, 3, 8, 1, 1],
            [1, 4, 1, 5, 1],
            [3, 7, 4, 1, 2],
            [2, 3, 5, 6, 1],
        ],
        b=[1, 2, 3, 4, 5],
        c=[4, 3, 2, 1, 1],
        restrictions_types=[
            Problem.RestrictionType.GEQ,
            Problem.RestrictionType.EQ,
            Problem.RestrictionType.EQ,
            Problem.RestrictionType.EQ,
            Problem.RestrictionType.LEQ
        ],
        x_restrictions=[True, True, True, True, False],
    )

    # prb = Problem(
    #     dim=2,
    #     A=[[1, 1], [1, -2]],
    #     b=[7, 4],
    #     c=[-2, 3],
    #     restrictions_types=[Problem.RestrictionType.EQ, Problem.RestrictionType.LEQ],
    #     x_restrictions=[True, False],
    # )

    # prb.Print()
    # prb.ToStandart()
    # print("----------------")
    # prb.Print()
    # print("----------------")
    # N, B, A, b, c, v = initialize_simplex(prb.A, prb.b, prb.c)
    # print(simplex(N, B, A, b, c, v))

    prb.Print()
    N, B, A, b, c, v = to_canon(prb.A, prb.restrictions_types, prb.b, prb.x_restrictions, prb.c)
    print()
    res = brute_force(A, b, c)
    print("res:")
    print(res)
