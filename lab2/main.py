#!/usr/bin/env python

# from potential import *
import bruteforce
import numpy as np

def print_solution(costs, solution):
    total_cost = 0

    print(f"склад \t->\t потребитель \t кол-во \t стоимость")
    for i in range(len(costs)):
        for j, cost in enumerate(costs[i]):
            if solution[i][j] == 0:
                continue

            print(f"{i} \t\t->\t\t {j} \t\t\t {solution[i][j]} \t\t {cost * solution[i][j]}")
            total_cost += cost * solution[i][j]

    print()
    print("Общая стоимость: " + str(total_cost))
    return total_cost

if __name__ == "__main__":
    # supply = [16, 11, 22, 20]
    # demand = [25, 11, 17, 7, 9]
    # costs = [[9, 5, 7, 6, 12], [6, 2, 10, 2, 6], [4, 8, 5, 9, 8], [5, 4, 16, 11, 14]]

    supply = [4, 21, 13, 10]
    demand = [15, 2, 11, 8, 12]
    costs = [
        [5, 13, 17, 5, 3],
        [2, 6, 9, 3, 11],
        [7, 14, 16, 9, 6],
        [3, 10, 21, 9, 2]
    ]

    print("Решение методом перебора опорных точек")

    A, b, c = bruteforce.to_canon(supply, demand, costs)
    A.pop()
    b.pop()
    brute_solution = bruteforce.brute_force(A, b, c)
    brute_solution = np.reshape(brute_solution, (len(supply), len(demand)))

    print_solution(costs, brute_solution)

    # problem = PotentialMethod(demand, supply, costs)
    # problem.print()
    # problem.north_west_corner()
    # problem.print()
