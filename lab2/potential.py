from dataclasses import dataclass
import copy
import tabulate
from enum import Enum


class PotentialMethod:
    @dataclass
    class Cell:
        value: float = float("NaN")
        cost: float = float("NaN")
        delta: float = float("NaN")

    @dataclass
    class CycleElement:
        row: int
        col: int
        mark: str

    class Direction(Enum):
        TOP = 0
        BOT = 1
        LEFT = 2
        RIGHT = 3

    def __init__(self, demand: list, supply: list, costs: list[list]) -> None:
        n = len(demand)
        m = len(supply)
        assert len(costs) == m and len(costs[0]) == len(demand)

        self.demand = copy.deepcopy(demand)
        self.supply = copy.deepcopy(supply)
        self.cells = []
        self.u = [] * m
        self.v = [] * n

        for i in range(m):
            self.cells.append([])
            for j in range(n):
                self.cells[i].append(PotentialMethod.Cell(cost=costs[i][j]))

    def north_west_corner(self):
        n = len(self.demand)
        m = len(self.supply)
        for i in range(m):
            for j in range(i, n):
                if self.demand[j] == 0 and self.supply[i] == 0:
                    break
                elif self.supply[i] == 0:
                    break
                elif self.demand[j] == 0:
                    continue

                self.cells[i][j].value = min(self.supply[i], self.demand[j])
                self.supply[i] -= self.cells[i][j].value
                self.demand[j] -= self.cells[i][j].value

    def potential(self):
        self.north_west_corner()
        self.
        pass

    def print(self, cycle: list = []):
        rows = list()
        headers = [""]
        for col, item in enumerate(self.demand):
            headers.append(f"consumer {col + 1} needs {item}")
        for row, item in enumerate(self.supply):
            cur_row = list()
            cur_row.append(f"supplier {row + 1} supplies {item}")
            for col in range(len(self.demand)):
                match = [x.mark for x in cycle if x.col == col and x.row == row]
                cur_row.append(
                    f"{f'[{match[0]}]' if len(match) > 0 else ''}\ncost:"
                    f" {self.cells[row][col].cost}\nvalue: {self.cells[row][col].value}"
                )
            rows.append(cur_row)
        tablefmt = "fancy_grid"
        print(tabulate.tabulate(rows, headers, tablefmt=tablefmt))

    def find_cycle(self, row: int, col: int, cycle: list[CycleElement], direction):
        cycle = copy.deepcopy(cycle)

        if row >= len(self.supply) or col >= len(self.demand) or row < 0 or col < 0:
            return False, cycle

        if self.cells[row][col].value != float("NaN"):
            if len(cycle) == 0:
                cycle.append(PotentialMethod.CycleElement(row, col, "+"))
            elif cycle[-1].row == row and cycle[-1].col == col:
                return True, cycle
            else:
                cycle.append(
                    PotentialMethod.CycleElement(
                        row, col, "+" if cycle[-1].mark == "-" else "-"
                    )
                )

            if direction == PotentialMethod.Direction.TOP:
                return self.find_cycle(row - 1, col, cycle, direction)
            elif direction == PotentialMethod.Direction.BOT:
                return self.find_cycle(row - 1, col, cycle, direction)
            elif direction == PotentialMethod.Direction.LEFT:
                return self.find_cycle(row, col - 1, cycle, direction)
            elif direction == PotentialMethod.Direction.RIGHT:
                return self.find_cycle(row, col + 1, cycle, direction)
            else:
                raise Exception("Invalid enum")

        else:
            left = self.find_cycle(row, col - 1, cycle, direction)
            right = self.find_cycle(row, col + 1, cycle, direction)
            bot = self.find_cycle(row - 1, col, cycle, direction)
            top = self.find_cycle(row + 1, col, cycle, direction)

            if left[0]:
                return left
            elif right[0]:
                return right
            elif bot[0]:
                return bot
            elif top[0]:
                return top
            else:
                return False, cycle
