from greet import get_last, greet


def test_get_last_multiple():
    assert get_last([1, 2, 3]) == 3


def test_get_last_single():
    assert get_last([5]) == 5


def test_greet_with_user():
    assert greet({"name": "Ada"}) == "Hello, Ada!"


def test_greet_with_none():
    assert greet(None) == "Hello, stranger!"
