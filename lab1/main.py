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
        x_restrictions=[
            Problem.RestrictionType.GEQ,
            None
        ],  # n
    )

    prb2 = Problem(
        dim=2,
        A=[[1, 1]],  # m*n
        b=[7],  # m
        c=[2, 3],  # n
        restrictions_types=[Problem.RestrictionType.LEQ],  # m
        x_restrictions=[
            Problem.RestrictionType.GEQ,
            Problem.RestrictionType.GEQ
        ],  # n
    )

    prb3 = Problem(
        dim=6,
        A=[
            [1, 2, 3, 4, 1, 1],
            [2, 3, 8, 1, 1, 1],
            [1, 4, 1, 5, 1, 1],
            [3, 7, 4, 1, 2, 1],
            [2, 3, 5, 6, 1, 1],
            [3, 2, 1, 4, 1, 1],
        ],
        b=[1, 2, 3, 4, 5, 3],
        c=[4, 3, 2, 0, 0, 0],
        restrictions_types=[
            Problem.RestrictionType.GEQ,
            Problem.RestrictionType.EQ,
            Problem.RestrictionType.EQ,
            Problem.RestrictionType.EQ,
            Problem.RestrictionType.LEQ,
            Problem.RestrictionType.LEQ,
        ],
        x_restrictions=[
            Problem.RestrictionType.GEQ,
            Problem.RestrictionType.GEQ,
            None,
            None,
            None,
            None
        ],
    )

    prb4 = Problem(
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
        x_restrictions=[
            Problem.RestrictionType.GEQ,
            Problem.RestrictionType.GEQ,
            Problem.RestrictionType.GEQ,
            Problem.RestrictionType.GEQ,
            None
        ],
    )

    prb4.solve()
