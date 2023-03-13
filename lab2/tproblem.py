import copy
import tabulate


class TProblem:
    def __init__(self, demand: list, supply: list, costs: list[list]) -> None:
        self.demand = copy.deepcopy(demand)
        self.supply = copy.deepcopy(supply)
        self.costs = copy.deepcopy(costs)

    def print_table(self):
        rows = list()
        headers = [""]
        for col, item in enumerate(self.demand):
            headers.append(f"consumer {col + 1} needs {item}")
        for row_num, item in enumerate(self.supply):
            cur_row = list()
            cur_row.append(f"supplier {row_num + 1} supplies {item}")
            for col_num in range(len(self.demand)):
                cur_row.append(self.costs[row_num][col_num])
            rows.append(cur_row)
        # tablefmt="latex"
        print(tabulate.tabulate(rows, headers))
