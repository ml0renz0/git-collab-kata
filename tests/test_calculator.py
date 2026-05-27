from app.calculator import add, exponentiation, multiply, subtract


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(2, 3) == 6


def test_exponentiation():
    assert exponentiation(2, 3) == 8
