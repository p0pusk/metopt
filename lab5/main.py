import task
import zoutendijk as z
import numpy as np

if __name__ == '__main__':
    x0 = z.initial_approximation()
    eta0 = -max(r(x0) for r in task.rs)

    res = z.zoutendijk_method(x0, eta0)

    print(f"Answer: {res}")
    print(f"f(x) = {task.f(res)}")

    # task.rs += [
    #     lambda x: -3 * x[0] + 1 + 3 * x[1]
    # ]
    #
    # task.grad_rs += [lambda x: [
    #     -3,
    #     3,
    #     0
    # ]]

    # x0 = z.initial_approximation()
    # eta0 = -max(r(x0) for r in task.rs)
    #
    # res = z.zoutendijk_method(x0, eta0)
    #
    # print(f"Answer: {res}")
    # print(f"f(x) = {task.f(res)}")
