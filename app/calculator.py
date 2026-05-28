"""Tiny calculator module used by the Git collaboration kata.

Do not solve exercises here in advance. Each exercise asks students to modify
this file from a branch and submit a pull request.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b
