from app.calculator import add, subtract, divide, modulus, multiply, exponentiation


def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2

def test_divide():
    assert divide(15, 3) == 5

def test_modulus():
    assert modulus(9, 2) == 1

def test_multiply():
    assert multiply(5, 3) == 15

def test_exponentiation():
    assert exponentiation(2, 3) == 8
