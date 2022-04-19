# Неевин Кирилл P3213
# Лабораторная работа #5


from typing import Callable

import numpy
from graph import *
from methods import *

methods = (  # тут заюзай namedtuple
    (newton, 'Многочлен Ньютона с конечными разностями'),
    (lagrange, 'Многочлен Лагранжа')
)

functions = (
    (lambda t: math.cos(t), 'cos(x)'),
    (lambda t: 2 ** t, '2^x'),
    (lambda t: t ** 7 - 3 * (t ** 4) + t ** 3 - 5*t, 'x^7 - 3x^4 + x^3 - 5x')
)

MAX_POINTS = 20


def create_dataset(get_line: Callable[..., str]):
    try:
        x = list(map(float, get_line().split(',')))
        y = list(map(float, get_line().split(',')))
        if len(x) != len(y):
            raise
        x, y = zip(*sorted(zip(x, y)))
    except:
        print("Введите корректную таблицу.")
        return None
    return [x, y]


def number_input(prompt: str, mn=1.0, mx=math.inf) -> float:
    while True:
        ans = input(prompt)
        try:
            num = float(ans)
            if num < mn or num > mx:
                print(f'Число должно быть в интервале [{round(mn, 1)}, {round(mx, 1)}].')
                continue
            return num
        except:
            continue


def float_interval_choice() -> [float, float]:
    while True:
        ans = input('Введите интервал: ').split()
        try:
            left, right = float(ans[0]), float(ans[1])
            if left >= right:
                print(f'Введите корректный интервал.')
                continue
            return left, right
        except:
            continue


def print_indexed_list(indexed_list, start=1):
    for index, item in enumerate(indexed_list, start=start):
        print(f'{index}. {item}')


def bool_choice(prompt: str) -> bool:
    return input(prompt + ' [y/n] ').strip() == 'y'


def read_table():
    while True:
        filename = input("Введите имя файла для загрузки исходных данных и интервала "
                         "или пустую строку, чтобы ввести вручную: ")
        try:
            input_function = input if filename == '' else open(filename, "r").readline
            dataset = create_dataset(input_function)
            if dataset is not None:
                return dataset
        except FileNotFoundError:
            print('Файл не найден.')


if __name__ == '__main__':
    while True:
        if bool_choice('Вы хотите использовать исходные данные на основе функции?'):
            print('Выберите функцию. ')
            print_indexed_list(map(lambda tup: tup[1], functions))
            index = int(number_input('Введите номер: ', mn=1, mx=len(functions)))
            func, _ = functions[index - 1]
            left, right = float_interval_choice()
            nodes = int(
                number_input(f'Введите количество узлов интерполяции [2; {MAX_POINTS}]: ', mn=2, mx=MAX_POINTS)
            )

            x = list(numpy.linspace(left, right, nodes))
            y = list(map(lambda t: func(t), x))
            dataset = [x, y]
        else:
            dataset = read_table()
            left = min(dataset[0])
            right = max(dataset[0])

        print("\nИсходные данные:\n" + tabulate(dataset, tablefmt='grid', floatfmt='2.4f') + "\n")

        x0 = number_input('Введите x0: ', mn=left, mx=right)

        print('Результаты:')
        x, y = dataset
        for solve, name in methods:
            try:
                result = solve(x, y, x0)
                graph(dataset, x0, result, solve, name)
                print(name + ':', result)
            except Exception as e:
                print(e)

        if input('\nЕще раз? [y/n] ') != 'y':
            break

