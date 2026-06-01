"""Tiny calculator module used by the Git collaboration kata.

Do not solve exercises here in advance. Each exercise asks students to modify
this file from a branch and submit a pull request.
"""


def add(left, right):
    return left + right


def subtract(left, right):
    return left - right


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b


def calculate_tax(amount, rate):
    return amount * rate


def experimental_discount(amount, rate):
    return amount - (amount * rate)


def factorial(n):
    if not isinstance(n, int):
        raise TypeError("factorial is only defined for integers")

    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")

    result = 1
    for value in range(2, n + 1):
        result *= value
    return result
