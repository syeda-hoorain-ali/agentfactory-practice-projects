def calculate_total(items):
    """Calculate total price of items."""
    total = 0
    for item in items:
        total += item["price"]
    return total


def apply_discount(total, percent):
    """Apply discount to total."""
    return total - (total * percent / 100)
