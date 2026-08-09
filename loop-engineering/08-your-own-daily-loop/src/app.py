def calculate_total(items):
    total = 0
    for item in items:
        total += item["price"]
    print("total calculated:", total)
    return total


def apply_discount(total, percent):
    return total - (total * percent / 100)
