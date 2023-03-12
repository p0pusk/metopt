import PySimpleGUI as sg
from problem import *


class Interface:
    def __init__(self):
        self.method = Problem.Method.BRUTEFORCE
        self.dim = 2
        self.max_dim = 6
        self.restrictions_num = 2

    def display_result(self, result):
        if self.method is None:
            return None

        sg.popup("Result of the method ' " + str(self.method) + " ' " + str(result))

    @staticmethod
    def display_error():
        sg.popup_error("There is some problem with input data or method")

    def __create_window(self):
        sg.theme("DarkAmber")
        layout = [
            [
                sg.Text("Dimension:"),
                sg.Combo(
                    values=[*range(1, self.max_dim + 1)],
                    default_value=self.dim,
                    readonly=True,
                    enable_events=True,
                    key="-DIMENSION-",
                ),
            ],
            [
                sg.Text("Number of restrictions:"),
                sg.Combo(
                    values=[*range(1, self.max_dim + 1)],
                    default_value=self.restrictions_num,
                    readonly=True,
                    enable_events=True,
                    key="-RESTRICTIONS-",
                ),
            ],
            [sg.Button("Submit"), sg.Button("Cancel")],
        ]

        return sg.Window(
            "Lab1 Linear Programming",
            layout,
            use_default_focus=False,
            resizable=True,
            auto_size_text=True,
            font=60,
        )

    def create_function_row(self):
        row = []
        for i in range(self.dim):
            if i != 0:
                row.append(sg.Text("+"))
            else:
                row.append(sg.Text("f(x) = "))
            row.append(sg.Input(size=(2, 0), key=("c", i)))
            row.append(sg.Text(f"x_{i} "))

        row.append(sg.Text("-->"))
        row.append(
            sg.Combo(
                ["MIN", "MAX"], default_value="MAX", readonly=True, key="opt_direction"
            )
        )
        return row

    def create_restrictions_input_row(self, row_number: int):
        row = []
        for i in range(self.dim):
            if i != 0:
                row.append(sg.Text("+"))
            row.append(sg.Input(size=(2, 0), key=("A", row_number, i)))
            row.append(sg.Text(f"x_{i} "))

        row.append(
            sg.Combo(
                values=["<=", ">=", "="],
                default_value="<=",
                readonly=True,
                size=(2, 0),
                key=("restrictions", row_number),
            )
        )
        row.append(sg.Input(size=(2, 0), key=("b", row_number)))
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
                sg.Checkbox(f"x_{i} >= 0", default=True, key=("x_restrictions", i))
            )
        return x_restr

    def create_problem_window(self):
        layout = [
            [
                sg.Text("Choose method:"),
                sg.Listbox(
                    ["bruteforce", "simplex"],
                    default_values="bruteforce",
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                    no_scrollbar=True,
                    size=(30, 0),
                    enable_events=True,
                    key="-MODE-",
                ),
            ],
            [sg.Text("Objective function:")],
            [self.create_function_row()],
            [sg.Text("Restrictions:")],
            [self.create_restrictions_input()],
            [self.create_x_restrictions_input()],
            [sg.Button("Solve"), sg.Button("Cancel")],
        ]

        return sg.Window("Lab1", layout, resizable=True, font=30)

    def read_input(self, values):
        self.method = (
            Problem.Method.BRUTEFORCE
            if values["-MODE-"] == "bruteforce"
            else Problem.Method.SIMPLEX
        )
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

            if values["restrictions", i] == "<=":
                restrictions_types[i] = Problem.RestrictionType.LEQ
            elif values["restrictions", i] == ">=":
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

    def run(self):
        window = self.__create_window()
        create_problem = False
        while True:
            event, values = window.read()
            if event in (None, "Exit", "Cancel"):
                window.close()
                break
            if event in ("Submit"):
                create_problem = True
                window.close()
                break
            elif event == "-DIMENSION-":
                self.dim = values["-DIMENSION-"]
            elif event == "-RESTRICTIONS-":
                self.restrictions_num = values["-RESTRICTIONS-"]

        if create_problem:
            window = self.create_problem_window()

            while True:
                event, values = window.read()
                if event in (None, "Exit", "Cancel"):
                    break
                if event == "Solve":
                    problem = self.read_input(values)
                    if problem == None:
                        self.display_error()
                    else:
                        problem.print()
                        try:
                            x = problem.solve(self.method)
                            print("====")
                            print(f"our's x = {x}")
                            print(f"scipy x = {problem.solve(Problem.Method.SCIPY)}")
                        except Exception as e:
                            self.display_error()
