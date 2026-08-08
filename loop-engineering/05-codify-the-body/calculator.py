"""A tiny calculator module — three independent bugs, one per function.

Each bug lives in its own function, on purpose: that's what lets three
parallel worktrees fix them at the same time with no risk of collision.
"""


def subtract(a, b):
    """Return a minus b."""
    return a + b  # bug: should be subtraction


def divide(a, b):
    """Divide a by b and return the result."""
    return a // b  # bug: integer division truncates the result


def is_even(n):
    """Return True if n is even."""
    return n % 2 == 1  # bug: inverted condition
