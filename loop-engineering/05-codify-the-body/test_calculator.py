from calculator import subtract, divide, is_even


def test_subtract():
    assert subtract(10, 3) == 7


def test_subtract_negative():
    assert subtract(3, 10) == -7


def test_divide():
    assert divide(7, 2) == 3.5


def test_divide_exact():
    assert divide(10, 2) == 5.0


def test_is_even_true():
    assert is_even(4) is True


def test_is_even_false():
    assert is_even(3) is False
