def calculate_total(items):
    """Calculate the total price of all items."""
    total = 0
    for item in items:
        total += item["price"]
    # print("total calculated:", total)
    return total


def apply_discount(total, percent):
    """Apply a discount percentage to the total amount."""
    return total - (total * percent / 100)
