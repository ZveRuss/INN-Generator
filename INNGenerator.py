# -*- coding: utf-8 -*-
import argparse
from random import randint

# Так называемые контрольные числа
control_nums_ul = (2, 4, 10, 3, 5, 9, 4, 6, 8)
control_nums_fl = (
    (7, 2, 4, 10, 3, 5, 9, 4, 6, 8),
    (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8),
)


def get_random_kno():
    """ Случайный Код Налогового Органа """
    return str(randint(10000, 19999))[1:]


def get_controls_inn_ul(inn):
    """ Получить контрольное число для ИНН Юридического лица """
    inn = inn[:-1] if len(inn) == 10 else inn

    control_num = sum([x * int(y) for (x, y) in zip(control_nums_ul, inn)]) % 11
    control_num = 0 if control_num == 10 else control_num

    return str(control_num)


def get_controls_inn_fl(inn):
    """ Получить контрольные числа для ИНН Физического лица """
    inn = inn[:-2] if len(inn) == 12 else inn
    first_control_num = sum([x * int(y) for (x, y) in zip(control_nums_fl[0], inn)]) % 11
    first_control_num = 0 if first_control_num == 10 else first_control_num
    inn += str(first_control_num)

    second_control_num = sum([x * int(y) for (x, y) in zip(control_nums_fl[1], inn)]) % 11
    second_control_num = 0 if second_control_num == 10 else second_control_num

    return str(first_control_num), str(second_control_num)


def get_random_inn_ul(kno_num: str = None) -> str:
    """ Получить случайный ИНН Юридического Лица """
    if not kno_num:
        kno_num = get_random_kno()
    inn = kno_num + str(randint(100000, 199999))[1:]
    inn += get_controls_inn_ul(inn)

    return inn


def get_random_inn_fl(kno_num: str = None) -> str:
    """ Получить случайный ИНН Физического Лица """
    if not kno_num:
        kno_num = get_random_kno()
    inn = kno_num + str(randint(1000000, 1999999))[1:]
    inn += ''.join(get_controls_inn_fl(inn))

    return inn


def validate_inn(inn):
    """ Выполнить валидацию ИНН """
    if inn.isdigit() and len(inn) in (10, 12):
        if len(inn) == 10:
            control = get_controls_inn_ul(inn)
            return True if control == inn[-1] else False
        else:
            controls = ''.join(get_controls_inn_fl(inn))
            return True if controls == inn[-2:] else False
    else:
        return False


if __name__ == '__main__':
    try:
        while True:
            try:
                args = list(map(int, input('Input KNO and count desired INN-numbers:\n').split()))
                if len(args) > 1:
                    kno = str(args[0])
                    n = args[1]
                elif 0 < len(args) < 2:
                    kno = str(args[0])
                    n = 1
                else:
                    kno = None
                    n = 1
            except ValueError:
                print('Incorrect input format, must be: [KNO: number] [count: number]')
                continue

            for i in range(n):
                if kno:
                    print(get_random_inn_ul(kno_num=kno), end='\n')
                    # print(get_random_inn_fl(kno_num=kno), end='\n')
                else:
                    print(get_random_inn_ul(), end='\n')
                    # print(get_random_inn_fl(), end='\n')
    except KeyboardInterrupt:
        print('Done.')
