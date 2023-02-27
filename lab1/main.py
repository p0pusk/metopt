#!/usr/bin/env python

import interface
from problem import *
from simplex import *
from bruteforce import *


if __name__ == "__main__":
    # values = interface.Interface().get_data()

    prb = Problem(
        dim=2,
        A=[[1, 1], [1, -2]],  # m*n
        b=[7, 4],  # m
        c=[-2, 3],  # n
        restrictions_types=[
            Problem.RestrictionType.EQ,
            Problem.RestrictionType.LEQ,
        ],  # m
        x_restrictions=[True, False],  # n
    )

    prb2 = Problem(
        dim=2,
        A=[[1, 1]],  # m*n
        b=[7],  # m
        c=[2, 3],  # n
        restrictions_types=[Problem.RestrictionType.LEQ],  # m
        x_restrictions=[True, True],  # n
    )

    prb3 = Problem(
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
            Problem.RestrictionType.LEQ,
        ],
        x_restrictions=[True, True, True, True, False],
    )

    prb3.Print()
    prb3.ToStandart()
    print("----------------")
    prb3.Print()
    print("----------------")
    N, B, A, b, c, v = initialize_simplex(prb3.A, prb3.b, prb3.c)
    print("simplex ans:")
    print(simplex(N, B, A, b, c, v))
    N, B, A, b, c, v = to_canon(
        prb3.A, prb3.restrictions_types, prb3.b, prb3.x_restrictions, prb3.c
    )
    print("bruteforce ans:")
    print(brute_force(A, b, c))
