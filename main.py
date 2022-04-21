# Неевин Кирилл P3213
# Лабораторная работа #5

from collections import namedtuple
from typing import Callable
import math

import numpy
from tabulate import tabulate

from graph import graph
from methods import newton, lagrange


Method = namedtuple('Method', ['name', 'interpolate'])
Function = namedtuple('Function', ['func', 'display_name'])

METHODS = (
    Method('Многочлен Ньютона с конечными разностями', newton),
    Method('Многочлен Лагранжа', lagrange),
)
FUNCTIONS = (
    Function(lambda x: x ** 3 + 2 * x ** 2 - 5 * x - 6, 'x^3 + 2*x^2 - 5*x - 6'),  # [-5; 5]
    Function(lambda x: 2 ** x, '2^x'),
    Function(lambda x: math.sin(x), 'sin(x)'),
)
MIN_POINTS, MAX_POINTS = 2, 20


def create_dataset(get_line: Callable[..., str]):
    try:
        x_generated = list(map(float, get_line().split(',')))
        y_generated = list(map(float, get_line().split(',')))
        if len(x_generated) != len(y_generated):
            raise
        x_generated, y_generated = zip(*sorted(zip(x_generated, y_generated)))
    except:
        print('Введите корректную таблицу.')
        return None
    return [x_generated, y_generated]


def number_input(prompt: str, mn=1.0, mx=math.inf) -> float:
    while True:
        ans = input(prompt)
        try:
            num = float(ans)
            if num < mn or num > mx:
                print(f'Число должно быть в интервале [{round(mn, 1)}; {round(mx, 1)}].')
                continue
            return num
        except:
            continue


def float_interval_choice() -> [float, float]:
    while True:
        ans = input('Введите интервал: ').split()
        try:
            l, r = float(ans[0]), float(ans[1])
            if l >= r:
                print(f'Введите корректный интервал.')
                continue
            return l, r
        except:
            continue


def print_indexed_list(indexed_list, start=1):
    for indx, item in enumerate(indexed_list, start=start):
        print(f'{indx}. {item}')


def bool_choice(prompt: str) -> bool:
    return input(prompt + ' [y/n] ').strip() == 'y'


def read_table():
    while True:
        filename = input('Введите путь файла для загрузки исходных данных, пустую строку - чтобы ввести вручную: ')
        try:
            input_function = input if filename == '' else open(filename, 'r').readline
            dataset = create_dataset(input_function)
            if dataset is not None:
                return dataset
        except FileNotFoundError:
            print('Файл не найден!')


if __name__ == '__main__':
    while True:
        if bool_choice('Сгенерировать входные даннные на основе функции?'):
            print('Выберите функцию:')
            print_indexed_list(map(lambda f: f.display_name, FUNCTIONS))
            index = int(number_input('Номер: ', mn=1, mx=len(FUNCTIONS))) - 1
            func, _ = FUNCTIONS[index]
            left, right = float_interval_choice()
            nodes = int(
                number_input(f'Количество узлов интерполяции [{MIN_POINTS}; {MAX_POINTS}]: ', mn=MIN_POINTS, mx=MAX_POINTS)
            )
            x_vals = list(numpy.linspace(left, right, nodes))
            y_vals = list(map(lambda t: func(t), x_vals))
            dataset = [x_vals, y_vals]
        else:
            dataset = read_table()
            left = min(dataset[0])
            right = max(dataset[0])
        print('\nИсходные данные:\n' + tabulate(dataset, tablefmt='grid', floatfmt='2.4f') + "\n")
        x0 = number_input('Введите x0: ', mn=left, mx=right)
        print('Результаты:')
        x_vals, y_vals = dataset
        for meth in METHODS:
            try:
                result = meth.interpolate(x_vals, y_vals, x0)
                print(meth.name + ':', result)
                graph(dataset, x0, result, meth.interpolate, meth.name)
            except Exception as e:
                raise e
        if input('\nЕще раз? [y/n] ') != 'y':
            break
