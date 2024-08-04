"""
Helps me find the three dragons with most diverse skills covered in Dragon Mania Legends game!
User need to put in CSV, all the dragon they have along with map of associated skills and
this script will figure everything out!

Not very optimized algorithm! Probably the worst, but works for me!
"""

import csv


def casting2d(arr):
    # Force convert int in string to integer
    for i in range(len(arr)):
        el = arr[i]
        try:
            arr[i] = int(el)
        except:
            pass
    return arr


def encdata(arr):
    # Encode dragons name with their index
    arr2 = list(tuple(arr))
    arr2 = arr2[1:]
    for i in range(len(arr2)):
        arr2[i][0] = i + 1
    return arr2


def addlist(*lists):
    # Alzaberic addition of lists of same size
    size = len(lists[0])
    suml = [0 for i in range(size)]
    for l1 in lists:
        l1 = list(l1)
        for i in range(size):
            suml[i] += l1[i]

    return suml


def bubbleSort(arr):
    # Bubble sorting
    n = len(arr)
    arr2 = list(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr2[j] > arr2[j + 1]:
                arr2[j], arr2[j + 1] = arr2[j + 1], arr2[j]

    return arr2


def removecopies(arr):
    # Remove copies of data
    # Also removes different permutation of copies
    arr2 = list(arr)
    size = len(arr2)
    d = []
    for i in range(size):
        l1 = arr2[i]
        d.append(bubbleSort(l1))
    t = 1
    while t == 1:
        t = 0
        for i in range(len(d)):
            for j in range(len(d)):
                if i != j and j < len(d) and i < j < len(d):
                    if d[i] == d[j]:
                        d.pop(j)
                        t = 1
    return d

    return arr2


data = []

with open("Dragon.csv") as f:
    creader = csv.reader(f)
    for rec in creader:
        if rec != []:
            crec = casting2d(rec)
            data.append(crec)

endata = []
cdata = []

# Fully true copy of list
# y=list(y) not always work
# if y has element of type list
for i in range(len(data)):
    cdata.append(tuple(data[i]))

endata = encdata(data)

size = len(endata)

fdata = []
f2data = []

# Checks for dragon with unique capability
# Such that all 3 dragon skills do not intersect
for i in range(size):
    l1 = endata[i][1:]
    for j in range(size):
        if j != i:
            l2 = endata[j][1:]
            for k in range(size):
                if k != i and k != j:
                    l3 = endata[k][1:]
                    su = addlist(l1, l2, l3)
                    if 2 not in su and 3 not in su:
                        fdata.append(
                            [cdata[i + 1][0], cdata[j + 1][0], cdata[k + 1][0]]
                        )
                    if 3 not in su:
                        if su.count(2) == 1:
                            f2data.append(
                                [cdata[i + 1][0], cdata[j + 1][0], cdata[k + 1][0]]
                            )


fdata = removecopies(fdata)
print("Best Dragon combinations\n", fdata)
if fdata == []:
    f2data = removecopies(f2data)
    print("Good Dragon combinations\n", f2data)
