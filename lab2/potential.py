from dataclasses import dataclass
import math
import copy
import tabulate
from enum import Enum

import numpy as np


class PotentialMethod:
    @dataclass
    class Cell:
        row: int
        col: int
        value: float = float("NaN")
        cost: float = float("NaN")
        delta: float = float("NaN")
        mark: str = ""

    @dataclass
    class CycleElement:
        row: int
        col: int
        mark: str

    class Direction(Enum):
        TOP = 1
        BOT = -1
        LEFT = -2
        RIGHT = 2

    def __init__(self, demand: list, supply: list, costs: list[list]) -> None:
        n = len(demand)
        m = len(supply)
        assert len(costs) == m and len(costs[0]) == len(demand)

        self.demand = copy.deepcopy(demand)
        self.supply = copy.deepcopy(supply)
        self.costs = copy.deepcopy(costs)
        self.cells: list[list[PotentialMethod.Cell]] = []
        self.u = [float("nan")] * len(self.costs)
        self.v = [float("nan")] * len(self.costs[0])
        self.bfs = []
        self.deltas = []
        self.ws = []

        for i in range(m):
            self.cells.append([])
            for j in range(n):
                self.cells[i].append(PotentialMethod.Cell(i, j, cost=costs[i][j]))

    def north_west_corner(self):
        i = 0
        j = 0
        while len(self.bfs) < len(self.supply) + len(self.demand) - 1:
            s = self.supply[i]
            d = self.demand[j]
            v = min(s, d)
            self.supply[i] -= v
            self.demand[j] -= v
            self.bfs.append(((i, j), v))
            self.cells[i][j].value = v
            if self.supply[i] == 0 and i < len(self.supply) - 1:
                i += 1
            elif self.demand[j] == 0 and j < len(self.demand) - 1:
                j += 1

    def recalculate_potentials(self):
        self.u = [float("nan")] * len(self.costs)
        self.v = [float("nan")] * len(self.costs[0])
        self.u[0] = 0
        bfs_copy = self.bfs.copy()
        while len(bfs_copy) > 0:
            for index, bv in enumerate(bfs_copy):
                i, j = bv[0]
                if math.isnan(self.u[i]) and math.isnan(self.v[j]):
                    continue
                cost = self.costs[i][j]
                if math.isnan(self.u[i]):
                    self.u[i] = cost - self.v[j]
                else:
                    self.v[j] = cost - self.u[i]
                bfs_copy.pop(index)
                break

        for i, row in enumerate(self.costs):
            for j, cost in enumerate(row):
                non_basic = all([p[0] != i or p[1] != j for p, v in self.bfs])
                if non_basic:
                    cost = self.costs[i][j]
                    self.cells[i][j].delta = self.u[i] + self.v[j] - cost
                    self.ws.append(((i, j), self.u[i] + self.v[j] - cost))

    def get_entering_variable_position(self):
        ws_copy = self.ws.copy()
        ws_copy.sort(key=lambda w: w[1])
        return ws_copy[-1][0]

    def get_possible_next_nodes(self, loop, not_visited):
        last_node = loop[-1]
        nodes_in_row = [n for n in not_visited if n[0] == last_node[0]]
        nodes_in_column = [n for n in not_visited if n[1] == last_node[1]]
        if len(loop) < 2:
            return nodes_in_row + nodes_in_column
        else:
            prev_node = loop[-2]
            row_move = prev_node[0] == last_node[0]
            if row_move:
                return nodes_in_column
            return nodes_in_row

    def get_loop(self, bv_positions, ev_position):
        def inner(loop):
            if len(loop) > 3:
                can_be_closed = (
                    len(self.get_possible_next_nodes(loop, [ev_position])) == 1
                )
                if can_be_closed:
                    return loop
            not_visited = list(set(bv_positions) - set(loop))
            possible_next_nodes = self.get_possible_next_nodes(loop, not_visited)
            for next_node in possible_next_nodes:
                new_loop = inner(loop + [next_node])
                if new_loop:
                    return new_loop

        return inner([ev_position])

    def loop_pivoting(self, bfs, loop):
        even_cells = loop[0::2]
        odd_cells = loop[1::2]
        get_bv = lambda pos: next(v for p, v in bfs if p == pos)
        leaving_position = sorted(odd_cells, key=get_bv)[0]
        leaving_value = get_bv(leaving_position)

        new_bfs = []
        for p, v in [bv for bv in bfs if bv[0] != leaving_position] + [(loop[0], 0)]:
            if p in even_cells:
                v += leaving_value
            elif p in odd_cells:
                v -= leaving_value
            new_bfs.append((p, v))

        return new_bfs

    def can_be_improved(self):
        for p, v in self.ws:
            if v > 0:
                return True
        return False

    def solve(self):
        def inner(bfs):
            self.recalculate_potentials()
            print(f"Iteration:")
            self.print()
            if self.can_be_improved():
                ev_position = self.get_entering_variable_position()
                print(ev_position)
                loop = self.get_loop([p for p, v in bfs], ev_position)
                print(loop)
                return inner(self.loop_pivoting(bfs, loop))
            return bfs

        self.north_west_corner()
        basic_variables = inner(self.bfs)
        solution = np.zeros((len(self.costs), len(self.costs[0])))
        for (i, j), v in basic_variables:
            solution[i][j] = v

        return solution

    def print(self, cycle: list = []):
        sum = 0
        for row in range(len(self.supply)):
            for col in range(len(self.demand)):
                if not math.isnan(self.cells[row][col].value):
                    sum += self.cells[row][col].value * self.cells[row][col].cost

        rows = list()
        headers = [f"sum = {sum}"]
        for col, item in enumerate(self.demand):
            headers.append(f"consumer {col + 1} needs {item}")
        headers.append("")
        for row, item in enumerate(self.supply):
            cur_row = list()
            cur_row.append(f"supplier {row + 1} supplies {item}")
            for col in range(len(self.demand)):
                cur_row.append(
                    f"{f'[{self.cells[row][col].mark}]' if self.cells[row][col].mark != ''  else ''}\ncost:"
                    f" {self.cells[row][col].cost}\nvalue:"
                    f" {self.cells[row][col].value}\ndelta:"
                    f" {self.cells[row][col].delta}"
                )
            cur_row.append(f"U[{row + 1}] = {self.u[row]}")
            rows.append(cur_row)
        last_row = [""]
        for col in range(len(self.demand)):
            last_row.append(f"V[{col + 1}] = {self.v[col]}")
        rows.append(last_row)

        tablefmt = "fancy_grid"
        print(tabulate.tabulate(rows, headers, tablefmt=tablefmt))
