import PySimpleGUI as sg
import problem


class Interface:
    def __init__(self):
        self.method = None
        self.dim = 3
        self.max_dim = 6
        self.restrictions_num = 3

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
                sg.Text("Choose method:"),
                sg.Listbox(
                    ["bruteforce", "simplex"],
                    default_values="bruteforce",
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                    no_scrollbar=True,
                    size=(30, 0),
                ),
            ],
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
                    default_value=self.dim,
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
            [sg.Text("Objective function:")],
            [self.create_function_row()],
            [sg.Text("Restrictions:")],
            [self.create_restrictions_input()],
            [self.create_x_restrictions_input()],
            [sg.Button("Solve"), sg.Button("Cancel")],
        ]

        return sg.Window("Lab1", layout, resizable=True, font=30)

    def read_input(self, values):
        A = [[0.0] * (self.restrictions_num) for _ in range(self.dim)]
        b = [0.0] * self.restrictions_num
        c = [0.0] * self.dim
        x_restrictions = [problem.Problem.RestrictionType.NONE] * self.dim
        restrictions_types = [
            problem.Problem.RestrictionType.EQ
        ] * self.restrictions_num
        opt_direction = problem.Problem.ObjectiveDirection.MAX
        if values["opt_direction"] == "MIN":
            opt_direction = problem.Problem.ObjectiveDirection.MIN

        for row in range(self.dim):
            if values["c", row] == "":
                return None
            c[row] = float(values["c", row])
            if values["x_restrictions", row]:
                x_restrictions[row] = problem.Problem.RestrictionType.GEQ

            for col in range(self.restrictions_num):
                if (values["A", row, col]) == "":
                    return None
                else:
                    A[row][col] = float(values["A", row, col])

        for i in range(self.restrictions_num):
            if values["b", i] == "":
                return None
            b[i] = float(values["b", i])

            if values["restrictions", i] == "<=":
                restrictions_types[i] = problem.Problem.RestrictionType.LEQ
            elif values["restrictions", i] == ">=":
                restrictions_types[i] = problem.Problem.RestrictionType.GEQ
            else:
                restrictions_types[i] = problem.Problem.RestrictionType.EQ

        return problem.Problem(
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
                    print(problem)
                    if problem == None:
                        self.display_error()
                    else:
                        problem.print()
