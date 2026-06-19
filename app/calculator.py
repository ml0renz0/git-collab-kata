"""Tiny calculator module used by the Git collaboration kata.

Do not solve exercises here in advance. Each exercise asks students to modify
this file from a branch and submit a pull request.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def factorial(n):
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")

    result = 1
    for value in range(2, n + 1):
        result *= value
    return result
