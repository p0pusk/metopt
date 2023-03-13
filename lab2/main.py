#!/usr/bin/env python

from tproblem import *
from potential import *

if __name__ == "__main__":
    supply = [16, 11, 22, 20]
    demand = [25, 11, 17, 7, 9]
    costs = [[9, 5, 7, 6, 12], [6, 2, 10, 2, 6], [4, 8, 5, 9, 8], [5, 4, 16, 11, 14]]

    problem = PotentialMethod(demand, supply, costs)
    problem.print()
    problem.north_west_corner()
    problem.print()
