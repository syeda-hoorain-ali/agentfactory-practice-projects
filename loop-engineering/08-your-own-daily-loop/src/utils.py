def format_currency(amount):
    """Format an amount as currency."""
    return f"${amount:,.2f}"


SUPPORTED_CURRENCIES = [
    "USD", "EUR", "GBP", "PKR", "INR", "AED", "SAR",
    "CAD", "AUD", "JPY", "CNY", "SGD", "HKD", "NZD"
]
