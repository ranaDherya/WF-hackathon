# Auto-generated validation functions

import re

def regex_validator(data, patterns):
    """
    Validate data against a list of regex patterns.
    """
    for pattern in patterns:
        if re.fullmatch(pattern, data):
            return True
    return False

# Example usage
# data = "123456"  # Example data to validate
# patterns = ["^\d{4,6}$", "^\d{2,4}$", "^[A-Z0-9]{6}$"]  # List of regex patterns
# is_valid = regex_validator(data, patterns)
# print(is_valid)

import re

def regex_validator(data, patterns):
    """
    Validate data against a list of regex patterns.
    """
    for pattern in patterns:
        if re.fullmatch(pattern, data):
            return True
    return False

# Example usage
# data = "123456"  # Example data to validate
# patterns = ["^\d{4,6}$", "^\d{2,4}$", "^[A-Z0-9]{6}$"]  # List of regex patterns
# is_valid = regex_validator(data, patterns)
# print(is_valid)

def list_validator(data, allowed_values):
    """
    Validate data against a list of allowed values.
    """
    return data in allowed_values

# Example usage
# data = "NAICS"  # Example data to validate
# allowed_values = ["NAICS", "SIC", "GICS"]  # List of allowed values
# is_valid = list_validator(data, allowed_values)
# print(is_valid)

def list_validator(data, allowed_values):
    """
    Validate data against a list of allowed values.
    """
    return data in allowed_values

# Example usage
# data = "NAICS"  # Example data to validate
# allowed_values = ["NAICS", "SIC", "GICS"]  # List of allowed values
# is_valid = list_validator(data, allowed_values)
# print(is_valid)

from datetime import datetime

def date_validator(data):
    """
    Validate data against the date format YYYY-MM-DD.
    """
    try:
        datetime.strptime(data, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Example usage
# data = "2023-10-05"  # Example data to validate
# is_valid = date_validator(data)
# print(is_valid)

from datetime import datetime

def date_validator(data):
    """
    Validate data against the date format YYYY-MM-DD.
    """
    try:
        datetime.strptime(data, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Example usage
# data = "2023-10-05"  # Example data to validate
# is_valid = date_validator(data)
# print(is_valid)

def decimal_validator(data, decimal_places):
    """
    Validate that the data is a decimal number with the specified number of decimal places.
    """
    try:
        # Split the data into integer and decimal parts
        integer_part, decimal_part = data.split('.')
        # Check if the decimal part has the correct number of places
        if len(decimal_part) == decimal_places:
            return True
        else:
            return False
    except ValueError:
        return False

# Example usage
# data = "0.0005"  # Example data to validate
# decimal_places = 4  # Number of decimal places
# is_valid = decimal_validator(data, decimal_places)
# print(is_valid)

def decimal_validator(data, decimal_places):
    """
    Validate that the data is a decimal number with the specified number of decimal places.
    """
    try:
        # Split the data into integer and decimal parts
        integer_part, decimal_part = data.split('.')
        # Check if the decimal part has the correct number of places
        if len(decimal_part) == decimal_places:
            return True
        else:
            return False
    except ValueError:
        return False

# Example usage
# data = "0.0005"  # Example data to validate
# decimal_places = 4  # Number of decimal places
# is_valid = decimal_validator(data, decimal_places)
# print(is_valid)

