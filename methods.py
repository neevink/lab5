import ctypes
import math
from functools import lru_cache

from tabulate import tabulate


def check_nodes(nodes: list) -> bool:
    """Проверить, что узлы равноотстоящие"""
    h = nodes[1] - nodes[0]
    for i in range(len(nodes) - 1):
        if not math.isclose(nodes[i + 1] - nodes[i], h):
            return False
    return True


@lru_cache(maxsize=None)
def get_finite_differences(obj_id: int) -> list:
    y = ctypes.cast(obj_id, ctypes.py_object).value

    y_differences = [[i] for i in y]
    for i in range(1, len(y)):
        for j in range(len(y) - i):
            y_differences[j].append(y_differences[j + 1][-1] - y_differences[j][-1])
    field_names = ['yi'] + [f'd{i} Yi' for i in range(1, len(y_differences))]
    print('\nКонечные разности:\n' + tabulate(y_differences, field_names, tablefmt='grid', floatfmt='2.4f') + "\n")
    return y_differences


def get_t(k: int, t: float, back=False) -> float:
    curr_t = 1
    for i in range(k):
        curr_t *= (t + i) if back else (t - i)
    return curr_t / math.factorial(k)


def newton(x: list, y: list, x0: float):
    if not check_nodes(x):
        raise Exception('Заданы неравноотстоящие узлы, нельзя применить метод Ньютона с конечными разностями!')
    if x0 in x:
        return y[x.index(x0)]

    dy = get_finite_differences(id(y))
    h = (x[1] - x[0])
    nearest_point_index = max(int(x0 // h) - int(x[0] // h), 1)

    result = 0
    if x0 - x[0] < x[-1] - x0:  # идем вперёд
        nearest_point_index -= 1
        t = (x0 - x[nearest_point_index]) / h
        for i in range(len(dy) - nearest_point_index):
            result += dy[nearest_point_index][i] * get_t(i, t)
    else:  # иначе идём назад
        t = (x0 - x[nearest_point_index + 1]) / h
        for i in range(nearest_point_index):
            result += dy[i][nearest_point_index + 1 - i] * get_t(i, t, back=True)

        #nearest_point_index -= 1
        #t = (x0 - x[nearest_point_index]) / h
        #for i in range(len(dy) - nearest_point_index):
        #    result += dy[nearest_point_index][i] * get_t(i, t)
    return result


def lagrange(x: list, y: list, x0: float):
    result = 0
    for j in range(len(y)):
        mul = 1
        for i in range(len(x)):
            mul *= (x0 - x[i]) / (x[j] - x[i]) if i != j else 1
        result += y[j] * mul
    return result
