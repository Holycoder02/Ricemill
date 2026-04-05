"""
Input validation utilities for Rice Mill ERP.
"""

import re


def is_valid_gst(gst_number):
    """
    Validate Indian GST number format.
    Format: 2 digits + 10 alphanumeric + 1 digit + Z + 1 alphanumeric
    Example: 22AAAAA0000A1Z5
    """
    if not gst_number:
        return True  # Optional field
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return bool(re.match(pattern, gst_number.upper()))


def is_valid_phone(phone):
    """Validate Indian phone number (10 digits, optionally with +91 prefix)."""
    if not phone:
        return True  # Optional field
    cleaned = re.sub(r'[\s\-\+]', '', phone)
    if cleaned.startswith('91') and len(cleaned) == 12:
        cleaned = cleaned[2:]
    return bool(re.match(r'^[6-9][0-9]{9}$', cleaned))


def is_valid_ifsc(ifsc):
    """Validate Indian IFSC code (4 letters + 0 + 6 chars)."""
    if not ifsc:
        return True
    return bool(re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', ifsc.upper()))


def is_positive_number(value):
    """Check if a string represents a positive number."""
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False


def is_non_negative_number(value):
    """Check if a string represents a non-negative number."""
    try:
        return float(value) >= 0
    except (ValueError, TypeError):
        return False


def is_non_empty(value):
    """Check if a string is non-empty after stripping whitespace."""
    return bool(value and str(value).strip())


def validate_weight_pair(empty_weight, loaded_weight):
    """Validate that loaded weight >= empty weight."""
    try:
        ew = float(empty_weight)
        lw = float(loaded_weight)
        return lw >= ew
    except (ValueError, TypeError):
        return False


def safe_float(value, default=0.0):
    """Safely convert a value to float, returning default on failure."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value, default=0):
    """Safely convert a value to int, returning default on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
