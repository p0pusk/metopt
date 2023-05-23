import random

import numpy as np
from task import *
from scipy.optimize import linprog


def initial_approximation(x0=None, eps=1e-3):
    """
    Calculate the initial approximation for the given x0.

    Parameters:
    x0 (list): Initial approximation.

    Returns:
    list: Updated approximation.
    """
    if x0 is None:
        x0 = []
        for _ in range(dim):
            x0 += [1 + random.uniform(-0.1, 0.1)]

    eta = max(r(x0) for r in rs)
    if eta < 0:
        return x0

    valid = False
    while not valid:
        res = simplex(x0, -eta)
        s, eta = res.x[:dim], res.fun

        alpha = 1

        while not valid:
            alpha /= 2
            if alpha < 2 ** -10:
                break

            x_next = x0 + alpha * s
            valid = f(x_next) - f(x0) < eta * alpha / 2 and all(r(x_next) < 0 for r in rs)

        x0 += alpha * s

    return x0


def get_active_constraints(x, delta):
    """
    Determine the active constraints for the given x and delta.

    Parameters:
    x (list): Current approximation.
    delta (float): Current delta value.

    Returns:
    list: Indices of active constraints.
    """
    return [i for i in range(len(rs)) if -delta <= rs[i](x) <= 0]


def step_size(x, eta, direction):
    """
    Determine the step size for the given parameters.

    Parameters:
    x (list): Current approximation.
    eta (float): Current eta value.
    direction (list): Current direction.

    Returns:
    float: Step size.
    """
    alpha = 1.0

    for _ in range(1000):
        new_x = [x_k + alpha * s_k for x_k, s_k in zip(x, direction)]
        cond = f(new_x) - f(x) <= eta * alpha / 2 and all(r(new_x) <= 0 for r in rs)

        if cond:
            return alpha

        alpha /= 2

    return alpha



def simplex(x, delta):
    """
    Solve the linear programming problem for the given x and delta.

    Parameters:
    x (list): Current approximation.
    delta (float): Current delta value.

    Returns:
    scipy.optimize.OptimizeResult: Result of the linear programming problem.
    """
    active_constraints = get_active_constraints(x, delta)
    A_ub = np.zeros(shape=(1 + len(active_constraints), dim + 1))
    A_ub[:, dim] = -1
    A_ub[0, :dim] = grad_f(x)
    for j, i in enumerate(active_constraints):
        A_ub[j + 1, 0:dim] = grad_rs[i](x)

    return linprog(
        c=np.array([0] * dim + [1]),
        A_ub=A_ub,
        b_ub=np.zeros(A_ub.shape[0]),
        bounds=[[-1, 1]] * dim + [[None, None]],
        method='simplex'
    )


def zoutendijk_method(x0, eta0, eps=1e-5):
    """
    Implementation of the Zoutendijk method.

    Parameters:
    x0 (list): Initial approximation.
    eta (float): Initial eta value.

    Returns:
    list: Solution of the Zoutendijk method.
    """
    x, delta = x0, -eta0

    i = 0
    for i in range(1000):
        res = simplex(x, delta)
        *s, eta0 = res.x

        if eta0 < delta:
            x = [x_k + step_size(x, eta0, s) * s_k for x_k, s_k in zip(x, s)]
        else:
            delta /= 2

        if delta < -max([r(x) for r in rs]) and abs(delta) < eps:
            break

    print(f'Number of iterations: {i}')

    return x
