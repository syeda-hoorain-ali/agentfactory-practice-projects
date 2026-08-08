from calculator import divide, average, percentage


def test_divide_exact():
    assert divide(10, 2) == 5.0


def test_divide_returns_float_result():
    assert divide(7, 2) == 3.5


def test_average():
    assert average([1, 2, 3, 4]) == 2.5


def test_percentage():
    assert percentage(25, 200) == 12.5
