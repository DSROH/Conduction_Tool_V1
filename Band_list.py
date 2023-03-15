import ttkbootstrap as ttkbst
import tkinter as tk


def merge_dic(x, y):
    z = x
    z.update(y)
    return z


def dict_compare_list(v, list_a):
    if v == 1:  # 3G
        Blist = {
            1: [5],
            2: [5],
            4: [5],
            5: [5],
            8: [5],
        }
        rat = "B"
    elif v == 2:  # LTE
        Blist = {
            1: [5, 10, 15, 20],
            2: [5, 10, 15, 20],
            3: [5, 10, 15, 20],
            4: [5, 10, 15, 20],
            5: [5, 10],
            7: [5, 10, 15, 20],
            8: [5, 10],
            12: [5, 10],
            13: [5, 10],
            17: [5, 10],
            18: [5, 10, 15],
            19: [5, 10, 15],
            20: [5, 10, 15, 20],
            25: [5, 10, 15, 20],
            26: [5, 10, 15],
            28: [5, 10, 15, 20],
            66: [5, 10, 15, 20],
            38: [5, 10, 15, 20],
            39: [5, 10, 15, 20],
            40: [5, 10, 15, 20],
            41: [5, 10, 15, 20],
        }
        rat = "B"
    elif v == 3:  # NR
        Blist = {
            1: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
            2: [5, 10, 15, 20, 25, 30, 35, 40],
            3: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
            5: [5, 10, 15, 20, 25],
            7: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
            8: [5, 10, 15, 20, 25, 30, 35],
            12: [5, 10, 15],
            13: [5, 10],
            20: [5, 10, 15, 20],
            25: [5, 10, 15, 20, 25, 30, 35, 40, 45],
            26: [5, 10, 15, 20],
            28: [5, 10, 15, 20, 25, 30],
            66: [5, 10, 15, 20, 25, 30, 35, 40, 45],
            38: [5, 10, 15, 20, 25, 30, 35, 40],
            39: [5, 10, 15, 20, 25, 30, 35, 40],
            40: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80],
            41: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
            77: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
            78: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100],
        }
        rat = "n"

    keys_to_remove = [key for key in Blist.keys() if key not in list_a]
    for key in keys_to_remove:
        Blist.pop(key)

    return rat, Blist


def longest_value(dict_a):
    max_length = max(len(value) for value in dict_a.values())
    longest_values = [value for key, value in dict_a.items() if len(value) == max_length]
    if len(longest_values) == 1:
        return longest_values[0]
    else:
        values = list(dict_a.values())
        values.sort(key=len, reverse=True)
        return values[0]
