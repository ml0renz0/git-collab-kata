import pytest

from app.calculator import add, divide, factorial, subtract


def test_add():
    assert add(2, 3) == 5


def test_add_casts_string_numbers_to_int():
    assert add("2", "3") == 5


def test_add_rejects_none():
    with pytest.raises(ValueError):
        add(None, 3)


def test_subtract():
    assert subtract(5, 3) == 2


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_factorial_zero():
    assert factorial(0) == 1


def test_factorial_five():
    assert factorial(5) == 120


def test_factorial_negative_raises_value_error():
    with pytest.raises(ValueError):
        factorial(-1)
