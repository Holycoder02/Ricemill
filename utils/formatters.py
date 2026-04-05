"""
Display formatting utilities for Rice Mill ERP.
"""


def format_currency(amount, symbol="₹"):
    """Format a number as Indian currency with comma separation."""
    try:
        amount = float(amount)
        if amount < 0:
            return f"-{symbol} {format_indian_number(abs(amount))}"
        return f"{symbol} {format_indian_number(amount)}"
    except (ValueError, TypeError):
        return f"{symbol} 0.00"


def format_indian_number(num):
    """
    Format a number in Indian numbering system.
    e.g., 1234567.89 → 12,34,567.89
    """
    num = float(num)
    integer_part = int(num)
    decimal_part = f"{num:.2f}".split('.')[1]

    s = str(integer_part)
    if len(s) <= 3:
        return f"{s}.{decimal_part}"

    last_three = s[-3:]
    remaining = s[:-3]

    # Add commas every 2 digits from right for the remaining part
    groups = []
    while remaining:
        groups.append(remaining[-2:])
        remaining = remaining[:-2]

    groups.reverse()
    formatted = ','.join(groups) + ',' + last_three

    return f"{formatted}.{decimal_part}"


def format_weight(value, unit="Kg"):
    """Format weight with unit."""
    try:
        return f"{float(value):,.2f} {unit}"
    except (ValueError, TypeError):
        return f"0.00 {unit}"


def convert_to_kg(value, unit):
    """Convert a weight value to kilograms."""
    value = float(value)
    conversions = {
        "Ton": value * 1000,
        "Quintal": value * 100,
        "Kg": value,
    }
    return conversions.get(unit, value)


def convert_from_kg(kg_value, target_unit):
    """Convert kilograms to a target unit."""
    kg_value = float(kg_value)
    conversions = {
        "Ton": kg_value / 1000,
        "Quintal": kg_value / 100,
        "Kg": kg_value,
    }
    return conversions.get(target_unit, kg_value)


WEIGHT_UNITS = ["Ton", "Quintal", "Kg"]
