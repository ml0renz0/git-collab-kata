"""Tiny calculator module used by the Git collaboration kata.

Do not solve exercises here in advance. Each exercise asks students to modify
this file from a branch and submit a pull request.
"""


def add(a, b):
    if a is None or b is None:
        raise ValueError("add does not accept None")
    return int(a) + int(b)


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def exponentiation(base, exponent):
    return base ** exponent


def modulus(a, b):
    return a % b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b
