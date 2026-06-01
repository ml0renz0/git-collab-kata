import pytest

from app.calculator import (
    add,
    calculate_tax,
    divide,
    experimental_discount,
    factorial,
    subtract,
)


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2

def test_divide():
    assert divide(10, 2) == 5.0


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_calculate_tax():
    assert calculate_tax(100, 0.21) == 21.0


def test_experimental_discount():
    assert experimental_discount(100, 0.10) == 90


def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_positive():
    assert factorial(5) == 120


def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)


def test_factorial_rejects_non_integer():
    with pytest.raises(TypeError):
        factorial(2.5)
