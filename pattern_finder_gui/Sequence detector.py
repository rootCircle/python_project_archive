# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 16:54:48 2020

@author: dell
This program detect sequence of inputted series

"""

import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle

# Defining window
root = tk.Tk()

# Setting Theme
style = ThemedStyle(root)
style.set_theme("breeze")  # Top themes : Arc, Equilux, Breeze

# Inputting number of datas
ttk.Label(root, text="Enter number of values").grid(row=0, column=0)
ent = ttk.Entry(root)
ent.grid(row=0, column=1)

global Entry
Entry = []

global Lab
Lab = []

# Button
ttk.Button(root, text="Input data", command=lambda: enter_values(ent)).grid(
    row=1, column=2
)


Btn = ttk.Button(
    root, text="Identify series", state="disabled", command=lambda: extract_values()
)
Btn.grid(row=13, column=2)


def enter_values(ent):
    start = len(Entry)
    # Destroying all previously present enteries
    for i in range(0, start):
        Entry[i].destroy()
        Lab[i].destroy()

    Entry.clear()
    Lab.clear()

    num = int(ent.get())  # Stores no. of enteries required

    # Showing text fields and label as per new requirement by user
    for i in range(0, num):
        Lab.append(ttk.Label(root, text="Enter value : "))
        Lab[i].grid(row=i + 3, column=0)
        Entry.append(ttk.Entry(root))
        Entry[i].grid(row=i + 3, column=1)

    Btn.config(state="active")


def extract_values():
    """
    It takes values of all entries and stores it in form of
    integer/float value in list(named data)

    Returns
    -------
    None.

    """
    data = []
    for i in range(0, len(Entry)):
        val = int(Entry[i].get())
        data.append(val)
    identify(data)  # Initiate the process of sequence detection of data


def check(arr):
    """
    Checks if all elements of list are same.

    Parameters
    ----------
    arr : list
        A array of integers/float.

    Returns
    -------
    result : boolean
        Return True if all elements are same or equal.

    Example
    -------
    >>> check([1,1,1,1])
    True
    >>> check([1,2,3,1,1])
    False

    """
    return all(i == arr[0] for i in arr)


def identify(data):
    st_ap = ap(data)
    st_gp = gp(data)


steps_ap = 1


def ap(data):
    SIZE = len(data)
    data_new = []
    for i in range(0, SIZE - 1):
        data_new.append(data[i + 1] - data[i])

    global steps_ap

    if check(data_new):
        print("Major difference :", data_new[0])
        print("AP Steps :", steps_ap)
        print("y=", data[0], "+(n-1)*", data_new[0])
        steps_ap = 1
    elif SIZE > 3:
        steps_ap = steps_ap + 1
        ap(data_new)
    else:
        print("No AP Found!")
    return steps_ap


steps_gp = 1


def gp(data):
    SIZE = len(data)
    data_new = []
    for i in range(0, SIZE - 1):
        data_new.append(data[i + 1] / data[i])

    global steps_gp

    if check(data_new):
        print("Major ratio :", data_new[0])
        print("GP Steps :", steps_gp)
        print("y=", data[0], "*", steps_gp, "^n")
        steps_gp = 1
    elif SIZE > 3:
        steps_gp = steps_gp + 1
        gp(data_new)
    else:
        print("No GP Found!")
    return steps_gp


def hp(data):
    SIZE = len(data)
    data_new = []
    for i in range(0, SIZE):
        data[i] = 1 / data[i]
    st_hp = ap(data)

    for i in range(0, SIZE - 1):
        data_new.append(data[i + 1] - data[i])

    global steps_hp

    if check(data_new):
        print("Major difference :", data_new[0])
        print("HP Steps :", steps_hp)
        steps_hp = 1
    elif SIZE > 3:
        steps_hp = steps_hp + 1
        ap(data_new)
    else:
        print("No HP Found!")
    return steps_hp


root.mainloop()
