from math import exp
import PySimpleGUI as sg
from problem import *


class Interface:
    def __init__(self):
        self.method = Problem.Method.BRUTEFORCE
        self.dim = 2
        self.max_dim = 6
        self.restrictions_num = 2
        font = ("Arial", 28)
        sg.set_options(font=font)
        sg.theme("Reddit")

    def display_result(self, result):
        if self.method is None:
            return None

        sg.popup("Result of the method ' " + str(self.method) + " ' " + str(result))

    @staticmethod
    def display_error(text: str):
        sg.popup_error(text)

    def __create_window(self):
        layout = [
            [
                sg.Text("Dimension:", expand_x=True, expand_y=True),
                sg.Combo(
                    values=[*range(1, self.max_dim + 1)],
                    default_value=self.dim,
                    readonly=True,
                    enable_events=True,
                    key="-DIMENSION-",
                    expand_x=True,
                ),
            ],
            [
                sg.Text("Number of restrictions:", expand_x=True, expand_y=True),
                sg.Combo(
                    values=[*range(1, self.max_dim + 1)],
                    default_value=self.restrictions_num,
                    readonly=True,
                    enable_events=True,
                    key="-RESTRICTIONS-",
                    expand_x=True,
                ),
            ],
            [sg.Button("Submit", expand_x=True), sg.Button("Cancel", expand_x=True)],
        ]

        return sg.Window(
            "Lab1 Linear Programming",
            layout,
            use_default_focus=False,
            resizable=True,
            auto_size_text=True,
        )

    def create_function_row(self):
        row = []
        for i in range(self.dim):
            if i != 0:
                row.append(sg.Text("+", expand_x=True, expand_y=True))
            else:
                row.append(sg.Text("f(x) = ", expand_x=True, expand_y=True))
            row.append(sg.Input(size=(2, 0), key=("c", i), expand_x=True))
            row.append(sg.Text(f"x_{i+1} ", expand_x=True))

        row.append(sg.Text("-->", expand_x=True))
        row.append(
            sg.Combo(
                ["MIN", "MAX"],
                default_value="MAX",
                readonly=True,
                key="opt_direction",
                expand_x=True,
            )
        )
        return row

    def create_restrictions_input_row(self, row_number: int):
        row = []
        for i in range(self.dim):
            if i != 0:
                row.append(sg.Text("+", expand_x=True, expand_y=True))
            row.append(sg.Input(size=(2, 0), key=("A", row_number, i), expand_x=True))
            row.append(sg.Text(f"x_{i+1} ", expand_x=True, expand_y=True))

        row.append(
            sg.Combo(
                values=["≤", "≥", "="],
                default_value="≤",
                readonly=True,
                key=("restrictions", row_number),
                expand_x=True,
            )
        )
        row.append(sg.Input(size=(2, 0), key=("b", row_number), expand_x=True))
        return row

    def create_restrictions_input(self):
        restrictions = []
        for row in range(self.restrictions_num):
            restrictions.append([self.create_restrictions_input_row(row)])
        return restrictions

    def create_x_restrictions_input(self):
        x_restr = []
        for i in range(self.dim):
            x_restr.append(
                sg.Checkbox(
                    f"x_{i+1} ≥ 0",
                    default=True,
                    key=("x_restrictions", i),
                    expand_x=True,
                )
            )
        return x_restr

    def create_problem_window(self):
        layout = [
            [
                sg.Text("Choose method:"),
                sg.Combo(
                    ["bruteforce", "simplex"],
                    default_value="bruteforce",
                    size=(30, 0),
                    readonly=True,
                    enable_events=True,
                    key="-MODE-",
                ),
            ],
            [sg.Text("Objective function:")],
            [self.create_function_row()],
            [sg.Text("Restrictions:")],
            [self.create_restrictions_input()],
            [self.create_x_restrictions_input()],
            [sg.Button("Solve", expand_x=True), sg.Button("Back", expand_x=True)],
        ]

        return sg.Window("Lab1", layout, resizable=True)

    def read_input(self, values):
        if values["-MODE-"] == "bruteforce":
            self.method = Problem.Method.BRUTEFORCE
        elif values["-MODE-"] == "simplex":
            self.method = Problem.Method.SIMPLEX

        A = [[0.0] * (self.dim) for _ in range(self.restrictions_num)]
        b = [0.0] * self.restrictions_num
        c = [0.0] * self.dim
        x_restrictions = [Problem.RestrictionType.NONE] * self.dim
        restrictions_types = [Problem.RestrictionType.EQ] * self.restrictions_num
        opt_direction = Problem.ObjectiveDirection.MAX
        if values["opt_direction"] == "MIN":
            opt_direction = Problem.ObjectiveDirection.MIN

        for col in range(self.dim):
            if values["c", col] == "":
                return None
            c[col] = float(values["c", col])
            if values["x_restrictions", col]:
                x_restrictions[col] = Problem.RestrictionType.GEQ

            for row in range(self.restrictions_num):
                if (values["A", row, col]) == "":
                    return None
                else:
                    A[row][col] = float(values["A", row, col])

        for i in range(self.restrictions_num):
            if values["b", i] == "":
                return None
            b[i] = float(values["b", i])

            if values["restrictions", i] == "≤":
                restrictions_types[i] = Problem.RestrictionType.LEQ
            elif values["restrictions", i] == "≥":
                restrictions_types[i] = Problem.RestrictionType.GEQ
            else:
                restrictions_types[i] = Problem.RestrictionType.EQ

        return Problem(
            dim=self.dim,
            A=A,
            b=b,
            c=c,
            restrictions_types=restrictions_types,
            obj_direction=opt_direction,
            x_restrictions=x_restrictions,
        )

    def open_starting_window(self):
        window = self.__create_window()
        while True:
            event, values = window.read()
            if event in (None, "Exit", "Cancel"):
                window.close()
                break
            if event in ("Submit"):
                window.close()
                self.open_input_win()
                break
            elif event == "-DIMENSION-":
                self.dim = values["-DIMENSION-"]
            elif event == "-RESTRICTIONS-":
                self.restrictions_num = values["-RESTRICTIONS-"]

    def open_input_win(self):
        window = self.create_problem_window()

        while True:
            event, values = window.read()
            if event in (None, "Exit"):
                break
            if event == "Back":
                window.close()
                self.open_starting_window()
                break
            elif event == "Solve":
                problem = self.read_input(values)
                if problem == None:
                    self.display_error("Not all values inserted")
                else:
                    try:
                        x = problem.solve(self.method)
                        sg.popup_no_buttons(
                            (
                                f"Solution by bruteforce:\nx = {x}"
                                if self.method == Problem.Method.BRUTEFORCE
                                else f"Solution by simplex:\nx = {x}"
                            ),
                            title="Solution",
                        )
                    except Exception as e:
                        self.display_error(
                            "Problem is not restricted, the answer is infinty"
                        )

    def run(self):
        self.open_starting_window()
