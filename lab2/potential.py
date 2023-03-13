import copy
import tabulate


class PotentialMethod:
    class Cell:
        def __init__(
            self, cost: float = float("NaN"), value: float = float("NaN")
        ) -> None:
            self.val = value
            self.cost = cost
            self.delta = float("NaN")

    def __init__(self, demand: list, supply: list, costs: list[list]) -> None:
        n = len(demand)
        m = len(supply)
        assert len(costs) == m and len(costs[0]) == len(demand)

        self.demand = copy.deepcopy(demand)
        self.supply = copy.deepcopy(supply)

        self.cells = [[PotentialMethod.Cell()] * n for _ in range(m)]
        print(self.cells)

        for i in range(m):
            for j in range(n):
                self.cells[i][j].cost = costs[i][j]

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

                self.cells[i][j].val = min(self.supply[i], self.demand[j])
                self.supply[i] -= self.cells[i][j].val
                self.demand[j] -= self.cells[i][j].val

    def print(self):
        rows = list()
        headers = [""]
        for col, item in enumerate(self.demand):
            headers.append(f"consumer {col + 1} needs {item}")
        for row, item in enumerate(self.supply):
            cur_row = list()
            cur_row.append(f"supplier {row + 1} supplies {item}")
            for col in range(len(self.demand)):
                cur_row.append(
                    f"cost: {self.cells[row][col].cost}\nvalue:"
                    f" {self.cells[row][col].val}"
                )
            rows.append(cur_row)
        # tablefmt="latex"
        print(tabulate.tabulate(rows, headers))
