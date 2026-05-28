import pytest

from app.calculator import add, calculate_tax, divide, subtract


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
