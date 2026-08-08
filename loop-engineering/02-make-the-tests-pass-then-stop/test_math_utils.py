from math_utils import add, is_even, mutiply_by_5

def test_add():
    assert add(2, 3) == 5

def test_is_even():
    assert is_even(4) is True

def test_mutiply_by_5():
    assert mutiply_by_5(3) == 15
