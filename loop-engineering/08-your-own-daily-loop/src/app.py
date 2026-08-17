def calculate_total(items):
    """Calculate the total price for a list of items."""
    total = 0
    for item in items:
        total += item["price"]
    return total


def apply_discount(total, percent):
    """Apply a percentage discount to the total."""
    return total - (total * percent / 100)
