import math
import random

# The f1, f2 and f3 functions return the product of 2 complex numbers radiuses

# R = sqrt{x_1^2 + y_1^2}  * sqrt{x_2^2 + y_2^2}
def f1(x1, y1, x2, y2):
    a = x1*x1 + y1*y1
    b = x2*x2 + y2*y2
    return math.sqrt(a) * math.sqrt(b)

# R = sqrt{(x_1^2 + y_1^2) * (x_2^2 + y_2^2)}
def f2(x1, y1, x2, y2):
    a = x1*x1 + y1*y1
    b = x2*x2 + y2*y2
    return math.sqrt(a * b)

# R = sqrt{x_2^2 y_1^2 + x_1^2 y_2^2 + x_1^2 x_2^2 + y_1^2 y_2^2}
def f3(x1, y1, x2, y2):
    x1Square = x1*x1
    x2Square = x2*x2

    y1Square = y1*y1
    y2Square = y2*y2

    a = x2Square * y1Square
    b = x1Square * y2Square
    c = x1Square * x2Square
    d = y1Square * y2Square
    return math.sqrt(a + b + c + d)

def randFloatMinus1To1():
    return 2*random.random() - 1

for i in range(10):
    x1 = randFloatMinus1To1()
    y1 = randFloatMinus1To1()
    x2 = randFloatMinus1To1()
    y2 = randFloatMinus1To1()

    result1 = f1(x1, y1, x2, y2)
    result2 = f2(x1, y1, x2, y2)
    result3 = f3(x1, y1, x2, y2)

    print(result1, result2, result3)
