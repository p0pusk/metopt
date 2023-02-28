from problem import Problem

prb1 = Problem(
    dim=2,
    A=[[1, 1], [1, -2]],  # m*n
    b=[7, 4],  # m
    c=[-2, 3],  # n
    restrictions_types=[
        Problem.RestrictionType.EQ,
        Problem.RestrictionType.LEQ,
    ],  # m
    x_restrictions=[Problem.RestrictionType.GEQ, Problem.RestrictionType.NONE],  # n
)

prb2 = Problem(
    dim=2,
    A=[[1, 1]],  # m*n
    b=[7],  # m
    c=[2, 3],  # n
    restrictions_types=[Problem.RestrictionType.LEQ],  # m
    x_restrictions=[Problem.RestrictionType.GEQ, Problem.RestrictionType.GEQ],  # n
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
        Problem.RestrictionType.NONE,
        Problem.RestrictionType.NONE,
        Problem.RestrictionType.NONE,
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
        Problem.RestrictionType.LEQ,
    ],
    x_restrictions=[
        Problem.RestrictionType.GEQ,
        Problem.RestrictionType.GEQ,
        Problem.RestrictionType.GEQ,
        Problem.RestrictionType.GEQ,
        Problem.RestrictionType.NONE,
    ],
)

prb5 = Problem(
    dim=2,
    A=[[2, -1], [1, -5]],
    b=[2, -4],
    x_restrictions=[Problem.RestrictionType.GEQ, Problem.RestrictionType.GEQ],
    restrictions_types=[Problem.RestrictionType.GEQ, Problem.RestrictionType.GEQ],
    c=[2, -1],
    obj_direction=Problem.ObjectiveDirection.MAX,
)
