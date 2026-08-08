"""Two tiny functions for Project 06 (the doorbell loop).

Each hides one of the two bug patterns this project plants on purpose:
an off-by-one error, and a deleted null check.
"""

from typing import Optional


def get_last(items: list) -> object:
    """Return the last item in the list."""
    return items[len(items) - 1]


def greet(user: Optional[dict]) -> str:
    """Return a greeting for user, or a generic one if user is missing."""
    if user is None:
        return "Hello, stranger!"
    return f"Hello, {user['name']}!"
