import math

"""
Program calculates 10 digit number using 10 conditions
x is a ten digit number
C is user input for each condition
Condition 1 :  x^2 >= C*10^20
Condition 2 :  x^2 <= C*10^20
Condition 3 :  sin x = C (approx)
Condition 4 :  log x >= C
Condition 5 :  Cube root of x <= C
Condition 6 :  Square root of x = C (exact to two decimals +/-0.02)
Condition 7 :  ln x <= C
Condition 8 :  Sum of all digit = C
Condition 9 :  Product of all digit = C
Condition 10 : Sum of square of all digit = C
"""


def cond1(x, c):
    return x * x >= c * 10**18


def cond2(x, c):
    return x * x <= c * 10**18


def cond3(x, c, precision=0.1):
    x_rad = x * math.pi / 180
    ans = round(math.sin(x_rad), 3)
    y = round(c, 3)
    return math.fabs(y - ans) < precision


def cond4(x, c):
    return math.log(x, 10) >= c


def cond5(x, c):
    return x ** (1 / 3) <= c


def cond6(x, t):
    c, mode = t
    if mode == "g":
        return round(math.sqrt(x), 2) <= round(c + 0.02, 2)
    elif mode == "l":
        return round(math.sqrt(x), 2) >= round(c - 0.02, 2)
    else:
        return round(math.sqrt(x), 2) == round(c, 2)


def cond7(x, c):
    return math.log(x) <= c


def cond8(x, s):
    c = 0
    for i in range(10):
        c += x % 10
        x = x // 10
    return c == s


def cond9(x, s):
    p = 1
    for i in range(10):
        p *= x % 10
        x = x // 10
    return p == s


def cond10(x, s):
    c2 = 0
    for i in range(10):
        c2 += (x % 10) ** 2
        x = x // 10
    return c2 == s


def supercondl(lower, upper, cond, val):
    step = 10**9
    nlower = lower
    while step != 0:
        t = 0
        for it in range(nlower, upper + step + 1, step):
            if it > 0 and cond(it, val):
                nlower = it - step
                t = 1
                break
        if t == 0 and upper - nlower > step:
            nlower = it - step

        step //= 10
    if nlower > lower:
        lower = nlower
    return lower, upper


def supercondu(lower, upper, cond, val):
    step = 10**9
    nupper = upper
    while step != 0:
        t = 0
        for i in range(nupper, lower - step - 1, -step):
            if i > 0 and cond(i, val):
                nupper = i + step
                t = 1
                break
        if t == 0 and nupper - lower > step:
            nupper = i + step
        step //= 10
    if nupper < upper:
        upper = nupper
    return lower, upper


def supercondArr(lower, upper, cond, val):
    l = []
    for i in range(lower, upper + 1):
        if cond(i, val):
            l.append(i)
    return l


def supercondArr2(data, cond, val):
    l = []
    for i in data:
        if cond(i, val):
            l.append(i)
    return l


def inputs():
    print("---------------------------------INPUT---------------------------------")
    c = float(input("Square of number is greater than <of order 10^18> : "))
    c2 = float(input("Square of number is less than <of order 10^18> : "))
    c3 = float(
        input(
            "sine of number (in degree) is approximately <3 decimal places> equal to : "
        )
    )
    c4 = float(input("Logarithm (base 10) of number is greater than : "))
    c5 = float(input("Cube root of number is less than : "))
    c6 = float(
        input("Square root of number is <Round to 2 decimal places> equal to : ")
    )
    c7 = float(input("Natural Logarithm(ln x) of number is less than : "))
    s8 = int(input("Sum of digits is equal to : "))
    s9 = int(input("Product of digits is equal to : "))
    s10 = int(input("Sum of square of all digit is equal to : "))
    l = [c, c2, c3, c4, c5, c6, c7, s8, s9, s10]

    return l


# Main Program
backtrack = []
lower = 10**9
upper = 10**10 - 1

values = inputs()
print("\n\n\n----------------------CALCULATING NUMBER------------")
# Find Lower value using condition 1
lower, upper = supercondl(lower, upper, cond1, values[0])
backtrack.append((lower, upper))
print("Passed step 1 of 10 [{},{}]".format(lower, upper))

# Find Upper value using condition 2
lower, upper = supercondu(lower, upper, cond2, values[1])
backtrack.append((lower, upper))
print("Passed step 2 of 10 [{},{}]".format(lower, upper))


# Updating Lower value using condition 4
lower, upper = supercondl(lower, upper, cond4, values[3])
backtrack.append((lower, upper))
print("Passed step 3 of 10 [{},{}]".format(lower, upper))

# Find Upper value using condition 5
lower, upper = supercondu(lower, upper, cond5, values[4])
backtrack.append((lower, upper))
print("Passed step 4 of 10 [{},{}]".format(lower, upper))

# Updating Lower and upper value using condition 6
lower, upper = supercondl(lower, upper, cond6, (values[5], "l"))
backtrack.append((lower, upper))

lower, upper = supercondu(lower, upper, cond6, (values[5], "g"))
backtrack.append((lower, upper))
print("Passed step 5 of 10 [{},{}]".format(lower, upper))

# Find Upper value using condition 7

lower, upper = supercondu(lower, upper, cond7, values[6])
backtrack.append((lower, upper))
print("Passed step 6 of 10 [{},{}]".format(lower, upper))

# Finding all possible data using condition 8,9,10
data = supercondArr(lower, upper, cond8, values[7])
backtrack.append(data)
print("Passed step 7 of 10", "Matches :", len(data))

data = supercondArr2(data, cond9, values[8])
backtrack.append(data)
print("Passed step 8 of 10", "Matches :", len(data))

data = supercondArr2(data, cond10, values[9])
backtrack.append(data)
print("Passed step 9 of 10", "Matches :", len(data))

final_data = []
for i in data:
    if cond3(i, values[2]):
        final_data.append(i)

backtrack.append(final_data)

print("Pass step 10 of 10", "Matches :", len(final_data))
print("\n" * 2, "------------------OUTPUT------------------", sep="")
print("Possible Values :", final_data)

if len(final_data) == 0:
    print("\n" * 2, "------------------BACKTRACKING DATA------------------", sep="")
    print("----Higher to Lower Probability of Data Order----")
    L = len(backtrack)

    for i in range(-1, -L - 1, -1):
        row = backtrack[i]
        if isinstance(row, list):
            if len(row) > 0:
                print("Possible data may be :", row)
        else:
            u = row[1]
            l = row[0]
            width = u - l
            if width != 0:
                print("Data may lie in limit [{},{}]".format(l, u))

elif len(final_data) > 1:
    precision = 0.01
    while len(final_data) > 1 or precision > 10**-5:
        final_data2 = []
        for i in final_data:
            if cond3(i, values[2], precision):
                final_data2.append(i)
        precision /= 10

        final_data = final_data2
        if len(final_data) == 1:
            break
    backtrack.append(final_data)

    print("\nAt Higher Precision Data may be :", final_data)
