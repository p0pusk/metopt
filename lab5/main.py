import task
import zoutendijk as z

if __name__ == '__main__':
    x0 = z.initial_approximation()
    eta0 = -max(r(x0) for r in task.rs)

    res = z.zoutendijk_method(x0, eta0)

    print(f"Answer: {res}")
    print(f"f(x) = {task.f(res)}")
