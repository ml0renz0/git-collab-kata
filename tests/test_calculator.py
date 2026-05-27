from app.calculator import add, divide, exponentiation, modulus, multiply, subtract
import pytest


def test_add():
    assert add(2, 3) == 5


def test_add_casts_string_numbers_to_int():
    assert add("2", "3") == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(2, 3) == 6


def test_exponentiation():
    assert exponentiation(2, 3) == 8


def test_modulus():
    assert modulus(10, 3) == 1


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
