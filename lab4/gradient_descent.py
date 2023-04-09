import numpy as np
from search import golden_section_search, backtracking_line_search


def gradient_descent(f, grad_f, x0=None, dim=2, eps=1e-2, search='golden_section'):
    """Градиентный метод первого порядка наискорейшего спуска.

    Args:
        f (callable): Целевая функция.
        grad_f (callable): Градиент целевой функции.
        x0 (np.ndarray): Начальное значение.
        dim (int): Размерность вектора.
        eps (float): Точность, по умолчанию равна 1e-2.
        search (string): метод нахождения оптимального шага (golden_section/backtracking_line).

    Returns:
        tuple:
            xs (List[np.ndarray]): Список всех точек на линии спуска.
            grads (List[np.ndarray]): Список всех градиентов в этих точках.
            alphas (List[float]): Список всех найденных оптимальных шагов.
            i (int): Количество итераций.
    """

    alphas = []
    xs = [np.array([0] * dim) if x0 is None else x0]
    grads = [grad_f(xs[-1])]
    i = 0

    while not np.linalg.norm(grads[-1]) < eps:
        # выбор оптимального шага
        if search == 'golden_section':
            alpha = golden_section_search(lambda a: f(xs[-1] - a * grads[-1]))
        else:
            alpha = backtracking_line_search(f, grad_f, xs[-1], -grads[-1])

        x = xs[-1] - alpha * grads[-1]
        grad = grad_f(x)

        # Проверка ортогональности звеньев градиентной ломаной
        # if abs(grad @ grads[-1]) < eps:
        #     break

        xs += [x]
        grads += [grad]
        alphas += [alpha]
        i += 1

    return xs, grads, alphas, i


def gradient_descent_dfp(f, grad_f, x0=None, dim=2, eps=1e-2, search='golden_section'):
    """
    Реализация градиентного метода второго порядка ДФП.

    Args:
        f (callable): функция, которую требуется минимизировать.
        grad_f (callable): функция, вычисляющая градиент функции f.
        x0 (numpy.ndarray): начальное значение вектора x.
        dim (int): размерность вектора.
        eps (float): точность вычисления результата.
        search (string): метод нахождения оптимального шага (golden_section/backtracking_line).

    Returns:
        tuple:
            xs (List[np.ndarray]): Список всех точек на линии спуска.
            grads (List[np.ndarray]): Список всех градиентов в этих точках.
            alphas (List[float]): Список всех найденных оптимальных шагов.
            i (int): Количество итераций.
    """

    H = np.eye(dim)  # начальная матрица Гессе

    xs = [np.array([0] * dim) if x0 is None else x0]
    grads = [grad_f(xs[-1])]
    alphas = []
    i = 0

    while not np.linalg.norm(grads[-1]) < eps:
        d = - H @ grads[-1]  # направление поиска

        # выбор оптимального шага
        if search == 'golden_section':
            alpha = golden_section_search(lambda a: f(xs[-1] - a * grads[-1]))
        else:
            alpha = backtracking_line_search(f, grad_f, xs[-1], d)

        s = alpha * d  # шаг

        x = xs[-1] + s
        grad = grad_f(x)

        # обновление матрицы Гессе по формуле ДФП
        y = grad - grads[-1]  # разность градиентов
        Hy = H @ y
        H = H - np.outer(Hy, Hy) / (y @ Hy) + np.outer(s, s) / (s @ y)

        # Проверка ортогональности звеньев градиентной ломаной
        # if abs(grad @ grads[-1]) < eps:
        #     break

        xs += [x]
        grads += [grad]
        alphas += [alpha]
        i += 1

    return xs, grads, alphas, i
